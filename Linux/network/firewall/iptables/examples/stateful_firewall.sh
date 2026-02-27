#!/bin/bash
# разрешается весь исходящий трафик и входящий для ранее инициированных соединений, а такжее новые входящие ssh подключения с 192.168.1.1

iptables -F

iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT

iptables -A INPUT -p tcp -m tcp -m state --state NEW --dport 22 -s 192.168.1.1 -j ACCEPT

iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables -A OUTPUT -m state --state NEW,ESTABLISHED,RELATED -j ACCEPT

iptables -P INPUT DROP
iptables -P OUTPUT DROP
