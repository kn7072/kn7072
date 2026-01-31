[источник](https://tokmakov.msk.ru/blog/item/484)

- [ Создание пользователя](#link_1)
- [ Создание каталога](#link_2)
- [ Конфигурация ssh-сервера](#link_3)
- [ Тестирование конфигурации](#link_4)
- [ Основные команды SFTP](#link_5)

# Настройка SFTP-сервера в Ubuntu 18.04 LTS

SFTP доступен по умолчанию без дополнительной настройки на всех серверах, имеющих доступ по SSH. Как следует из названия протокола, это безопасный способ передачи файлов на сервер с использованием зашифрованного SSH-соединения. В стандартной конфигурации сервер SSH предоставляет доступ к передаче файлов и к оболочке терминала всем системным пользователям с учетной записью.

Это не очень удобно, иногда нужно предоставить пользователю доступ по SFTP для передачи файлов, но запретить доступ к терминалу. Для начала добавим такого пользователя, потом ограничим его права и создадим каталог, куда это пользователь сможет загружать файлы.

## Создание пользователя <a name="link_1"></a>

Итак, создаем нового пользователя, основную группу и задаем пароль:

```
$ sudo groupadd sftp-group # создаем группу sftp-group
$ sudo useradd --no-create-home --gid sftp-group sftp-user # создаем пользователя
$ sudo passwd sftp-user # задаем пароль для пользователя sftp-user
```

## Создание каталога <a name="link_2"></a>

Чтобы ограничить доступ пользователя к SFTP одним каталогом, сначала нужно убедиться, что каталог соответствует требованиям. Сам каталог и все каталоги над ним в дереве файловой системы должны принадлежать `root`, а другие пользователи не должны иметь права на запись в них. Следовательно, невозможно просто предоставить ограниченный доступ к домашнему каталогу пользователя, поскольку домашние каталоги принадлежат пользователям, а не `root`.

В качестве целевого каталога загрузки будем использовать `/srv/sftp/sftp-user`. Каталог `/srv/sftp` будет принадлежать пользователю `root` и заблокирован для других пользователей. Подкаталог `/srv/sftp/sftp-user` будет принадлежать пользователю `sftp-user`, так что он сможет загружать в него файлы.

```
$ sudo mkdir /srv/sftp
$ sudo chown root:root /srv/sftp
$ sudo chmod 755 /srv/sftp
```

```
$ sudo mkdir /srv/sftp/sftp-user
$ sudo chown sftp-user:sftp-group /srv/sftp/sftp-user
```

## Конфигурация ssh-сервера <a name="link_3"></a>

На этом этапе нужно изменить конфигурацию ssh-сервера и заблокировать пользователю `sftp-user` доступ к терминалу, но разрешить доступ к передаче файлов. Открываем на редактирование файл конфигурации ssh-сервера и дописываем в конец

```
$ sudo nano /etc/ssh/sshd_config
```

```
# использовать встроенный sftp-сервер
Subsystem    sftp    internal-sftp

# только для пользователей группы sftp-group
Match Group sftp-group
    # только работа с файлами, запрет shell
    ForceCommand internal-sftp
    # разрешить аутентификацию по паролю
    PasswordAuthentication yes
    # разрешить доступ только к /srv/sftp
    ChrootDirectory /srv/sftp
    # запретить все, что не нужно для работы
    PermitTunnel no
    AllowAgentForwarding no
    AllowTcpForwarding no
    X11Forwarding no
```

```
$ sudo systemctl restart sshd.service
```

С функциональной точки зрения `sftp-server` и `internal-sftp` практически идентичны. Они построены из одного и того же исходного кода и реализуют SFTP-сервер. `Sftp-server` это отдельный бинарный файл, а `internal-sftp` это просто ключевое слово конфигурации. При указании `internal-sftp` будет использован встроенный SFTP-сервер, вместо запуска внешнего SFTP-сервера. В настоящее время `sftp-server` является избыточным и сохраняется для обратной совместимости.

```
#Subsystem    sftp    /usr/lib/openssh/sftp-server
Subsystem    sftp    internal-sftp
```

## Тестирование конфигурации <a name="link_4"></a>

Пользователь `sftp-user` не может подключиться по ssh и получить доступ к терминалу:

```
$ ssh sftp-user@192.168.110.9
sftp-user@192.168.110.9's password: пароль
This service allows sftp connections only.
Connection to 192.168.110.9 closed.
```

Но пользователь `sftp-user` может использовать SFTP для передачи файлов:

```
$ sftp sftp-user@192.168.110.9
sftp-user@192.168.110.9's password: пароль
Connected to 192.168.110.9.
> pwd
Remote working directory: /
> ls
sftp-user
```

## Основные команды SFTP <a name="link_5"></a>

Оказавшись в командной строке `sftp` можно получить список доступных команд с помощью команды `help`

```
> help
Available commands:
bye                                Quit sftp
cd path                            Change remote directory to 'path'
chgrp grp path                     Change group of file 'path' to 'grp'
chmod mode path                    Change permissions of file 'path' to 'mode'
chown own path                     Change owner of file 'path' to 'own'
df [-hi] [path]                    Display statistics for current directory or
                                   filesystem containing 'path'
exit                               Quit sftp
get [-afPpRr] remote [local]       Download file
reget [-fPpRr] remote [local]      Resume download file
reput [-fPpRr] [local] remote      Resume upload file
help                               Display this help text
lcd path                           Change local directory to 'path'
lls [ls-options [path]]            Display local directory listing
lmkdir path                        Create local directory
ln [-s] oldpath newpath            Link remote file (-s for symlink)
lpwd                               Print local working directory
ls [-1afhlnrSt] [path]             Display remote directory listing
lumask umask                       Set local umask to 'umask'
mkdir path                         Create remote directory
progress                           Toggle display of progress meter
put [-afPpRr] local [remote]       Upload file
pwd                                Display remote working directory
quit                               Quit sftp
rename oldpath newpath             Rename remote file
rm path                            Delete remote file
rmdir path                         Remove remote directory
symlink oldpath newpath            Symlink remote file
version                            Show SFTP version
!command                           Execute 'command' in local shell
!                                  Escape to local shell
?                                  Synonym for help
```

Текущий рабочий каталог:

```
> pwd # удаленный рабочий каталог
> lpwd # локальный рабочий каталог
```

Изменить рабочую директорию:

```
> cd uploads # сменить директорию на удаленной системе
> lcd uploads # сменить директорию на локальной системе
```

Список файлов и директорий:

```
> ls # список на удаленной системе
> lls # список на локальной системе
```

Загрузить на удаленную систему файл или директорию:

```
> put image.jpg # загрузить файл
> put -r images/ # загрузить директорию
```

Скачать с удаленной системы файл или директорию:

```
> get image.jpg # скачать файл
> get -r images/ # скачать директорию
```

Создать директорию:

```
> mkdir images # создать директорию на удаленной системе
> lmkdir images # создать директорию на локальной системе
```

Удалить директорию:

```
> rmdir images # удалить директорию на удаленной системе
> !rmdir images # удалить директорию на локальной системе
```

Выполнить произвольную команду на локальной системе:

```
> !команда
```

Выполнить несколько команд на локальной системе:

```
> ! # временно выходим из командной строки sftp
$ команда # выполняем команду в shell (bash)
$ команда # выполняем команду в shell (bash)
$ exit # возвращаемся к командной строке sftp
>
```

Завершить сеанс:

```
> exit # или quit или bye
```
