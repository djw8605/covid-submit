#!/bin/sh -x


#singularity run docker://lukasheinrich/folding:latest FAHClient --user=CERN --team=38188 --gpu=false --smp=true
cores=1
if [ $# -ne 0 ]; then
cores=$1
fi

FAHClient --user=Anonymous --team=258507 --gpu=false --smp=false --cpus=$cores
