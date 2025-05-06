#include <stdio.h>
#include <stdlib.h>

// https://gcc.gnu.org/onlinedocs/gcc/Common-Variable-Attributes.html#index-cleanup-variable-attribute
// https://habr.com/ru/articles/503536/
// https://nibblestew.blogspot.com/2016/07/comparing-gcc-c-cleanup-attribute-with.html
// gcc -g -Wall -O0 -o main main.c
/*
 функция, вызываемая атрибутом cleanup, должна принимать в качестве аргумента
 указатель на освобождаемую переменную, а у нас таковой является указатель на
 выделенную область памяти, то есть нам обязательно нужна функция, принимающая
 двойной указатель. Для этого нам нужна дополнительная функция-обёртка
 */
static void free_int(int **ptr) {
    free(*ptr);
    printf("cleanup done\n");
}

/*
 К тому же, мы не можем использовать универсальную функцию для освобождения
 любых переменных, потому что они будут требовать разных типов аргументов.
 Поэтому перепишем функцию так:
 */
static void _free(void *p) {
    free(*(void **)p);
    printf("cleanup done two\n");
}

int main() {
    int lenght = 10;
    int one = 1;
    int two = 2;
    __attribute__((cleanup(free_int))) int *ptr_one = malloc(sizeof(*ptr_one) * lenght);
    __attribute__((cleanup(_free))) int *ptr_two = malloc(sizeof(*ptr_two));
    // do something here
    ptr_one[0] = 3;
    ptr_one[1] = 4;
    printf("ptr one %p\n", ptr_one);
    /* ptr_two = &two; */
    return 0;
}
