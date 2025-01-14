#include <stdio.h>
#include <string.h>

// gcc -g -Wall -O3 -o strtok_r_2 strtok_r_2.c
int main() {
    char str[] = "Hello, World! Geeks for Geeks.";
    const char outer_delimiters[] = "!.";
    const char inner_delimiters[] = " ,";

    char *token;
    char *outer_saveptr = NULL;
    char *inner_saveptr = NULL;

    token = strtok_r(str, outer_delimiters, &outer_saveptr);

    while (token != NULL) {
        printf("Outer Token: %s\n", token);

        char *inner_token = strtok_r(token, inner_delimiters, &inner_saveptr);

        while (inner_token != NULL) {
            printf("Inner Token: %s\n", inner_token);
            inner_token = strtok_r(NULL, inner_delimiters, &inner_saveptr);
        }

        token = strtok_r(NULL, outer_delimiters, &outer_saveptr);
    }

    return 0;
}
