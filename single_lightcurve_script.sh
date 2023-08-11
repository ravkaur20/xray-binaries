#!/bin/bash



evt=$1
reg=$2
echo EvtFile=$1
echo RegionFile=$2


dmkeypar $evt TIMEDEL
tdl=`pget dmkeypar rval`
export tdl


dmcopy $evt"[sky=region($reg)]" evt.src
#dmcopy $var1"[sky=region($var3)]" evt.bkg

bintime=$(python3.9 /data/reu/rkaur/project/math_script.py)

#dt=500
#fdt=expr $dt / $tdl
#ndt=${fdt%.*}
#bintime=$("$ndt*$tdl" | bc)
echo $bintime

dmextract "evt.src[energy=300:7000][bin time=::$bintime]" evt.b.lc opt=ltc1 #bkg="evt.bkg[energy=300:7000]"
dmextract "evt.src[energy=300:1200][bin time=::$bintime]" evt.s.lc opt=ltc1 #bkg="evt.bkg[energy=300:1200]"
dmextract "evt.src[energy=1200:2000][bin time=::$bintime]" evt.m.lc opt=ltc1 #bkg="evt.bkg[energy=1200:2000]"
dmextract "evt.src[energy=2000:7000][bin time=::$bintime]" evt.h.lc opt=ltc1 #bkg="evt.bkg[energy=2000:7000]"

dmlist evt.b.lc"[cols time,count_rate,count_rate_err,counts,exposure,area]" data,clean > b.lc.txt
dmlist evt.s.lc"[cols time,count_rate,count_rate_err,counts,exposure,area]" data,clean > s.lc.txt
dmlist evt.m.lc"[cols time,count_rate,count_rate_err,counts,exposure,area]" data,clean > m.lc.txt
dmlist evt.h.lc"[cols time,count_rate,count_rate_err,counts,exposure,area]" data,clean > h.lc.txt
