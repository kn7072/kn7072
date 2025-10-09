CONF="/etc/tor/torrc"
BRIDGES_CONF="bridges.txt"

echo "Устанавливаем tor"
sudo apt install tor obfs4proxy

echo "Генерируем ${CONF}"
sudo systemctl stop tor
cat > ${CONF} <<'EOF'
VirtualAddrNetwork 192.168.100.0/10

AutomapHostsOnResolve 1

TransPort 10.0.0.1:9040
DNSPort 10.0.0.1:53

UseBridges 1
ClientTransportPlugin obfs4 exec /usr/bin/obfs4proxy
EOF

bridges_count=$(wc -l <"${BRIDGES_CONF}")
echo "Добавляем ${bridges_count} obfs4 в torrc"

while IFS= read -r line || [ -n "$line" ]; do
    echo "Bridge $line" >>"${CONF}"
done < "${BRIDGES_CONF}"

sudo systemctl start tor
