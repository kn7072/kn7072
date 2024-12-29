#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX 500

// https://c-for-dummies.com/blog/?p=1769
// gcc -g -Wall -O3 -o strsep_1 strsep_1.c
//
int main() {
    char string_x[] =
        "Returns, the , span : of the source , string not ,containing any "
        "character of : the given string., : xxx";
    char **words, *string, *token, *string_dub;
    int a, windex;
    string = string_x;

    /* allocate buffers */
    /* string = (char *)malloc(sizeof(char) * MAX); */
    words = (char **)malloc(sizeof(void *) * MAX / 2);
    /* if (string == NULL || words == NULL) { */
    /*     perror("Unable to allocate memory\n"); */
    /*     exit(1); */
    /* } */

    /* fetch the text */
    printf("Type some text: \n");
    /* fgets(string, MAX, stdin); */
    /* bail on no input */
    /* if (*(string + 0) == '\n') return (0); */

    /* parse words in the text */
    windex = 0;
    while ((*(words + windex) = strsep(&string, ":")) != NULL) {
        printf("%s \n", *(words + windex));
        string_dub = strdup(*(words + windex));
        while ((token = strsep(&string_dub, ",")) != NULL) {
            printf("token-'%s'- len %zd sizeof %zd\n", token, strlen(token), sizeof *token);
            printf("\n");
        }
        printf("%s \n", *(words + windex));

        windex++;
    }
    printf("end of words \n");
    /* output results */
    for (a = 0; a < windex; a++) {
        printf("---start %s \n", *(words + a));
        /* while ((token = strsep((words + a), ",")) != NULL) { */
        /*     printf("%s\n", token); */
        /* } */
        /* printf("--- end %s \n", *(words + a)); */
    }
    // putchar('\n');

    return (0);
}
