#!/bin/bash
# usage: ./startautodemo.sh n command-path-name

n=$1
cmdname=$2

for D in /tmp/pycore*; do
    if [ -d "${D}" ]; then
       for (( i = 1; i <= $n; i++ ))
	do
	      coresendmsg exec node=$i num=1001 cmd="$cmdname"
	done
   fi
done
