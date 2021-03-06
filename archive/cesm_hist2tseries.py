#! /usr/bin/env python
"""Make history files into timeseries"""

import os
import sys
from subprocess import check_call, Popen, PIPE
from glob import glob
import re
import click

import yaml
import tempfile
import logging

import cftime
import xarray as xr
import numpy as np

from workflow import task_manager as tm

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)

script_path = os.path.dirname(os.path.realpath(__file__))

USER = os.environ['USER']
ARCHIVE_ROOT = f'/glade/scratch/{USER}/archive'

tm.ACCOUNT = 'NCGD0011'
tm.MAXJOBS = 100

xr_open = dict(decode_times=False, decode_coords=False)

def get_year_filename(file):
    """Get the year from the datestr part of a file."""
    date_parts = [int(d) for d in file.split('.')[-2].split('-')]
    return date_parts[0]

class file_date(object):
    """Class with attributes for the start, stop, and middle of a file's time
       axis.
    """
    def __init__(self, file):
        with xr.open_dataset(file, **xr_open) as ds:
            time_units = ds.time.units
            calendar = ds.time.calendar
            tb = ds.time.bounds
            tb_dim = ds[tb].dims[-1]

            t0 = ds[tb].isel(**{'time': 0, tb_dim: 0})
            tf = ds[tb].isel(**{'time': -1, tb_dim: -1})

            self.date = cftime.num2date(np.mean([t0, tf]), units=time_units,
                                        calendar=calendar)
            self.year = self.date.year
            self.month = self.date.month
            self.day = self.date.day

            time_mid_point = cftime.num2date(ds[tb].mean(dim=tb_dim),
                                             units=time_units, calendar=calendar)

            self.t0 = time_mid_point[0]
            self.tf = time_mid_point[-1]


def get_date_string(files, freq):
    """return a date string for timeseries files"""

    date_start = file_date(files[0])
    date_end = file_date(files[-1])

    year = [date_start.t0.year, date_end.tf.year]
    month = [date_start.t0.month, date_end.tf.month]
    day = [date_start.t0.day, date_end.tf.day]

    if freq in ['day_1', 'day_5', 'daily', 'day']:
        return (f'{year[0]:04d}{month[0]:02d}{day[0]:02d}-'
                f'{year[1]:04d}{month[1]:02d}{day[1]:02d}')

    elif freq in ['month_1', 'monthly',  'mon']:
        return (f'{year[0]:04d}{month[0]:02d}-'
                f'{year[1]:04d}{month[1]:02d}')

    elif freq in ['year_1', 'yearly', 'year', 'ann']:
        return (f'{year[0]:04d}-'
                f'{year[1]:04d}')
    else:
        raise ValueError(f'freq: {freq} not implemented')


def get_vars(files):
    """get lists of non-time-varying variables and time varying variables"""

    with xr.open_dataset(files[0], **xr_open) as ds:
        static_vars = [v for v, da in ds.variables.items() if 'time' not in da.dims]
        static_vars = static_vars+['time', ds.time.attrs['bounds']]

        time_vars = [v for v, da in ds.variables.items() if 'time' in da.dims and
                     v not in static_vars]
    return static_vars, time_vars

# Insert gen_time_series function - same input arguements - main will just call it
# this would run through the history to timeseries
@click.command()
@click.argument('case')
@click.option('--components', default='atm, lnd, rof, ocn, ice, glc, wav')
@click.option('--nworkers', default=12)
@click.option('--archive-root', default=ARCHIVE_ROOT)
@click.option('--output-root', default=None)
@click.option('--only-streams', default=[])
@click.option('--only-variables', default=None)
@click.option('--year-groups', default=None)
@click.option('--demo', default=False, is_flag=True)
@click.option('--clobber', default=False, is_flag=True)

def _main(case, components=['atm', 'lnd', 'rof', 'ocn', 'ice', 'glc', 'wav'], nworkers=12,
         archive_root=ARCHIVE_ROOT, output_root=None,
         only_streams=[], only_variables=None,
         year_groups=None, demo=False, clobber=False):

    droot = os.path.join(archive_root, case)
    if isinstance(components, str):
        components = components.split(', ')

    if output_root is None:
        droot_out = droot
    else:
        droot_out = os.path.join(output_root, case)

    if year_groups is None:
        year_groups = [(0, 5)]
        report_year_groups = False

    elif isinstance(year_groups, str):
        year_groups = year_groups.split(',')
        year_groups = [tuple(int(i) for i in ygi.split(':')) for ygi in year_groups]
        report_year_groups = True
    else:
        raise ValueError('cannot parse year groups')

    if isinstance(only_streams, str):
        only_streams = only_streams.split(',')

    if isinstance(only_variables, str):
        only_variables = only_variables.split(',')

    logger.info('constructing time-series of the following year groups:')
    logger.info(year_groups)
    print()

    with open(f'{script_path}/cesm_streams.yml') as f:
        streams = yaml.safe_load(f)

    # Create a list for tasks - this will be used later to separate into workers
    task_list = []
    for component in components:
        print('='*80)
        logger.info(f'working on component: {component}')
        print('='*80)
        for stream, stream_info in streams[component].items():

            if only_streams:
                if stream not in only_streams:
                    continue

            print('-'*80)
            logger.info(f'working on stream: {stream}')
            print('-'*80)

            dateglob = stream_info['dateglob']
            dateregex = stream_info['dateregex']
            freq = stream_info['freq']

            dout = f'{droot_out}/{component}/proc/tseries/{freq}'
            if not os.path.exists(dout):
                os.makedirs(dout, exist_ok=True)

            # get input files
            files = sorted(glob(f'{droot}/{component}/hist/{case}.{stream}.{dateglob}.nc'))
            if len(files) == 0:
                logger.warning(f'no files: component={component}, stream={stream}')
                continue

            # get file dates
            files_year = [get_year_filename(f) for f in files]

            # get variable lists
            static_vars, time_vars = get_vars(files)
            if only_variables is not None:
                time_vars = [v for v in time_vars if v in only_variables]
                print(only_variables)
                if not static_vars:
                    continue

            # make a report
            logger.info(f'found {len(files)} history files')
            logger.info(f'history file years: {min(files_year)}-{max(files_year)}')
            logger.info(f'found {len(time_vars)} variables to process')
            logger.info(f'expecting to generate {len(time_vars) * len(year_groups)} timeseries files')

            for y0, yf in year_groups:

                if report_year_groups:
                    logger.info(f'working on year group {y0}-{yf}')

                files_group_i = [f for f, y in zip(files, files_year)
                                 if (y0 <= y) and (y <= yf)]

                fid, tmpfile = tempfile.mkstemp(suffix='.filelist', prefix='tmpfile',
                                                dir=os.environ['TMPDIR'])

                with open(tmpfile,'w') as fid:
                    for i, f in enumerate(files_group_i):
                        fid.write('%s\n'%f)

                # get the date string
                date_cat = get_date_string(files_group_i, freq)

                for i, v in enumerate(time_vars):
                    file_cat_basename = '.'.join([case, stream, v, date_cat, 'nc'])
                    file_cat = os.path.join(dout, file_cat_basename)

                    if not clobber:
                        if os.path.exists(file_cat):
                            print(f'exists: {file_cat_basename}...skipping')
                            continue

                    logger.info(f'creating {file_cat}')
                    vars = ','.join(static_vars+[v])
                    cat_cmd = [f'cat {tmpfile} | ncrcat -O -h -v {vars} {file_cat}']
                    compress_cmd = [f'ncks -O -4 -L 1 {file_cat} {file_cat}']

                    
                        
                    # Append lists of tasks
                    task_list.append(cat_cmd)
                    task_list.append(compress_cmd)

    # Make sure there are an even number of workers to match tasks
    if nworkers % 2 == 0:
        None
    else:
        nworkers - 1
    
    # Determine how many tasks to send to a single worker
    n = len(task_list) // (nworkers-1)

    # Create new task list which has a length = nworker
    dist_task_list = [task_list[i:i + n] for i in range(0, len(task_list), n)]


    for task in dist_task_list:
        jid = tm.submit(task,
                        modules=['nco'], memory='100GB')

        print()

    tm.wait()

if __name__ == '__main__':
    _main()