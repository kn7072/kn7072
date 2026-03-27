#!/bin/bash

# flushing all chains
iptables -F
# deleting all user-defined chains
iptables -X

# разрешются исходящие новые,установленые,связанные пакеты
iptables -A OUTPUT -m state --state NEW,ESTABLISHED,RELATED -j ACCEPT

# разрешение входящего и исхдящего ssh трафика
iptables -A INPUT -p tcp --dport 22 -j ACCEPT
iptables -A OUTPUT -p tcp --dport 22 -j ACCEPT

#create a new chain named ACCEPTED_MAC
iptables -N ACCEPTED_MAC

#add rules to the user defined-chain
iptables -A ACCEPTED_MAC -m mac --mac-source B8:81:98:22:C7:6B -j ACCEPT
iptables -A ACCEPTED_MAC -m mac --mac-source B8:81:98:22:C6:7C -j ACCEPT
iptables -A ACCEPTED_MAC -m mac --mac-source B8:81:98:22:23:AB -j ACCEPT
iptables -A ACCEPTED_MAC -m mac --mac-source B8:81:98:22:67:AA -j ACCEPT

# jump from the INPUT chain to the user-defined chain
# now packets traverse the iptables rules in the user-defined chain
iptables -A INPUT -j ACCEPTED_MAC

#if not dropped or accepted (terminating target) packets continue traversing the INPUT chain
iptables -A INPUT -p icmp -j ACCEPT
iptables -A OUTPUT -p icmp -j ACCEPT

# политика поумолчанию для входных и выходных цепочек
iptables -P OUTPUT DROP
iptables -P INPUT DROP
