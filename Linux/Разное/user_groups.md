# Пользователи и группы

В Linux группа — это совокупность пользователей. Основная цель групп — определить набор привилегий, таких как разрешение на чтение, запись или выполнение для данного ресурса, которые могут быть совместно использованы пользователями внутри группы. Пользователи могут быть добавлены в существующую группу, чтобы использовать предоставляемые ею привилегии.

## Группы Linux

Пользователь может принадлежать к двум типам групп:

1. Первичная группа или группа входа в систему — это группа, которая назначается файлам, создаваемым пользователем. Обычно имя основной группы совпадает с именем пользователя. Каждый пользователь должен принадлежать ровно к одной основной группе.

2. Вторичная или дополнительная группа — используется для предоставления определенных привилегий набору пользователей. Пользователь может быть участником нуля или нескольких вторичных групп.

### __/etc/passwd__
В файле /etc/passwd хранится вся информация о пользователях кроме пароля. Одна строка из этого файла соответствует описанию одного пользователя. Примерное содержание строки таково:

__vasyapupkin:x:1000:1000:Vasya Pupkin:/home/vpupkin:/bin/bash__

Строка состоит из нескольких полей, каждое из которых отделено от другого двоеточием. Значение каждого поля приведено в таблице.
№	Поле	Описание
1	vasyapupkin	Имя пользователя для входа в систему.
2	x	Необязательный зашифрованный пароль.
3	1000	Числовой идентификатор пользователя (UID).
4	1000	Числовой идентификатор группы (GID).
5	Vasya Pupkin	Поле комментария
6	/home/vpupkin	Домашний каталог пользователя.
7	/bin/bash	Оболочка пользователя.

Второе и последнее поля необязательные и могут не иметь значения.

---

### __/etc/group__ -все группы для всех пользователей
В /etc/group, как очевидно из названия хранится информация о группах. Она записана в аналогичном /etc/passwd виде:

__vasyapupkin:x:1000:vasyapupkin,petya__

№	Поле	Описание
1	vasyapupkin	Название группы
2	x	Необязательный зашифрованный пароль.
3	1000	Числовой идентификатор группы (GID).
4	vasyapupkin,petya	Список пользователей, находящихся в группе.

В этом файле второе и четвертое поля могут быть пустыми.

---

### __/etc/shadow__

Файл /etc/shadow хранит в себе пароли, по этому права, установленные на этот файл, не дают считать его простому пользователю. Пример одной из записей из этого файла:

__vasyapupkin:$6$Yvp9VO2s$VfI0t.o754QB3HcvVbz5hlOafmO.LaHXwfavJHniHNzq/bCI3AEo562hhiWLoBSqxLy7RJJNm3fwz.sdhEhHL0:15803:0:99999:7:::__

Здесь:
№	Поле	Описание
1	vasyapupkin	Имя пользователя для входа в систему.
2	$6$Yvp9VO2s$VfI0t.o754QB3HcvVbz5hlOafmO.LaHXwfavJHniHNzq/bCI3AEo562hhiWLoBSqxLy7RJJNm3fwz.sdhEhHL0	Необязательный зашифрованный пароль.
3	15803	Дата последней смены пароля.
4	0	Минимальный срок действия пароля.
5	99999	Максимальный срок действия пароля.
6	7	Период предупреждения о пароле.
7	Период неактивности пароля.
9	Дата истечения срока действия учётной записи.

---

__groups__ - покажит все группы пользователя(Первая группа — это основная группа.)
__groups linuxize__ покажет все группы пользователя linuxize

__id linuxize__ - выводит информацию об указанном пользователе и его группах


__getent group developers__ - Список всех участников группы developers
__getent group__ -Чтобы получить список всех групп

getent group | awk -F: '{ print $1}' -вывести имена групп

### System and Normal Users
//https://linuxize.com/post/how-to-list-users-in-linux/
There is no real technical difference between the system and regular (normal) users. Typically system users are created when installing the OS and new packages. In some cases, you can create a system user that will be used by some applications.

Normal users are the users created by the root or another user with sudo privileges. Usually, a normal user has a real login shell and a home directory.

Each user has a numeric user ID called UID. If not specified when creating a new user with the useradd command, the UID will be automatically selected from the __/etc/login.defs__ file depending on the UID_MIN and UID_MIN values.

To check the UID_MIN and UID_MIN values on your system, you can use the following command:
__grep -E '^UID_MIN|^UID_MAX' /etc/login.defs__
From the output above, we can see that all normal users should have a UID between 1000 and 60000. Knowing the minimal and maximal value allow us to query a list of all normal users in our system.

The command below will list all normal users in our Linux system:
__getent passwd {1000..60000}__

### Создание групп с помощью groupadd
используйте __groupadd__, за которым следует имя группы, которую вы хотите добавить. Существуют некоторые дополнительные параметры, единственным из которых является -g, который позволяет вам указать ID группы при создании группы

__groupadd account__ -создает группу account

Основные ключи:
Ключ	Описание
-g	Установить собственный GID.
-p	Пароль группы.
-r	Создать системную группу.

### Изменение группы

Сменить название группы, ее GID или пароль можно при помощи groupmod. Пример:

__sudo groupmod -n newtestgroup testgroup__ #Имя группы изменено с testgroup на newtestgroup

Опции groupmod:
Ключ	Описание
-g	Установить другой GID.
-n	Новое имя группы.
-p	Изменить пароль группы.

### Удаление группы

Удаление группы происходит так:

__sudo groupdel testgroup__

groupdel не имеет никаких дополнительных параметров.


### Управление свойствами группы

Для управления свойствами группы доступен __groupmod__. Вы можете использовать эту команду для изменения имени или идентификатора группы, но она не позволяет добавлять членов группы. Для этого вы используете usermod.


## Управление пользователями Linux

Добавление пользователя осуществляется при помощи команды useradd. Пример использоания:

__sudo useradd vasyapupkin__ - создаст в системе нового пользователя vasyapupkin

-b	Базовый каталог. Это каталог, в котором будет создана домашняя папка пользователя. По умолчанию /home
-с	Комментарий. В нем вы можете напечатать любой текст.
-d	Название домашнего каталога. По умолчанию название совпадает с именем создаваемого пользователя.
-e	Дата, после которой пользователь будет отключен. Задается в формате ГГГГ-ММ-ДД. По умолчанию отключено.
-f	Количество дней, которые должны пройти после устаревания пароля до блокировки пользователя, если пароль не будет изменен (период неактивности). Если значение равно 0, то запись блокируется сразу после устаревания пароля, при -1 - не блокируется. По умолчанию -1.
-g	Первичная группа пользователя. Можно указывать как GID, так и имя группы. Если параметр не задан будет создана новая группа название которой совпадает с именем пользователя.
-G	Список вторичных групп в которых будет находится создаваемый пользователь
-k	Каталог шаблонов. Файлы и папки из этого каталога будут помещены в домашнюю папку пользователя. По умолчанию /etc/skel.
-m	Ключ, указывающий, что необходимо создать домашнюю папку. По умолчанию домашняя папка не создается.
-p	Зашифрованный пароль пользователя. По умолчанию пароль не задается, но учетная пользователь будет заблокирован до установки пароля
-s	Оболочка, используемая пользователем. По умолчанию /bin/sh.
-u	Вручную задать UID пользователю.
-N - не создавать группу с именем пользователя.
-o - разрешить создание пользователя linux с неуникальным идентификатором UID;
-r - создать системного пользователя, не имеет оболочки входа, без домашней директории и с идентификатором до SYS_UID_MAX;
-D - отобразить параметры, которые используются по умолчанию для создания пользователя. Если вместе с этой опцией задать еще какой-либо параметр, то его значение по умолчанию будет переопределено.

### Параметры создания пользователя по умолчанию

Если при создании пользователя не указываются дополнительные ключи, то берутся настройки по умолчанию. Эти настройки вы можете посмотреть выполнив

__useradd -D__

Результат будет примерно следующий:

GROUP=100
HOME=/home
INACTIVE=-1
EXPIRE=
SHELL=/bin/sh
SKEL=/etc/skel
CREATE_MAIL_SPOOL=no

Если вас не устраивают такие настройки, вы можете поменять их выполнив

__sudo useradd -D -s /bin/bash__
где -s это ключ из таблицы выш

создадим пользователя с паролем и оболочкой /bin/bash
__sudo useradd -p password -s /bin/bash test1__
лучше создать пользователя без пароля, а затем при помощи утилиты passwd задать пароль
или воспользоваться рекомендацией
useradd -p принимает пароль ТОЛЬКО в зашифрованном виде. Именно по этому то что вы ввели, не равно тому что у вас запрашивает при авторизации. Лично мне помогло данное преобразование
__sudo useradd -m -p $(perl -e 'print crypt($ARGV[0], "password")' 'YOUR_PASSWORD') username__
таким образом после ключа -p водится уже зашифрованная версия вашего пароля. и при авторизации вводится всё как надо.


Дополнительные группы пользователя задаются с помощью параметра -G. Например, разрешим пользователю читать логи, использовать cdrom и пользоваться sudo:
__sudo useradd -G adm,cdrom,wheel -p password -s /bin/bash test2__

Также, можно установить дату, когда аккаунт пользователя будет отключен автоматически, это может быть полезно для пользователей, которые будут работать временно:
__sudo useradd -G adm,cdrom,wheel -p password -s /bin/bash -e 01:01:2018 test2__

Некоторых пользователей интересует создание пользователя с правами root linux, это очень просто делается с помощью useradd, если комбинировать правильные опции. Нам всего лишь нужно разрешить создавать пользователя с неуникальным uid, установить идентификатор в 0 и идентификатор основной группы тоже в 0. Команда будет выглядеть вот так:
__sudo useradd -o -u 0 -g 0 -s /bin/bash newroot__
чтобы удалить подобного пользователя небходимо выполнить
__sudo userdel --force newroot__

Добавление пользователя с заданными домашней директорией, командной оболочкой и комментариями. В этой команде опция "-m -d" создает пользователя с заданной домашней директорией, а опция "-s" задает командную оболочку, т.е. /bin/bash. Опция "-c" добавляет дополнительную информацию о пользователе, а опция "-U" создает/добавляет группу с тем же именем, что и у пользователя.
__useradd -m -d /var/www/ravi -s /bin/bash -c "TecMint Owner" -U ravi__

Добавление пользователя с заданными домашней директорией, командной оболочкой, комментариями и UID/GID. Эта команда очень похожа на предыдущую, но здесь мы определяем оболочку как "/bin/zsh", и задаем UID и GID для пользователя "tarunika". Здесь "-u" задает новый UID пользователя (т.е. 1000), а "-g" задает GID (т.е. 1000).
__useradd -m -d /var/www/tarunika -s /bin/zsh -c "TecMint Technical Writer" -u 1000 -g 1000 tarunika__

Добавление пользователя с домашней директорией, без оболочки, с комментариями и User ID.
Следующая команда очень похожа на две предыдущие, единственное отличие в том, что мы отключаем командную оболочку для пользователя "avishek" с заданным User ID (т.е. 1019). Это значит, что пользователь "avishek" не сможет авторизоваться в системе из командной оболочки.
__useradd -m -d /var/www/avishek -s /usr/sbin/nologin -c "TecMint Sr. Technical Writer" -u 1019 avishek__

Добавление пользователя с домашней директорией, skeleton directory, комментариями и User ID
Единственное, что меняется в этой команде, мы используем опцию "-k", чтобы задать skeleton directory, то есть /etc/custom.skel, а не умолчательную /etc/skel. Мы также используем опцию "-s", чтобы задать отдельную оболочку /bin/tcsh.
__useradd -m -d /var/www/navin -k /etc/custom.skell -s /bin/tcsh -c "No Active Member of TecMint" -u 1027 navin__

Добавление пользователя без домашней директории, без оболочки, без групп, и с комментариями
Приведенная ниже команда отличается от показанных ранее. Здесь мы используем опцию "-M", чтобы создать пользователя без домашней директории, и "-N", чтобы создать только пользователя (без группы). Аргумент "-r" используется для создания системного пользователя.
__useradd -M -N -r -s /bin/false -c "Disabled TecMint Member" clayton__

Чтобы войти в систему как только что созданный пользователь, вам необходимо установить пароль пользователя. Для этого выполните passwd команду с именем пользователя

### Изменение пароля

Изменить пароль пользователю можно при помощи утилиты passwd.

__sudo passwd vasyapupkin__

passwd может использоваться и обычным пользователем для смены пароля. Для этого пользователю надо ввести

__passwd__
и ввести старый и новый пароли.

Основные ключи passwd: 
-d	Удалить пароль пользователю. После этого пароль будет пустым, и пользователь сможет входить в систему без предъявления пароля.
-e	Сделать пароль устаревшим. Это заставит пользователя изменить пароль при следующем входе в систему.
-i	Заблокировать учетную запись пользователя по прошествии указанного количества дней после устаревания пароля.
-n	Минимальное количество дней между сменами пароля.
-x	Максимальное количество дней, после которого необходимо обязательно сменить пароль.
-l	Заблокировать учетную запись пользователя.
-u	Разблокировать учетную запись пользователя.

### Установка пустого пароля пользователя

Супер пользователь с помощью утилит командной строки passwd и usermod или путем редактирования файла /etc/shadow может удалить пароль пользователь, дав возможность входить в систему без указания пароля.

__sudo passwd -d vasyapupkin__
или
__sudo usermod -p "" vasyapupkin__

__Если учетная запись пользователя в этот момент была заблокирована командой passwd -l, то указанные выше команды так же снимут эту блокировку__

Установка пустого пароля может быть полезна как временное решение проблемы в ситуации, когда пользователь забыл свой пароль или не может его ввести из-за проблем с раскладкой клавиатуры. После этого имеет смысл принудить пользователя установить себе новый пароль при следующем входе в систему

__sudo passwd -e vasyapupkin__

## Получение информации о пользователях

__w__ – вывод информации (имя пользователя, рабочий терминал, время входа в систему, информацию о потребленных ресурсах CPU и имя запущенной программы) о всех вошедших в систему пользователях.

__who__ – вывод информации (имя пользователя, рабочий терминал, время входа в систему) о всех вошедших в систему пользователях.

__who am i или whoami или id__ – вывод вашего имени пользователя.

__users__ – вывод имен пользователей, работающих в системе.

__id имя_пользователя__ – вывод о идентификаторах пользователя: его uid, имя_пользователя, gid и имя первичной группы и список групп в которых состоит пользователь

__groups имя_пользователя__ – вывод списка групп в которых состоит пользователь.

## Удаление пользователя

Для того, чтобы удалить пользователя воспользуйтесь утилитой userdel. Пример использования:

__sudo userdel vasyapupkin__

userdel имеет всего два основных ключа:
Ключ	Описание
-f	Принудительно удалить пользователя, даже если он сейчас работает в системе.
-r	Удалить домашний каталог пользователя.

## Как пользоваться командой usermod в Linux?

usermod — это утилита командной строки, позволяющая изменять данные для входа пользователя.

ПАРАМЕТРЫ
-a, --append
           Добавить пользователя в дополнительную группу(ы). Использовать только вместе с
           параметром -G.

-c, --comment КОММЕНТАРИЙ
           Новое значение поля комментария в файле пользовательских паролей. Обычно его изменяют с помощью программы chfn(1).

           usermod -c "Test User" linuxize

-d, --home HOME_DIR
    Домашний каталог нового пользователя.

    Если указан параметр -m, то содержимое текущего домашнего каталога будет перемещено в
    новый домашний каталог, который будет создан, если он ещё не существует.

    usermod -d HOME_DIR -m USER

-e, --expiredate ДАТА_УСТАРЕВАНИЯ
    Дата, когда учётная запись пользователя будет заблокирована. Дата задаётся в формате
    ГГГГ-ММ-ДД.
    sudo usermod -e "2022-02-21" linuxize

    Пустое значение аргумента ДАТА_УСТАРЕВАНИЯ отключает устаревание учётной записи.
    sudo usermod -e "" linuxize

    Для этого параметра требуется файл /etc/shadow. При отсутствии в /etc/shadow создаётся
    необходимая запись.

    Используйте chage команду -l, чтобы просмотреть дату истечения срока действия пользователя:
    sudo chage -l linuxize

-f, --inactive ДНЕЙ
    Количество дней, которые должны пройти после устаревания пароля, чтобы учётная запись
    заблокировалась навсегда.

    Если указано значение 0, то учётная запись блокируется сразу после устаревания пароля,
    а при значении -1 данная возможность не используется.

    Для этого параметра требуется файл /etc/shadow. При отсутствии в /etc/shadow создаётся
    необходимая запись. 
-g, --gid ГРУППА
           Имя или числовой идентификатор новой первичной группы пользователя. Группа с таким именем должна существовать.

           Все файлы в домашнем каталоге пользователя, принадлежавшие предыдущей первичной группе пользователя, будут принадлежать новой группе.

           Группового владельца файлов вне домашнего каталога нужно изменить вручную.
           
           usermod -g developers linuxize

-G, --groups ГРУППА1[,ГРУППА2,...[,ГРУППАN]]]
    Список дополнительных групп, в которых числится пользователь. Перечисление групп
    осуществляется через запятую, без промежуточных пробелов. На указанные группы
    действуют те же ограничения, что и для группы указанной в параметре -g.

    Если пользователь — член группы, которой в указанном списке нет, то пользователь
    удаляется из этой группы. Такое поведение можно изменить с помощью параметра -a, при
    указании которого к уже имеющемуся списку групп пользователя добавляется список
    указанных дополнительных групп.

    usermod -a -G GROUP USER

-l, --login НОВОЕ_ИМЯ
    Имя пользователя будет изменено с ИМЯ на НОВОЕ_ИМЯ. Больше ничего не меняется. В
    частности, вероятно, должно быть изменено имя домашнего каталога и почтового ящика,
    чтобы отразить изменение имени пользователя.

    sudo usermod -l linuxize lisa

-L, --lock
    Заблокировать пароль пользователя. Это делается помещением символа «!» в начало
    шифрованного пароля, чтобы приводит к блокировке пароля. Не используйте этот параметр
    вместе с -p или -U.
    sudo usermod -L linuxize

    Замечание: если вы хотите заблокировать учётную запись (не только доступ по паролю),
    также установите значение EXPIRE_DATE в 1.
    sudo usermod -L -e 1 linuxize
    
    Чтобы разблокировать пользователя, запустите usermodс -Uопцией:
    usermod -U USER

-m, --move-home
    Переместить содержимое домашнего каталога в новое место.

    Этот параметр можно использовать только с параметром -d (или --home).

    Команда usermod пытается изменить владельцев файлов и копирует права, ACL и
    расширенные атрибуты, но после неё всё равно могут потребоваться некоторые ручные
    действия.

-o, --non-unique
    При использовании с параметром -u, этот параметр позволяет указывать не уникальный
    числовой идентификатор пользователя.

-p, --password ПАРОЛЬ
    Шифрованное значение пароля, которое возвращает функция crypt(3).

    Замечание: Этот параметр использовать не рекомендуется, так как пароль (или не
    шифрованный пароль) будет видим другими пользователям в списке процессов.

    Пароль будет записан в локальный файл /etc/passwd или /etc/shadow. Это может вызвать
    расхождения с базой данных паролей, настроенной в PAM.

    Вы должны проверить, что пароль соответствует политике системных паролей.

-R, --root КАТ_CHROOT
    Выполнить изменения в каталоге КАТ_CHROOT и использовать файлы настройки из каталога
    КАТ_CHROOT.

-s, --shell ОБОЛОЧКА
    Имя новой регистрационной оболочки пользователя. Если задать пустое значение, то будет
    использована регистрационная оболочка по умолчанию.

    sudo usermod -s /usr/bin/zsh linuxize

-u, --uid UID
    Новый числовой идентификатор пользователя (UID).

    Оно должно быть уникальным, если не используется параметр -o. Значение должно быть
    неотрицательным.

    Для почтового ящика и всех файлов, которыми владеет пользователь и которые расположены
    в его домашнем каталоге, идентификатор владельца файла будет изменён автоматически.

    Для файлов, расположенных вне домашнего каталога, идентификатор нужно изменять
    вручную.

    Никаких проверок по UID_MIN, UID_MAX, SYS_UID_MIN или SYS_UID_MAX из /etc/login.defs
    не производится.

    sudo usermod -u 1050 linuxize

-U, --unlock
    Разблокировать пароль пользователя. Это выполняется удалением символа «!» из начала
    шифрованного пароля. Не используйте этот параметр вместе с -p или -L.

    Замечание: если вы хотите разблокировать учётную запись (не только доступ по паролю),
    также установите значение EXPIRE_DATE (например, в to 99999 или равным значению EXPIRE
    из файла /etc/default/useradd).

    usermod -U USER

-v, --add-sub-uids FIRST-LAST
    Add a range of subordinate uids to the user's account.

    This option may be specified multiple times to add multiple ranges to a users account.

    No checks will be performed with regard to SUB_UID_MIN, SUB_UID_MAX, or SUB_UID_COUNT
    from /etc/login.defs.

-V, --del-sub-uids FIRST-LAST
    Remove a range of subordinate uids from the user's account.

    This option may be specified multiple times to remove multiple ranges to a users
    account. When both --del-sub-uids and --add-sub-uids are specified, the removal of all
    subordinate uid ranges happens before any subordinate uid range is added.

    No checks will be performed with regard to SUB_UID_MIN, SUB_UID_MAX, or SUB_UID_COUNT
    from /etc/login.defs.

-w, --add-sub-gids FIRST-LAST
    Add a range of subordinate gids to the user's account.

    This option may be specified multiple times to add multiple ranges to a users account.

    No checks will be performed with regard to SUB_GID_MIN, SUB_GID_MAX, or SUB_GID_COUNT
    from /etc/login.defs.

-W, --del-sub-gids FIRST-LAST
    Remove a range of subordinate gids from the user's account.

    This option may be specified multiple times to remove multiple ranges to a users
    account. When both --del-sub-gids and --add-sub-gids are specified, the removal of all
    subordinate gid ranges happens before any subordinate gid range is added.

    No checks will be performed with regard to SUB_GID_MIN, SUB_GID_MAX, or SUB_GID_COUNT
    from /etc/login.defs.

-Z, --selinux-user SEUSER
    Новый пользователь SELinux для пользовательского входа.

    При пустом значении SEUSER пользовательское сопоставление SELinux для пользователя
    LOGIN удаляется (если есть).    

# Конфигурационный файл sudo
https://hackware.ru/?p=11183

Программа sudo считывает конфигурацию из файла /etc/sudoers. Если в файле /etc/sudoers раскомментировать директиву
includedir /etc/sudoers.d

то дополнительно настройки будут считываться из всех файлов в директории /etc/sudoers.d.
Не рекомендуется напрямую править файл /etc/sudoers, рекомендуется использовать команду
visudo

которая откроет файл для редактирования. Кроме прочих функций, данная программа проверит синтаксис, и если в нём присутствует ошибка, то файл не будет сохранён.

При запуске visudo по умолчанию будет открыт файл /etc/sudoers. С помощью опции -f можно указать расположение файла в другом месте, например в /etc/sudoers.d. 

## Как разрешить пользователи выполнять только определённые команды с sudo

Необязательно каждому пользователю разрешать любые действия с sudo. Вы можете ограничить возможности пользователя выполнением только некоторых программ.

В файл /etc/sudoers нужно добавить строку вида: 
__Имя_пользователя Имя_машины=(Реальный_пользователь:Группа) команда__

В этой строке значения следующие:
- Имя_пользователя: Это тот пользователь, кто инициировал выполнение команды с sudo
- Имя_машины: Это имя хоста, где будет действительна команда sudo. Полезно если у вас много хостовых машин.
- (Реальный_пользователь): Тот пользователь, от чьего имени будет выполнена команда.
- Группа: группа, к которой принадлежит пользователь.
- команда: команда или набор команд, разрешённых для запуска с sudo этому Пользователю.

Предположим, я хочу разрешить пользователю admin выполнять любые команды от имени любых пользователей, тогда мне нужно добавить строку: 
__admin ALL=(ALL:ALL) ALL__

Другой вариант, я хочу разрешить пользователю admin выполнять только команды /home/admin/backup.sh и /usr/bin/apt, и выполнять их он может только от root, тогда мне нужно добавить строку:
__admin ALL=(root:ALL) /home/admin/backup.sh,/usr/bin/apt__
Обратите внимание, что если команд несколько, то они перечисляются через запятую без пробела. 

По умолчанию включена настройка, которая разрешает всем членам группы sudo выполнять любые команды с sudo. Эта настройка заключена в строке: 
__%sudo ALL=(ALL:ALL) ALL__

В зависимости от дистрибутива, она же может быть записана так:
%wheel ALL=(ALL) ALL
 ИЛИ
%wheel ALL=(ALL:ALL) ALL

Чтобы в действительности ограничить права пользователя, нужно закомментировать эту строку, то есть поставить перед ней символ #:
#%sudo  ALL=(ALL:ALL) ALL

## Как узнать, какие sudo полномочия имеются у пользователя

Мы только что узнали, что у определённого пользователя могут быть ограниченные полномочия на выполнение команд с sudo. Как узнать, какие именно команды может выполнить пользователь или как проверить, сработали ли наши настройки в файле /etc/sudoers?

Для вывода всех разрешённых команд или для проверки определённой команды, используется опция -l. Но если не указать опцию -U с именем интересующего пользователя, то будут выведены данные для пользователя по умолчанию (root). 

Пример проверки прав sudo для пользователя admin: 
__sudo -l -U admin__

Также можно узнать, является ли та или иная команда заблокированной или разрешённой для выполнения пользователем с sudo следующим образом: 
__sudo -l -U admin rm__
Если команда разрешена, то будет выведен полный путь до файла: 
__sudo -l -U admin apt__
/usr/bin/apt

## Как настроить использование sudo без пароля
Данная настройка только для тех пользователей, кто действительно понимает зачем он это делает и какие риски безопасности это влечёт.

Чтобы отключить запрос пароля ПОЛЬЗОВАТЕЛЮ при вводе одной или нескольких КОМАНД с sudo: 
__ПОЛЬЗОВАТЕЛЬ ALL=(ALL:ALL) NOPASSWD: КОМАНДА1,КОМАНДА2,КОМАНДА3__

Чтобы отключить запрос пароля ПОЛЬЗОВАТЕЛЮ при вводе любой команды с sudo: 
__ПОЛЬЗОВАТЕЛЬ ALL=(ALL:ALL) NOPASSWD: ALL__

Чтобы отключить запрос пароля всем пользователям при вводе одной или нескольких КОМАНД с sudo: 
__%sudo ALL=(ALL:ALL) NOPASSWD: КОМАНДА1,КОМАНДА2,КОМАНДА3__

Чтобы отключить запрос пароля всем пользователям при вводе любой команды с sudo: 
__%sudo ALL=(ALL:ALL) NOPASSWD: ALL__

К примеру, чтобы разрешить пользователю admin выполнять команды /home/admin/backup.sh и /usr/bin/apt с sudo без необходимости ввода пароля, нужно добавить строку: 
__admin ALL=(ALL:ALL) NOPASSWD: /home/admin/backup.sh,/usr/bin/apt__

вторая часть статьи - https://hackware.ru/?p=11193