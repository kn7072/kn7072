#include <stdio.h>

#include "common.h"

// gcc -Wall -g -O0 -o base common.c common.h base_operations.c

int main(void) {
    unsigned int x = 1;
    unsigned int number1 = 65535;
    fprintf(stdout, "%10u\n", x);

    x <<= 2;
    fprintf(stdout, "%10u\n", x);
    fflush(stdout);
    displayBits(x);
    displayBits(number1);
    displayBits(number1 & x);
    displayBits(~number1);
    return 0;
}
