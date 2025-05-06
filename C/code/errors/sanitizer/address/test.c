#include <stdio.h>
#include <stdlib.h>

/*
gcc -g3 -O0 -Wall -Wextra -fsanitize=address ./test.c -o ./main

gcc -g3 -O0 -Wall -Wextra ./test.c -o ./main
valgrind --leak-check=full --leak-resolution=med ./main
*/

int main(void) {
  int *m = (int *)malloc(10 * sizeof(int));

  for (int i = 0; i < 11; i++) {  // 11 - error, 10 - ok
    m[i] = i;
  }
  printf("%s\n", "");
  free(m);
  return 0;
}
