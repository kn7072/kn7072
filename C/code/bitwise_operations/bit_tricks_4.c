#include <stdio.h>

#include "common.h"
#define INT_BITS 32

// https://www.geeksforgeeks.org/c-program-to-rotate-bits-of-a-number/?ysclid=m5qlp43jzr883232600
// gcc -Wall -g -O0 -o bit_tricks_4 bit_tricks_4.c common.h common.c
/*
 Rotate bits of a number

Bit Rotation: A rotation (or circular shift) is an operation similar to shift
except that the bits that fall off at one end are put back to the other end. In
left rotation, the bits that fall off at left end are put back at right end. In
right rotation, the bits that fall off at right end are put back at left end.

Example:
Let n is stored using 8 bits.
Left rotation of n = 11100101 by 3 makes n = 00101111 (Left shifted by 3 and
first 3 bits are put back in last ). If n is stored using 16 bits or 32 bits
then left rotation of n (000…11100101) becomes 00..0011100101000.

Right rotation of n = 11100101 by 3 makes n = 10111100 (Right
shifted by 3 and last 3 bits are put back in first ) if n is stored using 8
bits. If n is stored using 16 bits or 32 bits then right rotation of n
(000…11100101) by 3 becomes 101000..0011100
*/

/*Function to left rotate n by d bits*/
int leftRotate(int n, unsigned int d) {
    /* In n<<d, last d bits are 0. To put first 3 bits of n
       at last, do bitwise or of n<<d with n >>(INT_BITS -
       d) */
    return (n << d) | (n >> (INT_BITS - d));
}

/*Function to right rotate n by d bits*/
int rightRotate(int n, unsigned int d) {
    /* In n>>d, first d bits are 0. To put last 3 bits of at
            first, do bitwise or of n>>d with n <<(INT_BITS
       - d) */
    return (n >> d) | (n << (INT_BITS - d));
}

/* Driver program to test above functions */
int main() {
    int n = 16;
    int n_rotated_left, n_rotated_right;
    int d = 2;
    displayBits(n);
    printf("Left Rotation of %d by %d is \n", n, d);
    n_rotated_left = leftRotate(n, d);
    displayBits(n_rotated_left);
    printf("%d", n_rotated_left);

    printf(" Right Rotation of %d by %d is \n", n, d);
    n_rotated_right = rightRotate(n, d);
    printf("%d", n_rotated_right);
    displayBits(n_rotated_right);
    return 0;
}
