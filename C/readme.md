
GMP
Пакет GMP содержит математические библиотеки. Они содержат полезные функции для арифметики с произвольной точностью. 
https://book.linuxfromscratch.ru/systemd/chapter08/gmp.html

# 8.19.1. Установка пакета GMP
## [Примечание] Примечание

Если вы выполняете сборку для 32-разрядной архитектуры x86, но ваш процессор, способен выполнять 64-разрядный код, и вы указали в переменных окружения CFLAGS, скрипт configure попытается выполнить настройку для 64-разрядной системы и завершится ошибкой. Чтобы избежать этого, необходимо вызвать команду configure с приведенным ниже параметром

ABI=32 ./configure ...

## [Примечание] Примечание

Настройки GMP по умолчанию собирают библиотеки, оптимизированные для процессора хоста. Если требуются библиотеки, подходящие для процессоров с меньшей производительностью, чем у процессора хоста, можно собрать общие библиотеки, добавив параметр --host=none-linux-gnu в команде configure.

Подготовьте GMP к компиляции:

./configure --prefix=/usr    \
            --enable-cxx     \
            --disable-static \
            --docdir=/usr/share/doc/gmp-6.3.0



Значение новых параметров настройки:

--enable-cxx

    Этот параметр включает поддержку C++
--docdir=/usr/share/doc/gmp-6.3.0

    Эта переменная указывает местоположение для документации.

Скомпилируйте пакет и сгенерируйте HTML-документацию:

make
make html

## Важно

Набор тестов для GMP в этом разделе считается критически важным. Ни в коем случае не пропускайте его.

Проверьте результаты:

make check 2>&1 | tee gmp-check-log

## Внимание

Код в GMP сильно оптимизирован для процессора, на котором он собран. Иногда код, определяющий процессор, неверно определяет возможности системы, и в тестах или других приложениях, использующих библиотеки gmp, возникают ошибки с сообщением "Illegal instruction". В этом случае gmp следует переконфигурировать с параметром --host=none-linux-gnu и пересобрать. 

Убедитесь, что все 199 тестов в наборе тестов пройдены. Проверьте результат, выполнив следующую команду:

awk '/# PASS:/{total+=$3} ; END{print total}' gmp-check-log

Установите пакет и его документацию:

make install
make install-html

# 8.19.2. Содержимое пакета GMP
Установленные библиотеки:
libgmp.so и libgmpxx.so
Созданные каталоги:
/usr/share/doc/gmp-6.3.0
# Краткое описание

libgmp Содержит точные математические функции

libgmpxx Содержит точные математические функции C++ 

# библиотеки libgmp.so и libgmpxx.so находятся в каталоге /usr/lib


##############
https://book.linuxfromscratch.ru/systemd/chapter08/mpfr.html
Пакет MPFR содержит функции для двоичных вычислений с плавающей запятой произвольной точности. 

# 8.20.1. Установка пакета MPFR

Исправьте тестовый пример, приводящий к ошибке в старых версиях Glibc:

sed -e 's/+01,234,567/+1,234,567 /' \
    -e 's/13.10Pd/13Pd/'            \
    -i tests/tsprintf.c

Подготовьте MPFR к компиляции:

./configure --prefix=/usr        \
            --disable-static     \
            --enable-thread-safe \
            --docdir=/usr/share/doc/mpfr-4.2.0

Скомпилируйте пакет и сгенерируйте HTML-документацию:

make
make html

# [Важно] Важно
Набор тестов для MPFR в этом разделе считается критически важным. Ни в коем случае не пропускайте его.

Выполните тестирование и убедитесь, что все 197 тестов пройдены:

make check

# Установите пакет и документацию к нему:

make install
make install-html

# 8.20.2. Содержимое пакета MPFR
Установленные библиотеки:
libmpfr.so
Созданные каталоги:
/usr/share/doc/mpfr-4.2.0
# Краткое описание
libmpfr
Содержит математические функции с произвольной точностью

# библиотека libmpfr.so находятся в каталоге /usr/lib

##################
# lib/missing: line 81: makeinfo: command not found
sudo apt-get install texinfo

##################
GDB
https://linuxfromscratch.org/blfs/view/svn/general/gdb.html

# Introduction to GDB

GDB, the GNU Project debugger, allows you to see what is going on “inside” another program while it executes -- or what another program was doing at the moment it crashed. Note that GDB is most effective when tracing programs and libraries that were built with debugging symbols and not stripped.


 Package Information

    Download (HTTP): https://ftp.gnu.org/gnu/gdb/gdb-14.1.tar.xz

    Download MD5 sum: 4a084d03915b271f67e9b8ea2ab24972

    Download size: 23 MB

    Estimated disk space required: 966 MB (add 805 MB for docs; add 710 MB for tests)

    Estimated build time: 2.1 SBU (add 0.4 SBU for docs; add 18 SBU for tests; all using parallelism=4)

# GDB Dependencies
Recommended Runtime Dependency

six-1.16.0 (Python 3 module, required at run-time to use GDB scripts from various LFS/BLFS packages with Python 3 installed in LFS)
Optional

Doxygen-1.9.8, GCC-13.2.0 (ada, gfortran, and go are used for tests), Guile-3.0.9, rustc-1.74.1 (used for some tests), Valgrind-3.22.0, and SystemTap (run-time, used for tests)

 Installation of GDB

# Install GDB by running the following commands:

mkdir build &&
cd    build &&

../configure --prefix=/usr          \
             --with-system-readline \
             --with-python=/usr/bin/python3 &&
make

Optionally, to build the API documentation using Doxygen-1.9.8, run:

make -C gdb/doc doxy
