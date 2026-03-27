#!/bin/bash

# роутер имеет два внешних интерфейса(два провайдера) eth1 и eth2
# если запросы из локальной сети поступают на порты ISP1 тогда
# все запросы перенаправляем через первого провайдера eth1, иначе через второго eth2

# web: 80 443
# email: 25 465 143 993 110 995
# ssh: 22

# запросы поступающие на эти порты будут перенаправляться на eth1 (-o eth1)
ISP1="22 25 80 110 143 443 465 993 995"

# flushing nat table and POSTROUTING chain
iptables -t nat -F POSTROUTING

# enable routing
echo "1" >/proc/sys/net/ipv4/ip_forward

for port in $ISP1; do
  iptables -t nat -A POSTROUTING -p tcp --dport "${port}" -o eth1 -j MASQUERADE
done

# Traffic not NATed goes over the 2nd connection
iptables -t nat -A POSTROUTING -o eth2 -j MASQUERADE
