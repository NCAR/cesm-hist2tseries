# cesm-hist2tseries

## Motivation
This tool is meant to be used for one specific task - converting [Community Earth System Model (CESM) output](https://www.cesm.ucar.edu/) from history to timeseries files.

This a common part of the post-processing workflow, and something that typically involves running a set of bash scripts, can be tough to reproduce and require a fair amount of modification.

This tool aims to fill a need for an open-source, well-documented tool for helping with this model post-processing step.

## What are "history files"? What are "timeseries files"?
CESM output is typically formatted in history files which include ***all model output fields*** organized into a single file for each timestep. This format can be difficult to deal with reading in 

## General workflow
This package has been compiled using tools that @matt-long put together, with underlying tool that combines the data being nco, specifically the `ncks` operator.

The underlying dependencies include:
* [NCO](http://nco.sourceforge.net/_)
* [workflow](https://github.com/NCAR/workflow)

NCO is used for the extraction of variables and concatenation of data, whereas workflow is used to interface with the scheduler.

When you run your scripts, batch jobs will be submitted for each variable you are outputing to individual timeseries files. Once the previous ones in queue are done, `workflow` will submit another job, working through all the variables you specified.

## What do I need to modify to get this to work?
We provide a sample bash script where you set your environment variables, including:
* PATH to your conda environment (ex. `/glade/work/$USER/miniconda/bin:$PATH`)
* TEMPDIR - your temp directory (ex. `/glade/scratch/$USER/tmp`)
* CASE - name of the case you are processing data for (ex. `g.e22a06.G1850ECOIAF_JRA_PHYS_DEV.TL319_g17.4p4z.001`)
* ARCHIVE_ROOT - where you store your cesm model output (default is `/glade/scratch/{USER}/archive`)
* ARGS - arguments to pass into the timeseries conversion tool (ex. `components`, `only-variables`)
    * ex. `ARGS = "--components ocn"`
        * This will only generate timeseries files from the ocean components
    * ex. `ARGS = "--only-variables zoo3_loss_zint, zoo4_loss_zing"`
        * Only processes these varaibles - by default, it will proces all the variables in the input components
    * ex. `ARGS = "--year-groups 1:61"`
        * Processes model years 1 through 61
    * These arguments should be combined into a single string, which is passed into the script - for an example, please look at the example bash script `post-proc_pbs.sh`
* campaign_path (optional) - path to campaign storage, only used if you are using globus to transfer

## Can I run this from the command line?
It should be noted that while it can be convenient to use this in a bash script, you can also use this in the command line as long as:
* You activate a python environment with all the required dependencies
* Set your environment variables properly
* Specify the `CASE` and `ARGS` in the following format when running the script:
    * `python cesm_hist2tseries.py {CASE} {ARGS}`

## How do I run this?
Once you access Casper, follow these steps:
1. Setup your bash script setting the required variables, specifying which components to operate on
1. Within the terminal, run `casperexec`
1. Ensure the permissions are set correctly on your bash file, then run `./post-proc.sh` relacing the name of the file with the name of your bash script
1. Move to your output directory (which is your case directory, under `proc` for each component) (ex. `/glade/scratch/{USER}/archive/CASE/COMPONENT/proc`) which will include a `tseries` directory, separated by `day`, `month`, and `year`, with the default being the time frequency of the history files.