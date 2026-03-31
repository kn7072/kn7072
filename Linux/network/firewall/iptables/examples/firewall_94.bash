#!/bin/bash

# permit loopback interface traffic
iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT

iptables -A INPUT -m state --state INVALID -j DROP
iptables -A OUTPUT -m state --state INVALID -j DROP

# allow icmp traffic
iptables -A INPUT -p icmp -j ACCEPT
iptables -A OUTPUT -p icmp -j ACCEPT

# allowed tcp ports
PERMIT_TCP="20 21 25 465 80 443 110 143 993"
for PORT in ${PERMIT_TCP}; do
  iptables -A INPUT -p tcp --dport "${PORT}" -j ACCEPT
done

# allow DNS traffic
iptables -A INPUT -p udp --dport 53 -j ACCEPT

# ip addresses allowed to connect using ssh
PERMIT_SSH="192.168.1.1 192.168.1.33 192.168.1.58 192.168.1.55"
for IP in ${PERMIT_SSH}; do
  iptables -A INPUT -p tcp --dport 22 -s "${IP}" -j ACCEPT
done

# permit no more than 50 concurent connections from the same ip address to our web server
# iptables -m connlimit --help
iptables -A INPUT -p tcp -m multiport --dports 80,443 -m connlimit --connlimit-above 50 -j DROP

# permit all traffic from the following mac addresses
ALLOWED_MAC="a0:b3:cc:49:df:65 a2:c8:84:2f:c6:3e 9e:d5:18:3a:93:e8"
for MAC in ${ALLOWED_MAC}; do
  # iptables -m mac --help
  iptables -A INPUT -m mac --mac-source "${MAC}" -j ACCEPT
done

# iptables -m state --help
iptables -A OUTPUT -m state --state NEW,ESTABLISHED,RELATED -j ACCEPT

# set default policy DROP
iptables -P INPUT DROP
iptables -P OUTPUT DROP
