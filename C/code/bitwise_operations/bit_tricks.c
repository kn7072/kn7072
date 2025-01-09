#include <stdio.h>
void displayMask(unsigned int);

// gcc -Wall -g -O0 -o bit_tricks bit_tricks.c
/*
x&1                 Evaluates to 1 if the number is odd else evaluates to 0
x & (x-1)           Clears the lowest set bit of x
x & ~(x-1)          Extracts the lowest set bit of x (all others are cleared)
x & ~((1 << i+1 ) - 1)  Clears all bits of x from LSB to ith bit x &
((1 << i) - 1)      Clears all bits of x from MSB to ith bit
x >>1               Divides x by 2
x << 1              Multiplies x by 2
ch | ''             Upper case English alphabet ch to lower case
ch & '_'            Lower case English alphabet ch to upper case
x && !(x & x-1)     Checking if given 32-bit integer is power of 2
log2(n & -n)+1      Find the last set bit
*/

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
    unsigned int number = 5;
    unsigned int i = 0;
    unsigned mask = 0;

    /*
    1) Check Whether Number is Even or Odd
    x & 1

    Logic:
    Even numbers have 0 as their LSB and Odd numbers have 1 as their LSB, so
    Bitwise AND with even numbers results in 0 and with odd numbers results in 1.
    Example: x = 29 (00011101), (x & 1) = 1, therefore x is an odd number x=
    16(10000), (x & 1) = 0, therefore x is an even number
     */
    number = 29;
    if (number & 1) {  // is odd
        displayBits(number);
    }
    number = 4;
    if (number & 1) {         // even
        displayBits(number);  // вывода не будет
    }
    /*
    2) Clear the Lowest Set bit of x
    x & (x-1)

    Logic:
    When you subtract 1 from x, all the bits to the right of the lowest set bit
    become 1, and the lowest set bit becomes 0 and performing a bitwise AND
    operation between x and (x-1) sets each bit to 0 except for the bits that are
    common in both x and (x-1).
    Example:
    x =         10101010
    x-1 =       10101001
    x & (x-1) = 10101000
     */
    number = 24;
    displayBits(number);
    displayBits(number & (number - 1));

    /*
    3) Extract the Lowest Set bit of x
    x & ~(x-1);

    Logic:
    When you subtract 1 from x, all the bits to the right of the lowest set bit
    become 1, and the lowest set bit becomes 0 and performing a bitwise AND
    operation between x and ~(x-1) sets each bit to 0 except for the lowest set
    bit of x.

    Example:
    x =          10101010
    ~(x-1) =     01010110
    x & ~(x-1) = 00000010
     */
    number = 26;
    displayBits(number);
    displayBits(number & ~(number - 1));

    /*
    4) Clear all bits from LSB to ith bit

    mask = ~((1 << i+1 ) - 1);
    x &= mask;

    Logic:
    To clear all bits from LSB to i-th bit, we have to AND x with mask having LSB
    to i-th bit 0. To obtain such mask, first left shift 1 i times. Now if we
    minus 1 from that, all the bits from 0 to i-1 become 1 and remaining bits
    become 0. Now we can simply take the complement of mask to get all first i
    bits to 0 and remaining to 1.

    Example:
    x = 29 (00011101) and we want to clear
    LSB to 3rd bit, total 4 bits
    mask -> 1 << 4 -> 16(00010000)
    mask -> 16 - 1 -> 15(00001111)
    mask -> ~mask  ->    11110000
    x & mask       -> 16(00010000)
     */
    number = 45;
    i = 3;
    mask = ~((1 << (i + 1)) - 1);
    displayBits(number);
    displayBits(mask);
    number &= mask;
    displayBits(number);

    /*
    5) Clearing all bits from MSB to i-th bit

    mask = (1 << i) - 1;
    x &= mask;

    Logic:
    To clear all bits from MSB to i-th bit, we have to AND x with mask having MSB
    to i-th bit 0. To obtain such mask, first left shift 1 i times. Now if we
    minus 1 from that, all the bits from 0 to i-1 become 1 and the remaining bits
    become 0.

    Example:
    x = 215 (11010111) and we want to clear MSB to 4th bit, total 4 bits
    mask -> 1 << 4 -> 16(00010000)
    mask -> 16 - 1 -> 15(00001111)
    x & mask       -> 7 (00000111)
     */

    number = 300;
    i = 5;
    mask = (1 << i) - 1;
    displayBits(number);
    displayBits(mask);
    number &= mask;
    displayBits(number);

    /*
    6) Divide by 2
    x >>= 1;

    Logic:
    When we do arithmetic right shift, every bit is shifted to right and blank
    position is substituted with sign bit of number, 0 in case of positive and 1
    in case of negative number. Since every bit is a power of 2, with each shift
    we are reducing the value of each bit by factor of 2 which is equivalent to
    division of x by 2.

    Example:
    x =      18(00010010)
    x >> 1 = 9 (00001001)
    */

    /*
    7) Multiplying by 2

    x <<= 1;

    Logic:
    When we do arithmetic left shift, every bit is shifted to left and blank
    position is substituted with 0 . Since every bit is a power of 2, with each
    shift we are increasing the value of each bit by a factor of 2 which is
    equivalent to multiplication of x by 2.

    Example:
    x =      18(00010010)
    x << 1 = 36(00100100)
     */
    return 0;
}
