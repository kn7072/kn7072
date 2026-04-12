#!/bin/bash
iptables -F # Очищаем все цепочки таблицы filter

# Создаем специальную цепочку для проверки пакетов из нашей подсети

iptables -N OUT_SUBNET
iptables -A OUT_SUBNET -s 192.168.1.33 -j RETURN # Запрещенный хост — выходим
iptables -A OUT_SUBNET -s 10.134.0.100 -j RETURN # Запрещенный хост — выходим

# Всем остальным хостам подсети разрешаем доступ к нужным портам

iptables -A OUT_SUBNET -p tcp -m multiport --dports 22,53,8080,139,445 -j ACCEPT
iptables -A OUT_SUBNET -p udp -m multiport --dports 53,123,137,138 -j ACCEPT
iptables -A OUT_SUBNET -p icmp --icmp-type 8 -j ACCEPT

# Разрешаем пакеты, если соединение уже было установлено ранее

iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

# Все пакеты из нашей подсети отправляем на проверку в цепочку `OUT_SUBNET`

iptables -A INPUT -s 192.168.1.0/24 -j OUT_SUBNET
iptables -P INPUT DROP    # Что не разрешено — то запрещено
iptables -P OUTPUT ACCEPT # На выход — можно все
