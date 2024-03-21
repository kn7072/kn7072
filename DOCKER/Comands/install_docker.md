# Установка Docker и настройка окружения

## Установка Docker(Install Docker Engine on CentOS)

[Ссылка на документацию](https://docs.docker.com/engine/install/centos/)

1. Выполнить команду:

    ```bash
    sudo yum install docker-ce docker-ce-cli containerd.io
    ```

2. Запуск Docker.

    ```bash
    sudo systemctl start docker
    ```

3. Проверим, что установили правильно.

    ```bash
    sudo docker run hello-world
    ```

4. Добавляем пользователя в группу docker.

    ```bash
    sudo usermod -aG docker ${USER}
    su - ${USER}
    ```

## Убедимся, что процессор поддерживает аппаратное ускорение виртуализации

Выполняем одну из команд.

```bash
    lsmod | grep '^kvm'
```

или

```bash
    egrep -c '(vmx|svm)' /proc/cpuinfo
```

Если в результате будет возвращено 0 - значит ваш процессор не поддерживает аппаратной виртуализации, если 1 или больше - то вы можете использовать KVM на своей машине.
__В биосе необходимо включить виртуализацию.__

## Как заливать образы в репозиторий

[Ссылка на новость](https://n.xxx.ru/news/c167d8af-2721-4d0f-8dba-ec47e6a3121d)
[Ссылка на новость](https://online.xxx.ru/news/28b5695b-d402-4020-a170-87c87c363c42)
Чтобы посмотреть доступные образы необходимо авторизоваться(доменный логин/пароль) в https://dev-image-store.xxx.ru/harbor
(https://dev-image-store.xxx.ru/harbor/projects/641355/repositories)

Образы android емуляторов находятся в репозитории dev-image-store.xxx.ru/xxx-testing/android

- Загрузить образ на локальную машину
    docker pull dev-image-store.xxx.ru/xxx-testing/android:10.0
- Заливаем образ с локальной машины в репозиторий
    1. Авторизуемся
        docker login --username USER --password TOKEN https://dev-image-store.xxx.ru
        где USER - доменный логин, TOKEN - CLI secret(из User Profile https://dev-image-store.xxx.ru/harbor)
    2. Сохнаряем образ на сервере
        docker push dev-image-store.xxx.ru/xxx-testing/android:10.0
        ВАЖНО, чтобы локальный образ(образ созданный на локальной машине) имел вточности такое название(разумется тег будет меняться),
        так как это адрес удаленного репозитория.
    3. Что делать если создали образ, но имя не соответствует стандарту?
        предположим у нас есть образ selenoid/android:10.0, а нам нужен dev-image-store.xxx.ru/xxx-testing/android:10.0
        выполним команду для изменения имени
        docker tag selenoid/android:10.0 dev-image-store.xxx.ru/xxx-testing/android:10.0
        после этого можно переходить к пункту 2

## Что делать если закончилось место в корневом разделе(/)

Чтобы не заниматься подобными настройками, рекомендуется указать желаемый размер корневого раздела 150G, за счет уменьшения home раздела(в поручении админам)

1. Останавливаем демон docker.

    ```bash
    sudo systemctl stop docker
    ```

2. Создаем конфиг демона.

    - Создаем файл(если не создан) /etc/docker/daemon.json
    - добавляем ключ "data-root": "/new/data/root/path"
    где "/new/data/root/path" новый путь для хранения образов и т.д
    должно получиться примерно так:

    {
        "data-root": "/new/data/root/path"
    }

3. Переносим данные в новый каталог.

    ```bash
    sudo cp -r /var/lib/docker /new/data/root/path
    ```

4. Запускаем демон docker.

```bash
    sudo systemctl start docker
```





