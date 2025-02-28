## Поиск ошибок работы с памятью в C/C++ при помощи Valgrind

17 апреля 2017

Если вы пишете код на языке C или C++, поиск и устранение ошибок работы с памятью, таких, как утечки, выход за границы массива или обращение к неинициализированной памяти, могут доставить немало хлопот. Существует по крайней мере два инструмента для решения этих проблем — Valgrind (не путать с [Vagrant](https://eax.me/vagrant/)!) и Clang’овский [MemorySanitizer](http://clang.llvm.org/docs/MemorySanitizer.html). Последний работает исключительно под Linux и показал себя несколько сырым и не слишком гибким инструментом, поэтому поговорим о Valgrind. Он довольно гибок и работает везде. Кроме того, в отличие от MemorySanitizer, Valgrind может находить неинициализированные данные с точностью до _одного бита_. Из недостатков Valgrind стоит отметить сравнительно низкую скорость работы.

### Простой пример

Перейдем сразу к делу и проверим работу Valgrind на такой программе:

```c
#include <stdio.h>  
#include <stdlib.h>  
#include <string.h>  
  
void run_test(int i)  
{  
  int delta = 123;  
  char* mem = malloc(1024);  
  strcpy(mem, "i = ");  
  printf("%s %d\n", mem, i + delta);  
  /* free(mem); */  
}  
  
void main()  
{  
  int i;  
  for(i = 0; i < 10; i++)  
    run_test(i);  
}
```
Компилируем с отладочными символами и запускаем ее под Valgrind:

```bash
gcc -O0 -g vgcheck.c -o vgcheck  
valgrind ./vgcheck
```

Результат:

```
==1948== HEAP SUMMARY:  
==1948==     in use at exit: 10,240 bytes in 10 blocks  
==1948==   total heap usage: 11 allocs, 1 frees, 11,264 bytes allo...  
==1948==  
==1948== LEAK SUMMARY:  
==1948==    definitely lost: 10,240 bytes in 10 blocks  
==1948==    indirectly lost: 0 bytes in 0 blocks  
==1948==      possibly lost: 0 bytes in 0 blocks  
==1948==    still reachable: 0 bytes in 0 blocks  
==1948==         suppressed: 0 bytes in 0 blocks  
==1948== Rerun with --leak-check=full to see details of leaked memory
```
Видим, что память утекла. Запускаем с `--leak-check=full`:

```
==2047== 10,240 bytes in 10 blocks are definitely lost in loss recor...  
==2047==    at 0x4C2AF1F: malloc (in /usr/lib/valgrind/vgpreload_mem...  
==2047==    by 0x400561: run_test (vgcheck.c:8)  
==2047==    by 0x4005AF: main (vgcheck.c:18)
```
Теперь раскомментируем вызов `free` и уберем инициализацию переменной `delta`. Посмотрим, увидит ли Valgrind обращение к неинициализированной памяти:
```
==2102== Conditional jump or move depends on uninitialised value(s)  
==2102==    at 0x4E8003C: vfprintf (in /usr/lib/libc-2.25.so)  
==2102==    by 0x4E87EA5: printf (in /usr/lib/libc-2.25.so)  
==2102==    by 0x4005CA: run_test (vgcheck.c:10)  
==2102==    by 0x4005F4: main (vgcheck.c:18)

```
Видит. Запустим с `--track-origins=yes` чтобы найти, откуда именно пришла неинициализированная переменаая:

```
==2205== Conditional jump or move depends on uninitialised value(s)  
==2205==    at 0x4E800EE: vfprintf (in /usr/lib/libc-2.25.so)  
==2205==    by 0x4E87EA5: printf (in /usr/lib/libc-2.25.so)  
==2205==    by 0x4005CA: run_test (vgcheck.c:10)  
==2205==    by 0x4005F4: main (vgcheck.c:18)  
==2205==  Uninitialised value was created by a stack allocation  
==2205==    at 0x400586: run_test (vgcheck.c:6)
```
Как видите, Valgrind нашел место объявления неинициализированной переменой с точностью до имени файла и номера строчки.

Теперь исправим все ошибки:

```
==2239== HEAP SUMMARY:  
==2239==     in use at exit: 0 bytes in 0 blocks  
==2239==   total heap usage: 11 allocs, 11 frees, 11,264 bytes allo...  
==2239==  
==2239== All heap blocks were freed -- no leaks are possible
```
Ну разве не красота?

### Пример посложнее — запускаем PostgreSQL под Valgrind

Рассмотрим, как происходит запуск под Valgrind больших программ, например, [PostgreSQL](https://eax.me/postgresql-install/). Работа с памятью в этой РСУБД устроена особым образом. Например, в ней используются иерархические пулы памяти (memory contexts). Для понимания всего этого хозяйства Valgrind’у нужны подсказки. Чтобы такие подсказки появились, нужно раскомментировать строчку:

```c
#define USE_VALGRIND
```

… в файле src/include/pg_config_manual.h, после чего полностью [пересобрать PostgreSQL](https://eax.me/postgresql-build/). Затем запуск под Valgrind осуществляется как-то так:

```bash
valgrind --leak-check=no --track-origins=yes --gen-suppressions=all \  
  --read-var-info=yes \  
  --log-file=$HOME/work/postgrespro/postgresql-valgrind/%p.log \  
  --suppressions=src/tools/valgrind.supp --time-stamp=yes \  
  --trace-children=yes postgres -D \  
  $HOME/work/postgrespro/postgresql-install/data-master \  
  2>&1 | tee $HOME/work/postgrespro/postgresql-valgrind/postmaster.log
```
Полный пример вы найдете в [файле valgrind.sh](https://github.com/afiskon/pgscripts/blob/master/valgrind.sh) из [этого репозитория](https://github.com/afiskon/pgscripts) на GitHub.

Обратите внимание на флаг `--leak-check=no`. Даже с упомянутыми подсказками Valgrind все равно не подходит для поиска утечек памяти в PostgreSQL. Он попросту будет генерировать слишком много ложных сообщений об ошибках. Поэтому здесь Valgrind используется только для поиска обращений к неинициализированной памяти.

Флаг `--trace-children=yes` в приведенной выше команде, как несложно догадаться, говорит Valgrind’у цепляться к процессам-потомкам.

Еще стоит отметить флаг `--suppressions`, который задает [файл с описанием ошибок](https://github.com/postgres/postgres/blob/master/src/tools/valgrind.supp), которые следует игнорировать, а также флаг `--gen-suppressions=all`, который в случае возникновения ошибок генерирует строки, которые можно добавить в этот самый файл для игнорирования ошибок. Кстати, в файле можно [использовать wildcards](https://wiki.wxwidgets.org/Valgrind_Suppression_File_Howto#Wildcards), в стиле:

{  
   <libpango>  
   Memcheck:Leak  
   ...  
   obj:/usr/*lib*/libpango*  
}

В зависимости от используемых флагов, `make installcheck` под Valgrind’ом на [моем ноутбуке](https://eax.me/fujitsu-lifebook-e733/) выполняется от получаса до часа. Для сравнения, без Valgrind’а соответствующий прогон тестов занимает порядка 3.5 минут. Отсюда можно сделать вывод, что программа под Valgrind выполняется в 10-20 раз медленнее.

### Использование Valgrind совместно с GDB

Посмотрев на приведенные выше отчеты Valgrind’а об ошибках, можно заметить, что в определенном смысле они недостаточно информативны. В частности, в них нет имен переменных и информации о том, какие конкретно данные в них лежали на момент возникновения ошибки. Решается эта проблема запуском Valgrind’а с флагами:

```bash
valgrind --vgdb=yes --vgdb-error=1 дальше_как_обычно
```

Эти флаги говорят Valgrind остановить процесс и запустить gdb-сервер после возникновения первой ошибки. Можно указать и `--vgdb-error=0`, чтобы подключиться к процессу отладчиком сразу после его запуска. Однако это может быть плохой идеей, если вы также указали `--trace-children=yes` и при этом программа создает множество дочерних процессов.

При возникновении ошибки Valgrind напишет:

```
==00:00:00:06.603 16153== TO DEBUG THIS PROCESS USING GDB: start GDB...  
==00:00:00:06.603 16153==   /path/to/gdb postgres  
==00:00:00:06.603 16153== and then give GDB the following command  
==00:00:00:06.603 16153==   target remote | vgdb --pid=16153
```
После этого, чтобы подключиться к процессу при помощи [GDB](https://eax.me/gdb/), говорим:

# где postgres - имя исполняемого файла  
```bash
gdb postgres
```
… и уже в отладчике:

target remote | vgdb --pid=16153

Из интересных дополнительных команд доступны следующие. Посмотреть список утечек:

monitor leak_check

Узнать, кто ссылается на память:
monitor who_points_at (address) (len)

Проверка инициализированности памяти (0 — бит инициализирован, 1 — не инициализирован, _ — not addressable):

monitor get_vbits (address) (len)

Прочее:
monitor help

Дальше отлаживаем, как обычно. Например, говорим `continue`. Как только произойдет следующая ошибка, программа снова остановится по брейкпоинту. Можно смотреть значения переменных, перемещаться между фреймами стека, ставить собственные брейкпоинты, и так далее.

### Заключение

К сожалению, в рамках одного поста невозможно рассмотреть абсолютно все возможности Valgrind. Например, в него входят инструменты [Callgrind](http://valgrind.org/docs/manual/cl-manual.html) и [Massif](http://valgrind.org/docs/manual/ms-manual.html), предназначенные для поиска узких мест в коде и профилирования памяти соответственно. Эти инструменты я не рассматриваю, так как для решения названных задач предпочитаю [использовать perf](https://eax.me/c-cpp-profiling/) и [Heaptrack](https://eax.me/heaptrack/). Также существует инструмент [Helgrind](http://valgrind.org/docs/manual/hg-manual.html), предназначенный для поиска гонок. Его изучение я вынужден оставить вам в качестве упражнения.

Как видите, пользоваться Valgrind крайне просто. Он, конечно, не идеален. Как уже отмечалось, Valgrind существенно замедляет выполнение программы. Кроме того, в нем случаются ложноположительные срабатывания. Однако последняя проблема решается составлением специфичного для вашего проекта файла подавления конкретных отчетов об ошибках. Так или иначе, если вы пишете на C/C++ и не прогоняете код под Valgrind хотя бы в [Jenkins](https://eax.me/jenkins/) или TeamCity незадолго до релиза, вы явно делаете что-то не так!
