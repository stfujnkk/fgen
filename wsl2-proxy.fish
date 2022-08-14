#!/usr/bin/env fish
set host_ip (cat /etc/resolv.conf |grep "nameserver" |cut -f 2 -d " ")
set -x HTTP_PROXY http://{$host_ip}:7890
set -x HTTPS_PROXY http://{$host_ip}:7890
set -x ALL_PROXY http://{$host_ip}:7890