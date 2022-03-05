# Автозапуск конетейнера selenoid_ui

## Создаем и настраиваем скрипт

Для работы службы необходим скрипт run_selenoid_ui.bash
Создадим и настроим скрипт, для этого:

1. Создаем каталог для этого выполняем
    cd ~ && mkdir selenoid_service && cd selenoid_service
2. На этом этапе мы находимся в каталоге selenoid_service, создадим файл скрипта
    vim run_selenoid_ui.bash

    далее добавляем код

container_name=selenoid-ui
delay=60
while true; do
    if [ "$( docker container inspect -f '{{.State.Status}}' $container_name )" == "running" ]; then
        echo "Container $container_name is running."
    else
        echo "Container $container_name is not running."
        docker run -d --rm --name selenoid-ui --link selenoid -p 8080:8080 aerokube/selenoid-ui --selenoid-uri http://selenoid:4444
    fi
    sleep $delay
done
3. Выставляем права
    chmod 744 run_selenoid_ui.bash

## Создаем Unit(service) selenoid-ui

Для этогo:

1. переходм в каталог /lib/systemd/system
2. создаем файл(создать файл можно разными способами в примере используется vim)
sudo vim selenoid-ui.service (важно открыть файл с правами root, т.e через sudo иначе редактирование файла будет не возможно)
3. добавляем в файл следующий код

[Unit]
Description=selenoid_ui
After=docker.service
Wants=network-online.target docker.socket
Requires=docker.socket

[Service]
Restart=always
ExecStart=/bin/bash /home/autotest/selenoid_service/run_selenoid_ui.bash
ExecStop=/usr/bin/docker container stop -t 5 selenoid_ui

[Install]
WantedBy=multi-user.target
4. Обновим даынные по службам(просим перечитать файлы конфигурация)
    sudo systemctl daemon-reload

## Управление службой

- Запустить службу
    sudo systemctl start selenoid_ui.service или sudo systemctl start selenoid_ui
    чтобы добавить службу в автозагрузку выполним
    sudo systemctl enable selenoid_ui.service (больше не нужно запускать - будет запускаться автоматически при старте системы)

- Проверить статус
    sudo systemctl status selenoid_ui.service

- Остановить службу
    sudo systemctl stop selenoid_ui
