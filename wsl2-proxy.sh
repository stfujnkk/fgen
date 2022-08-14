#!/bin/bash
host_ip=$(cat /etc/resolv.conf |grep "nameserver" |cut -f 2 -d " ")
export HTTP_PROXY="http://$host_ip:7890"
export HTTPS_PROXY="http://$host_ip:7890"
export ALL_PROXY="http://$host_ip:7890"