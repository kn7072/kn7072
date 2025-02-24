#include <stdio.h>
#include <stdlib.h>

#include "macros_tricks.h"

// gcc -Wall -Werror -Wextra -O0 -g0 -o macros_use macros_use.c macros_tricks.h
// gcc -E -o macros_tricks.i macros_tricks.c
int main(void) {
    char str[] __attribute__((unused)) = "str_1";
    char str_2[] __attribute__((unused)) = "str_2";

    int x = 2;
    int y = 4;
    int xy = x + y;
    // В данном случае макрос CONCAT(x, y) разворачивается в x##y или xy. То есть
    // в итоге мы получаем название переменной xy
    printf("%d\n", CONCAT(x, y));  // x + y
    PR("PR %d %d\n", x, y);

    printf("_COUNT_ARGS %d\n", _COUNT_ARGS(_1, _2, _3, _4, _5, _6, _7, N, i, k));

    printf("COUNT_ARGS %d\n", COUNT_ARGS(a, b, c, d, e));

    printf(
        "SELECT_NTH_HELPER_TEST + 2 params (_6, _7) %s\n",
        SELECT_NTH_HELPER_TEST(4, _1, _2, _3, _4, _5, _6, _7));                               //  _4_6, _7
    printf("SELECT_NTH_HELPER_TEST_1 %s\n", SELECT_NTH_HELPER_TEST(3, a, b, c, d, e, f, g));  //  _3f, g
    printf("SELECT_NTH_HELPER_TEST_2 %s\n", SELECT_NTH_HELPER_TEST(3, a, b, c, d, e));        //  _3
    // printf("SELECT_NTH_HELPER_TEST_Error %s\n", SELECT_NTH_HELPER_TEST(3, a, b,
    // c, d));       //  error

    printf("%d\n", SELECT_NTH(3, 10, 20, 30, 40, 50));  // 30
    APPLY(PRINT_2, "one", "two", "three", "four");

    return EXIT_SUCCESS;
}
