#!/bin/bash
clear
PYTHON=$(which python3)
SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
#echo "Script path: $SCRIPTPATH"
now="$(date +'%d/%m/%Y %T')"

res=$(/usr/bin/ntpstat)
rc=$?
while [ $rc != 0 ]
do
    echo "NTP not running, sleep 1 second at $now"
    sleep 1
done

SERVICE="$SCRIPTPATH/socket_to_mqtt.py"
LOG="log.txt"
process=$(pgrep -f "$SERVICE")
process=${process[0]}
#echo "the process ID of $mac is $process"

if [[ ! -z $process ]]
then
    echo "$SERVICE is running at $now"
else
#    echo "$SERVICE stopped at $now, restart!" >> $SCRIPTPATH/$LOG
    cd $SCRIPTPATH
    $PYTHON $SERVICE
fi
