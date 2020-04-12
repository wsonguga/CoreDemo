#!/bin/bash
sudo ifconfig $1 $3
sudo iptables --table nat --append POSTROUTING --out-interface $2 -j MASQUERADE
sudo iptables --append FORWARD --in-interface $1 -j ACCEPT
echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward

