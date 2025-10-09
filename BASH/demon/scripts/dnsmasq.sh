CONF="/etc/dnsmasq.conf"

echo "Устанавливаем dnsmasq"
sudo apt install dnsmasq

echo "Генерируем ${CONF}"
sudo systemctl stop dnsmasq
cat > "${CONF}" <<EOF
interface=wlan0

dhcp-range=10.0.0.10,10.0.0.250,12h
dhcp-option=3,10.0.0.1
dhcp-option=6,10.0.0.1

log-queries
log-dhcp
EOF

sudo systemctl start dnsmasq
