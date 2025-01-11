#include <stdbool.h>
#include <stdio.h>

#include "common.h"
const int x = 32;

// https://www.geeksforgeeks.org/case-conversion-lower-upper-vice-versa-string-using-bitwise-operators-cc/
// https://www.geeksforgeeks.org/count-set-bits-in-an-integer/
// gcc -Wall -g -O0 -o bit_tricks_1 bit_tricks_1.c common.h common.c
/*
LSB (least significant bit)
MSB (most significant bit)

ch | ''             Upper case English alphabet ch to lower case
ch & '_'            Lower case English alphabet ch to upper case
x && !(x & x-1)     Checking if given 32-bit integer is power of 2
log2(n & -n)+1      Find the last set bit
Count set bits in integer
Find log base 2 of 32 bit integer
Checking if given 32-bit integer is power of 2
Find the last set bit
Turn Off kth bit in a number
Turn On kth bit in a number
Check if kth bit is set for a number
Toggle the kth bit
*/

// Converts a string to uppercase
char *toUpperCase(char *a) {
    for (int i = 0; a[i] != '\0'; i++) {
        a[i] = a[i] & ~x;
    }
    return a;
}

// Converts a string to lowercase
char *toLowerCase(char *a) {
    for (int i = 0; a[i] != '\0'; i++) {
        a[i] = a[i] | x;
    }
    return a;
}

/* Function to get no of set bits in binary
representation of positive integer n */
unsigned int countSetBits(unsigned int n) {
    unsigned int count = 0;
    while (n) {
        count += n & 1;
        n >>= 1;
    }
    return count;
}

/* Function to get no of set bits in binary
representation of passed binary no. */
unsigned int countSetBitsKernighan(int n) {
    unsigned int count = 0;
    while (n) {
        n &= (n - 1);
        count++;
    }
    return count;
}

// Find log base 2 of 32 bit integer
int log2number(int x) {
    int res = 0;
    while (x >>= 1) {
        res++;
    }
    return res;
}

// Find the last set bit
int lastSetBit(int n) { return log2number(n & -n) + 1; }

// Checking if given 32-bit integer is power of 2
int isPowerof2(int x) { return (x && !(x & (x - 1))); }

// Turn Off kth bit in a number
int turnOffKthBit(int n, int k) { return n & ~(1 << (k - 1)); }

// Turn On kth bit in a number
int turnOnKthBit(int n, int k) { return n | (1 << (k - 1)); }

// Check if kth bit is set for a number
bool isKthBitSet(int n, int k) { return (n & (1 << (k - 1))) != 0; }

// Toggle the kth bit
int toggleKthBit(int n, int k) { return n ^ (1 << (k - 1)); }

int main(void) {
    char str[] = "SanjaYKannA";
    unsigned int number = 157;
    int number_int;
    unsigned int count = 0;
    /*
    Case conversion (Lower to Upper and Vice Versa) of a string using BitWise
    operators in C/C++

    Given a string, write a function that converts it either from lower to upper
    case or from upper to lower case using the bitwise operators &(AND), |(OR),
    ~(NOT) in place and returns the string. Many of us know that Bitwise
    manipulations are faster than performing arithmetic operations for a compiler
    as the data is stored in binary form 0’s and 1’s. Examples:

    Input : "LowerToUpPer"
    Output : "LOWERTOUPPER"
    Letters already in the uppercase remains the same.
    while rest get converted to uppercase.

    Input : "UPPerTOloweR"
    Output : "uppertolower"
    Letters already in the lowercase remains the same.
    while rest get converted to lowercase.
    */

    /*
    1.Lower to Upper Case This method simply subtracts a value of 32 from the
    ASCII value of lowercase letter by Bitwise ANDing (&) with negation (~) of 32
    converting the letter to uppercase.
    */
    printf("%s\n", toUpperCase(str));

    /*
    2.Upper to Lower Case Similarly, it adds a value of 32 to the ASCII value of
    uppercase letter by Bitwise ORing (|) with 32 converting the letter to
    lowercase.
    */
    printf("%s\n", toLowerCase(str));

    /*
    Count set bits in an integer

    Write an efficient program to count the number of 1s in the binary
    representation of an integer.

    Examples :
    Input : n = 6
    Output : 2
    Binary representation of 6 is 110 and has 2 set bits

    Input : n = 13
    Output : 3
    Binary representation of 13 is 1101 and has 3 set bits
    */

    displayBits(number);
    count = countSetBits(number);
    printf("%d\n", count);

    /*
    Count set bits in an integer - Brian Kernighan’s Algorithm

    Subtracting 1 from a decimal number flips all the bits after the rightmost set
    bit(which is 1) including the rightmost set bit.
    for example :
    10 in binary is 00001010
    9 in binary is  00001001
    8 in binary is  00001000
    7 in binary is  00000111
    So if we subtract a number by 1 and do it bitwise & with itself (n & (n-1)),
    we unset the rightmost set bit. If we do n & (n-1) in a loop and count the
    number of times the loop executes, we get the set bit count. The beauty of
    this solution is the number of times it loops is equal to the number of set
    bits in a given integer.

    1  Initialize count: = 0
    2  If integer n is not zero
      (a) Do bitwise & with (n-1) and assign the value back to n
          n: = n&(n-1)
      (b) Increment count by 1
      (c) go to step 2
    3  Else return count

    Example for Brian Kernighan’s Algorithm:
    n =  9 (1001)
    count = 0

    Since 9 > 0, subtract by 1 and do bitwise & with (9-1)
    n = 9 & 8  (1001 & 1000)
    n = 8
    count  = 1

    Since 8 > 0, subtract by 1 and do bitwise & with (8-1)
    n = 8 & 7  (1000 & 0111)
    n = 0
    count = 2

    Since n = 0, return count which is 2 now.
    */
    count = countSetBitsKernighan(number);
    printf("%d\n", count);

    /*
    Find log base 2 of 32 bit integer
    Logic: We right shift x repeatedly until it becomes 0, meanwhile we keep count
    on the shift operation. This count value is the log2(x).
    */
    number = 4;
    count = log2number(number);
    printf("log2(%d) = %d\n", number, count);

    number = 7;
    count = log2number(7);
    printf("log2(%d) = %d\n", number, count);

    number = 9;
    count = log2number(9);
    printf("log2(%d) = %d\n", number, count);

    /*
    Checking if given 32-bit integer is power of 2

    Logic:
    All the power of 2 have only single bit set e.g. 16 (00010000). If we minus 1
    from this, all the bits from LSB to set bit get toggled, i.e., 16-1 = 15
    (00001111). Now if we AND x with (x-1) and the result is 0 then we can say
    that x is power of 2 otherwise not. We have to take extra care when x = 0.

    Example :
    x =     16(00010000)
    x – 1 = 15(00001111)
    x & (x-1) = 0
    so, 16 is power of 2
    */

    number = 32;
    printf("number %d is power of 2 %d\n", number, isPowerof2(number));
    number = 10;
    printf("number %d is power of 2 %d\n", number, isPowerof2(number));

    /*
    Find the last set bit
    The logarithmic value of AND of x and -x to the base 2 gives the index of the
    last set bit(for 0-based indexing).
    */
    number = 36;
    number_int = 36;
    displayBits(number);
    displayBits(-number);
    displayBits(~number);
    displayBits(number_int);
    displayBits(-number_int);
    displayBits(~number_int);
    printf("last set bit of number %d is %d\n", number, lastSetBit(number));

    /*
    Playing with Kth bit
    1) Turn Off kth bit in a number
    2) Turn On kth bit in a number
    3) Check if kth bit is set for a number
    4) Toggle the kth bit
    */
    number = 37;
    int k = 3;
    displayBits(number);
    printf("Turn off %d bit of number %d\n", k, number);
    count = turnOffKthBit(number, k);
    displayBits(count);

    k = 8;
    printf("Turn on %d bit of number %d\n", k, number);
    count = turnOnKthBit(number, k);
    displayBits(count);

    printf("Check %d bit of number %d is %d\n", k, count, isKthBitSet(count, k));

    printf("Toggle %d bit of number %d\n", k, number);
    count = toggleKthBit(number, k);
    displayBits(count);

    return 0;
}
