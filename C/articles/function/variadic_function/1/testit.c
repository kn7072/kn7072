#include <stdarg.h>
#include <stdio.h>

// gcc -g3 -Wall -O0 -o testit testit.c

void testit(int i, ...) {
    va_list argptr;
    va_start(argptr, i);

    if (i == 0) {
        int n = va_arg(argptr, int);
        printf("%d\n", n);
    } else {
        char *s = va_arg(argptr, char *);
        printf("%s\n", s);
    }

    va_end(argptr);
}

int main() {
    testit(0, 0xFFFFFFFF);  // 1st problem: 0xffffffff is not an int
    testit(1, NULL);        // 2nd problem: NULL is not a char*
}
