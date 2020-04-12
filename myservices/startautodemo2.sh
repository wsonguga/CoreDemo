#!/bin/bash

n=$1
path=$2

filename=$(echo $path | awk -F"/" '{print $NF}')
folder=$(echo "${path%%/$filename*}")

for D in /tmp/pycore*; do
    if [ -d "${D}" ]; then
       for (( i = 1; i <= $n; i++ ))
	do
	      coresendmsg exec node=$i num=1001 cmd="$2"
	done
   fi
done
