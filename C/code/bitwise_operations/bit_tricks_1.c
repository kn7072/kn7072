#include <stdio.h>

#include "common.h"
const int x = 32;

// https://www.geeksforgeeks.org/case-conversion-lower-upper-vice-versa-string-using-bitwise-operators-cc/
// gcc -Wall -g -O0 -o bit_tricks_1 bit_tricks_1.c common.h common.c
/*
LSB (least significant bit)
MSB (most significant bit)

ch | ''             Upper case English alphabet ch to lower case
ch & '_'            Lower case English alphabet ch to upper case
x && !(x & x-1)     Checking if given 32-bit integer is power of 2
log2(n & -n)+1      Find the last set bit

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

int main(void) {
    char str[] = "SanjaYKannA";

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
    return 0;
}
