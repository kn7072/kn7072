# Как создать свой сервис для Linux

Если вы еще никогда не делали свои сервисы, начнем с основ. Systemd оперирует абстрактными единицами (unit), которые бывают разных типов, могут предоставлять различные ресурсы (процессы, сокеты, абстрактные «цели») и требовать других ресурсов для запуска.

Самый распространенный вид ресурса — сервис (service). Файлы с описаниями сервисов и всего прочего лежат в каталоге __/lib/systemd/system/__. Чтобы systemd нашел новый сервис, достаточно положить в этот каталог свой файл. Если этот сервис ранее не существовал, systemd прочитает файл и загрузит его в память. Однако, если вы редактируете файл ранее запущенного сервиса, не забудьте заставить systemd перечитать файлы командой 
__sudo systemctl daemon-reload__

## Создание Сервиса в Systemd
https://darksf.ru/2018/03/30/systemd-sozdanie-servisa-primery/

Создайте service-файл /etc/systemd/system/foo-daemon.service (замените foo-daemon на имя вашего сервиса):
- __$ sudo touch /etc/systemd/system/foo-daemon.service__
- __$ sudo chmod 664 /etc/systemd/system/foo-daemon.service__
Откройте файл foo-daemon.service и пропишите минимальные настройки, которые позволят управлять сервисом с помощью systemctl:
	
[Unit]
Description=Foo
 
[Service]
ExecStart=/usr/sbin/foo-daemon
 
[Install]
WantedBy=multi-user.target

После создания нового service-файла необходимо перезапустить systemd: 
__sudo systemctl daemon-reload__

Теперь вы можете делать start, stop, restart и проверять status сервиса:
__$ sudo systemctl start foo-daemon__
__$ sudo systemctl stop foo-daemon__
__$ sudo systemctl restart foo-daemon__
__$ systemctl status foo-daemon__

Чтобы добавить сервис в автозагрузку, необходимо активировать его:
__$ sudo systemctl enable foo-daemon__

Чтобы проверить логи сервиса, выполните:
__$ journalctl -u foo-daemon__

# Опции Service-файла в Systemd

- Service-файла в systemd обычно состоит из трех секций.
- Общие элементы конфигурации сервиса настраиваются в секциях [Unit] и [Install]
- Параметры конфигурации конкретного сервиса настраиваются в секции [Service].

## Важные Опции Секции [Unit]
Список всех опций секции [Unit]: __$ man systemd.unit__

- __Description__	Краткое описание юнита.
- __Documentation__	Список ссылок на документацию.
- __Before, After__	Порядок запуска юнитов.
- __Requires__ Если этот сервис активируется, перечисленные здесь юниты тоже будут активированы. Если один из перечисленных юнитов останавливается или падает, этот сервис тоже будет остановлен.
- __Wants__	Устанавливает более слабые зависимости, чем Requires. Если один из перечисленных юнитов не может успешно запуститься, это не повлияет на запуск данного сервиса. Это рекомендуемый способ установления зависимостей.
- __Conflicts__	Если установлено что данный сервис конфликтует с другим юнитом, то запуск последнего остановит этот сервис и наоборот.

## Важные Опции Секции [Install]
Список всех опций секции [Install]: __$ man systemd.unit__

- __Alias__	Дополнительные имена сервиса разделенные пробелами. Большинство команд в systemctl, за исключением systemctl enable, могут использовать альтернативные имена сервисов.
- __RequiredBy, WantedBy__	Данный сервис будет запущен при запуске перечисленных сервисов. Для более подробной информации смотрите описание опций Wants и Requires в секции [Unit].
- __Also__	Определяет список юнитов, которые также будут активированы или дезактивированы вместе с данным сервисом при выполнении команд systemctl enable или systemctl disable.

## Важные Опции Секции [Service]
Список всех опций секции [Service]: __$ man systemd.service__

- __Type__	Настраивает тип запуска процесса. Один из:
__simple__ (по умолчанию) — запускает сервис мгновенно. Предполагается, что основной процесс сервиса задан в ExecStart.
__forking__ — считает сервис запущенным после того, как родительский процесс создает процесс-потомка, а сам завершится.
__oneshot__ — аналогичен типу simple, но предполагается, что процесс должен завершиться до того, как systemd начнет отслеживать состояния юнитов (удобно для скриптов, которые выполняют разовую работу и завершаются). Возможно вы также захотите использовать __RemainAfterExit=yes__, чтобы systemd продолжал считать сервис активным и после завершения процесса.
__dbus__ — аналогичен типу simple, но считает сервис запущенным после того, как основной процесс получает имя на шине D-Bus.
__notify__ — аналогичен типу simple, но считает сервис запущенным после того, как он отправляет systemd специальный сигнал.
__idle__ — аналогичен типу simple, но фактический запуск исполняемого файла сервиса откладывается, пока не будут выполнены все задачи.

- __ExecStart__	Команды вместе с аргументами, которые будут выполнены при старте сервиса. Опция __Type=oneshot__ позволяет указывать несколько команд, которые будут выполняться последовательно. Опции __ExecStartPre__ и __ExecStartPost__ могут задавать дополнительные команды, которые будут выполнены до или после __ExecStart__.

- __ExecStop__	Команды, которые будут выполнены для остановки сервиса запущенного с помощью __ExecStart__.

- __ExecReload__ Команды, которые будут выполнены чтобы сообщить сервису о необходимости перечитать конфигурационные файлы.

- __Restart__	Если эта опция активирована, сервис будет перезапущен если процесс прекращен или достигнут timeout, за исключением случая нормальной остановки сервиса с помощью команды __systemctl stop__

- __RemainAfterExit__	Если установлена в значение True, сервис будет считаться запущенным даже если сам процесс завершен. Полезен с __Type=oneshot__. Значение по умолчанию False.

## Примеры Service-файлов в Systemd

[Unit]
Description=The NGINX HTTP and reverse proxy server
After=syslog.target network.target remote-fs.target nss-lookup.target
 
[Service]
Type=forking
PIDFile=/run/nginx.pid
ExecStartPre=/usr/sbin/nginx -t
ExecStart=/usr/sbin/nginx
ExecReload=/bin/kill -s HUP $MAINPID
ExecStop=/bin/kill -s QUIT $MAINPID
PrivateTmp=true
 
[Install]
WantedBy=multi-user.target

---

[Unit]
Description=The Apache HTTP Server
After=network.target remote-fs.target nss-lookup.target
 
[Service]
Type=notify
EnvironmentFile=/etc/sysconfig/httpd
ExecStart=/usr/sbin/httpd $OPTIONS -DFOREGROUND
ExecReload=/usr/sbin/httpd $OPTIONS -k graceful
ExecStop=/bin/kill -WINCH ${MAINPID}
KillSignal=SIGCONT
PrivateTmp=true
 
[Install]
WantedBy=multi-user.target

---

[Unit]
Description=Redis persistent key-value database
After=network.target
 
[Service]
ExecStart=/usr/bin/redis-server /etc/redis.conf --daemonize no
ExecStop=/usr/bin/redis-shutdown
User=redis
Group=redis
 
[Install]
WantedBy=multi-user.target

---

# Документация
https://www.freedesktop.org/software/systemd/man/systemd.service.html
https://www.freedesktop.org/software/systemd/man/systemd.unit.html