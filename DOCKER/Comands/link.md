[Документация](https://docs.docker.com/network/links/)
[Статья](https://dddpaul.github.io/blog/2015/01/08/docker-linking/)
[Статья](https://cisoclub.ru/socat-dlya-pentestinga/)

При создании тестовых окружений из нескольких контейнеров неизбежно возникает задача их взаимного связывания. Набивший оскомину пример: контейнеру с приложением нужен контейнер БД. В нашем же случае, контейнеру с балансером нужны контейнеры с апстримами.

Статья Linking Containers Together полностью раскрывает вопрос линковки контейнеров. Осветим вкратце лишь основные моменты:

- каждый контейнер необходимо как-то назвать с помощью опции --name;
- ссылка на контейнер-зависимость обозначается опцией --link;
- в итоге, внутри зависимого контейнера, инициализируется множество переменных окружения, содержащих параметры контейнера-зависимости, а также в __/etc/hosts__ заносится IP-адрес контейнера-зависимости.

Например, так выглядит последовательный запуск 3-х контейнеров, причем 3-й зависит от первых двух:
__docker run -d --privileged -p 2021:22 -p 8081:80 --name app1 smile/tomcat7__
__docker run -d --privileged -p 2022:22 -p 8082:80 --name app2 smile/tomcat7__
__docker run -d --privileged -p 2020:22 -p 80:80 --name gate --link app1:app1 --link app2:app2 smile/gate__

Для проверки можно использовать вывод docker inspect:

__docker inspect -f "{{ .HostConfig.Links }}" gate__

[/app1:/gate/app1 /app2:/gate/app2]

Опция -d (detach mode) здесь необходима, чтобы контейнеры запускались в фоновом режиме и не захватывали консоль.

Теперь, если зайти в контейнер gate __(ssh -p 2020 root@localhost)__ и посмотреть переменные окружения, то будет ясно, что gate 'видит' exposed-порты и IP-адрес контейнера-зависимости:

root@aba982937531:~# env | grep APP1
APP1_NAME=/gate/app1
APP1_PORT_22_TCP=tcp://172.17.0.28:22
APP1_PORT_80_TCP=tcp://172.17.0.28:80
APP1_PORT_22_TCP_ADDR=172.17.0.28
APP1_PORT_80_TCP_ADDR=172.17.0.28
APP1_PORT_22_TCP_PORT=22
APP1_PORT_80_TCP_PORT=80
APP1_PORT_80_TCP_PROTO=tcp
APP1_PORT_22_TCP_PROTO=tcp
APP1_PORT=tcp://172.17.0.28:22
...

Еще лучше дела обстоят с __/etc/hosts__:

root@aba982937531:~# __grep app1 /etc/hosts__
172.17.0.28	app1

Модификация /etc/hosts, например, дает возможность писать следующие кофиги Nginx:

 ```json
server {
    listen 80 default_server;
    server_name _;

    location /app1 {
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for; #
        proxy_pass http://app1:80/app1;                              # app1 host here
        proxy_redirect http://127.0.0.1:8081/app1 /app1;             #
    }

    location /app2 {
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for; #
        proxy_pass http://app2:80/app2;                              # and app2 host here
        proxy_redirect http://127.0.0.1:8082/app2 /app2;             #
    }
}
```

Таким образом, в первом приближении, встроенная возможность связывания контейнеров в Docker решает наши проблемы.