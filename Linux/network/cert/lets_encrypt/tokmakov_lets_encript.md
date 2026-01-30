[источник](https://tokmakov.msk.ru/blog/item/778)

- [ Установка certbot с использованием apt](#link_1)
- [ Синтаксис утилиты certbot](#link_2)
- [ Регистрация в Let's Encrypt](#link_3)
- [ Конфигурация виртуального хоста](#link_4)
- [ Выпуск SSL-сертификата](#link_5)
- [ Автоматическое обновление](#link_6)
- [ Использование плагина webroot](#link_7)
- [ Использование плагина standalone](#link_8)
- [ Использование плагина manual](#link_9)
- [ Конфигурационный файл](#link_10)
- [ Как отозвать сертификат](#link_11)
- [ Справка по certbot](#link_12)
- [ Установка certbot с использованием snap](#link_13)
  - [ Основные команды certbot](#link_14)
  - [ Сертификат для Nginx](#link_15)
  - [ Сертификат для Apache](#link_16)

# Let's Encrypt. Получение и обновление сертификатов

Let's Encrypt — центр сертификации, предоставляющий бесплатные криптографические сертификаты X.509 для шифрования передаваемых через интернет данных HTTPS и других протоколов, используемых серверами в Интернете. При этом, процесс выдачи сертификатов полностью автоматизирован.

Проект Let's Encrypt создан для того, чтобы большая часть интернет-сайтов смогла перейти к шифрованным подключениям (HTTPS). На типичном веб-сервере на базе Linux требуется выполнить две команды, которые настроят HTTPS-шифрование, получат и установят сертификат за несколько секунд.

## Установка certbot с использованием apt <a name="link_1"></a>

Чтобы SSL-сертификат от Let's Encrypt можно было выпустить и установить в конфигурацию веб-сервера, потребуется установить специальную утилиту `certbot`, которая помогает решить две задачи.

1. Получение сертификата — выполнение необходимых шагов аутентификации, чтобы доказать владение доменом, сохранение сертификата в директорию `/etc/letsencrypt/live/` и его регулярное продление.
2. При желании можно установить этот сертификат на веб-сервер — например, Apache или Nginx. Это делается путем изменения файлов конфигурации веб-сервера для использования полученного сертификата.

Вместе с утилитой `certbot` часто используют плагины `nginx` и `apache` — их нужно установить вместе с утилитой `certbot`. Плагины позволяют автоматизировать рутинные операции, но без них можно легко обойтись — мы рассмотрим оба варианта.

Если используется веб-сервер Nginx

```
# apt install certbot python3-certbot-nginx
```

Если используется веб-сервер Apache

```
# apt install certbot python3-certbot-apache
```

Плагины `nginx` и `apache` позволяют автоматизировать весь процесс — аутентификация, получение сертиката, изменение файлов конфигурации веб-сервера, обновление сертификата. Эти два плагина являются одновременно аутентификаторами и установщиками.

Аутентификаторы — это плагины, которые автоматически выполняют необходимые действия, чтобы доказать владение доменом, для которого запрашивается сертификат. Для получения сертификата всегда требуется аутентификатор.

Установщики — это плагины, которые могут автоматически изменять конфигурацию веб-сервера для обслуживания сайта по HTTPS, используя сертификаты, полученные `certbot`. Установщик необходим для того, чтобы `certbot` установил сертификат.

При установке с использованием `apt` будет установлена достаточно старая версия `certbot`. Для получения более новой версии `certbot` можно использовать установку с использованием `snap` — это будет рассмотрено ниже.

## Синтаксис утилиты certbot <a name="link_2"></a>

Указывается подкоманда и опции. Если подкоманда на задана — подразумевается `run`.

```
# certbot [подкоманда] [опции] [-d домен] [-d домен]
```

Часто используемые подкоманды и опции

- `certificates` — список всех сертификатов, полученных с помощью `certbot`
- `renew` — обновить все ранее полученные сертифкаты, которые будут найдены на сервере
- `certonly` — получить сертификат, но не устанавливать (не изменять файлы конфигурации веб-сервера)
- `register` — регистрация в Let's Encrypt для дальнейшего получения и обновления сертификатов
- `--dry-run` — протестировать `renew` или `certonly` без записи сертификатов на диск
- `--nginx` — использовать плагин `nginx` для получения и установки сертификата
- `--apache` — использовать плагин `apache` для получения и установки сертификата
- `--webroot` — использовать плагин `webroot` для получения сертификата
- `--force-renewal` — принудительно обновить сертификат, даже если срок действия не истекает
- `-v` или `--verbose` — подробный вывод, можно повторять, например `-vvv`

## Регистрация в Let's Encrypt <a name="link_3"></a>

Регистрация в Let's Encrypt требуется один раз и выполняется с помощью утилиты `certbot`. Но это необязательно, можно зарегистрироваться при первом выпуске сертификата.

```
# certbot register --email somebody@yandex.ru
Saving debug log to /var/log/letsencrypt/letsencrypt.log

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Please read the Terms of Service at
https://letsencrypt.org/documents/LE-SA-v1.4-April-3-2024.pdf. You must agree in
order to register with the ACME server. Do you agree?
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
(Y)es/(N)o: Y

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Would you be willing, once your first certificate is successfully issued, to
share your email address with the Electronic Frontier Foundation, a founding
partner of the Let's Encrypt project and the non-profit organization that
develops Certbot? We'd like to send you email about our work encrypting the web,
EFF news, campaigns, and ways to support digital freedom.
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
(Y)es/(N)o: N
Account registered.
```

На первом шаге запрашивается согласие с условиями использования сервиса Let's Encrypt, с которыми можно предварительно ознакомиться по предложенному адресу. На втором шаге предлагается выразить согласие на получение новостной рассылки от разработчиков `certbot`.

Регистрация нужна для формирования ключевой пары, которой впоследствии подписываются все запросы, что позволяет удостовериться в подлинности отправителя. Это важно, так как все запросы передаются по открытым каналам и теоретически возможен их перехват и модификация.

Адрес электронной почты, указываемый при регистрации, используется для рассылки уведомлений, например, при неудачной попытке продления сертификата. Поэтому следует указывать рабочий ящик, лучше всего собственный. Один и тот же адрес можно использовать для регистрации на разных хостах, ограничений в этом плане нет.

Учетная информация будет сохранена в каталог `/etc/letsencrypt/accounts`, если содержимое данной директории будет утрачено, то нельзя будет продлить сертификаты и придется получать их заново, создав новый аккаунт. Это следует учитывать, например, при переносе системы на новый сервер.

Если необходимо изменить адрес электронной почты аккаунта, скажем при смене администратора, то это можно сделать командой

```
# certbot register --update-registration --email somebody@mail.ru
```

Следует помнить, что технической возможности восстановления аккаунта нет — в случае его утраты придется заново выпускать все сертификаты.

## Конфигурация виртуального хоста <a name="link_4"></a>

Когда плагин `nginx` или `apache` будет выполнять автоматическую установку SSL-сертификата, ему потребуется найти в конфигурационных файлах Nginx или Apache конкретные строки, чтобы внести необходимые изменения. Нужно проверить директивы `ServerName` и `ServerAlias` (в случае Apache) или `server_name` (в случае Nginx) — что они указывают на домен, для которого планируется получить сертификат.

Если используется веб-сервер Nginx

```
# nano /etc/nginx/sites-available/example.com
```

```
server {
    listen 80;
    server_name example.com www.example.com;
    root /var/www/example.com/html;
    index index.html;
    location / {
        try_files $uri $uri/ =404;
    }
    access_log /var/log/nginx/example-com-access.log;
    error_log /var/log/nginx/example-com-error.log error;
}
```

Если используется веб-сервер Apache

```
# nano /etc/apache2/sites-available/example.com.conf
```

```
<VirtualHost *:80>
    ServerName example.com
    ServerAlias www.example.com
    ServerAdmin webmaster@example.com
    DocumentRoot /var/www/example.com/html
    DirectoryIndex index.html
    ErrorLog ${APACHE_LOG_DIR}/example-com-error.log
    CustomLog ${APACHE_LOG_DIR}/example-com-access.log combined
</VirtualHost>
```

## Выпуск SSL-сертификата <a name="link_5"></a>

Подготовка завершена, можно приступать непосредственно к выпуску и установке SSL-сертификата. Для установки, как уже упоминалось выше, можно использовать плагины, именно они изменят файл конфигурации виртуального хоста и перезапустят веб-сервер.

Если используется веб-сервер Nginx

```
# certbot --nginx --deploy-hook "systemctl reload nginx.service" -d example.com -d www.example.com
```

Если используется веб-сервер Apache

```
# certbot --apache --deploy-hook "systemctl reload apache2.service" -d example.com -d www.example.com
```

Произойдет запуск `certbot` с плагином для Nginx или Apache, опция `-d` необходима, чтобы обозначить доменные имена, для которых нужно получить сертификат.

Поскольку у Let's Encrypt есть лимиты на количество обращений за сертификатами, лучше всего для начала проверить, что сертификаты для целевого домена удастся получить, для этого выполняем команду ниже с флагом `--dry-run`.

```
# certbot certonly --dry-run -d example.com -d www.example.com
Saving debug log to /var/log/letsencrypt/letsencrypt.log
Account registered.
Simulating a certificate request for example.com and www.example.com
The dry run was successful.
```

Если был пропущен шаг регистрации выше, появится сообщение с просьбой указать адрес эл.почты и принять условия обслуживания. Адрес почты лучше указать действующий, так как Let's Encrypt будет отправлять туда письма о проблемах и другие уведомления.

```
# certbot --nginx --deploy-hook "systemctl reload nginx.service" -d example.com -d www.example.com
Saving debug log to /var/log/letsencrypt/letsencrypt.log
Requesting a certificate for example.com and www.example.com

Successfully received certificate.
Certificate is saved at: /etc/letsencrypt/live/example.comfullchain.pem
Key is saved at:         /etc/letsencrypt/live/example.com/privkey.pem
This certificate expires on 2024-08-31.
These files will be updated when the certificate renews.
Certbot has set up a scheduled task to automatically renew this certificate in the background.

Deploying certificate
Successfully deployed certificate for example.com to /etc/nginx/sites-enabled/example.com
Successfully deployed certificate for www.example.com to /etc/nginx/sites-enabled/example.com
Congratulations! You have successfully enabled HTTPS on https://example.com and https://www.example.com
```

Плагин `nginx` (или `apache`) перезапишет файл конфигурации виртуального хоста и перезапустит веб-сервер.

```
# cat /etc/nginx/sites-available/example.com
```

```
server {
    server_name example.com www.example.com;
    root /var/www/example.com/html;
    index index.html;
    location / {
        try_files $uri $uri/ =404;
    }
    access_log /var/log/nginx/example-com-access.log;
    error_log /var/log/nginx/example-com-error.log error;
    listen 443 ssl; # managed by Certbot
    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot
}
server {
    if ($host = www.example.com) {
        return 301 https://$host$request_uri;
    } # managed by Certbot
    if ($host = example.com) {
        return 301 https://$host$request_uri;
    } # managed by Certbot
    listen 80;
    server_name example.com www.example.com;
    return 404; # managed by Certbot
}
```

Срок действия сертификата — 90 дней. Но при установке утилиты `certbot` сразу настраивается автоматическое обновление сертификатов, которые истекают менее чем через 30 дней.

## Автоматическое обновление <a name="link_6"></a>

При установке утилиты `certbot` добавляется таймер Systemd, который настроен на запуск два раза в день. Этот таймер дает сигнал службе `certbot.service`, которая запускает утилиту `certbot` с подкомандой `renew`.

```
$ systemctl cat certbot.timer
```

```
# /lib/systemd/system/certbot.timer
[Unit]
Description=Run certbot twice daily
[Timer]
OnCalendar=*-*-* 00,12:00:00
RandomizedDelaySec=43200
Persistent=true
[Install]
WantedBy=timers.target
```

```
$ systemctl cat certbot.service
```

```
# /lib/systemd/system/certbot.service
[Unit]
Description=Certbot
Documentation=file:///usr/share/doc/python-certbot-doc/html/index.html
Documentation=https://certbot.eff.org/docs
[Service]
Type=oneshot
ExecStart=/usr/bin/certbot --quiet renew
PrivateTmp=true
```

Подкоманда `renew` пытается обновить любые ранее полученные сертификаты, срок действия которых истекает менее чем через 30 дней. Для попытки продления будут использоваться те же плагины и опции, которые использовались во время первоначальной выдачи сертификата, если не будут указаны другие плагины или опции. Для этого при первом получении сертификата создается файл конфигурации.

```
$ cat /etc/letsencrypt/renewal/example.com.conf
```

```
# renew_before_expiry = 30 days
version = 1.21.0
archive_dir = /etc/letsencrypt/archive/example.com
cert = /etc/letsencrypt/live/example.com/cert.pem
privkey = /etc/letsencrypt/live/example.com/privkey.pem
chain = /etc/letsencrypt/live/example.com/chain.pem
fullchain = /etc/letsencrypt/live/example.com/fullchain.pem
# Options used in the renewal process
[renewalparams]
account = 7a589f20732ac7b4bf1d2fccce1a457c
renew_hook = systemctl reload nginx.service
authenticator = nginx
installer = nginx
server = https://acme-v02.api.letsencrypt.org/directory
```

Также есть смысл периодически проверять, как работает механизм автоматического перевыпуска — это можно сделать с помощью опции `--dry-run`, которая не будет обновлять сертификат. Если ошибок при запуске не было — все в порядке.

```
$ certbot renew --dry-run
```

## Использование плагина webroot <a name="link_7"></a>

Плагин `webrooot` является аутентификатором, но не установщиком — сертификат будет получен, но не будет установлен. В этом его отличие от плагинов `nginx` и `apache` — которые являются одновременно аутентификаторами и установщиками. Установить полученный сертификат можно вручную или использовать плагин `nginx` или `apache` как установщик.

В этом случае при установке `certbot` нет необходимости в установке чего-то еще, как мы это делали выше, устанавливая плагин `nginx` или `apache`.

```
# apt install certbot
```

Для использования `webrooot` нужен каталог, в который `certbot` будет записывать свои файлы и который должен быть доступен из сети удостоверяющему серверу согласно протокола ACME. Давайте создадим такой каталог и сделаем его доступным для запросов извне по HTTP-протоколу.

```
# mkdir -p /var/www/letsencrypt/.well-known/acme-challenge
```

Если используется веб-сервер Nginx

```
# nano /etc/nginx/certbot.conf
```

```
location ^~ /.well-known/acme-challenge/ {
    root /var/www/letsencrypt/;
    default_type text/plain;
}
```

```
# nano /etc/nginx/sites-available/example.com
```

```
server {
    listen 80;
    server_name example.com www.example.com;
    root /var/www/example.com/html;
    index index.html;
    # подключаем созданный файл конфигурации
    include /etc/nginx/certbot.conf;
    location / {
        try_files $uri $uri/ =404;
    }
    access_log /var/log/nginx/example-com-access.log;
    error_log /var/log/nginx/example-com-error.log error;
}
```

Если используется веб-сервер Apache

```
# nano /etc/apache2/certbot.conf
```

```
Alias /.well-known/acme-challenge/ /var/www/letsencrypt/.well-known/acme-challenge/
<Directory "/var/www/letsencrypt/.well-known/acme-challenge/">
    ForceType text/plain
</Directory>
```

```
# nano /etc/nginx/sites-available/example.com.conf
```

```
<VirtualHost *:80>
    ServerName example.com
    ServerAlias www.example.com
    ServerAdmin webmaster@example.com
    DocumentRoot /var/www/example.com/html
    DirectoryIndex index.html
    # подключаем созданный файл конфигурации
    include /etc/apache2/certbot.conf
    ErrorLog ${APACHE_LOG_DIR}/example-com-error.log
    CustomLog ${APACHE_LOG_DIR}/example-com-access.log combined
</VirtualHost>
```

Файл конфигурации `certbot.conf` можно будет в дальнейшем использовать для всех прочих доменов, размещенных на веб-сервере. Подготовительные работы завершены, можно получать сертификат, для этого выполняем команду холостого прогона и потом команду получения сертификата.

```
# certbot certonly \
>    --dry-run
>    --webroot
>    --webroot-path /var/www/letsencrypt
>    -d example.com
>    -d www.example.com
```

```
# certbot certonly \
>    --webroot \
>    --webroot-path /var/www/letsencrypt \
>    --deploy-hook "systemctl reload nginx.service" \
>    -d example.com \
>    -d www.example.com
```

Может показаться лишним использование хука `deploy-hook` при первом получении сертификата — потому как нужно сперва изменить файл конфигурации виртуального хоста веб-сервера и только потом дать команду Nginx перечитать файлы конфигурации. Это сделано для того, чтобы хук попал в файл конфигурации, который будет использовать `certbot` при обновлении сертификата. Иначе потом придется редактировать файл конфигурации обновления сертификата, а это делать не рекомендуется.

Проверим, что файлы сертификатов получены и расположены в директории `/etc/letsencrypt/live/example.com` (на самом деле, там только ссылки, но так и должно быть).

```
$ ls -la /etc/letsencrypt/live/example.com
total 12
drwxr-xr-x 2 root root 4096 июн  3 14:49 .
drwx------ 3 root root 4096 июн  2 13:46 ..
lrwxrwxrwx 1 root root   39 июн  2 13:46 cert.pem -> ../../archive/example.com/cert1.pem
lrwxrwxrwx 1 root root   40 июн  2 13:46 chain.pem -> ../../archive/example.com/chain1.pem
lrwxrwxrwx 1 root root   44 июн  2 13:46 fullchain.pem -> ../../archive/example.com/fullchain1.pem
lrwxrwxrwx 1 root root   42 июн  2 13:46 privkey.pem -> ../../archive/example.com/privkey1.pem
-rw-r--r-- 1 root root  692 июн  2 13:46 README
```

После получения сертификата нужно вручную отредактировать файл конфигурации виртуального хоста и выполнить команду, чтобы Nginx перечитал файлы конфигурации.

```
# nano /etc/nginx/sites-available/example.com
```

```
server {
    listen 80;
    server_name example.com www.example.com;
    # редирект с http на https
    return 301 https://example.com$request_uri;
}
server {
    listen 443 ssl;
    server_name example.com www.example.com;
    # редирект с www.example.com на example.com
    if ($host = www.example.com) {
        return 301 https://example.com$request_uri;
    }
    root /var/www/example.com/html;
    index index.html;
    # файл конфигурации для обновления сертификатов
    include /etc/nginx/certbot.conf;
    location / {
        try_files $uri $uri/ =404;
    }

    # файлы сертификатов для работы по https
    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
    access_log /var/log/nginx/example-com-access.log;
    error_log /var/log/nginx/example-com-error.log error;
}
```

```
# systemctl reload nginx.service
```

При обновлении сертификатов файл конфигурации веб-сервера редактировать не нужно — но нужно, чтобы чтобы Nginx перечитал файлы конфигурации и связанные файлы, в том числе новый сертификат. При ручном обновлении сертификата можно добавить хук `deploy-hook` или просто дать команду Nginx перечитать файлы конфигурации.

```
# certbot renew --webroot --webroot-path /var/www/letsencrypt --deploy-hook "systemctl reload nginx.service"
```

Хук `deploy-hook` срабатывает только в том случае, если сертификат был успешно получен или обновлен. Есть еще хук `pre-hook` — срабатывает перед попыткой получения или обновления сертификата и хук `post-hook` — срабатывает после попытки получения или обновления сертификата (даже если попытка была неудачной).

Не забываем о существовании файла конфигурации, директивы из которого будут использованы при запуске подкоманды `renew` без дополнительных аргументов. Этот файл создается при первом получении сертифката и в дальнейшем используется при обновлении. Для автоматического обновления важно, чтобы в файле была директива `renew_hook`, которая предписывает запустить хук `deploy-hook`. _Когда-то хук `deploy-hook` назывался `renew-hook`, но потом был переименован — а в файле осталось старое наименование._

```
$ cat /etc/letsencrypt/renewal/example.com.conf
```

```
# renew_before_expiry = 30 days
version = 1.21.0
archive_dir = /etc/letsencrypt/archive/example.com
cert = /etc/letsencrypt/live/example.com/cert.pem
privkey = /etc/letsencrypt/live/example.com/privkey.pem
chain = /etc/letsencrypt/live/example.com/chain.pem
fullchain = /etc/letsencrypt/live/example.com/fullchain.pem
# Options used in the renewal process
[renewalparams]
account = 07e19228dc4251d026dd2ee5b43bfcd8
renew_hook = systemctl reload nginx.service
authenticator = webroot
webroot_path = /var/www/letsencrypt,
server = https://acme-v02.api.letsencrypt.org/directory
[[webroot_map]]
example.com = /var/www/letsencrypt
www.example.com = /var/www/letsencrypt
```

Разработчики `certbot` настоятельно не рекомендуют редактировать этот файл вручную. Поэтому нужно первом получении сертификата добавить хук `deploy-hook` — чтобы в файл конфигурации была добавлена соответствующая директива. Более новые версии `certbot` поддерживают подкоманду `reconfigure` для измения настроек обновления сертификата.

Автоматическое обновление при использовании `webroot` работает сразу после первого получения сертификата. При установке утилиты `certbot` добавляется таймер Systemd, который настроен на запуск два раза в день — чтобы проверять все сертификаты и перевыпускать те из них, которые истекают менее чем через 30 дней. Этот таймер дает сигнал службе `certbot.service`, которая запускает утилиту `certbot` с подкомандой `renew`. Подкоманда `renew` запускается без дополнительных опций, так что все настройки будут получены из файла конфигурации `/etc/letsencrypt/renewal/example.com.conf`.

## Использование плагина standalone <a name="link_8"></a>

Плагин `standalone` позволяет запустить встроенный в `certbot` веб-сервер, чтобы ответить на http-запросы проверки принадлежности домена. Если уже есть работающий на 80-м порту веб-сервер — то его нужно остановить на время получения сертификата. В этом помогут хуки хук `pre-hook` и `post-hook`.

```
# certbot certonly --standalone -d example.com -d www.example.com
```

Аутентифкатор `standalone` работает как аутентификаторы `nginx` и `apache` — создает необходимые файлы для проверки принадлежности домена без нашего участия. Автоматическое продление сертификата работает как обычно — через таймер `certbot.timer` и службу `certbot.service`.

```
$ cat /etc/letsencrypt/renewal/example.com.conf
```

```
# renew_before_expiry = 30 days
version = 1.21.0
archive_dir = /etc/letsencrypt/archive/example.com
cert = /etc/letsencrypt/live/example.com/cert.pem
privkey = /etc/letsencrypt/live/example.com/privkey.pem
chain = /etc/letsencrypt/live/example.com/chain.pem
fullchain = /etc/letsencrypt/live/example.com/fullchain.pem
# Options used in the renewal process
[renewalparams]
account = 7d09b0595db818aabf5632380d990d7c
authenticator = standalone
server = https://acme-v02.api.letsencrypt.org/directory
```

## Использование плагина manual <a name="link_9"></a>

Это очень похоже на использование плагина `webroot` — нужна директория, содержимое которой доступно по HTTP-протоколу. При использвании `webroot` — в эту директирию записываются файлы с определенным содержимым, чтобы подтвердить права на домен(ы). Для `manual` — мы должны создать файлы самостоятельно.

```
# certbot certonly --manual --deploy-hook "systemctl reload nginx.service" -d example.com -d www.example.com
..........
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Create a file containing just this data:
4EOgeJvzz5sotktiDFLwRG3OiqLA18Px9nAVUFByNjI.T8DgP_x2qmL6H_e1prH3N3yTlkXl6Ovtu5o1sG_jauw
And make it available on your web server at this URL:
http://www.example.com/.well-known/acme-challenge/4EOgeJvzz5sotktiDFLwRG3OiqLA18Px9nAVUFByNjI
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Press Enter to Continue Enter
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Create a file containing just this data:
Bmg5cG9fflELO5glvMdKfqdGg-hUVpwXT6NUf83QNr8.T8DgP_x2qmL6H_e1prH3N3yTlkXl6Ovtu5o1sG_jauw
And make it available on your web server at this URL:
http://example.com/.well-known/acme-challenge/Bmg5cG9fflELO5glvMdKfqdGg-hUVpwXT6NUf83QNr8
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Press Enter to Continue Enter только после создания файлов

Successfully received certificate.
Certificate is saved at: /etc/letsencrypt/live/example.com/fullchain.pem
Key is saved at:         /etc/letsencrypt/live/example.com/privkey.pem
This certificate expires on 2024-09-06.
These files will be updated when the certificate renews.

NEXT STEPS:
This certificate will not be renewed automatically. Autorenewal of --manual certificates requires
the use of an authentication hook script (--manual-auth-hook) but one was not provided. To renew
this certificate, repeat this same certbot command before the certificate's expiry date.
```

Утилита `certbot` сообщает, какие файлы нужно создать и что в них записать. После получения этой информации — нужно остановиться, открыть другой терминал и создать файлы. Потом вернуться в этот терминал и нажать `Enter` — наличие этих файлов будет проверено с помощью HTTP-запросов. После чего будет получены сертификаты — которые нужно прописать в файле конфигурации веб-сервера.

```
# echo '4EOge...' > /var/www/letsencrypt/.well-known/acme-challenge/4EOgeJvzz5sotktiDFLwRG3OiqLA18Px9nAVUFByNjI
# echo 'Bmg5c...' > /var/www/letsencrypt/.well-known/acme-challenge/Bmg5cG9fflELO5glvMdKfqdGg-hUVpwXT6NUf83QNr8
```

В самом конце утилита сообщает, что сертификаты не будут обновляться автоматически, для этого требуется скрипт проверки, который передается с помощью опции `--manual-auth-hook`, который не был предоставлен. Пример такого скрипта можно найти в документации `certbot` на сайте [eff-certbot.readthedocs.io](https://eff-certbot.readthedocs.io/).

## Конфигурационный файл <a name="link_10"></a>

При запуске `certbot` можно использовать опции или записать все насторойки в файла конфигурации `/etc/letsencrypt/cli.ini`. Настройки из файла конфигурации будут использованы при каждом запуске `certbot`.

```
# nano /etc/letsencrypt/cli.ini
```

```
# Because we are using logrotate for greater flexibility,
# disable the internal certbot logrotation.
max-log-backups = 0
# Adjust interactive output regarding automated renewal
preconfigured-renewal = True
```

Директива `max-log-backups` запрещает ротацию логов, потому что этим занимается служба `logrotate` — при установке утилиты `certbot` создается файл конфигурации.

```
$ cat /etc/logrotate.d/certbot
/var/log/letsencrypt/*.log {
    rotate 12
    weekly
    compress
    missingok
}
```

## Как отозвать сертификат <a name="link_11"></a>

Сертификат можно отозвать, указав его имя (как правило, совпадает с именем домена) или путь к файлу сертификата.

```
# certbot revoke --cert-name example.com
# certbot revoke --cert-path /etc/letsencrypt/live/example.com/cert.pem
```

После отзыва `certbot` спросит, нужно ли удалить сертификат локально. Если не удалить, `certbot` попытается обновить отозванные сертификаты при следующем запуске обновления сертификатов. Удалить сертификат локально можно с помощью подкоманды `delete` утилиты `certbot`.

```
# certbot delete --cert-name example.com
```

## Справка по certbot <a name="link_12"></a>

Короткую справку по утилите `certbot` можно получить с помощью опции `--help`, подробное описание — с помощью опции `--help all`.

```
$ certbot --help

certbot [SUBCOMMAND] [options] [-d DOMAIN] [-d DOMAIN] ...

Certbot can obtain and install HTTPS/TLS/SSL certificates.  By default,
it will attempt to use a webserver both for obtaining and installing the
certificate. The most common SUBCOMMANDS and flags are:

obtain, install, and renew certificates:
    (default) run   Obtain & install a certificate in your current webserver
    certonly        Obtain or renew a certificate, but do not install it
    renew           Renew all previously obtained certificates that are near
expiry
    enhance         Add security enhancements to your existing configuration
   -d DOMAINS       Comma-separated list of domains to obtain a certificate for

  (the certbot apache plugin is not installed)
  --standalone      Run a standalone webserver for authentication
  --nginx           Use the Nginx plugin for authentication & installation
  --webroot         Place files in a server's webroot folder for authentication
  --manual          Obtain certificates interactively, or using shell script
                    hooks

   -n               Run non-interactively
  --test-cert       Obtain a test certificate from a staging server
  --dry-run         Test "renew" or "certonly" without saving any certificates
                    to disk

manage certificates:
    certificates    Display information about certificates you have from Certbot
    revoke          Revoke a certificate (supply --cert-name or --cert-path)
    delete          Delete a certificate (supply --cert-name)

manage your account:
    register        Create an ACME account
    unregister      Deactivate an ACME account
    update_account  Update an ACME account
  --agree-tos       Agree to the ACME server's Subscriber Agreement
   -m EMAIL         Email address for important account notifications

More detailed help:

  -h, --help [TOPIC]    print this message, or detailed help on a topic;
                        the available TOPICS are:

   all, automation, commands, paths, security, testing, or any of the
   subcommands or plugins (certonly, renew, install, register, nginx,
   apache, standalone, webroot, etc.)
  -h all                print a detailed help page including all topics
  --version             print the version number
```

## Установка certbot с использованием snap <a name="link_13"></a>

Будет установлена более новая версия `certbot`, кроме того, не нужно отдельно устанавливать плагин `nginx` или `apache`.

```
$ sudo snap install --classic certbot
$ sudo ln -s /snap/bin/certbot /usr/bin/certbot
```

#### Основные команды certbot <a name="link_14"></a>

Регистрация в Let's Encrypt для дальнейшего получения сертификата

```
$ sudo certbot register --email somebody@mail.ru
```

Получение и установка сертификата, если используется веб-сервер Nginx

```
$ sudo certbot --nginx --deploy-hook "systemctl reload nginx.service" -d example.com -d www.example.com
```

Получение и установка сертификата, если используется веб-сервер Apache

```
$ sudo certbot --apache --deploy-hook "systemctl reload apache2.service" -d example.com -d www.example.com
```

Получение сертификата без установки, если используется веб-сервер Nginx

```
$ sudo certbot certonly --nginx --deploy-hook "systemctl reload nginx.service" -d example.com -d www.example.com
```

Получение сертификата без установки, если используется веб-сервер Apache

```
$ sudo certbot certonly --apache --deploy-hook "systemctl reload apache2.service" -d example.com -d www.example.com
```

Проверка автоматического обновления сертификата

```
$ sudo certbot renew --dry-run
```

#### Сертификат для Nginx <a name="link_15"></a>

Получение сертификата с использованием плагина, установка вручную

```
$ sudo certbot certonly --nginx -d example.com -d www.example.com
```

Редактируем файл конфигурации виртуального хоста веб-сервера Nginx

```
$ sudo nano /etc/nginx/sites-available/example.com
```

```
server {
    listen 80;
    server_name example.com www.example.com;
    # редирект с http на https
    return 301 https://example.com$request_uri;
}
server {
    listen 443 ssl;
    server_name example.com www.example.com;
    root /var/www/example.com/html;
    index index.html;
    location / {
        try_files $uri $uri/ =404;
    }
    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;
    access_log /var/log/nginx/example-com-access.log;
    error_log /var/log/nginx/example-com-error.log error;
}

```

Файл конфигурации для обновления сертификата

```
$ cat /etc/letsencrypt/renewal/example.com.conf
```

```
# renew_before_expiry = 30 days
version = 2.11.0
archive_dir = /etc/letsencrypt/archive/example.com
cert = /etc/letsencrypt/live/example.com/cert.pem
privkey = /etc/letsencrypt/live/example.com/privkey.pem
chain = /etc/letsencrypt/live/example.com/chain.pem
fullchain = /etc/letsencrypt/live/example.com/fullchain.pem
# Options used in the renewal process
[renewalparams]
account = 27d21ab2294258ab57924eadb37e814f
authenticator = nginx
installer = nginx
server = https://acme-v02.api.letsencrypt.org/directory
key_type = ecdsa
```

При первом получении сертификата забыл использовать хук `deploy-hook` — нужно это исправить. Иначе после обновления сертификата Nginx продолжит работать со старым. Файл конфигурации обновления сертификата не рекомендуется редактировать вручную, вместо этого предлагается использовать подкоманду `reconfigure`.

```
$ sudo certbot reconfigure --cert-name example.com --deploy-hook "systemctl reload nginx.service" --run-deploy-hook
```

При запуске утилиты `certbot` с опцией `dry-run` или `reconfigure` — хук `deploy-hook` не запускается. Опция `run-deploy-hooks` позволяет изменить это — можно проверить статус службы `nginx.service`, что хук действительно отработал.

```
$ sudo systemctl status nginx.service
● nginx.service - A high performance web server and a reverse proxy server
     Loaded: loaded (/lib/systemd/system/nginx.service; enabled; vendor preset: enabled)
     Active: active (running) since Sun 2024-06-09 10:23:06 MSK; 79min ago
       Docs: man:nginx(8)
    Process: 2073 ExecStartPre=/usr/sbin/nginx -t -q -g daemon on; master_process on; (code=exited, status=0/SUCCESS)
    Process: 2074 ExecStart=/usr/sbin/nginx -g daemon on; master_process on; (code=exited, status=0/SUCCESS)
    Process: 2315 ExecReload=/usr/sbin/nginx -g daemon on; master_process on; -s reload (code=exited, status=0/SUCCESS)
   Main PID: 2075 (nginx)
      Tasks: 2 (limit: 1067)
     Memory: 3.9M
        CPU: 166ms
     CGroup: /system.slice/nginx.service
             ├─2075 "nginx: master process /usr/sbin/nginx -g daemon on; master_process on;"
             └─2316 "nginx: worker process" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" ""

июн 09 10:23:06 example.com systemd[1]: Starting A high performance web server and a reverse proxy server...
июн 09 10:23:06 example.com systemd[1]: Started A high performance web server and a reverse proxy server.
июн 09 11:42:27 example.com systemd[1]: Reloading A high performance web server and a reverse proxy server...
июн 09 11:42:27 example.com systemd[1]: Reloaded A high performance web server and a reverse proxy server.
```

Файл конфигурации для обновления сертификата

```
$ cat /etc/letsencrypt/renewal/example.com.conf
```

```
# renew_before_expiry = 30 days
version = 2.11.0
archive_dir = /etc/letsencrypt/archive/example.com
cert = /etc/letsencrypt/live/example.com/cert.pem
privkey = /etc/letsencrypt/live/example.com/privkey.pem
chain = /etc/letsencrypt/live/example.com/chain.pem
fullchain = /etc/letsencrypt/live/example.com/fullchain.pem
# Options used in the renewal process
[renewalparams]
account = 27d21ab2294258ab57924eadb37e814f
authenticator = nginx
installer = nginx
server = https://acme-v02.api.letsencrypt.org/directory
key_type = ecdsa
renew_hook = systemctl reload nginx.service
```

#### Сертификат для Apache <a name="link_16"></a>

Давайте посмотрим еще, какие изменения в файлах конфигурации Apache выполняет `certbot`, если использовать плагин `apache` как аутентификатор и установщик.

```
$ sudo certbot --apache --deploy-hook "systemctl reload apache2.service" -d example.com -d www.example.com
```

```
$ cat /etc/apache2/sites-available/example.com.conf
```

```
<VirtualHost *:80>
    ServerName example.com
    ServerAlias www.example.com
    ServerAdmin webmaster@example.com
    DocumentRoot /var/www/example.com/html
    DirectoryIndex index.html
    RewriteEngine on
    RewriteCond %{SERVER_NAME} =example.com [OR]
    RewriteCond %{SERVER_NAME} =www.example.com
    RewriteRule ^ https://%{SERVER_NAME}%{REQUEST_URI} [END,NE,R=permanent]
    ErrorLog ${APACHE_LOG_DIR}/example-com-error.log
    CustomLog ${APACHE_LOG_DIR}/example-com-access.log combined
</VirtualHost>
```

```
$ cat /etc/apache2/sites-available/example.com-le-ssl.conf
```

```
<IfModule mod_ssl.c>
    <VirtualHost *:443>
        ServerName example.com
        ServerAlias www.example.com
        ServerAdmin webmaster@example.com
        DocumentRoot /var/www/example.com/html
        DirectoryIndex index.html
        Include /etc/letsencrypt/options-ssl-apache.conf
        SSLCertificateFile /etc/letsencrypt/live/example.com/fullchain.pem
        SSLCertificateKeyFile /etc/letsencrypt/live/example.com/privkey.pem
        ErrorLog ${APACHE_LOG_DIR}/example-com-error.log
        CustomLog ${APACHE_LOG_DIR}/example-com-access.log combined
    </VirtualHost>
</IfModule>
```

Файл конфигурации для обновления сертификата

```
$ cat /etc/letsencrypt/renewal/example.com.conf
```

```
# renew_before_expiry = 30 days
version = 2.11.0
archive_dir = /etc/letsencrypt/archive/example.com
cert = /etc/letsencrypt/live/example.com/cert.pem
privkey = /etc/letsencrypt/live/example.com/privkey.pem
chain = /etc/letsencrypt/live/example.com/chain.pem
fullchain = /etc/letsencrypt/live/example.com/fullchain.pem
# Options used in the renewal process
[renewalparams]
account = 1953385a34edb11a5a1cd6cb8907edbe
renew_hook = systemctl reload apache2.service
authenticator = apache
installer = apache
server = https://acme-v02.api.letsencrypt.org/directory
key_type = ecdsa
```

Один момент для меня остался непонятным. Почему в документации не указывается, что хук `deploy-hook` является обязательным при первом получении сертификата? В противном случае, будет сформирован неправильный файл конфигурации обновления сертификата. И после обновления сертификата — веб-сервер продолжит работать со старым, пока не будет выполнена команда `systemctl reload nginx` или `systemctl reload apache2`.
