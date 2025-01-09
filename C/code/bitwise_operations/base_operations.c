#include <stdio.h>

// gcc -Wall -g -O0 -o base base_operations.c

void displayBits(unsigned int value);  // prototype

// display bits of an unsigned int value
void displayBits(unsigned int value) {
    // define displayMask and left shift 31 bits
    unsigned int displayMask = 1 << 31;
    printf("%10u = ", value);
    // loop through bits
    for (unsigned int c = 1; c <= 32; ++c) {
        putchar(value & displayMask ? '1' : '0');
        value <<= 1;       // shift value left by 1
        if (c % 8 == 0) {  // output space after 8 bits
            putchar(' ');
        }
    }
    putchar('\n');
}

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
