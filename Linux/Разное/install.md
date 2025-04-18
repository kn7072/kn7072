# Использование команды Install в Linux

[Главное меню](https://andreyex.ru/) » [Linux](https://andreyex.ru/category/linux/) » **Использование команды Install в Linux**

Нет, она ничего не устанавливает. Удивлены?

Да, несмотря на название «install», команда install не устанавливает никаких пакетов. Это продвинутый способ копирования файлов, при котором вы можете задать такие атрибуты, как право собственности на файл.

Для установки пакетов вам следует использовать менеджер пакетов вашего дистрибутива Linux, такой как apt, dpkg, dnf, yum, zypper и т.д.

Большинство пользователей Linux даже не знают о существовании этой команды install, не говоря уже о том, чтобы использовать ее.

Взгляните на некоторые примеры использования команды install, и, возможно, вы сможете включить ее в свой командный арсенал.

## Как использовать команду install

В этом разделе мы начнем с базовых примеров и постепенно перейду к некоторым продвинутым, где команда install действительно великолепна.

Мы начнем с копирования файлов с помощью команды install.

### 1. Скопируйте файлы с помощью команды install

Если вы хотите скопировать файлы, как вы это делаете, [используя команду cp](https://andreyex.ru/operacionnaya-sistema-linux/komanda-cp-v-linux-7-prakticheskih-primerov/), то все, что вам нужно сделать, это указать целевой файл и расположение, куда файл необходимо скопировать:

install Filename Directory

Например, здесь мы скопировали Test.txt файл в каталог Demo:

install Test.txt ~/Demo

$ install Test.txt ~/Demo
$ tree ~/Demo

/home/alex/Demo
Test. txt

0 directories, 1 file

### 2. Запретите использование временных меток при копировании файлов

По умолчанию команда install сохраняет исходные права доступа к файлу и права собственности, но обновляет временные метки временем, когда файл был скопирован.

Чтобы предотвратить это, используйте флаг -p, как показано здесь:

install -p Filename Directory_name

Например, здесь мы скопировали один и тот же файл Haruki.txt с флагом -p и без него, чтобы отобразить исходные и измененные временные метки.

### 3. Создайте каталог с помощью команды install

Чтобы создать новый каталог, как вы это делаете с помощью команды mkdir, вам нужно будет использовать флаг -d, как показано здесь:

install -d Directory_name

Вот что мы сделали, чтобы создать новый каталог с именем hello внутри моего домашнего каталога:

$ install -d ~/hello

$ cd hello 


bash: cd: hello: No such file or directory


$ install -d ~/hello <- Создание новой директории
$ cd hello 

~/hello$

### 4. Создайте новый каталог и скопируйте в него файлы (целиком)

Если вы хотите скопировать файлы в новый каталог, то вы можете пропустить создание каталога, поскольку вы можете выполнить оба действия одной командой.

[

Читать  Как заменить все после шаблона с помощью команды `sed`

](https://andreyex.ru/linux/kak-zamenit-vse-posle-shablona-s-pomoshhyu-komandy-sed/)

Для этой цели вам нужно будет использовать два флага: -D и -t (позже я объясню их):

install -D -t Directory_name Filename

Например, здесь мы скопировали Test.txt файл в каталог My_dir:

$ cd My_dir

bash: cd: My_dir: No such file or directory

$ install -D -t My_dir Test.txt
$ tree My_dir/

dir/
Test.txt

0 directories, 1 file

Видели это? Изначально не было каталога с именем My_dir но когда мы использовали команду install, она создала каталог, а затем скопировала указанный файл.

Здесь,

- -D: Этот флаг используется для создания всех основных компонентов целевого назначения. Проще говоря, он создаст путь, если указанный путь не существует.
- -t: Сокращение от —target-directory, которое используется для указания целевого каталога.

В дополнение к приведенной выше цепочке команд я бы рекомендовал добавить флаг -v, чтобы получить подробный вывод, который напечатает, что делает команда:

install -v -D -t Directory_name Filename

$ install -v -D -t my_dir Test.txt 

install: creating directory 'my_dir' 

'Test.txt' -> 'my_dir/Test.txt'

### 5. Установите разрешения с помощью команды install

Пользователи Linux обычно [используют команду chmod для изменения прав доступа к файлам](https://andreyex.ru/operacionnaya-sistema-linux/primery-komand-chmod-v-linux/), но команда install позволяет вам сделать это при копировании файла в другое расположение или при создании нового каталога.

Для этой цели вам придется использовать флаг -m с командой install, поэтому здесь мы покажем вам, как вы можете использовать его при копировании файлов и создании каталогов.

#### Установите права доступа к файлу при его копировании

Лично нам больше всего нравится использовать команду install, где вы можете изменять/устанавливать права доступа к файлу при копировании файла.

Для этого вы можете использовать флаг -m следующим образом:

install -m <permission_numbers> Filename Directory

$ install -v -m 644 nano.txt My_dir/ 

'nano.txt' -> 'My_dir/nano.txt'

$ ls -l ~/My_dir/

total 0
-rw-r-- - 1 alex alex 0 Dec 26 20:45 nano.txt 
-rwxr-xr-x 1 alex alex 0 Dec 26 20:25 Test.txt 

#### Установите разрешения при создании каталога

Чтобы установить разрешения при создании каталогов, используйте флаг -m следующим образом:

install -m <permission_numbers> -d Directory_name

Например, здесь мы создали каталог с именем LHB с разрешением 777:

install -m 777 -d LHB

$ install -m 777 -d LHB  $ ls -la LHB

total 16

drwxrwxrwx 2 alex alex 4096 Dec 26 21:49 drwxr-x- + 83 alex alex 12288 Dec 26 21:49

[

Читать  Ввод, вывод и перенаправление ошибок в Linux

](https://andreyex.ru/linux/vvod-vyvod-i-perenapravlenie-oshibok-v-linux/)

### 6. Смена владельца с помощью команды install

Для изменения или назначения владельца потребуются права sudo.

Команда install позволяет вам изменить владельца при копировании файла или создании нового каталога. Это безумие. Верно?

Для этого вам необходимо добавить имя пользователя к флагу -o.

Итак, давайте рассмотрим, как вы можете использовать флаг -o с файлами и каталогами.

#### Изменение владельца при копировании файла

Чтобы изменить владельца файла при копировании файла, используйте флаг -o следующим образом:

sudo install -o <owner_user> Filename Directory

$ getfacl Test.txt

# file: Test.txt
# owner: alex   <- До
# group: alex
user::rw-
group::rw-
other:: r

$ sudo install -o andreyex Test.txt My_dir/ 
$ getfacl My_dir/Test.txt

# file: My_dir/Test.txt
# owner: andreyex  <- После
# group: root
user::rwx
group: :r-x
other::r-x

#### Назначьте владельца каталога при создании

Чтобы назначить владельца каталога при создании каталога, используйте флаг -o следующим образом:

sudo install -d -o <owner_user> Directory_name

Например, здесь мы назначили пользователя andreyex каталогу Bash_hash:

sudo install -d -o andreyex Bash_hash

$ getfacl Bash_hash 

# file: Bash_hash 
# owner: andreyex
# group: root
user::rwx
group::r-x
other: : r-

### 7. Измените владельца группы с помощью команды install

Вы можете использовать команду install для изменения владельца группы при копировании файла или создании каталога.

Для этой цели вы должны использовать флаг -g, и вот как вы его используете.

#### Измените групповое право собственности на файл при его копировании

Чтобы [изменить групповое право собственности на файл](https://andreyex.ru/operacionnaya-sistema-linux/komanda-chown-v-linux/) при его копировании, используйте флаг -g с командой install следующим образом:

sudo install Filename -g <group_name> Directory

$ getfacl Test.txt

# file: Test.txt
# owner: alex
# group: alex
user::rw-
group::rw-
other:: r-

$ sudo install Test.txt -g new_group My_dir/ 
$ getfacl My_dir/Test.txt

# file: My_dir/Test.txt # owner: root
# group: new_group
user::rwx
group: :r-x
other::r-x

#### Создайте новый каталог с определенным владельцем группы

Используя команду install, вы можете назначить групповое владение каталогом во время создания каталога. Для этого используйте команду install с флагом -g, как показано здесь:

sudo install -d -g <group_name> <directory_name>

$ sudo install -d -g new_group Hello_world 
$ getfacl Hello_world/

# file: Hello_world/ 
# owner: root 
# group: new_group

user::rwx
group::r-x
other: :r-x

### 8. Создайте резервные копии файлов с помощью команды install

Это не ваш традиционный способ создания резервной копии в Linux. Когда вы используете команду install для переопределения, скопировав ее снова в то же место с флагом -b, она добавит тильду (~) в конце файла, указывающую на файл резервной копии.

[

Читать  5 примеров команд Cal в Linux

](https://andreyex.ru/linux/komandy-linux-i-komandy-shell/5-primerov-komand-cal-v-linux/)

Чтобы создать резервную копию, вам нужно выполнить 2 простых шага:

- Убедитесь, что у вас уже есть такой же файл в целевом расположении, и если нет, то сначала сделайте копию файла в целевое расположение.
- Используйте команду install с флагом -b для создания файла резервной копии.

Звучит запутанно? Позвольте мне помочь.

#### Шаг 1: Создайте копию файла (избегайте, если это уже сделано)

Это просто, просто используйте команду install и укажите целевой файл и целевой каталог. Подробно обсуждается в первом примере.

Итак, здесь я скопировал Test.txt файл в My_dir каталог:

install Test.txt My_dir/

$ install Test.txt My_dir/  
$ tree My_dir/

My_dir/
-Test. txt

0 directories, 1 file

#### Шаг 2: Используйте флаг -b для создания резервной копии файла

Если у вас есть копия файла в целевом расположении, используйте команду install, чтобы скопировать тот же файл в то же расположение, но с флагом -b:

install -b Filename Directory_name

Ранее мы скопировали Test.txt файл, и теперь мы будем использовать тот же самый, но с флагом -b, как показано здесь, для создания резервной копии:

install -b Test.txt My_dir/

$ install -b Test.txt My_dir/  
$ tree My_dir/

My_dir/
-Test.txt
-Test.txt~

The backup file

0 directories, 2 files

Она создает файл, заканчивающийся тильдой (~), который является нашим файлом резервной копии.

Но вы можете изменить суффикс, используя флаг -S, и выбрать то, что душе угодно:

install -b -S <suffix> Filename Directory

Например. здесь я использовал суффикс .bkp:

install -b -S .bkp Test.txt My_dir/

$ install -b -S .bkp Test.txt My_dir/  
$ tree My_dir/

My_dir/
-Test.txt
-Test.txt~
-Test.txt.bkp

0 directories, 3 files

## Заключение

Если вы продвинутый пользователь и хотите быть более продуктивным, то команда install разработана для таких пользователей, как вы.

Но если это выглядит слишком сложным и запутанным, то вы можете пропустить эту команду и использовать вместо нее другие инструменты, такие как использование команды cp для копирования файлов:

Или использование [команды mkdir](https://andreyex.ru/linux/kak-sozdat-katalog-v-linux-s-pomoshhyu-komandy-mkdir/) для получения большего контроля над созданием каталогов:

После завершения работы вы можете узнать, как [изменить владельца и разрешения в Linux](https://andreyex.ru/linux/razresheniya-v-linux/):