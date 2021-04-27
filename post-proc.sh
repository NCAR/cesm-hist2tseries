#!/bin/bash
#PBS -N post-proc
#PBS -l select=1:mem=1GB
#PBS -q casper
#PBS -A NCGD0011
#PBS -l 01:00:00
#PBS -j oe

if [ -z $MODULEPATH_ROOT ]; then
  unset MODULEPATH_ROOT
else
  echo "NO MODULEPATH_ROOT TO RESET"
fi
if [ -z $MODULEPATH ]; then
  unset MODULEPATH
else
  echo "NO MODULEPATH TO RESET"
fi
if [ -z $LMOD_SYSTEM_DEFAULT_MODULES ]; then
  unset LMOD_SYSTEM_DEFAULT_MODULES
else
  echo "NO LMOD_SYSTEM_DEFAULT_MODULES TO RESET"
fi
#source /etc/profile

# Export some environment variables
export TERM=xterm-256color
export HOME=/glade/u/home/$USER
unset LD_LIBRARY_PATH
export PATH=/glade/work/#USER/miniconda/bin:$PATH
export PYTHONUNBUFFERED=False
export TMPDIR=/glade/scratch/$USER/tmp

# Load the nco/list modules
module load nco
module list

# Activate your python environment
source activate hist_ts

# Future addition - automating moving to campaign
campaign_path=/glade/campaign/cgd/oce/projects/besome/cesm-cases

# Specify the case name
CASE=g.e22a06.G1850ECOIAF_JRA_PHYS_DEV.TL319_g17.4p4z.001

# In this next section, we continually add onto the arguements, making this more readable
# Specify which components to use (default is all)
ARGS="--components ocn"

# Specify which variables to use (default is all)
ARGS="${ARGS} --only-variables zoo3_loss_zint,zoo4_loss_zint,POC_FLUX_IN" #graze_sp_zoo1,graze_diaz_zoo1,graze_sp_zoo2,graze_cocco_zoo2,graze_diaz_zoo2,grazePAR_avg,PD,TEMP,HMXL,spChl,diatChl,diazChl,coccoChl,POC_FLUX_IN,pocToSed,IFRAC,O2,photoC_cocco_zint,spC,diatC,diazC,coccoC,zoo1C,zoo2C,zoo3C,zoo4C,x_graze_zoo1_zint,x_graze_zoo2_zint,x_graze_zoo3_zint,x_graze_zoo4_zint,photoC_TOT_zint,photoC_sp_zint,photoC_diat_zint,photoC_diaz_zint,Fe,NO3,PO4,SiO3"

# Specify which stream to use
#ARGS="${ARGS} --only-streams pop.h"

# Specify which model years to use - can use start:end or list as in comment
ARGS="${ARGS} --year-groups 1:61" #,63:124,125:186,187:248,249:310"

# Specify whether to transfer to campaign - this is not supported yet
#ARGS="${ARGS} --campaign-transfer --campaign-path ${campaign_path}"

# Whether to use "demo"
#DEMO=  #"--demo"

# Prints out the arguements and case - ensuring you know what is being passed in
echo ${ARGS} ${CASE}

# Run the python script the proper casename and arguements
./cesm_hist2tseries.py ${CASE} ${ARGS}



