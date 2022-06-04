scp example-photo.png remote_linux_username@linux_hostname_or_local_ip:/remote/directory/on/linux/pc

scp username@from_host_ip:/home/ubuntu/myfile /cygdrive/c/Users/Anshul/Desktop

Из PowerShall windows
из windows на lunux - каталог
scp -r 'e:\SELENOID\TEST' sg.chernov@usd-hahinnix.corp.tensor.ru:/home/local/TENSOR-CORP/sg.chernov/test_selenoid_1/images/selenium


из lunux на windows - каталог
scp -r sg.chernov@usd-hahinnix.corp.tensor.ru:/home/local/TENSOR-CORP/sg.chernov/test_selenoid_1/images/selenium 'e:\SELENOID\TEST'

scp  sg.chernov@usd-hahinnix.corp.tensor.ru:/home/autotest/images/selenium/android/entrypoint.sh 'e:\SELENOID\TEST'

scp  autotest@test-selenium-builder6.unix.tensor.ru:/home/autotest/images/selenium/android/entrypoint.sh 'e:\SELENOID\TEST'

scp 'e:\SELENOID\TEST\entrypoint.sh' sg.chernov@usd-hahinnix.corp.tensor.ru:/home/local/TENSOR-CORP/sg.chernov/images/selenium/android
scp 'e:\SELENOID\TEST\entrypoint.sh' autotest@psdr-autotest9.unix.tensor.ru:/home/autotest/images/selenium/android/


scp 'e:\SELENOID\TEST\entrypoint.sh' autotest@psdr-autotest9.unix.tensor.ru:/home/autotest/images/selenium/android/

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