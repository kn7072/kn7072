В статье разберём **«Единое дерево каталогов»** в Linux и стандарт **«File Hierarchy Standard»** к которому должны стремиться все дистрибутивы Linux.

## Стандарт FHS

Linux дистрибутивы стараются придерживаться стандарта **FHS** (_Filesystem Hierarchy Standard_). Этот стандарт описывает как должна выглядеть структура каталогов. То есть по какому пути система будет искать определенные файлы. Например, программы должны лежать в одном каталоге, а библиотеки для них в другом. И программа будет знать где искать библиотеку для своей работы, если программист создававший её придерживался этого стандарта**.** Вот [ссылка](https://www.pathname.com/fhs/) на этот стандарт. В моей статье написан краткий обзор этого стандарта.

Так как различных дистрибутивов Linux много (про некоторые я писал [здесь](https://sysadminium.ru/selection_linux/#Pro_raznye_distributivy)). И программы создаваемые для **Linux** разрабатываются очень большим числом программистов, то был необходим такой стандарт. Придерживаться его должны программисты пишущие программы для Linux, а также программисты пишущие дистрибутивы Linux.

Также этот стандарт облегчает жизнь пользователям, так как пользователь будет примерно знать где какие файлы находятся, куда установилась программа, где искать конфигурационные файлы для настройки сервера и так далее.

Этот стандарт периодически подвергается изменению. Сейчас структура каталогов по стандарту **FHS** выглядит следующим образом:

- **/** — Корневой каталог. С него всё начинается.
- **/bin** — Здесь лежат основные утилиты, которые могут использовать как обычные пользователи так и системные администраторы. Но эти утилиты необходимы, когда не смонтированы другие файловые системы. В каталоге bin не должно быть подкаталогов. Например, здесь лежат такие утилиты: cat, cp, echo, kill, ln, ls, mkdir, mv, rm, sh, su.
- **/boot** — Этот каталог содержит статические файлы загрузчика. То-есть, всё необходимое для процесса загрузки, за исключением файлов конфигурации, которые не нужны во время загрузки. Здесь хранятся данные, которые используются до того, как ядро начнет выполнять программы пользовательского режима. Это могут быть сохраненные основные загрузочные секторы и карты секторов.
- **/etc** — Содержит файлы конфигурации. Такие файлы используются для настройки работы программ. Обычно файл конфигурации это простой текстовый файл и он не должен быть исполняемым.
- **/etc/opt** — Этот каталог содержит конфигурационные файлы дополнительных программ расположенных в каталоге **/opt**.
- **/home** — Здесь лежат подкаталоги, которые используются как домашние каталоги обычных пользователей. Это файловая система зависит от конкретного хоста, то-есть содержимое будут отличаться на разных хостах. Поэтому ни одна программа не должна полагаться на это расположение.
- **/lib** — Этот каталог содержит библиотеки для программ из каталогов **/bin** и **/sbin**, а также модули ядра. В системах, поддерживающих более одного двоичного формата, для которых требуются отдельные библиотеки, может существовать один или несколько вариантов каталога (**/lib32**, **/lib64**, **/libx32**).
- **/media** — Точки монтирования для съёмных носителей.
- **/mnt** — Точки монтирования для временного монтирования, например сетевых файловых систем (NFS, Samba).
- **/opt** — Дополнительное программное обеспечение. Пакет, который будет установлен сюда, должен располагать свои статические файлы в отдельном подкаталоге **/opt/<пакет>**.
- **/root** — Домашний каталог пользователя root (суперпользователя).
- **/sbin** — Утилиты, используемые системным администратором (доступные только для root пользователя). Они могут понадобится для загрузки, восстановления или починки системы. При загрузке системы каталог **/sbin** используется наравне с **/bin**. В этом каталоге также не должно быть подкаталогов, только бинарные файлы. Здесь могут лежать такие утилиты: shutdown, reboot, mkfs, fsck, swapon, swapoff.
- **/srv** — Данные для сервисов предоставляемых системой. Основная цель заключается в том, чтобы пользователи могли найти местоположение файлов данных для конкретного сервиса (службы).
- **/tmp** — Каталог для временных файлов, которые не сохраняются после перезагрузки. Этот каталог должен быть доступен для программ, которым требуются временные файлы. Программы не должны предполагать, что какие-либо файлы или каталоги здесь сохраняются между вызовами программы.
- **/usr** — Это каталог вторичной иерархия, например **/usr/bin** и **/usr/sbin** — дополнительные программы, а **/usr/lib** — библиотеки для этих программ. Это данные, доступные только для чтения. Предполагается что этот каталог может быть использован для обмена между различными хостами.
- **/var** — Здесь хранятся файлы с изменяемыми данными (логи, базы данных, почтовые файлы).
- **/var/tmp** — Временные файлы, которые должны быть сохранены после перезагрузки.
- **/var/opt** — Изменяемые файлы для программ расположенных в каталоге **/opt**.


## Псевдо-файловые или виртуальное файловые системы

- **/dev** — Сюда монтируется специальная файловая систем — **devfs**. Когда какой-либо драйвер в процессе загрузки или работы обнаруживает обслуживаемое им устройство, он создаёт для этого устройства специальный файл. Если устройство уже не активно, то этот специальный файл удаляется. Специальные файлы не содержат данных, а просто служат точками, через которые приложения могут обратиться к драйверу соответствующего устройства.
- **/proc** — В этот каталог монтируется виртуальная файловая система — **procfs**. Файловая система **procfs** является де-факто стандартным методом Linux для обработки информации о процессах и системе. Таким образом в каталоге будет информация о состоянии ядра и запущенных процессах в системе.
- **/run** — Каталог, в который монтируется виртуальная файловая система — **tmpfs**. Каталог показывает данные, относящиеся к запущенным процессам. Это временное хранилище данных для процессов, служб и других системных компонентов.
- **/sys** — Показывает устройства и драйверы. Файловая система **sysfs** экспортирует в пространство пользователя информацию ядра Linux о присутствующих в системе устройствах и драйверах.

## Практика

Чтобы увидеть структуру каталогов можно воспользоваться утилитой
tree. С помощью опций -d
— можно выводить только каталоги, а с помощью опции
-L 1
— можно вывести только первую часть иерархии не спускаясь ниже.

 tree -d -L 1 /

Если в вашем дистрибутиве не предустановлена эта утилита, то обычно она входит в стандартные репозитории и устанавливается, например так:

apt install tree

Все дистрибутивы Linux придерживаются стандарта, но могут немного отходить от него. Поэтому лучше изучить свой дистрибутив самостоятельно.

Также виртуальные файловые системы помогут изучить вашу систему:

- **/proc** — покажет запущенные процессы;
- **/sys** — покажет информацию о ядре и драйвере (модулях ядра);
- **/dev** — покажет подключенные устройства.

Для начала иcледования тоже можно воспользоваться утилитой tree:

tree -d -L 1 /proc

tree -d -L 1 /sys
tree -d -L 1 /dev

## Рекомендации

Для системных администраторов я бы рекомендовал самописные программы или скрипты класть в каталоги:

- **/usr/local/bin** — если утилита или скрипт предназначена для всех пользователей сервера.
- **/usr/local/sbin** — если утилита или скрипт должна быть доступна только пользователю root.

Если приложение большое, со множеством файлов, то их лучше положить в каталог — **/opt/<имя_программы>**.

Персональные скрипты можно хранить в домашнем каталоге, например **~/bin**. Дополнительно можете этот каталог добавить в переменную **PATH**.