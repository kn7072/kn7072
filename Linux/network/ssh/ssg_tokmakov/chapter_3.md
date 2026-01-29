[источник](https://tokmakov.msk.ru/blog/item/495)

- [ Вход на сервер по ключу](#link_1)
- [ Настройка сервера](#link_2)
  - [ 1. Добавляем пользователя ssh-vpn](#link_3)
  - [ 2. Настройки OpenSSH сервера](#link_4)
  - [ 3. Создаем TUN устройство при загрузке](#link_5)
  - [ 4. Пересылка пакетов tun0→ens3 и ens3→tun0](#link_6)
  - [ 5. Перезагружаем сервер](#link_7)
- [ Настройка маршрутизатора](#link_8)
  - [ 1. Сетевые интерфейсы и форвардинг](#link_9)
  - [ 2. Создание пользователя ssh-vpn](#link_10)
  - [ 3. Создаем TUN устройство при загрузке](#link_11)
  - [ 4. Создаем туннель при загрузке](#link_12)
  - [ 5. Заворачиваем трафик в туннель](#link_13)
  - [ 6. Перезагружаем маршрутизатор](#link_14)
- [ Теперь все готово](#link_15)

# VPN-канал с помощью OpenSSH. Часть третья

Мы посмотрели, как можно завернуть весь трафик одного компьютера в защищенный туннель. Теперь посмотрим, как можно направить в туннель трафик всех компьютеров локальной сети. Итак, у нас есть сервер с белым ip-адресом `123.123.123.123`, несколько компьютеров в сети `192.168.250.0/24` и маршрутизатор, который обеспечивает для этих компов выход в интернет.

![](chapter_3_images/dc64a8704eed9d6014f1bc09bc267c9b_MD5.jpg)

Для простоты будем считать, что у нас есть физический доступ к маршрутизатору `gateway` и настройку сервера будем выполнять с него. Для этого настроим аутентификацию по ключу на сервере для пользователя `evgeniy`.

## Вход на сервер по ключу <a name="link_1"></a>

Создаем ключи на маршрутизаторе для пользователя `evgeniy`:

```
$ ssh-keygen
```

Копируем публичный ключ на сервер:

```
$ ssh-copy-id -i ~/.ssh/id_rsa.pub evgeniy@123.123.123.123
```

Проверяем аутентификацию по ключу:

```
$ ssh evgeniy@123.123.123.123
Welcome to Ubuntu 18.04.4 LTS (GNU/Linux 4.15.0-91-generic x86_64)
```

## Настройка сервера <a name="link_2"></a>

### 1. Добавляем пользователя ssh-vpn <a name="link_3"></a>

Создаем пользователя `ssh-vpn`:

```
# useradd -mU ssh-vpn
# mkdir /home/ssh-vpn/.ssh/ # директория для хранения ключей
# chown ssh-vpn:ssh-vpn /home/ssh-vpn/.ssh/
# chmod 700 /home/ssh-vpn/.ssh/
```

### 2. Настройки OpenSSH сервера <a name="link_4"></a>

Изменяем настройки ssh-сервера:

```
# nano /etc/ssh/sshd_config
```

```
# Разрешаем создание сетевых туннелей
PermitTunnel point-to-point
# Запрещаем аутентификацию для root
PermitRootLogin no
# Разрешаем аутентификацию по ключу
PubkeyAuthentication yes
# Запрещаем аутентификацию по паролю
PasswordAuthentication no
# Этим пользователям можно входить
AllowUsers evgeniy ssh-vpn
```

```
# systemctl restart ssh.service
```

### 3. Создаем TUN устройство при загрузке <a name="link_5"></a>

Теперь нужно добавить TUN устройство при загрузке системы, которое будет доступно для чтения и записи пользователю `ssh-vpn`.

```
# nano /etc/systemd/network/50-ssh-vpn.netdev
```

```
[NetDev]
Name=tun0
Kind=tun
[Tun]
User=ssh-vpn
```

```
# nano /etc/systemd/network/50-ssh-vpn.network
```

```
[Match]
Name=tun0
[Address]
Address=192.168.200.1/30
Peer=192.168.200.2/30
[Network]
Address=192.168.200.1/30
[Route]
Destination=192.168.250.0/24
Gateway=192.168.200.2
```

Здесь мы указываем маршрут до подсети `192.168.250.0/24` для интерфейса `tun0` — пакеты надо отправлять через шлюз `192.168.200.2`. Другими словами — отправлять пакеты на интерфейс `tun0` маршрутизатора `gateway`. Маршрутизатор перекинет эти пакеты с интерфейса `tun0` на интерфейс `enp0s8` и отправит дальше — компьютеру `pc1` или `pc2`.

### 4. Пересылка пакетов tun0→ens3 и ens3→tun0 <a name="link_6"></a>

Маршрутизатор будет направлять трафик в туннель, но что делать с этим трафиком — сервер пока не знает. Нужно включить пересылку пакетов между интерфейсами `tun0` и `ens3`.

```
# nano /etc/sysctl.conf

net.ipv4.ip_forward=1
```

```
# iptables -P FORWARD DROP

# iptables -A FORWARD -i tun0 -o ens3 -s 192.168.250.0/24 -j ACCEPT
# iptables -A FORWARD -i ens3 -o tun0 -d 192.168.250.0/24 -j ACCEPT
```

Теперь добавим SNAT (подмена адреса источника), что позволит всем компьютерам подсети `192.168.250.0/24` выходить в интернет, используя единственный ip-адрес `123.123.123.123`.

```
# iptables -t nat -A POSTROUTING -o ens3 -s 192.168.250.0/24 -j MASQUERADE
```

Правила мы добавили, но они пропадут при перезагрузке сервера. Так что их нужно сохранить и восстанавливать при перезагрузке. В этом нам поможет пакет `iptables-persistent`, который добавит новую службу `netfilter-persistent.service`:

```
# apt install iptables-persistent
```

При установке пакета будет предложено сохранить текущие правила `iptables`:

- в файл `/etc/iptables/rules.v4` для протокола IPv4
- в файл `/etc/iptables/rules.v6` для протокола IPv6

### 5. Перезагружаем сервер <a name="link_7"></a>

Перезагружаем сервер и смотрим сетевые интерфейсы, маршруты и правила форвардинга:

```
$ ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: ens3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 52:54:00:3c:57:5a brd ff:ff:ff:ff:ff:ff
    inet 123.123.123.123/24 brd 123.123.123.255 scope global ens3
       valid_lft forever preferred_lft forever
    inet6 fe80::5054:ff:fe3c:575a/64 scope link
       valid_lft forever preferred_lft forever
3: tun0: <POINTOPOINT,MULTICAST,NOARP,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 500
    link/none
    inet 192.168.200.1 peer 192.168.200.2/30 scope global tun0
       valid_lft forever preferred_lft forever
    inet6 fe80::873f:8e56:6aec:88bf/64 scope link stable-privacy
       valid_lft forever preferred_lft forever
```

На самом деле такой вывод команды `ip addr` будет только после того, как мы настроим маршрутизатор `gateway`. А в этот момент интерфейс `tun0` будет выключен, потому что туннель еще не создан. Но мы это скоро исправим.

```
$ route -n
Destination     Gateway         Genmask           Flags   Metric   Ref   Use   Iface
------------------------------------------------------------------------------------
0.0.0.0         123.123.123.1   0.0.0.0           UG      0        0     0     ens3
123.123.123.0   0.0.0.0         255.255.255.0     U       0        0     0     ens3
192.168.200.0   0.0.0.0         255.255.255.252   U       0        0     0     tun0
192.168.250.0   192.168.200.2   255.255.255.0     UG      0        0     0     tun0
```

Красным выделены маршруты, которые были добавлены при создании TUN устройства.

```
# iptables -t filter -L -v --line-numbers
..........
Chain FORWARD (policy DROP 0 packets, 0 bytes)
num   pkts   bytes   target   prot   opt   in     out    source             destination
1        0       0   ACCEPT   all    --    tun0   ens3   192.168.250.0/24   anywhere
2        0       0   ACCEPT   all    --    ens3   tun0   anywhere           192.168.250.0/24
..........
```

```
# iptables -t nat -L -v --line-numbers
..........
Chain POSTROUTING (policy ACCEPT 0 packets, 0 bytes)
num   pkts   bytes   target       prot   opt   in    out    source             destination
1        0       0   MASQUERADE   all    --    any   ens3   192.168.250.0/24   anywhere
..........
```

## Настройка маршрутизатора <a name="link_8"></a>

Перед настройкой нужно сделать небольшое лирическое отступление. Если бы мы просто настраивали маршрутизатор, нам нужно было включить пересылку пакетов между интерфейсами, создать несколько правил для `netfilter` с помошью утилиты `iptables` и добавить SNAT:

```
# nano /etc/sysctl.conf

net.ipv4.ip_forward=1
```

```
# iptables -P FORWARD DROP

# iptables -A FORWARD -i enp0s8 -o enp0s3 -s 192.168.250.0/24 -j ACCEPT # enp0s8 -> enp0s3
# iptables -A FORWARD -i enp0s3 -o enp0s8 -d 192.168.250.0/24 -j ACCEPT # enp0s3 -> enp0s8

# iptables -t nat -A POSTROUTING -o enp0s3 -s 192.168.250.0/24 -j MASQUERADE
```

Но, поскольку мы будем направлять весь трафик в туннель, порядок действий будет несколько иным.

### 1. Сетевые интерфейсы и форвардинг <a name="link_9"></a>

Сначала настраиваем сетевые интерфейсы:

```
# nano /etc/netplan/01-netcfg.yaml
```

```
network:
  version: 2
  renderer: networkd
  ethernets:
    enp0s3:
      dhcp4: no
      addresses: [192.168.150.2/24]
      gateway4: 192.168.150.1
      nameservers:
        addresses: [8.8.8.8, 8.8.4.4]
    enp0s8:
      dhcp4: no
      addresses: [192.168.250.1/24]
```

Пересылка пакетов между интерфейсами по умолчанию отключена, так что редактируем файл `/etc/sysctl.conf`:

```
# nano /etc/sysctl.conf

net.ipv4.ip_forward=1
```

После этого настраиваем `netfilter` с помощью утилиты `iptables`:

```
# iptables -P FORWARD DROP

# iptables -A FORWARD -i enp0s8 -o tun0 -s 192.168.250.0/24 -j ACCEPT # enp0s8 -> tun0
# iptables -A FORWARD -i tun0 -o enp0s8 -d 192.168.250.0/24 -j ACCEPT # tun0 -> enp0s8
```

Правила мы добавили, но они пропадут при перезагрузке сервера. Так что их нужно сохранить и восстанавливать при перезагрузке. В этом нам поможет пакет `iptables-persistent`, который добавит новую службу `netfilter-persistent.service`:

```
# apt install iptables-persistent
```

При установке пакета будет предложено сохранить текущие правила `iptables`:

- в файл `/etc/iptables/rules.v4` для протокола IPv4
- в файл `/etc/iptables/rules.v6` для протокола IPv6

### 2. Создание пользователя ssh-vpn <a name="link_10"></a>

Создаем пользователя `ssh-vpn`:

```
# useradd -mU ssh-vpn
```

Создаем публичный и приватный ключи:

```
# su ssh-vpn # дальше все команды выполянем от имени пользователя ssh-vpn
$ cd /home/ssh-vpn/
$ ssh-keygen
Generating public/private rsa key pair.
Enter file in which to save the key (/home/ssh-vpn/.ssh/id_rsa): Enter
Created directory '/home/ssh-vpn/.ssh/'.
Enter passphrase (empty for no passphrase): Enter
Enter same passphrase again: Enter
Your identification has been saved in /home/ssh-vpn/.ssh/id_rsa.
Your public key has been saved in /home/ssh-vpn/.ssh/id_rsa.pub.
$ exit # завершаем сеанс работы под пользователем ssh-vpn
```

Теперь нам надо скопировать публичный ключ на сервер с помощью команды `scp`. Но у нас нет доступа для пользователя `evgeniy`:

- к директории `/home/ssh-vpn/.ssh/` на маршрутизаторе
- к директории `/home/ssh-vpn/.ssh/` на сервере

Изменяем права на директорию `/home/ssh-vpn/.ssh/` на маршрутизаторе:

```
# chmod 707 /home/ssh-vpn/.ssh/
```

Изменяем права на директорию `/home/ssh-vpn/.ssh/` на сервере:

```
# chmod 707 /home/ssh-vpn/.ssh/
```

Копируем от имени пользователя `evgeniy` публичный ключ на сервер:

```
$ scp /home/ssh-vpn/.ssh/id_rsa.pub evgeniy@123.123.123.123:/home/ssh-vpn/.ssh/authorized_keys
```

Возвращаем обратно права на директорию на маршрутизаторе:

```
# chmod 700 /home/ssh-vpn/.ssh/
```

Задаем владельца и права для файла `authorized_keys` на сервере:

```
# chown ssh-vpn:ssh-vpn /home/ssh-vpn/.ssh/authorized_keys
# chmod 600 /home/ssh-vpn/.ssh/authorized_keys
```

Возвращаем обратно права на директорию на сервере:

```
# chmod 700 /home/ssh-vpn/.ssh/
```

И надо обязательно выполнить вход по ssh на сервер от имени пользователя `ssh-vpn` с маршрутизатора, чтобы был создан файл `known_hosts`. Иначе потом, при автоматическом создании туннеля в момент загрузки `gateway`, получим сообщение об ошибке «Host key verification failed».

```
# su ssh-vpn # команду выполяняем от имени пользователя ssh-vpn
$ ssh -i ~/.ssh/id_rsa ssh-vpn@123.123.123.123
..........
Are you sure you want to continue connecting (yes/no)? yes
..........
$ exit # завершаем ssh-сеанс c сервером 123.123.123.123
$ exit # завершаем сеанс работы под пользователем ssh-vpn
```

### 3. Создаем TUN устройство при загрузке <a name="link_11"></a>

Теперь нужно добавить TUN устройство при загрузке системы, которое будет доступно для чтения и записи пользователю `ssh-vpn`.

```
# nano /etc/systemd/network/50-ssh-vpn.netdev
```

```
[NetDev]
Name=tun0
Kind=tun
[Tun]
User=ssh-vpn
```

```
# nano /etc/systemd/network/50-ssh-vpn.network
```

```
[Match]
Name=tun0
[Address]
Address=192.168.200.2/30
Peer=192.168.200.1/30
[Network]
Address=192.168.200.2/30
```

### 4. Создаем туннель при загрузке <a name="link_12"></a>

Для этого нам нужна служба, которая будет создавать туннель при загрузке системы. Кроме того, при обрыве связи эта служба будет пытаться снова установить соединение.

```
# nano /etc/systemd/system/ssh-vpn-tunnel-to-server.service
```

```
[Unit]
Description=SSH tunnel to 123.123.123.123 at startup
Requires=network-online.target
After=network-online.target
[Service]
User=ssh-vpn
ExecStartPre=/bin/sh -c 'until ping -c1 123.123.123.123; do sleep 1; done;'
ExecStart=/usr/bin/ssh -i /home/ssh-vpn/.ssh/id_rsa -N -w 0:0 ssh-vpn@123.123.123.123
Restart=always
RestartSec=3
[Install]
WantedBy=multi-user.target
```

Сообщаем системе про новый unit-файл:

```
# systemctl daemon-reload
```

Добавляем новую службу в автозагрузку:

```
# systemctl enable ssh-vpn-tunnel-to-server.service
```

### 5. Заворачиваем трафик в туннель <a name="link_13"></a>

Чтобы перенаправить весь трафик подсети `192.168.250.0/24` через туннель, нужно вместо старого шлюза — `192.168.150.1` (через интерфейс `enp0s3`) указать новый — `192.168.200.1` (через интерфейс `tun0`). Но при этом потеряется связь с сервером — поэтому перед заменой шлюза нужно добавить маршрут до сервера.

```
# ip route add 123.123.123.123/32 via 192.168.150.1 dev enp0s3
# ip route replace default via 192.168.200.1 dev tun0
```

Но эти два маршрута пропадут при перезагрузке системы, так что добавим две новые службы:

```
# nano /etc/systemd/system/ssh-vpn-route-to-server.service
```

```
[Unit]
Description=Route to server for SSH tunnel at startup
Requires=network-online.target ssh-vpn-tunnel-to-server.service
After=network-online.target ssh-vpn-tunnel-to-server.service
[Service]
ExecStartPre=/bin/sh -c 'until ping -c1 123.123.123.123; do sleep 1; done;'
ExecStart=/bin/ip route add 123.123.123.123 via 192.168.150.1 dev enp0s3
RemainAfterExit=yes
[Install]
WantedBy=multi-user.target
```

```
# nano /etc/systemd/system/ssh-vpn-new-default-route.service
```

```
Description=Replace default route for SSH tunnel at startup
Requires=network-online.target ssh-vpn-tunnel-to-server.service ssh-vpn-route-to-server.service
After=network-online.target ssh-vpn-tunnel-to-server.service ssh-vpn-route-to-server.service
[Service]
ExecStartPre=/bin/sh -c 'until ping -c1 192.168.200.1; do sleep 1; done;'
ExecStart=/bin/ip route replace default via 192.168.200.1 dev tun0
RemainAfterExit=yes
[Install]
WantedBy=multi-user.target
```

Сообщим системе про два новых unit-файла:

```
# systemctl daemon-reload
```

Добавляем новые службы в автозагрузку:

```
# systemctl enable ssh-vpn-route-to-server.service
# systemctl enable ssh-vpn-new-default-route.service
```

### 6. Перезагружаем маршрутизатор <a name="link_14"></a>

Перезагружаем маршрутизатор, чтобы добавить TUN-устройство, создать SSH-туннель и завернуть трафик клиента в туннель:

```
# reboot
```

После этого смотрим сетевые интерфейсы, маршруты и правила форвардинга:

```
$ ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:31:44:64 brd ff:ff:ff:ff:ff:ff
    inet 192.168.150.2/24 brd 192.168.150.255 scope global dynamic enp0s3
       valid_lft 24945sec preferred_lft 24945sec
    inet6 fe80::a00:27ff:fe31:4464/64 scope link
       valid_lft forever preferred_lft forever
3: enp0s8: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:06:4a:53 brd ff:ff:ff:ff:ff:ff
    inet 192.168.250.1/24 brd 192.168.250.255 scope global enp0s8
       valid_lft forever preferred_lft forever
    inet6 fe80::a00:27ff:fe06:4a53/64 scope link
       valid_lft forever preferred_lft forever
4: tun0: <POINTOPOINT,MULTICAST,NOARP,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 500
    link/none
    inet 192.168.200.2 peer 192.168.200.1/30 scope global tun0
       valid_lft forever preferred_lft forever
    inet6 fe80::1f5a:a3e3:341e:96cf/64 scope link stable-privacy
       valid_lft forever preferred_lft forever
```

```
$ route -n
Destination     Gateway          Genmask           Flags   Metric   Ref   Use   Iface
--------------------------------------------------------------------------------------
0.0.0.0           192.168.200.1   0.0.0.0           UG      0        0     0     tun0
0.0.0.0           192.168.150.1   0.0.0.0           UG      100      0     0     enp0s3
123.123.123.123   192.168.150.1   255.255.255.255   UGH     0        0     0     enp0s3
192.168.150.0     0.0.0.0         255.255.255.0     U       0        0     0     enp0s3
192.168.150.1     0.0.0.0         255.255.255.255   UH      100      0     0     enp0s3
192.168.200.0     0.0.0.0         255.255.255.252   U       0        0     0     tun0
192.168.250.0     0.0.0.0         255.255.255.0     U       0        0     0     enp0s8
```

Красным выделены маршруты, которые мы добавили. А зеленым — маршрут, который был добавлен при создании TUN-устройства.

```
# iptables -t filter -L -v --line-numbers
..........
Chain FORWARD (policy DROP 0 packets, 0 bytes)
num   pkts bytes   target   prot   opt   in       out      source             destination
1        0     0   ACCEPT   all    --    enp0s8   tun0     192.168.250.0/24   anywhere
2        0     0   ACCEPT   all    --    tun0     enp0s8   anywhere           192.168.250.0/24
..........
```

## Теперь все готово <a name="link_15"></a>

Теперь все готово, так что открываем на компьютере `pc1` браузер и смотрим свой ip-адрес:

![](chapter_3_images/7b6371f2b1c8c7cd7ba85f9f5a920d4f_MD5.png)
