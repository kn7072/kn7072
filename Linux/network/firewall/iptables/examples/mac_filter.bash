#!/bin/bash
# разрешить доступ в интернет только для некоторых машин с заданными мак адресами
iptables -F FORWARD

PERMITTED_MACS="52:54:00:63:88:2e 52:54:00:63:88:22 52:54:00:63:88:21"

for MAC in $PERMITTED_MACS; do
  iptables -A FORWARD -m mac --mac-source "${MAC}" -j ACCEPT
  echo "${MAC} permitted"
done

iptables -P FORWARD DROP
