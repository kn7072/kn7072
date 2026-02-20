[источник](https://forensicanvil.ru/forum/topic/tools/wireshark-filtry-shpargalka?ysclid=mlupf2hng4442980587)

- [ Что такое Wireshark](#link_1)
  - [ Возможности Wireshark](#link_2)
  - [ Типы фильтров в Wireshark](#link_3)
    - [ Capture Filters (фильтры захвата) ](#link_4)
    - [ Display Filters (фильтры отображения) ](#link_5)
  - [ Когда использовать Wireshark](#link_6)
- [ Основы работы с фильтрами](#link_7)
  - [ Интерфейс фильтров](#link_8)
    - [ Filter Toolbar ](#link_9)
    - [ Capture Options ](#link_10)
  - [ Сохранение и загрузка фильтров](#link_11)
    - [ Filter Buttons ](#link_12)
    - [ Filter Macros ](#link_13)
- [ Синтаксис фильтров Wireshark](#link_14)
  - [ Основные операторы](#link_15)
  - [ Функции и операторы](#link_16)
    - [ Строковые операторы ](#link_17)
    - [ Арифметические операторы ](#link_18)
    - [ Специальные операторы ](#link_19)
- [ Фильтры по протоколам](#link_20)
  - [ Основные сетевые протоколы](#link_21)
    - [ Ethernet ](#link_22)
    - [ ARP ](#link_23)
    - [ IPv4/IPv6 ](#link_24)
  - [ Транспортные протоколы](#link_25)
    - [ TCP ](#link_26)
    - [ UDP ](#link_27)
    - [ ICMP ](#link_28)
- [ Фильтры по IP адресам и портам](#link_29)
  - [ IP адрес фильтры](#link_30)
    - [ Источник и получатель ](#link_31)
    - [ Диапазоны IP ](#link_32)
    - [ Window size ](#link_33)
    - [ TCP handshake ](#link_34)
  - [ TCP retransmissions](#link_35)
    - [ Retransmitted packets ](#link_36)
    - [ Lost packets ](#link_37)
- [ Фильтры по HTTP трафику](#link_38)
  - [ HTTP методы](#link_39)
    - [ Request methods ](#link_40)
    - [ Response codes ](#link_41)
  - [ HTTP headers](#link_42)
    - [ Request headers ](#link_43)
    - [ Response headers ](#link_44)
  - [ HTTP cookies и сессии](#link_45)
    - [ Cookies ](#link_46)
    - [ Authentication ](#link_47)
  - [ HTTPS/SSL](#link_48)
    - [ SSL/TLS ](#link_49)
    - [ Certificates ](#link_50)
- [ Фильтры по содержимому пакетов](#link_51)
  - [ Строковые фильтры](#link_52)
    - [ Contains оператор ](#link_53)
    - [ Matches оператор (регулярные выражения) ](#link_54)
  - [ Байтовые фильтры](#link_55)
    - [ Hex значения ](#link_56)
  - [ Размер пакетов](#link_57)
    - [ Packet length ](#link_58)
  - [ Время и последовательность](#link_59)
    - [ Time-based ](#link_60)
    - [ Sequence-based ](#link_61)
- [ Продвинутые фильтры](#link_62)
  - [ Expert Info фильтры](#link_63)
    - [ Errors and warnings ](#link_64)
    - [ Protocol-specific ](#link_65)
  - [ Statistics фильтры](#link_66)
    - [ Conversations ](#link_67)
    - [ Endpoints ](#link_68)
  - [ IO Graph фильтры](#link_69)
    - [ Throughput ](#link_70)
    - [ Error rates ](#link_71)
  - [ Custom columns и fields](#link_72)
    - [ Protocol fields ](#link_73)
    - [ Custom expressions ](#link_74)
- [ Комбинация фильтров](#link_75)
  - [ Логические комбинации](#link_76)
    - [ AND комбинации ](#link_77)
    - [ OR комбинации ](#link_78)
    - [ NOT комбинации ](#link_79)
  - [ Комплексные фильтры](#link_80)
    - [ Network troubleshooting ](#link_81)
    - [ Security analysis ](#link_82)
    - [ Performance analysis ](#link_83)
- [ Практические примеры использования](#link_84)
  - [ Анализ веб-трафика](#link_85)
    - [ HTTP анализ ](#link_86)
    - [ HTTPS анализ ](#link_87)
    - [ Cookie анализ ](#link_88)
  - [ Анализ сетевых проблем](#link_89)
    - [ Retransmissions ](#link_90)
    - [ Packet loss ](#link_91)
    - [ High latency ](#link_92)
  - [ Безопасность и forensics](#link_93)
    - [ Port scanning ](#link_94)
    - [ Malware traffic ](#link_95)
    - [ Data exfiltration ](#link_96)
  - [ Мониторинг приложений](#link_97)
    - [ Database queries ](#link_98)
    - [ API calls ](#link_99)
    - [ Error responses ](#link_100)
- [ Советы по работе с Wireshark](#link_101)
  - [ Захват трафика](#link_102)
    - [ Выбор интерфейса ](#link_103)
    - [ Capture filters ](#link_104)
  - [ Анализ трафика](#link_105)
    - [ Follow streams ](#link_106)
    - [ Expert Info ](#link_107)
  - [ Производительность](#link_108)
    - [ Large captures ](#link_109)
    - [ Memory usage ](#link_110)
  - [ Безопасность](#link_111)
    - [ Sensitive data ](#link_112)
    - [ Legal considerations ](#link_113)
- [ Часто задаваемые вопросы](#link_114)
  - [ Основы Wireshark](#link_115)
  - [ Фильтры](#link_116)
  - [ Производительность](#link_117)
  - [ Безопасность](#link_118)
- [ Заключение](#link_119)
  - [ Ключевые принципы эффективного использования:](#link_120)
  - [ Рекомендации по изучению:](#link_121)
  - [ Лучшие практики:](#link_122)

## Что такое Wireshark <a name="link_1"></a>

Wireshark - это мощный инструмент для анализа сетевого трафика, который позволяет захватывать и детально анализировать сетевые пакеты. Программа поддерживает более 3000 протоколов и является стандартом де-факто для network forensics и troubleshooting.

### Возможности Wireshark <a name="link_2"></a>

- Packet Capture - захват пакетов в реальном времени
- Protocol Analysis - глубокий анализ протоколов
- Traffic Filtering - фильтрация трафика по различным критериям
- Statistical Analysis - статистика сетевого трафика
- Export Functions - экспорт данных в различные форматы
- Graphical Interface - удобный GUI для анализа
- Command Line Tools - tshark для автоматизации

### Типы фильтров в Wireshark <a name="link_3"></a>

#### Capture Filters (фильтры захвата) <a name="link_4"></a>

- Применяются на этапе захвата пакетов
- Определяют, какие пакеты захватывать
- Используют синтаксис libpcap/tcpdump
- Экономят ресурсы системы

#### Display Filters (фильтры отображения) <a name="link_5"></a>

- Применяются к уже захваченному трафику
- Позволяют фильтровать отображаемые пакеты
- Более гибкий синтаксис
- Не влияют на производительность захвата

### Когда использовать Wireshark <a name="link_6"></a>

- Network Troubleshooting - диагностика сетевых проблем
- Security Analysis - анализ подозрительного трафика
- Protocol Development - отладка сетевых протоколов
- Performance Analysis - анализ производительности сети
- Forensic Analysis - анализ инцидентов безопасности
- Learning - изучение сетевых технологий

## Основы работы с фильтрами <a name="link_7"></a>

### Интерфейс фильтров <a name="link_8"></a>

#### Filter Toolbar <a name="link_9"></a>

- Filter Bar - поле для ввода фильтров отображения
- Filter Expression Buttons - быстрые фильтры по протоколам
- Filter Bookmarks - сохраненные фильтры
- Coloring Rules - цветовая подсветка пакетов

#### Capture Options <a name="link_10"></a>

- Interface Selection - выбор сетевого интерфейса
- Capture Filter - фильтр захвата пакетов
- Options - дополнительные настройки захвата

### Сохранение и загрузка фильтров <a name="link_11"></a>

#### Filter Buttons <a name="link_12"></a>

- Save Filter - сохранить текущий фильтр
- Manage Filter Buttons - управление сохраненными фильтрами
- Filter Button Preferences - настройки кнопок фильтров

#### Filter Macros <a name="link_13"></a>

- $variable - использование переменных в фильтрах
- ${variable} - расширенный синтаксис переменных

## Синтаксис фильтров Wireshark <a name="link_14"></a>

### Основные операторы <a name="link_15"></a>

| Оператор | Описание         | Пример                                                     |
| -------- | ---------------- | ---------------------------------------------------------- |
| `==`     | Равно            | `ip.addr == 192.168.1.1`                                   |
| `!=`     | Не равно         | `ip.addr != 192.168.1.1`                                   |
| `<`      | Меньше           | `tcp.port < 1024`                                          |
| `<=`     | Меньше или равно | `tcp.port <= 1024`                                         |
| `>`      | Больше           | `tcp.port > 1024`                                          |
| `>=`     | Больше или равно | `tcp.port >= 1024`                                         |
| `&&`     | И (логическое)   | `ip.src == 1.2.3.4 && tcp.port == 80`                      |
| `\|`     | ИЛИ (логическое) | `tcp.port == 80 \| tcp.port == 443`                        |
| `!`      | НЕ (отрицание)   | `!tcp.port == 80`                                          |
| `()`     | Группировка      | `(tcp.port == 80 \| tcp.port == 443) && ip.src == 1.2.3.4` |

### Функции и операторы <a name="link_16"></a>

#### Строковые операторы <a name="link_17"></a>

- `contains` - содержит подстроку
- `matches` - регулярное выражение
- `starts_with` - начинается с
- `ends_with` - заканчивается на

#### Арифметические операторы <a name="link_18"></a>

- `+`, `-`, `*`, `/` - арифметические операции
- `&`, `\|`, `^` - побитовые операции
- `` - сдвиги

#### Специальные операторы <a name="link_19"></a>

- `in {1 2 3}` - значение в множестве
- `slice[start:end]` - срез массива/строки
- `upper()`, `lower()` - преобразование регистра

## Фильтры по протоколам <a name="link_20"></a>

### Основные сетевые протоколы <a name="link_21"></a>

#### Ethernet <a name="link_22"></a>

1. `eth` - все Ethernet пакеты
2. `eth.addr == aa:bb:cc:dd:ee:ff` - пакеты с конкретным MAC
3. `eth.src == aa:bb:cc:dd:ee:ff` - пакеты от конкретного MAC
4. `eth.dst == aa:bb:cc:dd:ee:ff` - пакеты к конкретному MAC
5. `eth.type == 0x0800` - IPv4 пакеты
6. `eth.type == 0x0806` - ARP пакеты
7. `eth.type == 0x86dd` - IPv6 пакеты

#### ARP <a name="link_23"></a>

8. `arp` - все ARP пакеты
9. `arp.opcode == 1` - ARP request
10. `arp.opcode == 2` - ARP reply
11. `arp.src.hw_mac == aa:bb:cc:dd:ee:ff` - ARP от конкретного MAC
12. `arp.dst.hw_mac == aa:bb:cc:dd:ee:ff` - ARP к конкретному MAC

#### IPv4/IPv6 <a name="link_24"></a>

13. `ip` - все IPv4 пакеты
14. `ipv6` - все IPv6 пакеты
15. `ip.version == 4` - IPv4 пакеты
16. `ip.version == 6` - IPv6 пакеты
17. `ip.ttl <> 200` - пакеты с высоким TTL

### Транспортные протоколы <a name="link_25"></a>

#### TCP <a name="link_26"></a>

19. `tcp` - все TCP пакеты
20. `tcp.port == 80` - HTTP трафик
21. `tcp.port == 443` - HTTPS трафик
22. `tcp.port == 22` - SSH трафик
23. `tcp.port == 23` - Telnet трафик
24. `tcp.port == 25` - SMTP трафик
25. `tcp.port == 53` - DNS трафик
26. `tcp.port == 110` - POP3 трафик
27. `tcp.port == 143` - IMAP трафик
28. `tcp.port == 3389` - RDP трафик
29. `tcp.port == 5900` - VNC трафик

#### UDP <a name="link_27"></a>

30. `udp` - все UDP пакеты
31. `udp.port == 53` - DNS запросы
32. `udp.port == 67` - DHCP server
33. `udp.port == 68` - DHCP client
34. `udp.port == 69` - TFTP
35. `udp.port == 123` - NTP
36. `udp.port == 161` - SNMP
37. `udp.port == 500` - IKE (VPN)
38. `udp.port == 1194` - OpenVPN

#### ICMP <a name="link_28"></a>

39. `icmp` - все ICMP пакеты
40. `icmp.type == 0` - Echo Reply (ping ответ)
41. `icmp.type == 8` - Echo Request (ping запрос)
42. `icmp.type == 3` - Destination Unreachable
43. `icmp.type == 11` - Time Exceeded
44. `icmp.code == 0` - Network unreachable

## Фильтры по IP адресам и портам <a name="link_29"></a>

### IP адрес фильтры <a name="link_30"></a>

#### Источник и получатель <a name="link_31"></a>

45. `ip.src == 192.168.1.1` - пакеты от конкретного IP
46. `ip.dst == 192.168.1.1` - пакеты к конкретному IP
47. `ip.addr == 192.168.1.1` - пакеты с участием IP
48. `ip.src != 192.168.1.1` - пакеты не от этого IP
49. `ip.dst != 192.168.1.1` - пакеты не к этому IP

#### Диапазоны IP <a name="link_32"></a>

50. `ip.src >= 192.168.1.0 && ip.src = 1024 && tcp.port 1000` - пакеты с высоким sequence number

#### Window size <a name="link_33"></a>

83. `tcp.window_size == 0` - zero window пакеты
84. `tcp.window_size <> 60000` - большое окно

#### TCP handshake <a name="link_34"></a>

86. `tcp.flags.syn == 1 && tcp.flags.ack == 0` - SYN пакеты
87. `tcp.flags.syn == 1 && tcp.flags.ack == 1` - SYN-ACK пакеты
88. `tcp.flags.ack == 1 && !tcp.flags.syn && !tcp.flags.fin` - ACK пакеты

### TCP retransmissions <a name="link_35"></a>

#### Retransmitted packets <a name="link_36"></a>

89. `tcp.analysis.retransmission` - повторно переданные пакеты
90. `tcp.analysis.fast_retransmission` - fast retransmissions
91. `tcp.analysis.duplicate_ack` - duplicate acknowledgments

#### Lost packets <a name="link_37"></a>

92. `tcp.analysis.lost_segment` - потерянные сегменты
93. `tcp.analysis.ack_lost_segment` - ACK на потерянные сегменты

## Фильтры по HTTP трафику <a name="link_38"></a>

### HTTP методы <a name="link_39"></a>

#### Request methods <a name="link_40"></a>

94. `http.request.method == "GET"` - GET запросы
95. `http.request.method == "POST"` - POST запросы
96. `http.request.method == "PUT"` - PUT запросы
97. `http.request.method == "DELETE"` - DELETE запросы
98. `http.request.method == "HEAD"` - HEAD запросы
99. `http.request.method == "OPTIONS"` - OPTIONS запросы

#### Response codes <a name="link_41"></a>

100. `http.response.code == 200` - успешные ответы
101. `http.response.code >= 400` - ошибки клиента/сервера
102. `http.response.code == 404` - Not Found
103. `http.response.code == 500` - Internal Server Error

### HTTP headers <a name="link_42"></a>

#### Request headers <a name="link_43"></a>

104. `http contains "User-Agent"` - запросы с User-Agent
105. `http.user_agent contains "Mozilla"` - Firefox/Chrome
106. `http.referer contains "google.com"` - реферер Google
107. `http.host == "example.com"` - запросы к домену

#### Response headers <a name="link_44"></a>

108. `http.server contains "Apache"` - Apache сервер
109. `http.server contains "nginx"` - Nginx сервер
110. `http.content_type == "text/html"` - HTML контент
111. `http.content_length > 1000` - большие ответы

### HTTP cookies и сессии <a name="link_45"></a>

#### Cookies <a name="link_46"></a>

112. `http contains "Cookie"` - запросы с куками
113. `http.cookie contains "session_id"` - сессионные куки
114. `http.set_cookie contains "PHPSESSID"` - установка сессии

#### Authentication <a name="link_47"></a>

115. `http.authorization` - HTTP аутентификация
116. `http.authbasic` - Basic аутентификация
117. `http.authdigest` - Digest аутентификация

### HTTPS/SSL <a name="link_48"></a>

#### SSL/TLS <a name="link_49"></a>

118. `ssl` - все SSL/TLS трафик
119. `ssl.handshake` - handshake пакеты
120. `ssl.record.version == 0x0303` - TLS 1.2
121. `ssl.record.version == 0x0304` - TLS 1.3

#### Certificates <a name="link_50"></a>

122. `ssl.handshake.certificate` - сертификаты
123. `ssl.handshake.extensions_server_name == "example.com"` - SNI

## Фильтры по содержимому пакетов <a name="link_51"></a>

### Строковые фильтры <a name="link_52"></a>

#### Contains оператор <a name="link_53"></a>

124. `frame contains "password"` - пакеты содержащие "password"
125. `tcp contains "login"` - TCP пакеты с "login"
126. `udp contains "admin"` - UDP пакеты с "admin"
127. `http contains "sql"` - HTTP с "sql"

#### Matches оператор (регулярные выражения) <a name="link_54"></a>

128. `frame matches "[Pp]assword"` - case-insensitive password
129. `http.request.uri matches "/admin/.*"` - URI начинающиеся с /admin/
130. `tcp.payload matches "user|login"` - user или login

### Байтовые фильтры <a name="link_55"></a>

#### Hex значения <a name="link_56"></a>

131. `frame[0:4] == 45:00:00:3c` - первые 4 байта
132. `tcp.payload[0:2] == ff:fe` - BOM в UTF-16
133. `udp.payload[10:4] == de:ad:be:ef` - magic bytes

### Размер пакетов <a name="link_57"></a>

#### Packet length <a name="link_58"></a>

134. `frame.len > 1500` - пакеты больше MTU
135. `frame.len <> 1000` - TCP payload > 1KB
136. `udp.length > 512` - UDP пакеты > 512 байт
137. `http.content_length > 10000` - HTTP контент > 10KB

### Время и последовательность <a name="link_59"></a>

#### Time-based <a name="link_60"></a>

140. `frame.time >= "2024-01-01 00:00:00"` - пакеты после даты
141. `frame.time 1.0` - задержки > 1 секунды

#### Sequence-based <a name="link_61"></a>

143. `frame.number > 1000` - пакеты после номера 1000
144. `frame.number % 100 == 0` - каждый 100-й пакет
145. `tcp.stream == 1` - пакеты из TCP потока 1

## Продвинутые фильтры <a name="link_62"></a>

### Expert Info фильтры <a name="link_63"></a>

#### Errors and warnings <a name="link_64"></a>

146. `expert.message` - все сообщения эксперта
147. `expert.severity == 0` - ошибки (Error)
148. `expert.severity == 1` - предупреждения (Warning)
149. `expert.severity == 2` - заметки (Note)

#### Protocol-specific <a name="link_65"></a>

150. `expert.protocol == "tcp"` - TCP ошибки
151. `expert.protocol == "http"` - HTTP ошибки
152. `expert.group == "checksum"` - checksum ошибки

### Statistics фильтры <a name="link_66"></a>

#### Conversations <a name="link_67"></a>

153. `ip.addr==192.168.1.1 && ip.addr==192.168.1.2` - разговор между IP
154. `tcp.stream` - группировка по TCP потокам
155. `udp.stream` - группировка по UDP потокам

#### Endpoints <a name="link_68"></a>

156. `eth.addr` - Ethernet endpoints
157. `ip.addr` - IP endpoints
158. `tcp.port` - TCP port endpoints
159. `udp.port` - UDP port endpoints

### IO Graph фильтры <a name="link_69"></a>

#### Throughput <a name="link_70"></a>

160. `tcp.port==80` - HTTP throughput
161. `tcp.port==443` - HTTPS throughput
162. `udp.port==53` - DNS traffic

#### Error rates <a name="link_71"></a>

163. `tcp.analysis.retransmission` - retransmission rate
164. `tcp.analysis.duplicate_ack` - duplicate ACK rate
165. `icmp` - ICMP traffic

### Custom columns и fields <a name="link_72"></a>

#### Protocol fields <a name="link_73"></a>

166. `tcp.window_size` - TCP window size
167. `tcp.analysis.acks_frame` - ACK analysis
168. `http.request_in` - HTTP request timing
169. `http.response_in` - HTTP response timing

#### Custom expressions <a name="link_74"></a>

170. `tcp.time_delta > 0.1` - TCP timing analysis
171. `frame.len / tcp.len > 2` - overhead analysis
172. `tcp.flags.push && tcp.len > 0` - push flag analysis

## Комбинация фильтров <a name="link_75"></a>

### Логические комбинации <a name="link_76"></a>

#### AND комбинации <a name="link_77"></a>

173. `ip.src == 192.168.1.1 && tcp.port == 80` - IP и порт
174. `http && tcp.port == 8080` - HTTP на нестандартном порту
175. `ssl && tcp.port != 443` - SSL не на 443 порту

#### OR комбинации <a name="link_78"></a>

176. `tcp.port == 80 || tcp.port == 443` - HTTP или HTTPS
177. `udp.port == 53 || tcp.port == 53` - DNS по UDP или TCP
178. `icmp.type == 8 || icmp.type == 0` - ping request/reply

#### NOT комбинации <a name="link_79"></a>

179. `!tcp.port == 80` - не HTTP трафик
180. `!dns` - не DNS запросы
181. `!(ip.src == 192.168.1.1)` - не от конкретного IP

### Комплексные фильтры <a name="link_80"></a>

#### Network troubleshooting <a name="link_81"></a>

182. `tcp.analysis.retransmission && tcp.stream == 1` - ретрансмиссии в потоке
183. `tcp.analysis.lost_segment` - потерянные сегменты
184. `tcp.analysis.duplicate_ack` - duplicate ACKs

#### Security analysis <a name="link_82"></a>

185. `tcp.flags.syn == 1 && tcp.flags.ack == 0 && ip.src != 192.168.1.0/24` - внешние SYN сканы
186. `tcp.flags.rst == 1 && tcp.flags.ack == 1` - RST ответы на закрытые порты
187. `icmp.type == 3 && icmp.code == 3` - port unreachable

#### Performance analysis <a name="link_83"></a>

188. `tcp.time_delta > 1.0` - медленные соединения
189. `frame.len > 1460` - oversized packets
190. `tcp.window_size == 0` - zero window condition

## Практические примеры использования <a name="link_84"></a>

### Анализ веб-трафика <a name="link_85"></a>

#### HTTP анализ <a name="link_86"></a>

http

```text
.request.method == "POST" && http contains "password"
```

Найти POST запросы с паролями в открытом виде.

#### HTTPS анализ <a name="link_87"></a>

tcp

```text
.port == 443 && ssl.handshake.extensions_server_name contains "bank"
```

Найти HTTPS соединения к банковским сайтам.

#### Cookie анализ <a name="link_88"></a>

http

```text
contains "session" && http.cookie contains "PHPSESSID"
```

Найти HTTP трафик с PHP сессиями.

### Анализ сетевых проблем <a name="link_89"></a>

#### Retransmissions <a name="link_90"></a>

tcp

```text
.analysis.retransmission && tcp.stream == 5
```

Найти ретрансмиссии в конкретном TCP потоке.

#### Packet loss <a name="link_91"></a>

tcp

```text
.analysis.lost_segment
```

Найти потерянные TCP сегменты.

#### High latency <a name="link_92"></a>

tcp

```text
.time_delta > 0.5
```

Найти медленные TCP соединения.

### Безопасность и forensics <a name="link_93"></a>

#### Port scanning <a name="link_94"></a>

tcp

```text
.flags.syn == 1 && tcp.flags.ack == 0 && ip.src != 192.168.1.0/24
```

Найти SYN сканы из внешней сети.

#### Malware traffic <a name="link_95"></a>

udp

```text
.port == 53 && dns.qry.name contains ".onion"
```

Найти DNS запросы к Tor hidden services.

#### Data exfiltration <a name="link_96"></a>

tcp

```text
.len > 10000 && !http
```

Найти большие TCP передачи не по HTTP.

### Мониторинг приложений <a name="link_97"></a>

#### Database queries <a name="link_98"></a>

tcp

```text
.port == 3306 && mysql.query contains "SELECT"
```

Найти MySQL SELECT запросы.

#### API calls <a name="link_99"></a>

tcp

```text
.port == 443 && http.request.uri contains "/api/"
```

Найти HTTPS API вызовы.

#### Error responses <a name="link_100"></a>

http

```text
.response.code >= 500
```

Найти HTTP ошибки сервера.

## Советы по работе с Wireshark <a name="link_101"></a>

### Захват трафика <a name="link_102"></a>

#### Выбор интерфейса <a name="link_103"></a>

- Используйте promiscuous mode для захвата всего трафика
- Выбирайте правильный интерфейс (WiFi, Ethernet)
- Для wireless включайте monitor mode

#### Capture filters <a name="link_104"></a>

- `host 192.168.1.1` - трафик конкретного хоста
- `net 192.168.1.0/24` - трафик подсети
- `port 80` - трафик конкретного порта
- `tcp portrange 20-25` - диапазон портов

### Анализ трафика <a name="link_105"></a>

#### Follow streams <a name="link_106"></a>

- Правый клик → Follow → TCP Stream
- Полный просмотр TCP соединений
- Экспорт в текстовый файл

#### Expert Info <a name="link_107"></a>

- Analyze → Expert Info
- Просмотр ошибок и предупреждений
- Группировка по протоколам

### Производительность <a name="link_108"></a>

#### Large captures <a name="link_109"></a>

- Используйте ring buffers для больших захватов
- Фильтруйте на этапе захвата, а не отображения
- Сохраняйте только необходимые пакеты

#### Memory usage <a name="link_110"></a>

- Закрывайте неиспользуемые окна
- Используйте display filters для больших файлов
- Рассмотрите command-line tshark для автоматизации

### Безопасность <a name="link_111"></a>

#### Sensitive data <a name="link_112"></a>

- Не захватывайте трафик с конфиденциальной информацией
- Используйте фильтры для исключения чувствительных данных
- Удаляйте захваченные файлы после анализа

#### Legal considerations <a name="link_113"></a>

- Получайте разрешение на захват трафика
- Соблюдайте privacy laws
- Не анализируйте чужой трафик без разрешения

## Часто задаваемые вопросы <a name="link_114"></a>

### Основы Wireshark <a name="link_115"></a>

Что такое Wireshark?  
Бесплатный анализатор сетевых протоколов для захвата и анализа пакетов.

Чем отличается capture filter от display filter?  
Capture filter применяется при захвате (экономит ресурсы), display filter - при просмотре захваченных пакетов.

Как захватывать трафик в Wireshark?  
Выберите интерфейс → Start capture. Для wireless нужен monitor mode.

Можно ли анализировать HTTPS в Wireshark?  
Да, но для расшифровки нужен приватный ключ сервера или SSLKEYLOGFILE.

### Фильтры <a name="link_116"></a>

Как создать сложный фильтр?  
Используйте логические операторы && (AND), || (OR), ! (NOT) и группировку ().

Почему фильтр не работает?  
Проверьте синтаксис. Display filters чувствительны к регистру. Используйте автодополнение.

Как сохранить фильтр?  
Filter → Filter Button → Save. Или используйте Filter Bookmarks.

Можно ли использовать регулярные выражения?  
Да, с оператором matches: `frame matches "regex"`

### Производительность <a name="link_117"></a>

Wireshark тормозит с большим файлом  
Используйте display filters для уменьшения количества отображаемых пакетов.

Как анализировать гигабайтные файлы?  
Используйте command-line tshark или splitcap для разделения файлов.

Захват тормозит систему  
Используйте capture filters для захвата только нужного трафика.

### Безопасность <a name="link_118"></a>

Безопасно ли использовать Wireshark?  
Да, но будьте осторожны с захватом чувствительного трафика.

Могут ли меня засечь при анализе сети?  
При passive анализе - нет. Активное сканирование может быть обнаружено.

Как защитить захваченные данные?  
Храните в зашифрованных контейнерах, удаляйте после использования.

## Заключение <a name="link_119"></a>

Wireshark фильтры - мощный инструмент для глубокого анализа сетевого трафика. Эта шпаргалка содержит более 190 готовых фильтров для различных сценариев использования.

### Ключевые принципы эффективного использования: <a name="link_120"></a>

1. Начинайте с широких фильтров - постепенно сужайте область
2. Комбинируйте фильтры - используйте логические операторы
3. Сохраняйте полезные фильтры - создавайте bookmark'и
4. Изучайте протоколы - понимание структуры помогает в анализе
5. Используйте статистики - IO Graphs, Conversations, Endpoints

### Рекомендации по изучению: <a name="link_121"></a>

- Практика - анализируйте свой собственный трафик
- Документация - читайте Wireshark Wiki и RFC
- Сообщество - участвуйте в форумах и Ask Wireshark
- Курсы - проходите официальные Wireshark University курсы
- Эксперименты - тестируйте фильтры в лабораторных условиях

### Лучшие практики: <a name="link_122"></a>

- Всегда получайте разрешение на анализ чужого трафика
- Используйте capture filters для снижения нагрузки
- Регулярно обновляйте Wireshark до последней версии
- Изучайте новые протоколы и их особенности
- Делитесь полезными фильтрами с сообществом

Wireshark - это не просто инструмент, а целый фреймворк для понимания сетевых технологий. Мастерство приходит с практикой и глубоким пониманием протоколов.
