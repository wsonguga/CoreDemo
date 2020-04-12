#!/bin/bash
export ServiceHOME=/home/student/CoreDemo/myservices
#homefolder="$(pwd)"
#homefolder="/tmp/pycore.55045-n1.conf"
#nodeid=`echo "$homefolder" | grep -Eo "[[:digit:]]+" | tail -n1`

# echo $ServiceHOME/bcastsendrecv.py 192.168.0.255 >> tmp.log
stdbuf -oL nohup $ServiceHOME/bcastsendrecv.py 192.168.0.255 >> sendrecv.log

#if [ $nodeid -eq 1 ]; then
#  echo $ServiceHOME/bcastsend.py 192.168.0.255 >> tmp.log
#  stdbuf -oL nohup $ServiceHOME/bcastsend.py 192.168.0.255 >> send.log
#else
#  echo $CoreHOME/bcastrecv.py >> tmp.log
#  stdbuf -oL nohup $ServiceHOME/bcastrecv.py >> recv.log
#fi

