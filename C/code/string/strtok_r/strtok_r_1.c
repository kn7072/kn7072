#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// gcc -g -Wall -O3 -o strtok_r_1 strtok_r_1.c
// 1,2:3,4:5,6|,|:
// 1, 2:3, 4:5,6#,#:
int main(int argc, char *argv[]) {
    char *str1, *str2, *token, *subtoken;
    char *saveptr1, *saveptr2;
    int j;

    if (argc != 4) {
        fprintf(stderr, "Usage: %s string delim subdelim\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    for (j = 1, str1 = argv[1];; j++, str1 = NULL) {
        token = strtok_r(str1, argv[2], &saveptr1);
        if (token == NULL) break;
        printf("%d: %s\n", j, token);

        for (str2 = token;; str2 = NULL) {
            subtoken = strtok_r(str2, argv[3], &saveptr2);
            if (subtoken == NULL) break;
            printf(" --> %s\n", subtoken);
        }
    }

    exit(EXIT_SUCCESS);
}
