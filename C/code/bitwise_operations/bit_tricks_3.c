#include "common.h"

// https://www.geeksforgeeks.org/set-bits-given-range-number/?ysclid=m5pl797p2x59483621
// gcc -Wall -g -O0 -o bit_tricks_3 bit_tricks_3.c common.c common.h
/*
 Set all the bits in given range of a number

Given a non-negative number n and two values l and r. The problem is to set the
bits in the range l to r in the binary representation of n, i.e, to unset bits
from the rightmost lth bit to the rightmost r-th bit. Constraint: 1 <= l <= r <=
number of bits in the binary representation of n.

Examples :
Input : n = 17, l = 2, r = 3
Output : 23
(17)10 = (10001)2
(23)10 = (10111)2
The bits in the range 2 to 3 in the binary
representation of 17 are set.

Input : n = 50, l = 2, r = 5
Output : 62

Approach: Following are the steps:


1. Find a number 'range' that has all set
   bits in given range. And all other bits
   of this number are 0.
   range = (((1 << (l - 1)) - 1) ^ ((1 << (r)) - 1));

2. Now, perform "n = n | range". This will
   set the bits in the range from l to r
   in n.
 */

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

// Driver program to test above
int main() {
    unsigned int n = 17;
    unsigned int new_n;
    unsigned int l = 1, r = 3;
    displayBits(n);
    new_n = toggleBitsFromLToR(n, l, r);
    displayBits(new_n);
    return 0;
}
