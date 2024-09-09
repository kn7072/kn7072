[источник](https://zalinux.ru/?p=6000)
# Как узнать, какой процесс изменяет файл

В Linux имеется платформа аудита, которая позволяет узнать обо всех случаях доступа к файлу, его изменениях или запуске. Также можно вести наблюдение за изменением целых директорий.
## Как установить auditd (auditctl)  

В **Debian, Linux Mint, Kali Linux, Ubuntu** и их производных для установки выполните команду:

|   |   |
|---|---|
|1|`sudo` `apt` `install` `auditd`|

В **Arch Linux, Manjaro, BlackArch** и их производных данный пакет называется **audit** и входит в **core** репозиторий, следовательно, он предустановлен по умолчанию.

В **CentOS** для установки выполните команду:

|   |   |
|---|---|
|1|`yum` `install` `audit`|
## Как запустить монитор доступа и изменений файла  

Необходимо начать с добавления правил. Следующая команда добавляет монитор доступа и изменения файла **/etc/resolv.conf**:

|   |   |
|---|---|
|1|`sudo` `auditctl -w` `/etc/resolv``.conf -p wa`|

Это пример команды с другой нотацией, но выполняет она идентичное действие — мониторит все изменения и доступ к файлу **/etc/resolv.conf**:

|   |   |
|---|---|
|1|`sudo` `auditctl -a always,``exit` `-F path=``/etc/resolv``.conf -F perm=wa`|

Проверить, какие правила добавлены, можно следующей командой:

|   |   |
|---|---|
|1|`sudo` `auditctl -l`|

Хотя правило добавлено, служба аудита ещё не запущена. Для её запуска выполните команду:

|   |   |
|---|---|
|1|`sudo` `systemctl start auditd.service`|

Если вы хотите добавить данную службу в автозагрузку, то выполните:

|   |   |
|---|---|
|1|`sudo` `systemctl` `enable` `auditd.service`|
## Запуск auditd без перевода в фон  

Предыдущая команда запустит **auditd** как демон, то есть служба в фоне. Если вам это не нужно и вы хотите запустить auditd на переднем плане, то вместо использования systemctl выполните следующую команду:

|   |   |
|---|---|
|1|`sudo` `auditd -f`|

В этом случае все события с отслеживаемыми файлами или папками будут отображаться в стандартном выводе. При этом файл журнала не будет вестись.

Это полезно при отладке правил, либо если вам нужно проследить за событиями в короткий промежуток времени.

## Как просмотреть журнал auditd  
man ausearch\(8\)
Журнал auditd хранится в файле **/var/log/audit/audit.log**. Но вместо того, что просматривать его напрямую, можно воспользоваться утилитой ausearch, например:

|   |   |
|---|---|
|1|`sudo` `ausearch -f` `/etc/resolv``.conf`|

Если будет выведено

|   |   |
|---|---|
|1|`<no matches>`|

значит данный файл ещё не трогала ни одна программа.

Если события произошли, там будут примерно следующие записи:

|   |   |
|---|---|
|1<br><br>2<br><br>3<br><br>4<br><br>5<br><br>6<br><br>7<br><br>8<br><br>9<br><br>10<br><br>11<br><br>12<br><br>13<br><br>14<br><br>15<br><br>16<br><br>17<br><br>18<br><br>19<br><br>20<br><br>21<br><br>22<br><br>23<br><br>24|`----`<br><br>`time->Sun May 16 07:02:16 2021`<br><br>`type=PROCTITLE msg=audit(1621137736.023:543): proctitle=6765646974002F6574632F7265736F6C762E636F6E66`<br><br>`type=PATH msg=audit(1621137736.023:543): item=1 name="/etc/resolv.conf" inode=160660 dev=103:02 mode=0100644 ouid=0 ogid=0 rdev=00:00 nametype=NORMAL cap_fp=0 cap_fi=0 cap_fe=0 cap_fver=0 cap_frootid=0`<br><br>`type=PATH msg=audit(1621137736.023:543): item=0 name="/etc/" inode=131073 dev=103:02 mode=040755 ouid=0 ogid=0 rdev=00:00 nametype=PARENT cap_fp=0 cap_fi=0 cap_fe=0 cap_fver=0 cap_frootid=0`<br><br>`type=CWD msg=audit(1621137736.023:543): cwd="/home/mial"`<br><br>`type=SYSCALL msg=audit(1621137736.023:543): arch=c000003e syscall=257 success=no exit=-17 a0=ffffff9c a1=55da2dd00770 a2=800c1 a3=1b6 items=2 ppid=78750 pid=78751 auid=1000 uid=0 gid=0 euid=0 suid=0 fsuid=0 egid=0 sgid=0 fsgid=0 tty=pts1 ses=2 comm="pool-gedit" exe="/usr/bin/gedit" key=(null)`<br><br>`----`<br><br>`time->Sun May 16 07:02:16 2021`<br><br>`type=PROCTITLE msg=audit(1621137736.023:544): proctitle=6765646974002F6574632F7265736F6C762E636F6E66`<br><br>`type=PATH msg=audit(1621137736.023:544): item=1 name="/etc/resolv.conf" inode=160660 dev=103:02 mode=0100644 ouid=0 ogid=0 rdev=00:00 nametype=NORMAL cap_fp=0 cap_fi=0 cap_fe=0 cap_fver=0 cap_frootid=0`<br><br>`type=PATH msg=audit(1621137736.023:544): item=0 name="/etc/" inode=131073 dev=103:02 mode=040755 ouid=0 ogid=0 rdev=00:00 nametype=PARENT cap_fp=0 cap_fi=0 cap_fe=0 cap_fver=0 cap_frootid=0`<br><br>`type=CWD msg=audit(1621137736.023:544): cwd="/home/mial"`<br><br>`type=SYSCALL msg=audit(1621137736.023:544): arch=c000003e syscall=257 success=yes exit=11 a0=ffffff9c a1=55da2dd00770 a2=20041 a3=1b6 items=2 ppid=78750 pid=78751 auid=1000 uid=0 gid=0 euid=0 suid=0 fsuid=0 egid=0 sgid=0 fsgid=0 tty=pts1 ses=2 comm="pool-gedit" exe="/usr/bin/gedit" key=(null)`<br><br>`----`<br><br>`time->Sun May 16 07:02:16 2021`<br><br>`type=PROCTITLE msg=audit(1621137736.029:545): proctitle=6765646974002F6574632F7265736F6C762E636F6E66`<br><br>`type=PATH msg=audit(1621137736.029:545): item=4 name="/etc/resolv.conf" inode=163335 dev=103:02 mode=0100644 ouid=0 ogid=0 rdev=00:00 nametype=CREATE cap_fp=0 cap_fi=0 cap_fe=0 cap_fver=0 cap_frootid=0`<br><br>`type=PATH msg=audit(1621137736.029:545): item=3 name="/etc/resolv.conf" inode=160660 dev=103:02 mode=0100644 ouid=0 ogid=0 rdev=00:00 nametype=DELETE cap_fp=0 cap_fi=0 cap_fe=0 cap_fver=0 cap_frootid=0`<br><br>`type=PATH msg=audit(1621137736.029:545): item=2 name="/etc/.goutputstream-VQ4G30" inode=163335 dev=103:02 mode=0100644 ouid=0 ogid=0 rdev=00:00 nametype=DELETE cap_fp=0 cap_fi=0 cap_fe=0 cap_fver=0 cap_frootid=0`<br><br>`type=PATH msg=audit(1621137736.029:545): item=1 name="/etc/" inode=131073 dev=103:02 mode=040755 ouid=0 ogid=0 rdev=00:00 nametype=PARENT cap_fp=0 cap_fi=0 cap_fe=0 cap_fver=0 cap_frootid=0`<br><br>`type=PATH msg=audit(1621137736.029:545): item=0 name="/etc/" inode=131073 dev=103:02 mode=040755 ouid=0 ogid=0 rdev=00:00 nametype=PARENT cap_fp=0 cap_fi=0 cap_fe=0 cap_fver=0 cap_frootid=0`<br><br>`type=CWD msg=audit(1621137736.029:545): cwd="/home/mial"`<br><br>`type=SYSCALL msg=audit(1621137736.029:545): arch=c000003e syscall=82 success=yes exit=0`|
Чтобы узнать, какая программа выполнила действие, смотрите строку «**exe=**».

## Как остановить службу auditd  

Чтобы удалить службу из автозагрузки, выполните команду:

---

|   |   |
|---|---|
|1|`sudo` `systemctl disable auditd.service`|

Если вы попытаетесь остановить службу следующей командой:

|   |   |
|---|---|
|1|`sudo` `systemctl stop auditd.service`|

То вы получите сообщение, что это не удалось, так как операция отклонена:

|   |   |
|---|---|
|1<br><br>2|`Failed to stop auditd.service: Operation refused, unit auditd.service may be requested by dependency only (it is configured to refuse manual start/stop).`<br><br>`See system logs and 'systemctl status auditd.service' for details.`|

Для остановки службы выполните команду:

|   |   |
|---|---|
|1|`sudo` `auditctl --signal TERM`|

## Как удалить все правила отслеживания изменений папок и файлов  

Чтобы удалить сразу все правила, выполните команду:

|   |   |
|---|---|
|1|`sudo` `auditctl -D`|

Возможно удаление отдельных правил (как по отслеживаемому событию, так и по привязанному идентификатору).

## Ошибка «Error opening /var/log/audit/audit.log (Нет такого файла или каталога)»  

Если вы получили ошибку

|   |   |
|---|---|
|1|`Error opening /var/log/audit/audit.log (Нет такого файла или каталога)`|

То она означает, что служба audit не была запущена (вы забыли её запустить, она не запустилась из-за ошибки, либо вы запустили её на переднем плане).

## Примеры настройки auditd  

Чтобы посмотреть все системные вызовы, сделанные определённой программой:

|   |   |
|---|---|
|1|`sudo` `auditctl -a always,``exit` `-S all -F pid=1005`|

Чтобы увидеть файлы, открываемые определённым пользователем:

|   |   |
|---|---|
|1|`sudo` `auditctl -a always,``exit` `-S openat -F auid=510`|

Чтобы увидеть неудачные вызовы openat:

---

|   |   |
|---|---|
|1|`sudo` `auditctl -a always,``exit` `-S openat -F success=0`|

Для слежения за изменениями файла (два способа выражения):

|   |   |
|---|---|
|1<br><br>2|`sudo` `auditctl -w` `/etc/shadow` `-p wa`<br><br>`sudo` `auditctl -a always,``exit` `-F path=``/etc/shadow` `-F perm=wa`|

Для рекурсивного слежения за директорией на предмет изменений (два способа выражения):

|   |   |
|---|---|
|1<br><br>2|`sudo` `auditctl -w` `/etc/` `-p wa`<br><br>`sudo` `auditctl -a always,``exit` `-F` `dir``=``/etc/` `-F perm=wa`|

Чтобы посмотреть, получал ли администратор доступ к файлам пользователя:

|   |   |
|---|---|
|1|`sudo` `auditctl -a always,``exit` `-F` `dir``=``/home/` `-F uid=0 -C auid!=obj_uid`|

## Файлы auditd  

- **/etc/audit/auditd.conf** — конфигурационный файл для демона audit
- **/etc/audit/audit.rules** — правила audit для загрузки во время запуска
- **/etc/audit/rules.d/** — директория, содержащая индивидуальные наборы правил для компиляции в один файл с помощью augenrules
- **/etc/audit/plugins.d/** — директория, содержащая индивидуальные файлы конфигураций плагинов
- **/var/run/auditd.state** — сообщение о внутреннем состоянии

## Документация по auditd  

В данной статье показано, как начать использовать auditd для отслеживания изменений в файле и отслеживанию доступа к файлу.

Возможности auditd не исчерпываются показанными примерами и имеется несколько утилит, с множеством настроек и опций, которые позволяют очень гибко настраивать правила мониторинга происходящего в файловой системе, а также выполнять другие сопутствующие действий.

С помощью **man** вы можете ознакомиться со следующей документацией:

- **auditd.conf**
- **auditd-plugins**
- **ausearch**
- **aureport**
- **auditctl**
- **augenrules**
- **audit.rules**
