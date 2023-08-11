#!/bin/bash

cd $1
binsize=$2

reg_files=(*reg3.fits)
evt_files=(*regevt3.fits)

for i in ${!evt_files[@]}; do

    evt=${evt_files[i]}
    echo $evt
    reg=${reg_files[i]}
    echo $reg

    dmkeypar $evt TIMEDEL
    tdl=`pget dmkeypar rval`
    export tdl

    dmcopy $evt"[sky=region($reg)]" $evt.src

    evt_str=($evt)
    filename=${evt_str:5:5}_bintime.txt

    bintime=$(python3.9 /data/reu/rkaur/project/math_script.py $binsize)
    echo $bintime
    echo $filename
    echo $bintime > $filename

    dmextract "$evt.src[energy=300:7000][bin time=::$bintime]" $evt.b.lc opt=ltc1 #bkg="evt.bkg[energy=300:7000]"
    dmextract "$evt.src[energy=300:1200][bin time=::$bintime]" $evt.s.lc opt=ltc1 #bkg="evt.bkg[energy=300:1200]"
    dmextract "$evt.src[energy=1200:2000][bin time=::$bintime]" $evt.m.lc opt=ltc1 #bkg="evt.bkg[energy=1200:2000]"
    dmextract "$evt.src[energy=2000:7000][bin time=::$bintime]" $evt.h.lc opt=ltc1 #bkg="evt.bkg[energy=2000:7000]"

    dmlist $evt.b.lc"[cols time,count_rate,count_rate_err,counts,exposure,area]" data,clean > $evt.b.lc.txt
    dmlist $evt.s.lc"[cols time,count_rate,count_rate_err,counts,exposure,area]" data,clean > $evt.s.lc.txt
    dmlist $evt.m.lc"[cols time,count_rate,count_rate_err,counts,exposure,area]" data,clean > $evt.m.lc.txt
    dmlist $evt.h.lc"[cols time,count_rate,count_rate_err,counts,exposure,area]" data,clean > $evt.h.lc.txt
  
done
