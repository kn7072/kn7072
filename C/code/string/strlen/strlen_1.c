#include <stdio.h>
#include <string.h>

// gcc -g -Wall -O3 -o strlen_1 strlen_1.c
int main(void) {
    const char *ptchar = "1234567890";
    char str[] = "1234567890";

    printf("ptchar %s, strlen %zd sizeof %zd\n", ptchar, strlen(ptchar), sizeof(*ptchar));
    printf("ptchar %s %zd sizeof %zd\n", str, strlen(str), sizeof str);
    printf("sizeof char %zd\n", sizeof(char));
    printf("sizeof *char %zd\n", sizeof(char *));
    printf("sizeof *double %zd\n", sizeof(double *));
    printf("sizeof *void %zd\n", sizeof(void *));
    return 0;
}
