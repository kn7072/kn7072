[источник](https://www.linuxshop.ru/articles/a26710803-cisco_bazovye_komandy_i_nastroyki?ysclid=mlatlsjzko794393033)

# Cisco базовые команды и настройки

### Cisco базовые команды и настройки

**show startup-config**  
Показывает содержимое конфигурации, которая применяется при загрузке. Можно скопировать эти данные в буфер обмена и сохранить в файл в качестве бэкапа конфигурации. Этот файл потом можно просто вставить (с небольшими оговорками) из буфера обмена в экран консоли, дать команду wr mem, и этим восстановить конфигурацию (многие программы, автоматически сохраняющие и обновляющие конфигурацию, применяют как раз такой метод).

**show running-config  
**Команда show running-config показывает текущую конфигурацию устройства. Running-configuration – это конфигурация, загруженная в данный момент в оперативную память роутера. Когда вы вносите изменения в оборудование, как раз эта конфигурация изменяется. НО ПОСЛЕ ПЕРЕЗАГРУЗКИ ОН ЗАМЕНЯЕТСЯ НА **startup-config**, так что не бойтесь испортить после перезагрузки все вернеться.

**copy startup-config running-config**

Отменяет все сделанные (если были) изменения в конфигурации. То же самое произойдет, если выключить/включить питание (перезагрузить устройство).

**copy running-config startup-config**  
Сохраняет в энергонезависимой памяти все изменения, сделанные в конфигурации. Полный аналог команды write или write memory.

**Как зайти в режим конфигурации cisco:**

conf t

**Как добавить строчку в конфигурацию:**

прим добавить проброс (просто пишем строчку):

ip nat inside source static tcp 192.168.10.4 22 XXX.XXX.XXX.XXXX 22 extendable

**Пример: добавить ip на интерфейсе:**

interface Vlan1  (вначале указываем на каком интерфейсе)

ip address 192.168.10.4 255.255.255.0 secondary  (добавляем второй, если без secondary то замените)

**Как удалить строчку в конфигурацию:**

Перед строчкой пишем no и пишем строчку прим: 

no ip nat inside source static tcp 192.168.10.4 22 XXX.XXX.XXX.XXXX 22 extendable

**Как перегрузить cisco:**

reload in 1   (1 это время в минутах через сколько)

И решение как в cisco 871 открыть SSH во вне, сделать проброс порта на внутренний IP

### **100 команд Cisco IOS** 

**“?”**  
На первый взгляд использование ? для вызова помощи кажется достаточно простым. Однако Cisco IOS кардинально отличается от других операционных систем в плане использования команды помощи. Поскольку Cisco IOS – это операционная система с командным интерфейсом, существуют тысячи команд для настройки и управления, а использование ? поможет сэкономить немало времени.  
Эту команду можно применять различными способами. Во-первых, используйте ?, если не знаете какую команду написать. Например, вы можете написать ? в командной строке для вывода всех возможных команд.  
Также можно использовать ?, если вы не знаете аргумент какой-либо команды. Например, можно ввести show ip ? Если команде не нужно никаких аргументов, роутер предложит только CR (возврат каретки).  
Наконец, можно использовать? для просмотра всех команд, начинающихся с определённой буквы. Например, show c? покажет все команды, начинающиеся с буквы c.

**show running-configuration**  
Команда show running-config показывает текущую конфигурацию устройства. Running-configuration – это конфигурация, загруженная в данный момент в оперативную память роутера. Когда вы вносите изменения в оборудование, как раз эта конфигурация изменяется.  
Важно помнить, что конфигурация не сохраняется пока не выполнить copy running-configuration startup-configuration. Команду show running-config можно сокращать до sh run.

**copy running-configuration startup-configuration**  
Эта команда сохранит текущие модификации в настройках (running-configuration, которая хранится в RAM), в энергонезависимую RAM (NVRAM). Если внезапно исчезнет электропитание, то данные в NVRAM сохранятся. Другими словами, если вы внесёте изменения в конфигурацию роутера или перезагрузите его, не используя перед этим данную команду, то все изменения будут утеряны. Команду можно сократить до copy run start.  
Команда copy также используется для копирования текущей или стартовой конфигурации на TFTP-сервер.

**show interface**  
Команда show interface отображает состояние интерфейсов маршрутизатора. Вот некоторые выводимые параметры:

- Состояние интерфейса (вкл./выкл.)
- Состояние протокола на интерфейсе
- Использование
- Ошибки
- MTU

Эта команда играет важную роль для диагностики роутера или свитча. Её также можно использовать с указанием конкретного интерфейса, например, **sh int fa0/0**.

```R1#show interface ?  Async                         Async interface
  BVI                             Bridge-Group Virtual Interface
  CTunnel                    CTunnel interface
  Dialer                        Dialer interface
  FastEthernet           FastEthernet IEEE 802.3
  Loopback                 Loopback interface
  Multilink                  Multilink-group interface
  Null                           Null interface
  Port-channel           Ethernet Channel of interfaces
  Tunnel                     Tunnel interface
  Vif                             PGM Multicast Host interface
  Virtual-Template       Virtual Template interface
  Virtual-TokenRing    Virtual TokenRing
  XTagATM               Extended Tag ATM interface
  accounting              Show interface accounting
  crb                            Show interface routing/bridging info
  dampening             Show interface dampening info
  description             Show interface description
  irb                             Show interface routing/bridging info
  mac-accounting     Show interface MAC accounting info
  mpls-exp                 Show interface MPLS experimental accounting info
  precedence             Show interface precedence accounting info
 rate-limit                 Show interface rate-limit info
  stats                         Show interface packets & octets, in & out, by switching path
  summary                Show interface summary
  switching                Show interface switching
  \|                               Output modifiers
```

**show ip interface**

Более распространёнными, чем show interface являются команды:  
**show ip interface** и **show ip interface brief**.   
Команда **show ip interface** предоставляет огромное количество информации о конфигурации и состоянии протокола IP и его службах на всех интерфейсах.   
Команда **show ip interface brief** даёт краткий обзор интерфейсов, включая IP-адрес, статусы Layer 2 и Layer 3.

**config terminal, enable, interface, and router**  
У роутеров Cisco есть несколько разных режимов управления, в каждом из них отображаются или изменяются определённые параметры. Очень важно уметь перемещаться между этими режимами для успешной настройки маршрутизатора.  
Когда вы авторизуетесь на роутере (SSH, Telnet, Console), сначала вы попадаете в user mode (пользовательский режим, где приглашение выглядит как >).   
В этом режиме можно написать enable для переключения в привилегированный режим   
*(приглашение выглядит как #).*   
В привилегированном режиме отображается любая информация, но нельзя вносить никакие изменения. Для того, чтобы попасть в режим глобальной конфигурации введите:   
**config terminal** (или **config t**)   
*(приглашение станет выглядеть как (config)# ).*   
В этом режиме можно изменять любые настройки. Для изменения параметра интерфейса (например, IP-адреса) переключитесь в режим конфигурирования командой: **interface**   
*(приглашение выглядит как (config-if)#).*   
Помимо этого, из режима глобальной конфигурации вы можете попасть в режим конфигурации роутера с помощью команды **router** {protocol}. Для выхода из любого режима введите **exit**.

**no shutdown**  
Команда no shutdown включает интерфейс. Она используется в режиме конфигурации интерфейса. Может быть полезна при диагностике или конфигурации новых интерфейсов. Если с каким-либо интерфейсом возникла проблема, можно попробовать ввести shut и no shut. Разумеется, для того, чтобы выключить интерфейс введите shutdown. Команду можно сократить до no shut.

**show ip route**  
Команда show ip route выводит таблицу маршрутизации роутера. Она состоит из списка всех сетей, которые доступны роутеру, их метрике (приоритет маршрутов) и шлюза. Команду можно сократить до **sh ip ro**. Также после неё могут быть параметры, например **sh ip ro ospf** (показывает всю маршрутизацию OSPF).  
Для очистки всей таблицы маршрутизации необходимо выполнить **clear ip route \***. Для удаления конкретного маршрута необходимо указать адрес сети после команды, например clear ip route 1.1.1.1.

**show version**  
Команда show version показывает регистр конфигурации (в основном настройки загрузки маршрутизатора), когда последний раз роутер загружался, версию IOS, имя файла IOS, модель устройства, а также количество оперативной и флэш-памяти. Команду можно сократить до **sh ver**.

**debug**  
У команды debug есть много параметров, и она не работает без них. Эта команда предоставляет детальную отладочную информацию по конкретному приложению, протоколу или службе. Например, debug ip route будет сообщать вам каждый раз, когда маршрут добавляется или удаляется из роутера.  
**show startup-config**  
Показывает содержимое конфигурации, которая применяется при загрузке. Можно скопировать эти данные в буфер обмена и сохранить в файл в качестве бэкапа конфигурации. Этот файл потом можно просто вставить (с небольшими оговорками) из буфера обмена в экран консоли, дать команду wr mem, и этим восстановить конфигурацию (многие программы, автоматически сохраняющие и обновляющие конфигурацию, применяют как раз такой метод).

**copy startup-config running-config**  
Отменяет все сделанные (если были) изменения в конфигурации. То же самое произойдет, если выключить/включить питание (перезагрузить устройство).

**copy running-config startup-config**  
Сохраняет в энергонезависимой памяти все изменения, сделанные в конфигурации. Полный аналог команды write или write memory.

**write**  
Сохраняет в энергонезависимой памяти все изменения, сделанные в конфигурации. Полный аналог команды write memory или copy running-config startup-config.

**show flash**  
Показывает размер, свободное место и содержимое (в виде списка) энергонезависимой памяти, которая работает с точно так же, как диск. На этом диске хранятся файлы, с которых записана IOS и конфигурация циски (startup-config и другие). Файлами можно манипулировать командами IOS.

**terminal monitor**  
Переключает вывод debug-информации с консольного порта (RS232) на консоль, подключенную через сетевой интерфейс.

(**no) service password-encryption**  
Команда, которая показывает пароли enable в конфиге в (открытом)закрытом виде

**(no) logging console**  
Команда, которая (выключает)включает вывод сообщений системного журнала на консоль (RS232)  
logging console <0-7>  
Команда, включает вывод сообщений системного журнала на консоль (RS232) определённого уровня (0 меньше всего сообщ. - emergencies System is unusable, 7 - больше всего сообщений - Debugging messages)  
logging buffered  
Указание сохранять сообщения в ОЗУ для последующего ознакомления  
show logging  
Вывод сообщений из ОЗУ

**show flash: all**  
Показывает статус flash - сколько занято, свободно, контрольные суммы, сколько банков и их параметры, тип микросхем памяти.

**show vlan   (\*\***show vlans  sh vlans)\*\*  
Показать существующие vlan и привязку к ним физических интерфейсов.

**erase nvram**  
Очистка конфигурации (startup-config и другая информация), полный сброс энергонезависимой памяти.

**configure** <memory|network|overwrite-network|terminal>  
Вход в один из разновидностей режима configure - изменение конфигурации. Наиболее часто используемый режим configure terminal (подключение как через консольный порт RS232, так и по сети через telnet или ssh).

**end**  
Полный выход из режима configure. **Тот же эффект дает Ctrl-Z.**

**exit**  
Шаг назад по дереву конфигурирования (например, выход из реж. конфигурирования одного из интерфейсов).

**no vlan n**  
Удалить vlan n.

**(no) shutdown**  
Административно (включить) выключить сетевой интерфейс.

**show vtp status**  
Показать конфигурацию режима VTP.  
vtp mode <server|client>  
Включить требуемый режим работы VTP.

**show debugging**  
Показать накопленную (в памяти) статистику отладки.  
undebug all  
Полностью выключить отладку.

**traceroute aaa.bbb.ccc.ddd**  
Аналог tracert aaa.bbb.ccc.ddd - показать маршрут до указанного IP.

**show process cpu**  
Показать статистику загрузки процессора (в том числе и каждой задачей).

**show process cpu history**  
Показать статистику загрузки процессора с временными графиками.

**who**  
Показать сеансы администраторов, залогинившихся в терминал циски. Выводит примерно следующее:  
   Line       User      Host(s)              Idle      Location

- 98 vty 0     ciadmin   idle                 00:00:00 10.50.9.152  
    Interface    User              Mode         Idle    Peer Address

**ssh -v 2 -l root a.b.c.d**  
Подсоединиться к <...?..> по SSH версии 2.

**no banner login**  
Удаляет из конфига все строки banner login (приветствие при логине).

**show interfaces port-channel n**  
Показывает состояние канала портов под номером n, какие порты туда входят.

**show ip eigrp neighbors**  
Показывает EIGRP-соседей, какими интерфейсами с ними контакт, номер EIGRP-процесса.  
**show ip eigrp interfaces**  
Показывает список интерфейсов, вовлеченных в EIGRP, номер EIGRP-процесса.  
**show ip eigrp traffic**  
**show ip eigrp topology**  
Показывает статистику работы EIGRP, номер EIGRP-процесса.

**snmp-server community** <строка*пароль> [номер access-листа]  
Команда вводится в режиме глобального конфигурирования. Настраивает доступ к внутреннему snmp-серверу для специального ПО (например, чтобы CiscoWorks Device Fault Manager мог собирать статистику о состоянии оборудования). Параметр <строка*пароль> представляет собой community-string, который используется для аутентификации при подключении. Если указать RW, то будет разрешен полный доступ (чтение и запись) в SNMP базу данных устройства (можно не только считывать состояние, но и менять параметры устройства), если RO, то доступ будет только на чтение. Номер access-листа позволяет отфильтровать нежелательные подключения.

**setup**   
Команда setup привилегированного режима запускает мастера первоначальной настройки.

**terminal history** size n  
Команда, меняющая количество запоминаемых ранее введенных команд (n max 256).

**telnet IP-адрес**  
Команда позволяет подключиться к другой циске. <Ctrl+Shift+6> позволяет приостановить сеанс Telnet (не разрывая его) и вернуться к собственной командной строке устройства. Команда disconnect без параметров позволяет разорвать последнее приостановленное соединение, а resume без параметров возобновляет последнее приостановленное соединение.

**show diag** [номер слота]  
Команда показывает подробную информацию о материнской плате устройства Cisco и/или об установленных в слоты адаптерах.

**show environment**  
Команда на некоторых устройствах (чаще дорогих и продвинутых) показывает состояние вентиляторов и температуру устройства, иногда значение питающих напряжений.

**show ip sockets**  
Команда показывает открытые порты и активные соединения устройства Cisco.

**show ip traffic**  
Команда показывает подробную инфо по трафику протоколов IP (много всего, в том числе количество пакетов broadcast и multicast), ICMP, TCP, BGP, IP-EIGRP, PIMv2, IGMP, UDP, OSPF, ARP и об ошибках.

**show line**  
Команда показывает инфо о линиях - интерфейсах специального типа, предназначенных для администрирования. Обычно это последовательная консоль (CTY, console 0 или линия 0), AUX (обычно линия 1) и консоли Telnet (например, VTY 0-181 или линии 18-199).  
show line summary  
Команда показывает быструю сводку о статистике использования всех линий.

**show sessions**  
Команда показывает информацию приостановленных сессиях Telnet.

**show snmp**  
Команда показывает статистику протокола SNMP (полезно при настройке и проверке работы протокола).

**show tcp**  
Команда показывает подробную статистику о всех открытых соединениях с устройством Cisco

**send \***  
Команда позволяет отсылать сообщение в консоль всех залогиненных пользователей на устройстве. 

verify flash:имя_файла_IOS  
Команда позволяет проверить целостность файла (проверяются контрольные суммы). Полезно выполнить после копирования IOS во флеш (например, при обновлении IOS-а). 

clear ip nat translation \*  
Очистка таблицы NAT, обычно применяемая при смене правил NAT.

(config)# do команда  
Очень полезная команда режима конфигурирования, которая позволяет вводить команды обычного режима (например, do show running-config). Правда, в команде do уже не работает автозавершение команды клавишей Tab и подсказка по вводу ?.

### Примеры:

**Установка пароля для консоли**  
R1(config)#line console 0  
R1(config-line)#password cisco  
R1(config-line)#login

**Установка пароля для telnet**  
R1(config)#line vty 0 4  
R1(config-line)#password cisco  
R1(config-line)#login

**Удаление консольного пароля**  
router(config)#line console 0  
router(config-line)#no login  
router(config-line)#no password

**Удаление пароля Secret**  
router(config)#no enable secret

**Проверка параметра Register**  
router>enable  
router#show version

**Задание адреса-маски и административное включение интерфейса**  
R1(config)#interface Serial0/0/0  
R1(config-if)#ip address 192.168.2.1 255.255.255.0

**Административное выключение интерфейса маршрутизатора**  
router(config)#int s0/0  
router(config-if)#shutdown

**Включение интерфейса Serial**  
router#configure terminal  
router(config)#interface s0/0  
router(config-if)#no shutdown  
Установка тактовой частоты для интерфейса Serial  
router(config-if)#clock rate 64000

**Проверка интерфейса Serial**  
router(config)#show interfaces s0/0

**Добавить статическую запись в таблицу маршрутизации**  
Router(config)#ip route 10.10.10.0 255.255.255.0 {ip-address | exit-interface }

**Посмотреть таблицу маршрутизации**  
R1#show ip route

**Посмотреть интерфейсы**  
R1#show interfaces

**Посмотреть интерфейсы и их статистику в табличном виде**  
R1#show ip interface brief

**Посмотреть соседей устройства:**  
Router#show cdp neighbors  
Router#show cdp neighbors detail

**Глобальное выключение CDP (cisco discovery protocol):**  
Router(config)#no cdp run  
Выключение CDP (cisco discovery protocol) на интерфейсе:  
Router(config-if)#no cdp enable

**Статус DTE/DCE**  
router#show controllers s0/0

**Сохранение конфигурации**  
router#copy running-config startup-config

**Загрузка файла (например IOS) с TFTP сервера**  
R#copy tftp flash:

**Резервное копирование Startup конфига на TFTP**  
router#copy startup-config tftp

**Сохранение Running конфига**  
router#write memory  
router#copy run st

**Удаление конфигурации NVRAM**  
router#write erase

**Проверка конфигурации NVRAM**  
router#show startup-config

**Посмотреть таблицу MAC адресов свитча**  
show mac-address-table

**Статически прописать MAC адрес в таблицу адресов свитча**  
#mac-address-table static MAC address vlan {1-4096, ALL} interface interface-id command

**Создать VLAN**  
S1(config)#vlan 20  
S1(config-vlan)#name students

**Создаем интерфейс для управления VLAN**  
S1(config)#interface vlan 20  
S1(config-if)#ip address 10.2.2.1 255.255.255.0  
S1(config-if)#no shutdown

**Назначить порт для доступа к VLAN**  
S1(config)#interface fa0/18  
S1(config-if)#switchport mode access  
S1(config-if)#switchport access vlan 20

**Назначить порт для транка Cisco Dynamic Trunking protocol**  
S1(config)#interface fa0/18  
или S1(config-if)#switchport mode trunk  
ли S1(config-if)#switchport mode dynamic auto  
или S1(config-if)#switchport mode dynamic desirable  
или S1(config-if)#switchport mode nonegotiate

**какие vlan пропускать через trunk**  
S1(config-if)#switchport trunk allowed vlan 18 (можно указывать диапазоны или all)

**Переключиться обратно из trunk в режим доступа**  
S1(config-if)#no switchport trunk allowed vlan  
S1(config-if)#no switchport trunk native vlan  
S1(config-if)#switchport mode access

**Разрешить трафик местного (native) VLAN через порт транка**  
S1(config)#interface fa0/18  
S1(config-if)#switchport mode trunk  
S1(config-if)#switchport trunk native vlan 18  
S1#show interfaces fa0/18 switchport

**Посмотреть статистику VLAN**  
или show vlan brief  
или show vlan id 20  
или show vlan name students  
или show vlan summary

**Посмотреть статистику портов свитча**  
show interfaces vlan 20  
show interfaces fa0/18 switchport

**Назначить шлюз по умолчанию**  
S1(config)#ip default gateway 1.2.3.4

**Включить протокол динамической маршрутизации**  
R1(config)#router протокол (rip, eigrp и т.д.)  
R1(config-router)#network network_number [wildcard_mask]  
R1(config-if)#bandwidth 64

R1(config-router)#passive-interface s 0/0/0 Выключить динамическую маршрутизацию на интерфейсе  
или  
R1(config-router)#passive-interface default Выключить динамическую маршрутизацию на всех интерфейсах  
а потом на некоторых включить:  
R1(config-router)#no passive-interface s 0/0/0

R1#conf tEnter configuration commands, one per line.  End with CNTL/Z.  
R1(config)#int fa0/0  
R1(config-if)#ip address 10.1.3.1 255.255.255.0  
R1(config-if)#no shutdown  
R1(config-if)#exit  
R1(config)#int fa0/1  
R1(config-if)#ip address 10.1.2.1 255.255.255.0  
R1(config-if)#no shutdown  
R1(config-if)#end  
R1#  
R1#wr mem

 

### **Базовые команды для конфигурирования CISCO Switch**

**Установка пароля для консоли**S1(config)#line console 0  
S1(config-line)#password cisco  
S1(config-line)#login

**Установка пароля для telnet**  
S1(config)#line vty 0 4  
S1(config-line)#password cisco  
S1(config-line)#login

**Удаление консольного пароля**  
switch(config)#line console 0  
switch(config-line)#no login  
switch(config-line)#no password

**Удаление пароля Secret**  
switch(config)#no enable secret

**Проверка параметра Register**  
switch>enable  
switch#show version

**Административное выключение интерфейса маршрутизатора**  
switch(config)#int f0/0  
switchr(config-if)#shutdown

**Посмотреть таблицу MAC адресов свитча**  
show mac-address-table

**Статически прописать MAC адрес в таблицу адресов свитча**  
#mac-address-table static MAC address vlan {1-4096, ALL} interface interface-id command

**Создать VLAN**  
S1(config)#vlan 20  
S1(config-vlan)#name students

**Создаем интерфейс для управления VLAN**  
S1(config)#interface vlan 20  
S1(config-if)#ip address 10.2.2.1 255.255.255.0  
S1(config-if)#no shutdown

**Назначить порт для доступа к VLAN**  
S1(config)#interface fa0/18  
S1(config-if)#switchport mode access  
S1(config-if)#switchport access vlan 20

**Назначить порт для транка Cisco Dynamic Trunking protocol**  
S1(config)#interface fa0/18  
или S1(config-if)#switchport mode trunk  
ли S1(config-if)#switchport mode dynamic auto  
или S1(config-if)#switchport mode dynamic desirable  
или S1(config-if)#switchport mode nonegotiate

**Kакие vlan пропускать через trunk**  
S1(config-if)#switchport trunk allowed vlan 18 (можно указывать диапазоны или all)

**Переключиться обратно из trunk в режим доступа**  
S1(config-if)#no switchport trunk allowed vlan  
S1(config-if)#no switchport trunk native vlan  
S1(config-if)#switchport mode access

**Разрешить трафик местного (native) VLAN через порт транка**  
S1(config)#interface fa0/18  
S1(config-if)#switchport mode trunk  
S1(config-if)#switchport trunk native vlan 18  
S1#show interfaces fa0/18 switchport

**Посмотреть статистику VLAN**  
или show vlan brief  
или show vlan id 20  
или show vlan name students  
или show vlan summary

**Посмотреть статистику портов свитча**  
show interfaces vlan 20  
show interfaces fa0/18 switchport

**Назначить шлюз по умолчанию**  
S1(config)#ip default gateway 1.2.3.4

**Включить протокол динамической маршрутизации**  
R1(config)#router протокол (rip, eigrp и т.д.)  
R1(config-router)#network network_number [wildcard_mask]  
R1(config-if)#bandwidth 64

R1(config-router)#passive-interface s 0/0/0 Выключить динамическую маршрутизацию на интерфейсе  
или  
R1(config-router)#passive-interface default Выключить динамическую маршрутизацию на всех интерфейсах  
а потом на некоторых включить:  
R1(config-router)#no passive-interface s 0/0/0

R1#conf tEnter configuration commands, one per line.  End with CNTL/Z.  
R1(config)#int fa0/0  
R1(config-if)#ip address 10.1.3.1 255.255.255.0  
R1(config-if)#no shutdown  
R1(config-if)#exit  
R1(config)#int fa0/1  
R1(config-if)#ip address 10.1.2.1 255.255.255.0  
R1(config-if)#no shutdown  
R1(config-if)#end  
R1#  
R1#wr mem

 

### **Базовые команды для конфигурирования CISCO Switch**

**Установка пароля для консоли**S1(config)#line console 0  
S1(config-line)#password cisco  
S1(config-line)#login

**Установка пароля для telnet**  
S1(config)#line vty 0 4  
S1(config-line)#password cisco  
S1(config-line)#login

**Удаление консольного пароля**  
switch(config)#line console 0  
switch(config-line)#no login  
switch(config-line)#no password

**Удаление пароля Secret**  
switch(config)#no enable secret

**Проверка параметра Register**  
switch>enable  
switch#show version

**Административное выключение интерфейса маршрутизатора**  
switch(config)#int f0/0  
switchr(config-if)#shutdown

**Посмотреть таблицу MAC адресов свитча**  
show mac-address-table

**Статически прописать MAC адрес в таблицу адресов свитча**  
#mac-address-table static MAC address vlan {1-4096, ALL} interface interface-id command

**Создать VLAN**  
S1(config)#vlan 20  
S1(config-vlan)#name students

**Создаем интерфейс для управления VLAN**  
S1(config)#interface vlan 20  
S1(config-if)#ip address 10.2.2.1 255.255.255.0  
S1(config-if)#no shutdown

**Назначить порт для доступа к VLAN**  
S1(config)#interface fa0/18  
S1(config-if)#switchport mode access  
S1(config-if)#switchport access vlan 20

**Назначить порт для транка Cisco Dynamic Trunking protocol**  
S1(config)#interface fa0/18  
или S1(config-if)#switchport mode trunk  
ли S1(config-if)#switchport mode dynamic auto  
или S1(config-if)#switchport mode dynamic desirable  
или S1(config-if)#switchport mode nonegotiate

**Kакие vlan пропускать через trunk**  
S1(config-if)#switchport trunk allowed vlan 18 (можно указывать диапазоны или all)

**Переключиться обратно из trunk в режим доступа**  
S1(config-if)#no switchport trunk allowed vlan  
S1(config-if)#no switchport trunk native vlan  
S1(config-if)#switchport mode access

**Разрешить трафик местного (native) VLAN через порт транка**  
S1(config)#interface fa0/18  
S1(config-if)#switchport mode trunk  
S1(config-if)#switchport trunk native vlan 18  
S1#show interfaces fa0/18 switchport

**Посмотреть статистику VLAN**  
или show vlan brief  
или show vlan id 20  
или show vlan name students  
или show vlan summary

**Посмотреть статистику портов свитча**  
show interfaces vlan 20  
show interfaces fa0/18 switchport

**Назначить шлюз по умолчанию**  
S1(config)#ip default gateway 1.2.3.4
