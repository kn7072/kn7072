## создать мост с помощью ip или с помощью netplan

```
ip link add br0 type bridge
```

## запуск виртуальных машин

запускать под sudo

```
./start_machine.sh тут_имя_образа_с_виртуальной_машины
```

## установить ip на мост и запустить dhcp сервер

[источник](https://wiki.archlinux.org/title/QEMU#Networking)

```
ip addr add 172.20.0.1/16 dev br0
ip link set br0 up
dnsmasq -C /dev/null --interface=br0 --bind-interfaces --dhcp-range=172.20.0.2,172.20.255.254
```
