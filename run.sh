#!/bin/sh -x


#singularity run docker://lukasheinrich/folding:latest FAHClient --user=CERN --team=38188 --gpu=false --smp=true
cores=1
smp=false
if [ $# -ne 0 ]; then
cores=$1
smp=true
fi

FAHClient --user=Anonymous --team=258507 --gpu=false --smp=$smp --cpus=$cores --exit-when-done=true --max-units=1
