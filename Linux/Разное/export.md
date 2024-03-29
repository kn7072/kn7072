# Команда export - экспорт переменных и функций дочерним процессам в Linux.
https://white55.ru/export.html

export - это одна из встроенных команд оболочки пользователя bash, и предназначена для экспорта переменных и функций текущего процесса в дочерний процесс. На практике, команда export применяется в качестве основного средства для определения настроек конкретных приложений. По умолчанию, в операционных системах семейства Linux, переменные, созданные в среде родительского процесса не передаются автоматически дочернему. Чтобы переменная, созданная процессом A, была доступна запущенному им процессу B, необходимо перед запуском дочернего процесса B выполнить экспорт данной переменной с помощью команды export. Так, например, родительский процесс может определить путь к рабочему каталогу какой-либо программы, создав переменную и выполнив ее экспорт перед запуском.

В Linux, все процессы, кроме процесса init могут быть как дочерними, так и родительскими. Процесс init является родительским процессом для всех остальных, запускаемых процессов, имеет идентификатор PID равный 1 и используется для запуска всех прочих процессов в ходе загрузки системы и регистрации пользователей. Любой другой процесс всегда имеет родительский процесс, и может иметь дочерний.

Для получения идентификатора текущего процесса командной оболочки можно воспользоваться командой:

__echo $$__

в результате отобразится следующая информация:
6272 - идентификатор процесса ( PID )

Если запустить новую командную оболочку, например bash из текущей, командой
/bin/bash
и снова выполнить команду

__echo $$__
то отобразится идентификатор текущего процесса в виде другого числа, например 7224

Команда ps позволяет выводить информацию о связанных родительских и дочерних процессах с использованием параметра --ppid:

__ps --ppid 6272__ - отобразить список процессов, для которых родительским является процесс, PID которого равен 6272:

PID     TTY     TIME        CMD
7224    pts/0    00:00:00     bash

Если же выполнить команду, для отображения списка процессов, для которых родительским является процесс init ( PID=1), то мы получим список всех автоматически стартовавших на данный момент времени, процессов:

__ps --ppid 1__

PID  TTY  TIME  	CMD
417  ?	00:00:00	udevd
1655 ?	00:00:00	dhclient
1705 ?	00:00:00	auditd
1731 ?	00:00:00	rsyslogd
1774 ?	00:00:00	rpcbind
.
.

В данном списке не будет процессов, порожденных дочерними процессами процесса init. Для получения полного списка процессов в соответствии с их иерархией можно воспользоваться параметром -H :

__ps –e -H__ - отобразить дерево ( -H )всех процессов ( -e ) на данный момент времени.

В ходе загрузки и инициализации системы, процессы могут создавать некоторые переменные, значения которых могут использоваться другими процессами, как например, переменная PATH, описывающая пути поиска исполняемых файлов. Кроме того, некоторые процессы могут изменять набор существующих переменных, экспортируя ( передавая ) их, при необходимости, дочерним процессам.

Ниже приведен простой пример экспорта переменных из текущей командной оболочки в дочернюю:
__y=yandex.ru__ - установить значение переменной y, содержащее строку “yandex.ru”
__x=google.com__ - установить значение переменной x, содержащее строку “google.com”

__export x y__ - выполнить экспорт переменных x и y

__bash__ - запустить новый экземпляр командной оболочки bash

__echo $x $y__ - отобразить значение переменных x и y

google.com yandex.ru - результат выполнения команды, т.е. значения переменных x и y созданных родительским процессом.

Если выполнить запуск нового экземпляра командной оболочки bash, то в нем также будут доступны значения экспортируемых переменных x и y. И так далее – все процессы нижнего уровня иерархии могут использовать значения экспортированных переменных.

Команда export позволяет просматривать, удалять или добавлять элементы списка экспортируемых переменных.
__export –p__ - вывести список всех экспортируемых переменных. То же самое выполняется, если не задан никакой ключ.

__export –n x__ - удаление заданной переменной x из списка экспорта.

__export –f__ - экспорт переменной в качестве функции.

__Примеры использования:__

-Создание и экспорт функции testf:

y=yandex.ru - создание переменной y, принимающей строковое значение yandex.ru.
testf() { echo ping $y; } - создание функции testf, использующей переменную y.
testf - выполнение функции testf, использующей переменную y в текущей командной оболочке.
ping yandex.ru - результат выполнения функции testf.

export -f testf - экспорт функции testf.
export y - экспорт переменной y, используемой в функции testf.
bash - запуск дочерней оболочки bash.
testf - выполнение функции testf.
ping yandex.ru - результат.

Обычно, определение значений и экспорт переменных выполняется одной командой:
__export y=yandex.ru__ - создание и экспорт переменной y, принимающей строковое значение yandex.ru.

-Изменение переменной PATH
Наиболее широко команда export применяется для объявления и модификации переменной оболочки PATH:
__export PATH=$PATH:/home/localusr/bin__ - добавить к существующему пути поиска исполняемых файлов, определяеммому переменной PATH каталог /home/localusr/bin.

-Удаление экспортируемой переменной .
__export –n y__ - удаление из списка экспорта переменной y.
Для получения справочной информации по использованию команды export , используйте:
__man export__

Общие настройки оболочки для всех пользователей определяются содержимым файла /etc/profile. Обычно в нем определяется значение переменной PATH задающей пути поиска исполняемых файлов. В системах с несколькими оболочками, настройки для bash определяются содержимым файла /etc/bashrc. Для конкретных пользователей настройки определяются содержимым файлов в домашнем каталоге:

~/.bash_profile- индивидуальные пользовательские настройки среды окружения. В этом файле пользователи могут добавить дополнительные конфигурационные параметры, либо изменить настройки, заданные по умолчанию, например свое значение переменной PATH.

~/.bash_login - настройки, активируемые при входе в систему.

~/.profile - конфигурационные настройки оболочки данного пользователя.

~/.bashrc - конфигурационные настройки оболочки bash данного пользователя.

~/.bash_logout - команды, выполняемые при выходе из системы.