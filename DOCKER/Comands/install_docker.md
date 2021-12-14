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

## Что делать если закончилось место в корневом разделе(/)

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





