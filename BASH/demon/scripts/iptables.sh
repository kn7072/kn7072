echo "Устанавливаем iptables"
sudo apt install iptables

echo "Генерируем правила iptables"
sudo sysctl -w net.ipv4.ip_forward=1

sudo iptables -P FORWARD ACCEPT

sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

sudo iptables -t nat -A PREROUTING -i wlan0 -p tcp -j DNAT --to-destination 10.0.0.1:9040
sudo iptables -t nat -A PREROUTING -i wlan0 -p udp --dport 53 -j DNAT --to-destination 10.0.0.1:53

sudo iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE
