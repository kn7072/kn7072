[источник](https://laurvas.ru/bash-trap/)
# Trap — обработка сигналов и ошибок в Bash

```text
trap ДЕЙСТВИЕ СИГНАЛ...
```

Trap работает очень просто: при возникновении сигнала будет выполнено указанное действие. Если действие простое (последовательность команд, умещающаяся на одной строке), его можно указать прямо в аргументе `trap`. Если не очень простое, то надо объявить функцию и поместить вызов этой функции в `trap`.

Можно обрабатывать стандартные сигналы (их полный список выводится по `trap -l`). Также доступны специфические для Bash: `DEBUG`, `RETURN`, `ERR`, `EXIT`.

На практике trap оказывается не такой уж простой штукой. Дьявол как всегда кроется в деталях. Сейчас покажу.

- [Изучаем trap на простых примерах](https://laurvas.ru/bash-trap/#simple-example)
- [Переменные внутри trap](https://laurvas.ru/bash-trap/#variables-inside-trap)
- [Trap и функции](https://laurvas.ru/bash-trap/#trap-and-functions)
- [Практическое применение trap](https://laurvas.ru/bash-trap/#usage-examples)
- [Ограничения](https://laurvas.ru/bash-trap/#limitations)

### Изучаем trap на простых примерах

Ко мне понимание пришло одновременно с этим демонстрационным скриптом:

trap_signals_demo.sh

```bash
#!/bin/bash

trap 'echo trap SIGINT' SIGINT
trap 'echo trap SIGTERM' SIGTERM
trap 'echo trap SIGHUP' SIGHUP
trap 'echo trap SIGQUIT' SIGQUIT
trap 'echo trap EXIT' EXIT
trap 'echo trap ERR' ERR

echo 'start'
sleep 1m
echo 'end'
```

Скрипт выводит “start”, спит одну минуту, затем выводит “end”. Если во время сна поступает один из обрабатываемых сигналов, то просто выводится соответствующее сообщение.

Тестируем:

```
$ ./trap_signal_demo.sh
start
end
trap EXIT

$ ./trap_signal_demo.sh &
start
$ kill -SIGINT %1
trap SIGINT
trap ERR
end
trap EXIT

$ ./trap_signal_demo.sh &
start
$ kill -SIGHUP %1
Обрыв терминальной линии
trap SIGHUP
trap ERR
end
trap EXIT

$ ./trap_signal_demo.sh &
start
$ kill -SIGQUIT %1
Выход (core dumped)
trap SIGQUIT
trap ERR
end
trap EXIT

$ ./trap_signal_demo.sh &
start
$ kill -SIGTERM %1
Завершено
trap SIGTERM
trap ERR
end
trap EXIT
```

Вывод реального терминала выглядит несколько иначе, я скрыл несущественные детали. Поясню что здесь происходило. Я запускал скрипт в фоне (`&` после команды), затем командой `kill` посылал сигнал только что запущенному процессу. Чтобы послать `SIGINT`, не обязательно связываться с `kill`, можно во время работы скрипта нажать Ctrl+C.

**Если убрать из скрипта обработку прерывающих сигналов,** то будет уже не так. `SIGINT`, `SIGHUP`, `SIGTERM` не создают сигнал `ERR`, а сразу ведут на выход:

```
$ ./trap_signal_demo.sh &
start
$ kill -SIGINT %1
trap EXIT

$ ./trap_signal_demo.sh &
start
$ kill -SIGHUP %1
trap EXIT

$ ./trap_signal_demo.sh &
start
$ kill -SIGQUIT %1
Выход (core dumped)
trap ERR
end
trap EXIT

$ ./trap_signal_demo.sh &
start
$ kill -SIGTERM %1
trap EXIT
```

`SIGQUIT` создаёт `ERR`, но на выход не ведёт. Никакой закономерности тут нет, просто так работают дефолтные обработчики сигналов. У каждого сигнала своя специфика.

**Для игнорирования сигналов** используется пустой `trap`. Этот демонстрационный скрипт можно прервать только смертоносным сигналом `SIGKILL`.

```bash
#!/bin/bash
trap '' SIGINT SIGTERM SIGHUP SIGQUIT
sleep 1m
```

Вернуть дефолтный обработчик сигнала тоже можно, пусть и не совсем очевидным способом:

```text
trap - СИГНАЛ...
```

Вызов `trap` без аргументов покажет все установленные обработчики сигналов. Это полезно при отладке.

### Переменные внутри trap

Можно по-разному запихивать переменные внутрь `trap`. Здесь я использую `ls`, чтобы продемонстрировать обработку пробелов и `false` для имитации возникновения ошибки. Обратите внимание на кавычки.

variables_in_trap_demo1.sh

```bash
#!/bin/bash
F="one two"
trap 'ls $F' ERR
F="three four"
false
```

variables_in_trap_demo2.sh

```bash
#!/bin/bash
F="one two"
trap "ls $F" ERR
F="three four"
false
```

variables_in_trap_demo3.sh

```bash
#!/bin/bash
F="one two"
trap "ls \"$F\"" ERR
F="three four"
false
```

variables_in_trap_demo4.sh

```bash
#!/bin/bash
F="one two"
trap "ls \"\$F\"" ERR
F="three four"
false
```

variables_in_trap_demo5.sh

```bash
#!/bin/bash
F="one two"
trap 'ls "$F"' ERR
F="three four"
false
```

```
$ touch 'one two' 'three four'

$ ./variables_in_trap_demo1.sh
ls: невозможно получить доступ к three: Нет такого файла или каталога
ls: невозможно получить доступ к four: Нет такого файла или каталога
$ ./variables_in_trap_demo2.sh
ls: невозможно получить доступ к one: Нет такого файла или каталога
ls: невозможно получить доступ к two: Нет такого файла или каталога
$ ./variables_in_trap_demo3.sh
one two
$ ./variables_in_trap_demo4.sh
three four
$ ./variables_in_trap_demo5.sh
three four
```

Если вам непонятно почему так происходит, попробуйте запустить эти примеры с включенной опцией xtrace. Для этого добавьте в начале скрипта `set -x` или `set -o xtrace`. Или укажите в sha-bang’е `bash -x`. Или запускайте скрипты командой `bash -x СКРИПТ`.

### Trap и функции

Наследует ли функция обработчики сигналов? Если да, то в какой момент: при вызове функции или при её объявлении?

trap_and_functions_demo1.sh

```bash
#!/bin/bash

f1() {
  echo 'f1 start'
  echo 'trap inside f1:'
  trap
  echo 'f1 exit'
}

for sig in SIGINT SIGTERM SIGHUP SIGQUIT EXIT ERR RETURN; do
  trap "echo trap $sig" $sig
done

f2() {
  echo 'f2 start'
  echo 'trap inside f2:'
  trap
  echo 'f2 exit'
}

echo 'global trap:'
trap
echo 'call f1'
f1
echo 'call f2'
f2
echo 'end of script'
```

```
$ ./trap_and_functions_demo1.sh
global trap:
trap -- 'echo trap EXIT' EXIT
trap -- 'echo trap SIGHUP' SIGHUP
trap -- 'echo trap SIGINT' SIGINT
trap -- 'echo trap SIGQUIT' SIGQUIT
trap -- 'echo trap SIGTERM' SIGTERM
trap -- 'echo trap ERR' ERR
trap -- 'echo trap RETURN' RETURN
call f1
f1 start
trap inside f1:
trap -- 'echo trap EXIT' EXIT
trap -- 'echo trap SIGHUP' SIGHUP
trap -- 'echo trap SIGINT' SIGINT
trap -- 'echo trap SIGQUIT' SIGQUIT
trap -- 'echo trap SIGTERM' SIGTERM
f1 exit
call f2
f2 start
trap inside f2:
trap -- 'echo trap EXIT' EXIT
trap -- 'echo trap SIGHUP' SIGHUP
trap -- 'echo trap SIGINT' SIGINT
trap -- 'echo trap SIGQUIT' SIGQUIT
trap -- 'echo trap SIGTERM' SIGTERM
f2 exit
end of script
trap EXIT
```

Из выхлопа видно, что функция наследует обработчики сигналов в момент вызова. В противном случае `trap` первой функции был бы пустой.

Внимательные читатели заметили странное поведение обработчиков ERR и RETURN: они не наследуются! Чтобы получить обработку этих сигналов внутри функции, надо включить bash-опцию errtrace или объявить их явно в теле функции. Попробуйте сами.

Всё становится ещё запутаннее, если объявить функцию, которая выполняется в подоболочке (subshell). Этот пример отличается от предыдущего заменой фигурных скобочек на круглые:

trap_and_functions_demo2.sh

```bash
#!/bin/bash

f() (
  echo 'f start'
  echo 'trap inside f:'
  trap
  echo 'f exit'
)

for sig in SIGINT SIGTERM SIGHUP SIGQUIT EXIT ERR RETURN; do
  trap "echo trap $sig" $sig
done

echo 'global trap:'
trap
echo 'call f'
f
echo 'end of script'
```

```
$ ./trap_and_functions_demo2.sh
global trap:
trap -- 'echo trap EXIT' EXIT
trap -- 'echo trap SIGHUP' SIGHUP
trap -- 'echo trap SIGINT' SIGINT
trap -- 'echo trap SIGQUIT' SIGQUIT
trap -- 'echo trap SIGTERM' SIGTERM
trap -- 'echo trap ERR' ERR
trap -- 'echo trap RETURN' RETURN
call f
f start
trap inside f:
trap -- 'echo trap EXIT' EXIT
trap -- 'echo trap SIGHUP' SIGHUP
trap -- 'echo trap SIGINT' SIGINT
trap -- 'echo trap SIGQUIT' SIGQUIT
trap -- 'echo trap SIGTERM' SIGTERM
f exit
end of script
trap EXIT
```

Видим такое же поведение: наследуются все обработчики кроме ERR и RETURN. Однако если объявить какой-либо trap внутри функции, то наследование пропадает полностью!

trap_and_functions_demo3.sh

```bash
#!/bin/bash

f() (
  echo 'f start'
  trap 'echo f trap ERR' ERR
  echo 'trap inside f:'
  trap
  echo 'f exit'
)

for sig in SIGINT SIGTERM SIGHUP SIGQUIT EXIT ERR RETURN; do
  trap "echo trap $sig" $sig
done

echo 'global trap:'
trap
echo 'call f'
f
echo 'end of script'
```

```
$ ./trap_and_functions_demo3.sh
global trap:
trap -- 'echo trap EXIT' EXIT
trap -- 'echo trap SIGHUP' SIGHUP
trap -- 'echo trap SIGINT' SIGINT
trap -- 'echo trap SIGQUIT' SIGQUIT
trap -- 'echo trap SIGTERM' SIGTERM
trap -- 'echo trap ERR' ERR
trap -- 'echo trap RETURN' RETURN
call f
f start
trap inside f:
trap -- 'echo f trap ERR' ERR
f exit
end of script
trap EXIT
```

А как bash ведёт себя в обратной ситуации? Попадают ли обработчики сигналов из функций наружу? Да, если функция была объявлена без подоболочки. Пруф:

trap_and_functions_demo4.sh

```bash
#!/bin/bash

f1() {
  echo 'f1 start'
  for sig in SIGINT SIGTERM SIGHUP SIGQUIT EXIT ERR RETURN; do
    trap "echo f1 trap $sig" $sig
  done
  echo 'trap inside f1:'
  trap
  echo 'f1 exit'
}

f2() (
  echo 'f2 start'
  for sig in SIGINT SIGTERM SIGHUP SIGQUIT EXIT ERR RETURN; do
    trap "echo f2 trap $sig" $sig
  done
  echo 'trap inside f2:'
  trap
  echo 'f2 exit'
)

echo 'global trap:'
trap
echo 'call f1'
f1
echo 'global trap:'
trap
echo 'call f2'
f2
echo 'global trap:'
trap
echo end of script
```

```
$ ./trap_and_functions_demo4.sh
global trap:
call f1
f1 start
trap inside f1:
trap -- 'echo f1 trap EXIT' EXIT
trap -- 'echo f1 trap SIGHUP' SIGHUP
trap -- 'echo f1 trap SIGINT' SIGINT
trap -- 'echo f1 trap SIGQUIT' SIGQUIT
trap -- 'echo f1 trap SIGTERM' SIGTERM
trap -- 'echo f1 trap ERR' ERR
trap -- 'echo f1 trap RETURN' RETURN
f1 exit
f1 trap RETURN
global trap:
trap -- 'echo f1 trap EXIT' EXIT
trap -- 'echo f1 trap SIGHUP' SIGHUP
trap -- 'echo f1 trap SIGINT' SIGINT
trap -- 'echo f1 trap SIGQUIT' SIGQUIT
trap -- 'echo f1 trap SIGTERM' SIGTERM
trap -- 'echo f1 trap ERR' ERR
trap -- 'echo f1 trap RETURN' RETURN
call f2
f2 start
trap inside f2:
trap -- 'echo f2 trap EXIT' EXIT
trap -- 'echo f2 trap SIGHUP' SIGHUP
trap -- 'echo f2 trap SIGINT' SIGINT
trap -- 'echo f2 trap SIGQUIT' SIGQUIT
trap -- 'echo f2 trap SIGTERM' SIGTERM
trap -- 'echo f2 trap ERR' ERR
trap -- 'echo f2 trap RETURN' RETURN
f2 exit
f2 trap EXIT
global trap:
trap -- 'echo f1 trap EXIT' EXIT
trap -- 'echo f1 trap SIGHUP' SIGHUP
trap -- 'echo f1 trap SIGINT' SIGINT
trap -- 'echo f1 trap SIGQUIT' SIGQUIT
trap -- 'echo f1 trap SIGTERM' SIGTERM
trap -- 'echo f1 trap ERR' ERR
trap -- 'echo f1 trap RETURN' RETURN
end of script
f1 trap EXIT
```

Надеюсь эти примеры внесли ясность, а не запутали вас ещё больше.

### Практическое применение trap

В реальной жизни вам вряд ли придётся писать такие запутанные обработчики. Обычно всё сводится к двум сценариям.

**Блокировка скрипта lock-файлом:**

```bash
#!/bin/bash

LOCKFILE=/tmp/example_lockfile

if [[ -f $LOCKFILE ]]; then
  echo "script is already locked!" >&2
  exit 1
fi

touch $LOCKFILE
trap 'rm $LOCKFILE' EXIT

# Do things...
```

**Удаление временных файлов и подчистка за собой.**

Простой однострочный вариант:

```bash
#!/bin/bash

trap 'rm /tmp/tempfile' EXIT

# Do things...
```

С использованием функции:

```bash
#!/bin/bash

cleanup() {
    return_value=$?
    rm -rf "$tmpfile"
    exit $return_value
}

tmpfile=$(mktemp)
trap "cleanup" EXIT

# Do things...
```

К сожалению эта система не даёт 100% надёжности. Trap сработает при завершении скрипта любым из стандартных способов:

- при нормальном завершении,
- при возникновении ошибки при включённой опцией errexit,
- при получении прерывающего сигнала, который может быть обработан.

но не сработает, если:

- скрипт был убит сигналом SIGKILL,
- пришёл OOM-killer и убил ваш процесс,
- у компьютера внезапно отобрали питание.

### Ограничения

Bash умеет в рекурсию, но не вызывает обработчик сигнала, уже находясь в нём. Похоже, что в такой ситуации он вызывает дефолтный обработчик. Посмотрим:

trap_inside_trap.sh

```bash
#!/bin/bash

set -o errtrace

trapper() {
  echo trapper begin
  trap
  false
  echo trapper end
}

trap trapper ERR

false
echo end of script
```

```
$ ./trap_inside_trap.sh
trapper begin
trap -- 'trapper' ERR
trapper end
end
```

А если с подоболочкой? То же самое. Скорее всего так было сделано чтобы избежать зацикливания.
