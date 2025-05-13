#include <stdio.h>
#include <string.h>

// gcc -g -Wall -O3 -o strlen_1 strlen_1.c
int main(void) {
  const char *ptchar = "1234567890";
  char str[] = "1234567890";

  printf("ptchar %s, strlen %zd sizeof %zd\n", ptchar, strlen(ptchar), sizeof(*ptchar));
  printf("ptchar %s %zd sizeof %zd\n", str, strlen(str), sizeof str);
  printf("sizeof char %lu\n", sizeof(char));
  printf("sizeof *char %zd\n", sizeof(char *));
  printf("sizeof *double %zd\n", sizeof(double *));
  printf("Size of int: %lu bytes\n", sizeof(int));
  printf("Size of float: %lu bytes\n", sizeof(float));
  printf("Size of double: %lu bytes\n", sizeof(double));
  printf("sizeof *void %zd\n", sizeof(void *));
  printf("sizeof *long %zd\n", sizeof(long *));
  printf("sizeof long %lu\n", sizeof(long));
  printf("sizeof unsigned long %lu\n", sizeof(unsigned long));
  return 0;
}
