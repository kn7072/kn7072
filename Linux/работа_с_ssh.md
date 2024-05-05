scp example-photo.png remote_linux_username@linux_hostname_or_local_ip:/remote/directory/on/linux/pc

scp username@from_host_ip:/home/ubuntu/myfile /cygdrive/c/Users/Anshul/Desktop

Из PowerShall windows
из windows на lunux - каталог
scp -r 'e:\SELENOID\TEST' sg.chernov@usd-hahinnix.corp.xxx.ru:/home/local/xxx-CORP/sg.chernov/test_selenoid_1/images/selenium


из lunux на windows - каталог
scp -r sg.chernov@usd-hahinnix.corp.xxx.ru:/home/local/xxx-CORP/sg.chernov/test_selenoid_1/images/selenium 'e:\SELENOID\TEST'

scp  sg.chernov@usd-hahinnix.corp.xxx.ru:/home/autotest/images/selenium/android/entrypoint.sh 'e:\SELENOID\TEST'

scp  autotest@test-selenium-builder6.unix.xxx.ru:/home/autotest/images/selenium/android/entrypoint.sh 'e:\SELENOID\TEST'

scp 'e:\SELENOID\TEST\entrypoint.sh' sg.chernov@usd-hahinnix.corp.xxx.ru:/home/local/xxx-CORP/sg.chernov/images/selenium/android
scp 'e:\SELENOID\TEST\entrypoint.sh' autotest@psdr-autotest9.unix.xxx.ru:/home/autotest/images/selenium/android/


scp 'e:\SELENOID\TEST\entrypoint.sh' autotest@psdr-autotest9.unix.xxx.ru:/home/autotest/images/selenium/android/

## ssh config
[https://www.cyberciti.biz/faq/create-ssh-config-file-on-linux-unix/]

## Генерируем ключ
// http://feanor184.ru/linux/kak-sozdat-otkryityiy-zakryityiy-ssh-klyuch-v-linux.html
__ssh-keygen -t rsa__
нам предлагают указать место для хранения нашего ключа. По умолчанию этобудет папка .ssh в вашей домашней директории. Для того, чтобы согласиться с настройками по умолчанию, просто нажимаем «Enter».
Дальше, нас попросят ввести идентификационную фразу. (ВНИМАНИЕ! Это не фраза для соединения с удаленным хостом.) Она нужна для разблокировки закрытого ключа, поэтому она не поможет нам получить доступ к удаленному серверу, даже если на нем хранится наш закрытый ключ. Ввод этой фразы не является обязательным. Чтобы оставить ее пустой, просто можно нажать «Enter».

Теперь наш открытый( публичный ) и закрытый SSH-ключи могут быть сгенерированы. Открываем файловый менеджер и переходим в директорию .ssh. Там должны лежать два файла: __id_rsa и id_rsa.pub__.

__Загружаем файл id_rsa.pub в домашнюю директорию нашего удаленного хоста (под Linux)__. Далее нужно подключиться к нему с помощью SSH и переместить открытый ключ в его целевую директорию с помощью команд:
__cat id_rsa.pub >> ~/.ssh/authorized_keys__
__rm id_rsa.pub__

или с помощью утилиты 
__ssh-copy-id -i ~/.ssh/id_rsa.pub user@host__
котрая создает файл .ssh/authorized_keys на удаленной машине

### Решение возможных проблем
Теперь мы можем подключаться по ключу, но если вдруг что-то не получается, то нужно еще выставить права:
__chmod -u=rwX,go= ~/.ssh__
__chmod -u=rw,go=r ~/.ssh/authorized_keys__

Если это не помогло, смотрим конфигурационный файл SSH( в примере используем редактор nano ):
__sudo nano /etc/ssh/sshd_config__

Нужно проверить, чтобы следующие атрибуты имели корректные значения:

RSAAuthentication yes
PubkeyAuthentication yes 
PasswordAuthentication no

Перезапускаем сервер SSH на удаленном хосте:

__sudo /etc/init.d/ssh reload__

На этом все. Теперь мы можем выполнить авторизацию по ssh-ключу со своим удаленным хостом с помощью команды:

__ssh -i /path-to-private-key username@remote-host-ip-address__

## Аутентификация без пароля
[https://losst.ru/kak-polzovatsya-ssh]
Самый надежный и часто используемый способ аутентификации - с помощью пары ключей RSA. Секретный ключ хранится на компьютере, а публичный используется на сервере для удостоверения пользователя.
Настроить такое поведение очень легко. Сначала создайте ключ командой:

__ssh-keygen -t rsa__
Во время создания ключа нужно будет ответить на несколько вопросов, расположение оставляйте по умолчанию, если хотите подключаться без пароля - поле Passphare тоже оставьте пустым.

Затем отправляем ключ на сервер:
__ssh-copy-id -i ~/.ssh/id_rsa.pub user@host__

## Смотрим неудачные попытки входа SSH

Вот и все. Теперь при попытке подключится к этому серверу пароль запрашиваться не будет, а стазу произойдет подключение. Смотрите подробнее создание открытого ключа для ssh.
Хотите посмотреть были ли попытки неудачного доступа по ssh к вашему серверу и с каких IP адресов? Запросто, все запросы логируются в файл /var/log/secure, отфильтруем только нужные данные командой:

__cat /var/log/secure | grep "Failed password for"__

// https://habr.com/ru/post/435546/
// https://interface31.ru/tech_it/2017/04/ssh-tunneli-na-sluzhbe-sistemnogo-administratora.html
# 3 Туннель SSH (переадресация портов)
В простейшей форме SSH-туннель просто открывает порт в вашей локальной системе, который подключается к другому порту на другом конце туннеля.
__ssh -L локальный_порт:удаленный_адрес:удаленный_порт пользователь@сервер__

__ssh -L 9999:127.0.0.1:80 user@remoteserver__

Разберём параметр -L. Его можно представить как локальную сторону прослушивания. Таким образом, в примере выше порт 9999 прослушивается на стороне localhost и переадресуется через порт 80 на remoteserver. Обратите внимание, что 127.0.0.1 относится к localhost на удалённом сервере!

Поднимемся на ступеньку. В следующем примере порты прослушивания связываются с другими узлами локальной сети.
__ssh  -L 0.0.0.0:9999:127.0.0.1:80 user@remoteserver__

В этих примерах мы подключаемся к порту на веб-сервере, но это может быть прокси-сервер или любая другая служба TCP.


# 4. Обратный SSH-туннель
Здесь настроим прослушивающий порт на удалённом сервере, который будет подключаться обратно к локальному порту на нашем localhost (или другой системе).

__ssh -v -R 0.0.0.0:1999:127.0.0.1:902 192.168.1.100 user@remoteserver__


В этой SSH-сессии устанавливается соединение с порта 1999 на remoteserver к порту 902 на нашем локальном клиенте.