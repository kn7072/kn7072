[источник](https://tokmakov.msk.ru/blog/item/493)

- [ Вход на сервер по ключу с gw1 и gw2](#link_1)
- [ Настройка промежуточного сервера](#link_2)
  - [ 1. Добавляем пользователя ssh-vpn](#link_3)
  - [ 2. Настройки OpenSSH сервера](#link_4)
  - [ 3. Создаем два TUN устройства при загрузке](#link_5)
  - [ 4. Пересылка пакетов tun1→tun2 и tun2→tun1](#link_6)
  - [ 4. Перезагрузка промежуточного сервера](#link_7)
- [ Настройка маршрутизатора gw1](#link_8)
  - [ 1. Сетевые интерфейсы и форвардинг](#link_9)
  - [ 2. Создание пользователя ssh-vpn](#link_10)
  - [ 3. Создание TUN-устройства при загрузке](#link_11)
  - [ 4. Создаем туннель при загрузке](#link_12)
  - [ 5. Перезагрузка маршрутизатора](#link_13)
- [ Настройка маршрутизатора gw2](#link_14)
  - [ 1. Сетевые интерфейсы и форвардинг](#link_15)
  - [ 2. Создание пользователя ssh-vpn](#link_16)
  - [ 3. Создание TUN-устройства при загрузке](#link_17)
  - [ 4. Создаем туннель при загрузке](#link_18)
  - [ 5. Перезагрузка маршрутизатора](#link_19)

# VPN-канал с помощью OpenSSH. Часть четвертая

Рассмотрим еще один пример создания туннеля — для связи двух локальных сетей, расположенных далеко друг от друга. Если у маршрутизаторов нет белых ip-адресов, потребуется промежуточный сервер, у которого такой адрес есть. Надо создать два туннеля и разрешить на сервере пересылку пакетов между интерфейсами. А на маршрутизаторах обеспечить перенаправление в туннель пакетов, предназначенных для другой локальной сети. Должно получиться что-то вроде этого:

![](chapter_4_images/f517179eb486383d9c1e3752222e5e31_MD5.jpg)

Будем считать для простоты, что у нас есть физический доступ к маршртутизаторам `gw1` и `gw2`. А на промежуточном сервере будем работать по ssh с аутентификацией по ключу от имени пользователя `evgeniy`, который может получить права `root` через `sudo`.

## Вход на сервер по ключу с gw1 и gw2 <a name="link_1"></a>

Создаем ключи на машине `gw1` для пользователя `evgeniy`:

```
$ cd ~/.ssh/
$ ssh-keygen
```

Копируем публичный ключ на сервер:

```
$ ssh-copy-id -i id_rsa.pub evgeniy@123.123.123.123
```

Проверяем аутентификацию по ключу:

```
$ ssh evgeniy@123.123.123.123
Welcome to Ubuntu 18.04.4 LTS (GNU/Linux 4.15.0-91-generic x86_64)
```

После этого создаем ключи на машине `gw2` для пользователя `evgeniy`. Тут все по аналогии с `gw1`, так что подробно описывать не буду.

## Настройка промежуточного сервера <a name="link_2"></a>

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

### 3. Создаем два TUN устройства при загрузке <a name="link_5"></a>

Теперь нужно добавить два TUN устройства при загрузке системы, которые будут доступны для чтения и записи пользователю `ssh-vpn`.

```
# nano /etc/systemd/network/50-ssh-vpn.netdev
```

```
[NetDev]
Name=tun1
Kind=tun
[Tun]
User=ssh-vpn
```

```
# nano /etc/systemd/network/50-ssh-vpn.network
```

```
[Match]
Name=tun1
[Address]
Address=192.168.201.1/30
Peer=192.168.201.2/30
[Network]
Address=192.168.201.1/30
[Route]
Destination=10.10.10.0/24
Gateway=192.168.201.2
```

Здесь мы указываем маршрут до сети `10.10.10.0/24` для интерфейса `tun1` — пакеты надо отправлять через шлюз `192.168.201.2`. Другими словами — отправлять пакеты на интерфейс `tun1` маршрутизатора `gw1`. Маршрутизатор перекинет эти пакеты с интерфейса `tun1` на интерфейс `enp0s8` и отправит дальше — компьютеру `pc1` или `pc2`.

```
# nano /etc/systemd/network/60-ssh-vpn.netdev
```

```
[NetDev]
Name=tun2
Kind=tun
[Tun]
User=ssh-vpn
```

```
# nano /etc/systemd/network/60-ssh-vpn.network
```

```
[Match]
Name=tun2
[Address]
Address=192.168.202.1/30
Peer=192.168.202.2/30
[Network]
Address=192.168.202.1/30
[Route]
Destination=172.20.10.0/24
Gateway=192.168.202.2
```

Здесь мы указываем маршрут до сети `172.20.10.0/24` для интерфейса `tun2` — пакеты надо отправлять через шлюз `192.168.202.2`. Другими словами — отправлять пакеты на интерфейс `tun2` маршрутизатора `gw2`. Маршрутизатор перекинет эти пакеты с интерфейса `tun2` на интерфейс `enp0s8` и отправит дальше — компьютеру `pc3` или `pc4`.

### 4. Пересылка пакетов tun1→tun2 и tun2→tun1 <a name="link_6"></a>

Маршрутизаторы будут направлять трафик в туннель, но что делать с этим трафиком — промежуточный сервер пока не знает. Нужно включить пересылку пакетов между интерфейсами `tun1` и `tun2`.

```
# nano /etc/sysctl.conf

net.ipv4.ip_forward=1
```

```
# iptables -P FORWARD DROP

# iptables -A FORWARD -i tun1 -o tun2 -s 10.10.10.0/24 -d 172.20.10.0/24 -j ACCEPT
# iptables -A FORWARD -i tun2 -o tun1 -s 172.20.10.0/24 -d 10.10.10.0/24 -j ACCEPT
```

Правила мы добавили, но они пропадут при перезагрузке сервера. Так что их нужно сохранить и восстанавливать при перезагрузке. В этом нам поможет установка пакета `iptables-persistent`, который добавит новую службу `netfilter-persistent.service`:

```
# apt install iptables-persistent
```

При установке пакета будет предложено сохранить текущие правила `iptables`:

- в файл `/etc/iptables/rules.v4` для протокола IPv4
- в файл `/etc/iptables/rules.v6` для протокола IPv6

### 4. Перезагрузка промежуточного сервера <a name="link_7"></a>

Теперь все готово, перезагружаем промежуточный сервер и смотрим сетевые интерфейсы, маршруты и правила форвардинга:

```
$ ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: ens3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 2a:d6:aa:bf:a4:0b brd ff:ff:ff:ff:ff:ff
    inet 123.123.123.123/24 brd 123.123.123.255 scope global dynamic ens3
       valid_lft 59803sec preferred_lft 59803sec
    inet6 fe80::28d6:aaff:febf:a40b/64 scope link
       valid_lft forever preferred_lft forever
3: tun1: <POINTOPOINT,MULTICAST,NOARP,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 500
    link/none
    inet 192.168.201.1 peer 192.168.201.2/30 scope global tun1
       valid_lft forever preferred_lft forever
    inet6 fe80::9184:cdb6:4d5b:444d/64 scope link stable-privacy
       valid_lft forever preferred_lft forever
4: tun2: <POINTOPOINT,MULTICAST,NOARP,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 500
    link/none
    inet 192.168.202.1 peer 192.168.202.2/30 scope global tun2
       valid_lft forever preferred_lft forever
    inet6 fe80::2dcd:6955:73cd:1f31/64 scope link stable-privacy
       valid_lft forever preferred_lft forever
```

На самом деле такой вывод команды `ip addr` будет только после того, как мы настроим маршрутизаторы `gw1` и `gw2`. А в этот момент интерфейсы `tun1` и `tun2` будут выключены, потому что туннели еще не созданы. Но мы это скоро исправим.

```
$ route -n
Destination     Gateway         Genmask           Flags   Metric   Ref   Use Iface
----------------------------------------------------------------------------------
0.0.0.0         123.123.123.1   0.0.0.0           UG      100      0     0   ens3
10.10.10.0      192.168.201.2   255.255.255.0     UG      0        0     0   tun1
172.20.10.0     192.168.202.2   255.255.255.0     UG      0        0     0   tun2
123.123.123.0   0.0.0.0         255.255.255.0     U       0        0     0   ens3
192.168.201.0   0.0.0.0         255.255.255.252   U       0        0     0   tun1
192.168.202.0   0.0.0.0         255.255.255.252   U       0        0     0   tun2
```

Красным выделены маршруты, которые были добавлены при создании TUN устройств.

```
# iptables -L -v --line-numbers
..........
Chain FORWARD (policy DROP 0 packets, 0 bytes)
num   pkts   bytes   target   prot   opt   in     out    source           destination
1        0       0   ACCEPT   all    --    tun1   tun2   10.10.10.0/24    172.20.10.0/24
2        0       0   ACCEPT   all    --    tun2   tun1   172.20.10.0/24   10.10.10.0/24
..........
```

## Настройка маршрутизатора gw1 <a name="link_8"></a>

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
      addresses: [192.168.50.2/24]
      gateway4: 192.168.50.1
      nameservers:
        addresses: [8.8.8.8, 8.8.4.4]
    enp0s8:
      dhcp4: no
      addresses: [10.10.10.1/24]
      nameservers:
        addresses: [8.8.8.8, 8.8.4.4]
```

Маршрутизатор `gw1` должен обеспечивать выход в интернет для всех компьютеров из локальной сети `10.10.10.0/24`. Пересылка пакетов между интерфейсами по умолчанию отключена, так что редактируем файл `/etc/sysctl.conf`:

```
# nano /etc/sysctl.conf

net.ipv4.ip_forward=1
```

После этого настраиваем `netfilter` с помощью утилиты `iptables`:

```
# iptables -P FORWARD DROP

# iptables -A FORWARD -i enp0s8 -o enp0s3 -s 10.10.10.0/24 ! -d 172.20.10.0/24 -j ACCEPT # enp0s8 -> enp0s3
# iptables -A FORWARD -i enp0s3 -o enp0s8 ! -s 172.20.10.0/24 -d 10.10.10.0/24 -j ACCEPT # enp0s3 -> enp0s8
```

Мы отправляем в глобальную сеть только те пакеты, которые не предназначены для подсети `172.20.10.0/24`. Теперь для этих пакетов добавим SNAT (подмена адреса источника), что позволит всем компьютерам подсети `10.10.10.0/24` выходить в интернет, используя единственный ip-адрес `192.168.50.2`.

```
# iptables -t nat -A POSTROUTING -o enp0s3 -s 10.10.10.0/24 ! -d 172.20.10.0/24 -j MASQUERADE
```

Наконец, добавляем правила, которые будут перенаправлять в туннель пакеты с адресом назначения `172.20.10.0/24`:

```
# iptables -A FORWARD -i enp0s8 -o tun1 -s 10.10.10.0/24 -d 172.20.10.0/24 -j ACCEPT # enp0s8 -> tun1
# iptables -A FORWARD -i tun1 -o enp0s8 -s 172.20.10.0/24 -d 10.10.10.0/24 -j ACCEPT # tun1 -> enp0s8
```

Правила мы добавили, но они пропадут при перезагрузке маршрутизатора. Так что их нужно сохранить и восстанавливать при перезагрузке. В этом нам поможет установка пакета `iptables-persistent`, который добавит новую службу `netfilter-persistent.service`:

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
```

Теперь нам надо скопировать публичный ключ на промежуточный сервер с помощью команды `scp`. Но у нас нет доступа для пользователя `evgeniy` к директории `/home/ssh-vpn/.ssh/`, поэтому временно изменяем на нее права:

```
$ chmod 707 /home/ssh-vpn/.ssh/
```

Открываем еще один терминал (`Alt+F2`) и копируем публичный ключ на сервер:

```
$ scp /home/ssh-vpn/.ssh/id_rsa.pub evgeniy@123.123.123.123:/home/evgeniy/id_rsa_gw1.pub
```

Файл ключа копируем в домашнюю директорию пользователя `evgeniy` сервера. Потом, когда скопируем на сервер файл ключа с `gw2`, объеденим эти два файла и запишем в `/home/ssh-vpn/.ssh/authorized_keys`.

Переключаемся обратно на первый терминал (`Alt+F2`) и возвращаем права обратно:

```
$ chmod 700 /home/ssh-vpn/.ssh/
$ exit # завершаем сеанс работы под пользователем ssh-vpn
```

### 3. Создание TUN-устройства при загрузке <a name="link_11"></a>

Создаем при загрузке системы TUN-устройство:

```
# nano /etc/systemd/network/50-ssh-vpn.netdev
```

```
[NetDev]
Name=tun1
Kind=tun
[Tun]
User=ssh-vpn
```

```
# nano /etc/systemd/network/50-ssh-vpn.network
```

```
[Match]
Name=tun1
[Address]
Address=192.168.201.2/30
Peer=192.168.201.1/30
[Network]
Address=192.168.201.2/30
[Route]
Destination=172.20.10.0/24
Gateway=192.168.201.1
```

Здесь мы указываем маршрут до сети `172.20.10.0/24` для интерфейса `tun1` — пакеты надо отправлять через шлюз `192.168.201.1`. Другими словами — отправлять пакеты на интерфейс `tun1` промежуточного сервера. Промежуточный сервер перекинет эти пакеты с интерфейса `tun1` на интерфейс `tun2` и отправит дальше — маршртутизатору `gw2`.

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
ExecStart=/usr/bin/ssh -i /home/ssh-vpn/.ssh/id_rsa -N -w 1:1 ssh-vpn@123.123.123.123
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

### 5. Перезагрузка маршрутизатора <a name="link_13"></a>

Теперь все готово, перезагружаем маршрутизатор `gw1` и смотрим сетевые интерфейсы, маршруты и правила форвардинга:

```
$ ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:bd:93:ac brd ff:ff:ff:ff:ff:ff
    inet 192.168.50.2/24 brd 192.168.50.255 scope global dynamic enp0s3
       valid_lft 25047sec preferred_lft 25047sec
    inet6 fe80::a00:27ff:febd:93ac/64 scope link
       valid_lft forever preferred_lft forever
3: enp0s8: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:aa:3d:d9 brd ff:ff:ff:ff:ff:ff
    inet 10.10.10.1/24 brd 10.10.10.255 scope global enp0s8
       valid_lft forever preferred_lft forever
    inet6 fe80::a00:27ff:feaa:3dd9/64 scope link
       valid_lft forever preferred_lft forever
4: tun1: <POINTOPOINT,MULTICAST,NOARP,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 500
    link/none
    inet 192.168.201.2 peer 192.168.201.1/30 scope global tun1
       valid_lft forever preferred_lft forever
    inet6 fe80::3cac:775c:c18c:c0aa/64 scope link stable-privacy
       valid_lft forever preferred_lft forever
```

```
$ route -n
Destination     Gateway         Genmask           Flags   Metric   Ref   Use   Iface
-------------------------------------------------------------------------------------
0.0.0.0         192.168.50.1    0.0.0.0           UG      100      0     0     enp0s3
10.10.10.0      0.0.0.0         255.255.255.0     U       0        0     0     enp0s8
172.20.10.0     192.168.201.1   255.255.255.0     UG      0        0     0     tun1
192.168.50.0    0.0.0.0         255.255.255.0     U       0        0     0     enp0s3
192.168.50.1    0.0.0.0         255.255.255.255   UH      100      0     0     enp0s3
192.168.201.0   0.0.0.0         255.255.255.252   U       0        0     0     tun1
```

Красным выделены маршруты, которые были добавлены при создании TUN устройства.

```
# iptables -t filter -L -v --line-numbers
..........
Chain FORWARD (policy DROP 0 packets, 0 bytes)
num   pkts   bytes   target   prot   opt   in       out      source           destination
1        0       0   ACCEPT   all    --    enp0s8   enp0s3   10.10.10.0/24   !172.20.10.0/24
2        0       0   ACCEPT   all    --    enp0s3   enp0s8  !172.20.10.0/24   10.10.10.0/24
3        0       0   ACCEPT   all    --    enp0s8   tun1     10.10.10.0/24    172.20.10.0/24
4        0       0   ACCEPT   all    --    tun1     enp0s8   172.20.10.0/24   10.10.10.0/24
..........
```

Зеленым выделены правила, которые отвечают за пакеты, которые отправляются из подсети `10.10.10.0/24` в глобальную сеть интернет. Красным выделены правила, которые отвечают за пакеты, которые отправляются из подсети `10.10.10.0/24` в подсеть `172.20.10.0/24`.

```
# iptables -t nat -L -v --line-numbers
..........
Chain POSTROUTING (policy ACCEPT 0 packets, 0 bytes)
num   pkts   bytes   target       prot   opt   in    out      source          destination
1        0       0   MASQUERADE   all    --    any   enp0s3   10.10.10.0/24  !172.20.10.0/24
```

## Настройка маршрутизатора gw2 <a name="link_14"></a>

### 1. Сетевые интерфейсы и форвардинг <a name="link_15"></a>

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
      addresses: [172.20.10.1/24]
      nameservers:
        addresses: [8.8.8.8, 8.8.4.4]
```

Маршрутизатор `gw2` должен обеспечивать выход в интернет для всех компьютеров из локальной сети `172.20.10.0/24`. Пересылка пакетов между интерфейсами по умолчанию отключена, так что редактируем файл `/etc/sysctl.conf`:

```
# nano /etc/sysctl.conf

net.ipv4.ip_forward=1
```

После этого настраиваем `netfilter` с помощью утилиты `iptables`:

```
# iptables -P FORWARD DROP

# iptables -A FORWARD -i enp0s8 -o enp0s3 -s 172.20.10.0/24 ! -d 10.10.10.0/24 -j ACCEPT # enp0s8 -> enp0s3
# iptables -A FORWARD -i enp0s3 -o enp0s8 ! -s 10.10.10.0/24 -d 172.20.10.0/24 -j ACCEPT # enp0s3 -> enp0s8
```

Мы отправляем в глобальную сеть только те пакеты, которые не предназначены для подсети `10.10.10.0/24`. Теперь для этих пакетов добавим SNAT (подмена адреса источника), что позволит всем компьютерам подсети `172.20.10.0/24` выходить в интернет, используя единственный ip-адрес `192.168.150.2`.

```
# iptables -t nat -A POSTROUTING -o enp0s3 -s 172.20.10.0/24 ! -d 10.10.10.0/24 -j MASQUERADE
```

Наконец, добавляем правила, которые будут перенаправлять в туннель пакеты с адресом назначения `10.10.10.0/24`:

```
# iptables -A FORWARD -i enp0s8 -o tun2 -s 172.20.10.0/24 -d 10.10.10.0/24 -j ACCEPT # enp0s8 -> tun2
# iptables -A FORWARD -i tun2 -o enp0s8 -s 10.10.10.0/24 -d 172.20.10.0/24 -j ACCEPT # tun2 -> enp0s8
```

Правила мы добавили, но они пропадут при перезагрузке маршрутизатора. Так что их нужно сохранить и восстанавливать при перезагрузке. В этом нам поможет установка пакета `iptables-persistent`, который добавит новую службу `netfilter-persistent.service`:

```
# apt install iptables-persistent
```

При установке пакета будет предложено сохранить текущие правила `iptables`:

- в файл `/etc/iptables/rules.v4` для протокола IPv4
- в файл `/etc/iptables/rules.v6` для протокола IPv6

### 2. Создание пользователя ssh-vpn <a name="link_16"></a>

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
```

Теперь нам надо скопировать публичный ключ на промежуточный сервер с помощью команды `scp`. Но у нас нет доступа для пользователя `evgeniy` к директории `/home/ssh-vpn/.ssh/`, поэтому временно изменяем на нее права:

```
$ chmod 707 /home/ssh-vpn/.ssh/
```

Открываем еще один терминал (`Alt+F2`) и копируем публичный ключ на сервер:

```
$ scp /home/ssh-vpn/.ssh/id_rsa.pub evgeniy@123.123.123.123:/home/evgeniy/id_rsa_gw2.pub
```

Переключаемся обратно на первый терминал (`Alt+F2`) и возвращаем права обратно:

```
$ chmod 700 /home/ssh-vpn/.ssh/
$ exit # завершаем сеанс работы под пользователем ssh-vpn
```

Файл ключа копируем в домашнюю директорию пользователя `evgeniy` сервера. Теперь, когда на сервере есть оба ключа, запишем их оба в файл `authorized_keys`:

```
# cat /home/evgeniy/id_rsa_gw1.pub /home/evgeniy/id_rsa_gw2.pub > /home/ssh-vpn/.ssh/authorized_keys
# rm /home/evgeniy/id_rsa_gw1.pub
# rm /home/evgeniy/id_rsa_gw2.pub
# chown ssh-vpn:ssh-vpn /home/ssh-vpn/.ssh/authorized_keys
# chmod 600 /home/ssh-vpn/.ssh/authorized_keys
```

И надо обязательно выполнить вход по ssh на промежуточный сервер от имени пользователя `ssh-vpn` с маршрутизаторов `gw1` и `gw2`, чтобы был создан файл `known_hosts`. Иначе потом, при автоматическом создании туннеля в момент загрузки `gw1` и `gw2`, получим сообщение об ошибке «Host key verification failed».

Выполняем команды на маршрутизаторе `gw1`:

```
# su ssh-vpn # команду выполяняем от имени пользователя ssh-vpn
$ ssh -i ~/.ssh/id_rsa ssh-vpn@123.123.123.123
..........
Are you sure you want to continue connecting (yes/no)? yes
..........
$ exit # завершаем ssh-сеанс c сервером 123.123.123.123
$ exit # завершаем сеанс работы под пользователем ssh-vpn
```

Выполняем команды на маршрутизаторе `gw2`:

```
# su ssh-vpn # команду выполяняем от имени пользователя ssh-vpn
$ ssh -i ~/.ssh/id_rsa ssh-vpn@123.123.123.123
..........
Are you sure you want to continue connecting (yes/no)? yes
..........
$ exit # завершаем ssh-сеанс c сервером 123.123.123.123
$ exit # завершаем сеанс работы под пользователем ssh-vpn
```

### 3. Создание TUN-устройства при загрузке <a name="link_17"></a>

Создаем при загрузке системы TUN-устройство:

```
# nano /etc/systemd/network/50-ssh-vpn.netdev
```

```
[NetDev]
Name=tun2
Kind=tun
[Tun]
User=ssh-vpn
```

```
# nano /etc/systemd/network/50-ssh-vpn.network
```

```
[Match]
Name=tun2
[Address]
Address=192.168.202.2/30
Peer=192.168.202.1/30
[Network]
Address=192.168.202.2/30
[Route]
Destination=10.10.10.0/24
Gateway=192.168.202.1
```

Здесь мы указываем маршрут до сети `10.10.10.0/24` для интерфейса `tun2` — пакеты надо отправлять через шлюз `192.168.202.1`. Другими словами — отправлять пакеты на интерфейс `tun2` промежуточного сервера. Промежуточный сервер перекинет эти пакеты с интерфейса `tun2` на интерфейс `tun1` и отправит дальше — маршртутизатору `gw1`.

### 4. Создаем туннель при загрузке <a name="link_18"></a>

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
ExecStart=/usr/bin/ssh -i /home/ssh-vpn/.ssh/id_rsa -N -w 2:2 ssh-vpn@123.123.123.123
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

### 5. Перезагрузка маршрутизатора <a name="link_19"></a>

Теперь все готово, перезагружаем маршрутизатор `gw2` и смотрим сетевые интерфейсы, маршруты и правила форвардинга:

```
$ ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:fd:97:10 brd ff:ff:ff:ff:ff:ff
    inet 192.168.150.2/24 brd 192.168.150.255 scope global dynamic enp0s3
       valid_lft 20359sec preferred_lft 20359sec
    inet6 fe80::a00:27ff:fefd:9710/64 scope link
       valid_lft forever preferred_lft forever
3: enp0s8: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:69:a7:e0 brd ff:ff:ff:ff:ff:ff
    inet 172.20.10.1/24 brd 172.20.10.255 scope global enp0s8
       valid_lft forever preferred_lft forever
    inet6 fe80::a00:27ff:fe69:a7e0/64 scope link
       valid_lft forever preferred_lft forever
4: tun2: <POINTOPOINT,MULTICAST,NOARP,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 500
    link/none
    inet 192.168.202.2 peer 192.168.202.1/30 scope global tun2
       valid_lft forever preferred_lft forever
    inet6 fe80::dae5:dcd6:609a:3eb4/64 scope link stable-privacy
       valid_lft forever preferred_lft forever
```

```
$ route -n
Destination     Gateway         Genmask           Flags   Metric   Ref   Use   Iface
-------------------------------------------------------------------------------------
0.0.0.0         192.168.150.1   0.0.0.0           UG      100      0     0     enp0s3
10.10.10.0      192.168.202.1   255.255.255.0     UG      0        0     0     tun2
172.20.10.0     0.0.0.0         255.255.255.0     U       0        0     0     enp0s8
192.168.150.0   0.0.0.0         255.255.255.0     U       0        0     0     enp0s3
192.168.150.1   0.0.0.0         255.255.255.255   UH      100      0     0     enp0s3
192.168.202.0   0.0.0.0         255.255.255.252   U       0        0     0     tun2
```

Красным выделены маршруты, которые были добавлены при создании TUN устройства.

```
# iptables -t filter -L -v --line-numbers
..........
Chain FORWARD (policy DROP 0 packets, 0 bytes)
num   pkts   bytes   target   prot   opt   in       out      source           destination
1        0       0   ACCEPT   all    --    enp0s8   enp0s3   172.20.10.0/24  !10.10.10.0/24
2        0       0   ACCEPT   all    --    enp0s3   enp0s8  !10.10.10.0/24    172.20.10.0/24
3        0       0   ACCEPT   all    --    enp0s8   tun2     172.20.10.0/24   10.10.10.0/24
4        0       0   ACCEPT   all    --    tun2     enp0s8   10.10.10.0/24    172.20.10.0/24
..........
```

Зеленым выделены правила, которые отвечают за пакеты, которые отправляются из подсети `172.20.10.0/24` в глобальную сеть интернет. Красным выделены правила, которые отвечают за пакеты, которые отправляются из подсети `172.20.10.0/24` в подсеть `10.10.10.0/24`.

```
# iptables -t nat -L -v --line-numbers
..........
Chain POSTROUTING (policy ACCEPT 0 packets, 0 bytes)
num   pkts   bytes   target       prot   opt   in    out      source           destination
1        0       0   MASQUERADE   all    --    any   enp0s3   172.20.10.0/24  !10.10.10.0/24
```
