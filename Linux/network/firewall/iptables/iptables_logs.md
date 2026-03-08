[источник](https://habr.com/ru/articles/259169/?ysclid=mm4ywbd68y871874266)

# Способ заставить Iptables писать в свой лог и не дублировать в системный

В заметке рассказано о настройке журналирования iptables в отдельный файл. Большинство руководств предлагают два подхода, но, к сожалению, у меня на Debian они так и не заработали. Точнее, логи писались в `/var/log/iptables.log`, но продолжали дублироваться в `/var/log/messages` и `/var/log/syslog`, что очень раздражало и задача была незавершенной. Найдя способ не дублировать сообщения в системные, решил опубликовать полученные результаты.

#### Начало

Сам netfilter не пишет логи в принципе. Чтобы он начал это делать необходимо создать правило с действием LOG. Подробности можно посмотреть в [Iptables Tutorial](http://www.opennet.ru/docs/RUS/iptables/#LOGTARGET).

В качестве примера возьму правило логирования пингов и правило разрешающее их:

```
iptables -A INPUT -p ICMP --icmp-type 8 -j LOG --log-prefix "Ping detected: "iptables -A INPUT -p ICMP --icmp-type 8 -j ACCEPT
```

Теперь по событию, подпадающее под это правило, будет писаться сообщение в `/var/log/messages` и `/var/log/syslog`:

```
kernel: [122972.300408] Ping detected: IN=eth0 OUT= MAC=00:64:d9:36:7b:d7:00:24:2d:a6:e2:43:08:91 SRC=xxx.xxx.xxx.xxx DST=xxx.xxx.xxx.xxx LEN=60 TOS=0x00 PREC=0x00 TTL=124 ID=23020 PROTO=ICMP TYPE=8 CODE=0 ID=33602 SEQ=2462
```

Когда попаданий в правила много, то невозможно проанализировать системные сообщения, т.к. логи iptables’а наводняют весь файл логов.

#### Настройка

Для избежания вышеописанного необходимо изменить критерий в префиксе сообщения, например, так:

```
iptables -A INPUT -p ICMP --icmp-type 8 -j LOG --log-prefix "Iptables: Ping detected: "iptables -A INPUT -p ICMP --icmp-type 8 -j ACCEPT
```

И создать файл `/etc/rsyslog.d/iptables.conf` со следующим содержанием:

```
echo ':msg, contains, "Iptables: " -/var/log/iptables.log' > /etc/rsyslog.d/iptables.conf
echo '& ~' >> /etc/rsyslog.d/iptables.conf
```

Параметры:  
`& ~` — говорит о том, что дальнейшую обработку записи производить не следует, поэтому она не попадет в другие файлы логов.  
`"Iptables: "` — тот самый log-prefix — критерий по которому rsyslog принимает решение перенаправить лог в нужный файл. Префикс можно было и не менять, а оставить как есть — `Ping detected`, но если правило не одно, то удобнее иметь общий префикс для всех правил, который и был сделан.  
`/var/log/iptables.log` — сам файл лога.  
Перезапустить демон rsyslog:

```
systemctl restart rsyslog
```

Теперь сообщение в логе `/var/log/iptables.log` выглядит так:

```
kernel: [122972.300408] Iptables: Ping detected: IN=eth0 OUT= MAC=00:64:d9:36:7b:d7:00:24:2d:a6:e2:43:08:91 SRC=xxx.xxx.xxx.xxx DST=xxx.xxx.xxx.xxx LEN=60 TOS=0x00 PREC=0x00 TTL=124 ID=23020 PROTO=ICMP TYPE=8 CODE=0 ID=33602 SEQ=2462
```

Наконец Iptables пишет в свой личный лог не ~~засирая~~ трогая системные.  
Можно пойти дальше, создав правила для разных событий и каждое событие направить в свой лог, например:

```
# Логировать пакеты со статусом INVALID:
iptables -A INPUT -m state --state INVALID -j LOG --log-prefix "Iptables: Invalid packet: "

# Логировать INPUT пакеты, которые не попали ни в одно правило:
iptables -A INPUT -m limit --limit 3/minute --limit-burst 3 -j LOG --log-prefix "Iptables: INPUT packet died: "

# Логировать FORWARD пакеты, которые не попали ни в одно правило:
iptables -A FORWARD -m limit --limit 3/minute --limit-burst 3 -j LOG --log-prefix "Iptables: FORWARD packet died: "
```

Создать правила для ведения логирования каждого файла:

```
echo ':msg, contains, "Iptables: Invalid packet" -/var/log/iptables_invalid.log' > /etc/rsyslog.d/iptables_invalid.conf
echo '& ~' >> /etc/rsyslog.d/iptables_invalid.conf

echo ':msg, contains, "Iptables: INPUT" -/var/log/iptables_input.log' > /etc/rsyslog.d/iptables_input.conf
echo '& ~' >> /etc/rsyslog.d/iptables_input.conf

echo ':msg, contains, "Iptables: FORWARD" -/var/log/iptables_forward.log' > /etc/rsyslog.d/iptables_forward.conf
echo '& ~' >> /etc/rsyslog.d/iptables_forward.conf
```

Перезапустить rsyslog:

```
systemctl restart rsyslog
```

При такой конфигурации лог Iptables разделен на три части и каждая пишется в свой файл.

#### Ротация логов Iptables

Настроить ротацию логов iptables можно создав файл `/etc/logrotate.d/iptables` со следующим содержимым. Для одного общего лога:

```
/var/log/iptables.log {
    daily
    rotate 30
    compress
    missingok
    notifempty
    sharedscripts
}
```

или для раздельных:

```
/var/log/iptables_invalid.log {
    daily
    rotate 30
    compress
    missingok
    notifempty
}

/var/log/iptables_input.log {
    daily
    rotate 30
    compress
    missingok
    notifempty
}

/var/log/iptables_forward.log {
    daily
    rotate 30
    compress
    missingok
    notifempty
}
```

Где  
`daily` — ротировать ежедневно  
`rotate 30` — сохранять 30 последних ротированных файлов  
`compress` — сжимать  
`missingok` — отсутствие файла не является ошибкой  
`notifempty` — не обрабатывать пустые файлы  
Убедиться в правильности ротации можно принудительно запустив ее:

```
logrotate -f /etc/logrotate.conf
```

Работоспособность тестировалась на Debian 7 и Debian 8. Также должно работать на всех дистрибутивах, использующих Iptables и rsyslog.
