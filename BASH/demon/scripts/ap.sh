SSID=OculustTest
CONNECTION=$SSID-ap
SSID_PASSWORD=12345678
echo "Создаем точку доступа $SSID"
nmcli connection delete $CONNECTION
nmcli connection add type wifi ifname wlan0 con-name $CONNECTION ssid $SSID ipv4.method manual ipv4.addresse 10.0.0.1/24
nmcli connection modify $CONNECTION autoconnect no
nmcli connection modify $CONNECTION mode ap

#nmcli connection modify $CONNECTION ipv4.method manual
#nmcli connection modify $CONNECTION ipv4.address 10.0.0.1/24
nmcli connection modify $CONNECTION ipv4.dns 10.0.0.1
nmcli connection modify $CONNECTION ipv4.never-default yes

nmcli connection modify $CONNECTION ipv6.method disabled

nmcli connection modify $CONNECTION 802-11-wireless.band bg
nmcli connection modify $CONNECTION 802-11-wireless.channel 11
nmcli connection modify $CONNECTION 802-11-wireless.cloned-mac-address 00:12:34:56:78:9a

nmcli connection modify $CONNECTION 802-11-wireless-security.key-mgmt wpa-psk
nmcli connection modify $CONNECTION 802-11-wireless-security.psk $SSID_PASSWORD

nmcli connection up $CONNECTION

