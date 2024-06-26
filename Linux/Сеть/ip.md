# Синтаксис и опции утилиты ip

Сначала рассмотрим синтаксис команды. Утилита довольно многофункциональная, поэтому и синтаксис её вызова непростой:

__$ ip [опции] объект команда [параметры]__

Опции - это глобальные настройки, которые сказываются на работе всей утилиты независимо от других аргументов, их указывать необязательно.

- объект - это тип данных, с которым надо будет работать, например: адреса, устройства, таблица arp, таблица маршрутизации и так далее;
- команды - какое-либо действие с объектом;
- параметры - само собой, командам иногда нужно передавать параметры, они передаются в этом пункте.

Дальше рассмотрим все еще более подробно:

    -v, -Version - только вывод информации об утилите и ее версии.
    -h, -human - выводить данные в удобном для человека виде.
    -s, -stats - включает вывод статистической информации.
    -d, -details - показывать ещё больше подробностей.
    -f, -family - позволяет указать протокол, с которым нужно работать, если протокол не указан, то берется на основе параметров команды. Опция должна принимать одно из значений: bridge, dnet, inet, inet6, ipx или link. По умолчанию используется inet, link - означает отсутствие протокола.
    -o, -oneline - выводить каждую запись с новой строки.
    -r,-resolve - определять имена хостов с помощью DNS.
    -a, -all - применить команду ко всем объектам.
    -c, -color - позволяет настроить цветной, доступные значения: auto, always и never.
    -br, -brief - выводить только базовую информацию для удобства чтения.
    -4 - короткая запись для -f inet.
    -6 - короткая запись для -f inet-f inet6.
    -B - короткая запись для -f inet-f bridge.
    -0 - короткая запись для -f inet -f link.

Теперь давайте рассмотрим самые важные объекты.

    address или a - сетевые адреса.
    link или l - физическое сетевое устройство, такие как проводные соединения и адаптеры Wi-Fi.
    neighbour или neigh - просмотр и управление ARP.
    route или r - управление маршрутизацией трафика, отправляемого на адреса через интерфейсы (link).
    rule или ru - правила маршрутизации.
    tunnel или t - настройка туннелирования.

Остальные объекты
    addrlabel - конфигурация меток для выбора адреса протокола
    l2tp - туннель ethernet через IP (L2TPv3)
    maddress - управление многоадресными адресами
    monitor - мониторит состояние, следит за сообщениями netlink
    mroute - запись кэша многоадресной маршрутизации
    mrule - правило в базе данных политики многоадресной маршрутизации
    netns - управление сетевым пространством имён
    ntable - управлять работой кэша neighbor
    tcp_metrics/tcpmetrics - управление метриками TCP
    token - управлять идентификаторами интерфейса токена
    tuntap - управление устройствами TUN/TAP
    xfrm - управление политиками IPSec

Для полученя справки __ip link help__

Во время ввода имя объекта может быть сокращено до одной буквы. При неоднозначности используется алфавитный порядок. Например, __ip a show__, расшифровывается как __ip address show__. Тогда как в __ip r show__, r - означает route.

Теперь рассмотрим доступные команды, с помощью которых может быть выполнена настройка сети linux. Они зависят от объекта, к которому будут применяться. Вот основные команды: add, change, del или delete, flush, get, list или show, monitor, replace, restore, save, set, и update. Если команда не задана, по умолчанию используется show (показать).

Здесь тоже поддерживается сокращение и в большинстве случаев для выполнения нужного действия достаточно нескольких символов. Но алфавитный порядок соблюдается не всегда. Например, __ip a s__, означает __ip address show__, а не __ip address set__, к сожалению.

## Примеры использования ip

### 1 Просмотр IP адресов
  
- Доступные дейстия addr  __ip addr help__

- Чтобы посмотреть все IP адреса, связанные с сетевыми интерфейсами используйте такую команду:
    __ip a__ или __ip addr show__
    Для просмотра информации в кратком виде используйте опцию __-br__:
    __ip -br a show__

- Можно посмотреть IP адреса только по определённому сетевому интерфейсу, например: enp0s3:
    __ip a show enp0s3__ или __ip a show dev enp0s3__

- Можно отобразить только статические IP адреса:
    __ip a show dev enp0s3 permanent__
    Или только динамические:
    __ip a show dev enp0s3 dynamic__

### 2. Добавление IP адреса

- Чтобы присвоить IP адрес для устройства нужно использовать команду add. Её общий синтаксис такой:
    __ip addr add IP_адрес/маска dev интерфейс__
    Например, давайте присвоим тому же интерфейсу enp0s3 IP адрес 10.0.2.100 с маской подсети 255.255.255.0:
    __ip addr add 10.0.2.100/255.255.255.0 dev enp0s3__
    Маску можно указать и в сокращённом виде:
    __ip addr add 10.0.2.100/24 dev enp0s3__

### 3. Удаление IP адреса

- Чтобы удалить IP адрес из интерфейса надо использовать команду __del__. Синтаксис её очень похож на предыдущую команду. Например, удалим IP адрес 10.0.2.100:
__ip addr del 10.0.2.100/255.255.255.0 dev enp0s3__
Можно удалять IP адреса по одному или удалить все сразу с помощью команды __flush__:
__ip a flush__
Или же можно удалить адреса только определённой подсети:
__sudo ip a flush to 10.0.2.0/24__
Если вы будете применять эти команды к интерфейсу, с помощью которого у вас работает сеть, то сеть пропадёт и чтобы её вернуть надо будет перезагрузить сетевые службы.(https://losst.ru/kak-perezagruzit-set-v-ubuntu)

### 4. Список интерфейсов

- Чтобы посмотреть список сетевых интерфейсов используйте объект __link__:
    __ip l__ или __ip link show__

### 5. Включение или выключение интерфейсов

- Для решения этой задачи тоже используется объект __link__, но с командой __set__. Синтаксис её такой:
    __ip link set dev интерфейс действие__
    В качестве действия можно использовать __up__ или __down__. Например, чтобы отключить интерфейс enp0s3 выполните:
    __ip link set dev enp0s3 down__
    А чтобы включить его обратно:
    __ip link set dev enp0s3 up__

### 6. Настройка MTU

- Параметр MTU означает размер одного пакета, передаваемого по сети. Этот размер можно изменить с помощью команды set. Например, увеличим MTU для enp0s3 до 4000 тысяч байт:
__ip link set mtu 4000 dev enp0s3__

### 7. Настройка MAC адреса

- Адрес MAC - это физический адрес, который используется для определения какому устройству надо передать сетевой пакет в локальной сети. Прежде чем настраивать MAC адрес ваше устройство надо отключить:
    __sudo ip link set dev enp0s3 down__
    Затем можно установить адрес:
    __sudo ip link set dev enp0s3 address AA:BB:CC:DD:EE:FF__
    А потом включить интерфейс обратно:
    __sudo ip link set dev enp0s3 up__

### 8. Таблица ARP

- Чтобы отобразить таблицы соседей, используйте следующую команду
    __ip neigh show__
    Выходные данные показывают MAC-адреса устройств, которые являются частью системы, и их состояние. Состояние устройства может быть:
    __REACHABLE__ - означает валидную, достижимую запись до истечения таймаута.
    __PERMANENT__ - означает постоянную запись, которую может удалить только администратор
    __STALE__ - означает действительную, но недоступную запись
    __DELAY__ - означает, что ядро все еще ожидает проверки из устаревшей записи

- Именно протокол ARP отвечает за преобразование IP адресов в низкоуровневые MAC адреса. Для того чтобы не отправлять ARP запросы каждый раз в сеть, кэш хранится в таблице ARP на протяжении 20-ти минут. Чтобы посмотреть содержимое таблицы ARP используйте такую команду:
__ip neigh show__ или __ip n__

### 9. Добавление записи в таблицу ARP

- Обычно записи в эту таблицу попадают автоматически, но вы можете добавить их и вручную. Для этого используйте команду __add__ объекта __neigh__:
    __sudo ip neigh add 192.168.0.105 lladdr b0:be:76:43:21:41 dev enp0s3__
    В этом примере я заставил компьютер думать, что узел с IP 192.168.0.105 это 192.168.0.1. Теперь можно попытаться выполнить ping по этому адресу и оно будет работать, несмотря на то, что реально такого узла в сети нет.

### 10. Очистка таблицы ARP

- Вы можете удалять IP адреса по одному с помощью команды __del__:
    __sudo ip neigh del dev enp0s3 192.168.0.105__

- Можно удалить все записи для определённого сетевого интерфейса:
    __ip neigh flush dev enp0s3__
    Или очистить таблицу полностью командой flush:
    __ip neigh flush__

### 11. Просмотр таблицы маршрутизации

- Просмотрите полный список команд ip route с помощью следующей команды 
    __ip route help__
    С помощью объекта route вы можете проверять маршруты и управлять ими. Правила маршрутизации определяют, на какой сетевой интерфейс отправляется сетевой трафик в зависимости от целевого IP-адреса.
    Если сетевой пакет предназначен устройству, которое непосредственно подключено к отправителю, то путь пакета очевиден — этот пакет отправляется напрямую получателю. Но во всех других случаях необходимо принять решение, через какой сетевой интерфейс нужно отправить трафик. Самый частый пример, с которым многие из нас сталкиваются каждый день, это роутер: если он получил сетевой пакет, предназначенный для локального IP адреса, то он отправляет его через LAN интерфейс, если же пакет предназначен для Глобальной сети (или просто IP не входит в домашнюю локальную сеть), то такой пакет отправляется через WAN интерфейс. Эти правила и являются правилами маршрутизации. Всего различают две группы правил:
    __правила для определённых IP и диапазонов сетей__
    __правила для всего остального трафика, который не упомянут в предыдущих правилах — все такие сетевые пакеты отправляются по маршруту по умолчанию__

- Для просмотра таблицы маршрутизации используйте объект route и команду show:
    __ip route show__ или __ip r__

- Для просмотра всех записей в таблице маршрутизации используйте одну из следующих команд
    __ip route__ или __ip route list__

### 12. Добавление маршрута

- Синтаксис добавления нового маршрута в таблицу маршрутизации такой:

    __ip route add подсеть/маска via шлюз__
    Вместо шлюза можно указать сетевой интерфейс с помощью которого надо отправлять пакеты:

    __ip route add подсеть/маска dev устройство__
    Например, добавим новый маршрут для сети через тот же IP адрес:

    __sudo ip route add 169.255.0.0 via 169.254.19.153__
    Или можно указать сетевой интерфейс через который надо отправлять пакеты для определённой сети:
    __sudo ip route add 169.255.0.0 dev enp0s3__

    Мониторинг событий сетевых интерфейсов
    Всё, что происходит с сетевыми интерфейсами в режиме реального времени можно наблюдать с помощью команды:
    __ip monitor__
    Эта команда покажет удаление и добавление маршрутов, изменение IP адресов, включение и отключение сетевых устройств и другие события.
    Чтобы мониторить события, связанные с IPv6:
    __ip -6 monitor__

### 13. Удаление маршрута

- Удалить маршрут можно командой с аналогичным синтаксисом, только вместо add надо использовать del:
    __sudo ip route del 169.255.0.0 via 169.254.19.153__

### 14. Получить информацию о сетевом интерфейсе

- Чтобы увидеть информацию канального уровня обо всех доступных устройствах (у которых загружен драйвер), используйте команду:
    __ip link show__
- Если вы хотите, чтобы команда отображала информацию для одного конкретного устройства, введите следующее:
    __ip link show dev [device]__

- Чтобы просмотреть статистику по всем сетевым интерфейсам (такие детали, как переданные или отброшенные пакеты или даже ошибки), используйте:
    __ip -s link__

- Вы также можете увидеть аналогичную информацию для отдельного сетевого интерфейса:
    __ip -s link ls [interface]__

- Если вам нужно больше подробностей, добавьте еще __-s__ в синтаксис:
    __ip -s -s link ls [interface]__

- Чтобы увидеть список только работающих интерфейсов, используйте:
    __ip link ls up__    