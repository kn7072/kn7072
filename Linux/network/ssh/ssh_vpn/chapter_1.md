[источник](https://tokmakov.msk.ru/blog/item/491)

- [ Настройка сервера](#link_1)
- [ Настройка клиента](#link_2)
- [ Создаем туннель](#link_3)
- [ Аутентификаци по ключу](#link_4)
- [ Добавляем разные фишки](#link_5)
- [ Направляем трафик клиента в туннель](#link_6)

# VPN-канал с помощью OpenSSH. Часть первая

Начиная с версии 4.3 OpenSSH поддерживает устройства `tun/tap`, позволяющие создавать шифрованный туннель, что может быть полезно для удаленного администрирования. Это очень похоже на OpenVPN, основанный на TLS, но для реализации не нужно ничего дополнительно устанавливать и настраивать.

В терминологии компьютерных сетей, TUN и TAP — виртуальные сетевые драйверы ядра системы. Они представляют собой программные сетевые устройства, которые отличаются от обычных аппаратных сетевых карт.

TAP эмулирует Ethernet устройство и работает на канальном уровне модели OSI, оперируя кадрами Ethernet. TUN (сетевой туннель) работает на сетевом уровне модели OSI, оперируя IP пакетами. TAP используется для создания сетевого моста, тогда как TUN для маршрутизации.

Итак, есть сервер с белым ip-адресом `123.123.123.123` и клиент. На сервере и на клиенте установлена Ubuntu 18.04, на сервере установлен OpenSSH сервер. Нам надо построить туннель между клиентом и сервером, так что они будут в одной сети `192.168.200.0/30`. У сервера в этой сети будет ip-адрес `192.168.200.1`, а у клиента — `192.168.200.2`.

![](chapter_1_images/c7c024cf95a9bf9d101db048b06a5b65_MD5.jpg)

## Настройка сервера <a name="link_1"></a>

Для начала редактируем файл конфигурации ssh-сервера:

```
$ sudo nano /etc/ssh/sshd_config
```

```
PermitTunnel point-to-point
PermitRootLogin yes
```

```
$ sudo systemctl restart ssh.service
```

Параметр `PermitTunnel` разрешает использование перенаправления для устройств TUN и может принимать значения `yes`, `point-to-point` (3-й уровень модели OSI), `ethernet` (2-й уровень модели OSI) и `no`. Значение `yes` означает, что одновременно разрешается `point-to-point` и `ethernet`. Значение по умолчанию — `no`.

С помощью параметра `PermitRootLogin` мы разрешаем пользователю `root` подключаться к серверу. Это не очень хорошо, но необходимо для создания туннеля — чтобы «поднять» tun-интерфейсы, которые мы создадим на клиенте и на сервере, нужны права суперпользователя. _Пока оставим так, а потом настроим аутентификацию по ключу и изменим значение этого параметра на `without-password`_.

Теперь создаем виртуальный интерфейс `tun5`:

```
$ sudo ip tuntap add dev tun5 mode tun # создаем новый интерфейс tun5 типа TUN
$ sudo ip addr add 192.168.200.1/30 peer 192.168.200.2/30 dev tun5 # назначаем ip-адрес для интерфейса tun5
```

Удалить созданный виртуальный интерфейс можно командой

```
$ sudo ip tuntap del dev tun5 mode tun
```

Смотрим сетевые интерфейсы:

```$ ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: ens3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 2a:d6:aa:bf:a4:0b brd ff:ff:ff:ff:ff:ff
    inet 123.123.123.123/24 brd 123.123.123.255 scope global dynamic ens3
       valid_lft 57548sec preferred_lft 57548sec
    inet6 fe80::28d6:aaff:febf:a40b/64 scope link
       valid_lft forever preferred_lft forever
3: tun5: <POINTOPOINT,MULTICAST,NOARP> mtu 1500 qdisc noop state DOWN group default qlen 500
    link/none
    inet 192.168.200.1 peer 192.168.200.2/30 scope global tun5
       valid_lft forever preferred_lft forever
```

## Настройка клиента <a name="link_2"></a>

Аналогично, создаем виртуальный интерфейс `tun5`:

```
$ sudo ip tuntap add dev tun5 mode tun # создаем новый интерфейс tun5 типа TUN
$ sudo ip addr add 192.168.200.2/30 peer 192.168.200.1/30 dev tun5 # назначаем ip-адрес для интерфейса tun5
```

Смотрим сетевые интерфейсы:

```
$ ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:b8:4d:a6 brd ff:ff:ff:ff:ff:ff
    inet 192.168.110.18/24 brd 192.168.110.255 scope global dynamic noprefixroute enp0s3
       valid_lft 15607sec preferred_lft 15607sec
    inet6 fe80::70c1:93c9:7da4:45f5/64 scope link noprefixroute
       valid_lft forever preferred_lft forever
3: tun5: <POINTOPOINT,MULTICAST,NOARP> mtu 1500 qdisc noop state DOWN group default qlen 500
    link/none
    inet 192.168.200.2 peer 192.168.200.1/30 scope global tun5
       valid_lft forever preferred_lft forever
```

## Создаем туннель <a name="link_3"></a>

Обратите внимание, что команда выполняется на клиенте от имени пользователя `root` и подключаемся к серверу как пользователь `root`.

```
$ sudo -i
# ssh -w 5:5 -N root@123.123.123.123
```

Терминал после этого подвиснет, но это нормально — с помощью опции `-N` мы запрещаем выполнение команд на сервере. Так что для дальнейшей работы на клиенте потребуется запустить еще одну ssh-сессию.

Включаем интерфейсы на клиенте и на сервере:

```
$ sudo ip link set dev tun5 up # на сервере
$ sudo ip link set dev tun5 up # на клиенте
```

Смотрим сетевые интерфейсы на сервере:

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
       valid_lft 56876sec preferred_lft 56876sec
    inet6 fe80::28d6:aaff:febf:a40b/64 scope link
       valid_lft forever preferred_lft forever
3: tun5: <POINTOPOINT,MULTICAST,NOARP,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 500
    link/none
    inet 192.168.200.1 peer 192.168.200.2/30 scope global tun5
       valid_lft forever preferred_lft forever
    inet6 fe80::2494:dcf3:d888:9040/64 scope link stable-privacy
       valid_lft forever preferred_lft forever
```

Пингуем клиента по ip-адресу `192.168.200.2`

```
$ ping -c 3 192.168.200.2
PING 192.168.200.2 (192.168.200.2) 56(84) bytes of data.
64 bytes from 192.168.200.2: icmp_seq=1 ttl=64 time=0.033 ms
64 bytes from 192.168.200.2: icmp_seq=2 ttl=64 time=0.039 ms
64 bytes from 192.168.200.2: icmp_seq=3 ttl=64 time=0.052 ms
```

```
--- 192.168.200.2 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2026ms
rtt min/avg/max/mdev = 0.033/0.041/0.052/0.009 ms
```

На клиенте открываем еще один терминал и тоже смотрим сетевые интерфейсы:

```
$ ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:b8:4d:a6 brd ff:ff:ff:ff:ff:ff
    inet 192.168.110.18/24 brd 192.168.110.255 scope global dynamic noprefixroute enp0s3
       valid_lft 23237sec preferred_lft 23237sec
    inet6 fe80::70c1:93c9:7da4:45f5/64 scope link noprefixroute
       valid_lft forever preferred_lft forever
3: tun5: <POINTOPOINT,MULTICAST,NOARP,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 500
    link/none
    inet 192.168.200.2 peer 192.168.200.1/30 scope global tun5
       valid_lft forever preferred_lft forever
    inet6 fe80::6fe5:5671:b495:ebeb/64 scope link stable-privacy
       valid_lft forever preferred_lft forever
```

Пингуем сервер по ip-адресу `192.168.200.1`

```
$ ping -c 3 192.168.200.1
PING 192.168.200.1 (192.168.200.1) 56(84) bytes of data.
64 bytes from 192.168.200.1: icmp_seq=1 ttl=64 time=28.1 ms
64 bytes from 192.168.200.1: icmp_seq=2 ttl=64 time=24.0 ms
64 bytes from 192.168.200.1: icmp_seq=3 ttl=64 time=24.2 ms

--- 192.168.200.1 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2003ms
rtt min/avg/max/mdev = 24.012/25.484/28.145/1.889 ms
```

Обратите внимание на состояние `state` интерфейсов `tun5` на клиенте и на сервере — оно должно быть `UP`, т.е. интерфейсы включены.

## Аутентификаци по ключу <a name="link_4"></a>

Включаем на сервере аутентификацию по ключу:

```
$ sudo nano /etc/ssh/sshd_config

PubkeyAuthentication yes

$ sudo systemctl restart ssh.service
```

Создаем ключи на клиенте:

```$ sudo -i
# cd /root/.ssh
# ssh-keygen
Generating public/private rsa key pair.
Enter file in which to save the key (/root/.ssh/id_rsa): ssh-vpn
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in ssh-vpn.
Your public key has been saved in ssh-vpn.pub.
The key fingerprint is:
SHA256:9XLqQMz81z35G8XiYhnLg37vtSB0o16uuiS234PoKwA root@client
The key's randomart image is:
+---[RSA 2048]----+
|                 |
|                 |
|          .      |
| E     + . .   . |
|  .     S ..+o. o|
|   .   . ..*o*.oo|
|    .  oo.=oOoo+o|
|     ...+=o+=o..=|
|      o+o+==o+ooo|
+----[SHA256]-----+
```

Копируем публичный ключ на сервер:

```
# ssh-copy-id -i ssh-vpn.pub root@123.123.123.123
/usr/bin/ssh-copy-id: INFO: Source of key(s) to be installed: "ssh-vpn.pub"
/usr/bin/ssh-copy-id: INFO: attempting to log in with the new key(s), to filter out any that are already installed
/usr/bin/ssh-copy-id: INFO: 1 key(s) remain to be installed -- if you are prompted now it is to install the new keys
root@123.123.123.123's password: пароль

Number of key(s) added: 1

Now try logging into the machine, with:   "ssh 'root@123.123.123.123'"
and check to make sure that only the key(s) you wanted were added.
```

Проверяем, что можем подключаться к серверу как `root` без пароля:

```
# ssh -i ssh-vpn root@123.123.123.123
```

Welcome to Ubuntu 18.04.4 LTS (GNU/Linux 4.15.0-91-generic x86_64)

- Documentation: https://help.ubuntu.com
- Management: https://landscape.canonical.com
- Support: https://ubuntu.com/advantage

- Canonical Livepatch is available for installation.
  - Reduce system reboots and improve kernel security. Activate at:
    https://ubuntu.com/livepatch
    Last login: Fri Apr 3 12:17:48 2020 from xxx.xxx.xxx.xxx

Запрещаем пользователю `root` вход по паролю:

```
# nano /etc/ssh/sshd_config

RermitRootLogin without-password

# systemctl restart ssh.service
```

## Добавляем разные фишки <a name="link_5"></a>

Поднимаем туннель с помощью команды:

```
# ssh -i ~/.ssh/ssh-vpn -S /var/run/ssh-vpn -M -N -f -w 5:5 root@123.123.123.123
```

Опции команды для создания туннеля:

- Опция `-S` указывает расположение управляющего сокета для общего доступа к соединению. По его наличию можно сделать вывод о состоянии нашего туннеля. Если файл отсутствует, значит, по каким-то причинам, наше соединение разорвалось.
- Опция `-M` применяется вместе с опцией `-S`, создает «мастер» подключение. Нам это потребуется для разрыва соединения.
- Опция `-N` означает, что после создания туннеля никакая команда на стороне сервера не будет выполняться.
- Опция `-f` переводит процесс в фоновый режим.

Мультиплексирование — это возможность посылать более одного сигнала по одной линии или соединению. В OpenSSH мультиплексирование позволяет повторно использовать существующее исходящее TCP-соединение для нескольких одновременных SSH-сеансов с удаленным SSH-сервером, избегая затрат на создание нового TCP-соединения и повторную проверку подлинности каждый раз.

Клиент OpenSSH поддерживает мультиплексирование своих исходящих соединений, начиная с версии 3.9, используя директивы конфигурации `ControlMaster`, `ControlPath` и `ControlPersist`, которые задаются в `~/.ssh/config` и `/etc/ssh/ssh_config`. Опции времени выполнения `-M` и `-S` соответствуют `ControlMaster` и `ControlPath` соответственно.

Вот так создается управляющее TCP-соединение, которое может использоваться другими ssh-сеансами:

```
$ ssh -M -S /home/evgeniy/ssh-master.socket evgeniy@www.example.org
evgeniy@www.example.org's password: пароль
Welcome to Ubuntu 18.04.4 LTS (GNU/Linux 4.15.0-91-generic x86_64)
```

Теперь в другом терминале можно выполнять команды на сервере `www.example.com` без ввода пароля:

```
$ ssh -S /home/evgeniy/ssh-master.socket www.example.org apt update
```

Состояние управляющего TCP-соединения можно запросить с помощью опции `-O check`:

```
$ ssh -S /home/evgeniy/ssh-master.socket www.example.org -O check
```

Опция `-O exit` удаляет управляющий сокет и немедленно завершает все существующие подключения:

```
$ ssh -S /home/evgeniy/ssh-master.socket www.example.org -O exit
```

Давайте проверим, что процесс работает в фоне:

```
# ps -f -C ssh
UID     PID  PPID  C  STIME  TTY      TIME  CMD
root  18854  1655  0  13:05  ?    00:00:00  ssh -i /root/.ssh/ssh-vpn -S /var/run/ssh-vpn -M -N -f -w 5:5 root@123.123.123.123
```

Теперь — команда на отключение. Вот тут как раз нам пригодится файл-сокет и контроль соединения через него:

```
# ssh -S /var/run/ssh-vpn -O exit 123.123.123.123
```

## Направляем трафик клиента в туннель <a name="link_6"></a>

Чтобы перенаправить весь трафик клиента в туннель, нужно вместо старого шлюза — `192.168.110.1` (через интерфейс `enp0s3`) указать новый — `192.168.200.1` (через интерфейс `tun5`). Но при этом потеряется связь с сервером — поэтому перед заменой шлюза нужно добавить маршрут до сервера.

После этого весь трафик клиента направляется в туннель, но что делать с этим трафиком — сервер не знает. Нужно включить пересылку трафика между интерфейсами `tun5` и `ens3` и добавить SNAT, чтобы сервер подменял серый ip-адрес клиента на свой белый ip-адрес.

На клиенте выполняем команды:

```
# маршрут до сервера через старый шлюз, иначе все отвалится, когда у нас будет новый шлюз
# ip route add 123.123.123.123/32 via 192.168.110.1 dev enp0s3

# заменяем старый шлюз на новый, теперь все через туннель, кроме пакетов на 123.123.123.123
# ip route replace default via 192.168.200.1 dev tun5
```

На сервере выполняем команды:

```
# # пересылка трафика между интерфейсами
# echo 1 > /proc/sys/net/ipv4/ip_forward

# # SNAT (подмена адреса источника)
# iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
```

Конечно, вся эта конструкция развалится при перезагрузке клиента или сервера. Но мы все сделаем капитально во второй части.
