#!/bin/bash

iptables -P INPUT ACCEPT
iptables -P OUTPUT ACCEPT
iptables -P FORWARD ACCEPT

iptables -t filter -F
iptables -t raw -F
iptables -t nat -F
iptables -t mangle -F

iptables -X

ipset -F
ipset -X
