# PS

[ссылка loss](https://losst.ru/komanda-ps-v-linux)

## Что такое процесс?

Чтобы понять что отображает команда ps сначала надо разобратся что такое процесс. Процесс Linux - это экземпляр программы, запущенный в памяти. Все процессы можно разделить на обычные и фоновые. Более подробно об этом написано в статье управление процессами Linux. Linux - это многопользовательская система, каждый пользователь может запускать одни и те же программы, и даже один пользователь может захотеть запустить несколько экземпляров одной программы, поэтому ядру нужно как-то идентифицировать такие однотипные процессы. Для этого каждому процессу присваивается PID (Proccess Identificator).

Каждый из процессов может находиться в одном из таких состояний:

- Запуск - процесс либо уже работает, либо готов к работе и ждет, когда ему будет дано процессорное время;
- Ожидание - процессы в этом состоянии ожидают какого-либо события или освобождения системного ресурса. Ядро делит такие процессы на два типа - те, которые ожидают освобождения аппаратных средств и приостановление с помощью сигнала;
- Остановлено - обычно, в этом состоянии находятся процессы, которые были остановлены с помощью сигнала;
- Зомби - это мертвые процессы, они были остановлены и больше не выполняются, но для них есть запись в таблице процессов, возможно, из-за того, что у процесса остались дочерние процессы.

## Команда ps в Linux

Сначала рассмотрим общий синтаксис команды, здесь все очень просто:

__$ ps опции__

__$ ps опции | grep параметр__

Во втором варианте мы используем утилиту grep для того, чтобы отобрать нужные нам процессы по определенному критерию. Теперь рассмотрим опции утилиты. Они делятся на два типа - те, которые идут с дефисом Unix и те, которые используются без дефиса - BSD. Лучше пользоваться только опциями Unix, но мы рассмотрим и одни и другие. Заметьте, что при использовании опций BSD, вывод утилиты будет организован в BSD стиле.

    -A, -e, (a) - выбрать все процессы;
    -a - выбрать все процессы, кроме фоновых;
    -d, (g) - выбрать все процессы, даже фоновые, кроме процессов сессий;
    -N - выбрать все процессы кроме указанных;
    -С - выбирать процессы по имени команды;
    -G - выбрать процессы по ID группы;
    -p, (p) - выбрать процессы PID;
    --ppid - выбрать процессы по PID родительского процесса;
    -s - выбрать процессы по ID сессии;
    -t, (t) - выбрать процессы по tty;
    -u, (U) - выбрать процессы пользователя.

Опции форматирования:

    -с - отображать информацию планировщика;
    -f - вывести максимум доступных данных, например, количество потоков;
    -F - аналогично -f, только выводит ещё больше данных;
    -l - длинный формат вывода;
    -j, (j) - вывести процессы в стиле Jobs, минимум информации;
    -M, (Z) - добавить информацию о безопасности;
    -o, (o) - позволяет определить свой формат вывода;
    --sort, (k) - выполнять сортировку по указанной колонке;
    -L, (H)- отображать потоки процессов в колонках LWP и NLWP;
    -m, (m) - вывести потоки после процесса;
    -V, (V) - вывести информацию о версии;
    -H - отображать дерево процессов;

## Примеры

__ps__ - Чтобы просто посмотреть процессы в текущей оболочке.
__ps -A__ Все процессы, кроме лидеров групп, в том же режиме отображения
__ps -d__ Все процессы, включая фоновые и лидеры групп
__ps -f__ Чтобы вывести больше информации о процессах используйте опцию -f
При использовании опции -f команда выдает такие колонки:

    UID - пользователь, от имени которого запущен процесс;
    PID - идентификатор процесса;
    PPID - идентификатор родительского процесса;
    C - процент времени CPU, используемого процессом;
    STIME - время запуска процесса;
    TTY - терминал, из которого запущен процесс;
    TIME - общее время процессора, затраченное на выполнение процессора;
    CMD - команда запуска процессора;
    LWP - показывает потоки процессора;
    PRI - приоритет процесса.
__ps -Af__ вывести подробную информацию обо всех процессах
__ps -Fe__ Больше информации можно получить, использовав опцию -F
Эта опция добавляет такие колонки:

    SZ - это размер процесса в памяти;
    RSS - реальный размер процесса в памяти;
    PSR - ядро процессора, на котором выполняется процесс.

__ps -l__ Если вы хотите получить еще больше информации, используйте вместо -f опцию -l
Эта опция добавляет отображение таких колонок:

    F - флаги, ассоциированные с этим процессом;
    S - состояние процесса;
    PRI - приоритет процесса в планировщике ядра Linux;
    NI - рекомендованный приоритет процесса, можно менять;
    ADDR - адрес процесса в памяти;
    WCHAN - название функции ядра, из-за которой процесс находится в режиме ожидания.
__ps -fu root__ Дальше мы можем отобрать все процессы, запущенные от имени определенного пользователя
__ps -fHu root__ С помощью опции -H можно отобразить дерево процессов
__ps -fp 1__ информация только об определенном процессе, то вы можете использовать опцию -p и указать PID процесса
__ps -fp 1,2,3__ Через запятую можно указать несколько PID
__ps -fC chrome__ Опция -С позволяет фильтровать процессы по имени, например, выберем только процессы chrome
__ps -fL__ Дальше можно использовать опцию -L чтобы отобразить информацию о процессах
__ps -o pid,comm__ с помощью опции -o можно настроить форматирование вывода, например, вы можете вывести только pid процесса и команду
Вы можете выбрать такие колонки для отображения: __pcpu, pmem, args, comm, cputime, pid, gid, lwp, rss, start, user, vsize, priority__. Для удобства просмотра можно отсортировать вывод программы по нужной колонке, 
например, просмотр процессов, которые используют больше всего памяти __ps -Fe --sort rss__ 
или по проценту загрузки cpu __ps -FA --sort pcpu__
__ps -eM__  одна опция -M, которая позволяет вывести информацию про права безопасности и флаги SELinux для процессов
__ps -e | wc__ Общее количество запущенных процессов Linux
__ps L__ выводит все спецификаторы, которые можно использовать в -o или --filter
__ps -p 1334 -o comm=__ найти имя процесса по его pid
__ps -C clementine -o pid=__ найти pid по названию
__ps -t pts/0__ выбор процессов с помощью tty