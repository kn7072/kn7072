#include <stdio.h>

// Определим файл hello.c, который будет представлять код разделяемой библиотеки
extern char *message;

void print_data(int value) {
    printf("value: %d\n", value);
    printf("message: %s\n", message);
}

// Скомпилируем этот файл в разделяемую библиотеку
// gcc -c -fPIC  hello.c -o hello.o
// В итоге будет сгенерирован объектный файл hello.o.
// Далее для создания собственно разделяемой библиотеки выполним команду:
// gcc -shared hello.o -o hello.so
// ldd hello.so
