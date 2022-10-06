docker version
docker ps -a
docker images
docker run hello-world -создает и запускает контейнер
docker run --name myConrainer hello-world -создание контейнера с именем myConrainer
docker rm container_id -удалить контейнер
docker run -it busybox -подключаемся к процессу pid 1
    hostname -i        -ip контейнера

docker container prune -удалить все остановленные контейнеры

docker run nginx
docker run -d nginx   -запуск контейнера в фоновом режиме

docker container inspect container_id
docker container inspect container_id | grep IPAddress

docker stop container_id
docker exec -it container_id bash -запуск bash в запущенном контейнере

docker run -d -p 8080:80 nginx -запуск конейнер с пробросом порта 8080(локальной машины) на 80(порт внутри образа)

docker run -v путь_локального_каталога(host машины ):путь_в_контейнере nginx

форматирование команды(для улучшения читаемости)
docker run \
-d \
-p 8080:80 \
nginx


docker build .  -предполагается, что в текущей директории находится файл c имеем Dockerfile
docker build . -t my-image:1.0.0 создается образ с именем my-image и тегом 1.0.0