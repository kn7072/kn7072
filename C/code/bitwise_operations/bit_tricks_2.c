#include <stdio.h>

#include "common.h"
// gcc -Wall -g -O0 -o bit_tricks_2 bit_tricks_2.c common.c common.h

/*
https://www.geeksforgeeks.org/toggle-bits-given-range/?ysclid=m5peto5n3v965965438

Toggle bits in the given range

Given a non-negative number n and two values l and r. The problem is to toggle
the bits in the range l to r in the binary representation of n, i.e., to toggle
bits from the lth least significant bit bit to the rth least significant bit
(the rightmost bit as counted as first bit). A toggle operation flips a bit 0 to
1 and a bit 1 to 0. Constraint: 1 <= l <= r <= number of bits in the binary
representation of n. Examples:

    Input: n = 17, l = 1, r = 3
    Output: 22
    Explanation: (17)10 = (10001)2
                 (22)10 = (10110)2
    The bits in the range 1 to 3 in the binary representation of 17 are toggled.

    Input: n = 50, l = 2, r = 5
    Output: 44

    Explanation: (50)10 = (110010)2
                 (44)10 = (101100)2
    The bits in the range 2 to 5 in the binary representation of 50 are toggled.

Approach: Following are the steps:
    Calculate num as = ((1 << r) – 1) ^ ((1 << (l-1)) – 1) or as ((1 <<r)-l).
This will produce a number num having r number of bits and bits in the range l
to r (from rightmost end in binary representation) are the only set bits. Now,
perform n = n ^ num. This will toggle the bits in the range l to r in n.

 */

unsigned int toggleBitsFromLToR(unsigned int, unsigned int, unsigned int);

// function to toggle bits in the given range
unsigned int toggleBitsFromLToR(unsigned int n, unsigned int l, unsigned int r) {
    // calculating a number 'num' having 'r'
    // number of bits and bits in the range l
    // to r are the only set bits
    int num = ((1 << r) - 1) ^ ((1 << (l - 1)) - 1);

    // toggle bits in the range l to r in 'n'
    // and return the number
    // Besides this, we can calculate num as: num=(1<<r)-l .
    return (n ^ num);
}

int main() {
    unsigned int n = 17;
    unsigned int l = 1, r = 3;
    displayBits(n);
    n = toggleBitsFromLToR(n, l, r);
    displayBits(n);
    printf("%u\n", n);
    return 0;
}
