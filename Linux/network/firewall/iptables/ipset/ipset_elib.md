[источник](https://denis.elib.ru/ipset/)

- [ Установка ipset](#link_1)
- [ Создание нового списка](#link_2)
- [ Добавление адресов в список](#link_3)
- [ Удаление всех адресов из списка](#link_4)
- [ Удаление списка](#link_5)
- [ Удаление адреса из списка](#link_6)
- [ Переименование списка адресов](#link_7)
- [ Поменять местами содержимое списков адресов](#link_8)
- [ Просмотр списков адресов](#link_9)
- [ Проверка наличия адреса в списке](#link_10)
- [ Добавление ipset в iptables](#link_11)
- [ Блокировка по территориальной принадлежности](#link_12)

### Установка ipset <a name="link_1"></a>

```bash
sudo apt install ipset
```

### Создание нового списка <a name="link_2"></a>

Создание нового списка iplist

```bash
ipset -N iplist hash:net
ipset create iplist hash:net
```

### Добавление адресов в список <a name="link_3"></a>

Добавление адреса в список iplist

```bash
ipset -A iplist 8.8.8.8
ipset add iplist 8.8.8.8
```

Чтобы не отображались лишние сообщения при добавлении одинаковых адресов, что такой адрес уже есть, к команде добавляется элемент -exist

```bash
ipset -A -exist iplist 8.8.8.8
ipset add -exist iplist 8.8.8.8
```

### Удаление всех адресов из списка <a name="link_4"></a>

Удаление всех адресов из списка iplist. Очистка списка.

```bash
ipset -F iplist
ipset flush iplist
```

### Удаление списка <a name="link_5"></a>

Удаление списка iplist и его содержимого

```bash
ipset -X iplist
ipset destroy iplist
```

### Удаление адреса из списка <a name="link_6"></a>

Удаление адреса из списка iplist

```bash
ipset -D iplist 8.8.8.8
ipset del iplist 8.8.8.8
```

### Переименование списка адресов <a name="link_7"></a>

Переименовать список iplist в newlist. newlist не должен существовать!

```bash
ipset -E iplist newlist
ipset rename iplist newlist
```

### Поменять местами содержимое списков адресов <a name="link_8"></a>

Поменять местами содержимое списка iplist и newlist. Фактически переименование обоих списков. Оба списка должны существовать. Можно менять местами списки с совместимым типом данных.

```bash
ipset -W iplist newlist
ipset swap iplist newlist
```

### Просмотр списков адресов <a name="link_9"></a>

Просмотр всех списков

```bash
ipset -L
ipset list
```

Просмотр технической информации о списках без вывода адресов

```bash
ipset -L -terse
ipset list -terse
```

Просмотр адресов списка iplist

```bash
ipset -L iplist
ipset list iplist
```

### Проверка наличия адреса в списке <a name="link_10"></a>

Проверка наличия адреса 8.8.8.8 в списке iplist

```bash
ipset -T iplist 8.8.8.8
ipset test iplist 8.8.8.8
```

В зависимости от содержимого списка iplist будет выведено:

если адрес входит в список iplist

```
8.8.8.8 is in set iplist
```

если не входит

```
8.8.8.8 is NOT in set iplist
```

### Добавление ipset в iptables <a name="link_11"></a>

Разрешаем доступ к серверу с адресов, указанных в списке iplist по SSH (порт tcp 22)

```bash
iptables -A INPUT -p tcp -m set --match-set iplist src --dport 22 -j ACCEPT
```

Разрешаем доступ к серверу с любых адресов, кроме указанных в списке blocklist по HTTP (порт tcp 80)

```bash
iptables -A INPUT -p tcp -m set ! --match-set blocklist src --dport 80 -j ACCEPT
```

где:

```
- -m set — использовать модуль ipset
- —match-set — перечисление имен используемых списков адресов
- src или dst — проверять адреса списков с адресам источника или назначения
```

### Блокировка по территориальной принадлежности <a name="link_12"></a>

Чтобы заблокировать доступ с адресов по территориальной принадлежности необходимо создать скрипт, подгружающий списки адресов из GeoIP базы.

```bash
ipset -N geoblock nethash
for IP in $(wget -O geoblock https://www.ipdeny.com/ipblocks/data/countries/{cn,kr,tw,sg,hk}.zone)
do
ipset -A geoblock $IP
done
iptables -A INPUT -m set --match-set geoblock src -j DROP
```

[Original man page (ubuntu)](https://manpages.ubuntu.com/manpages/trusty/man8/ipset.8.html)
