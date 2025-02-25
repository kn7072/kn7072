#include <stdio.h>

// gcc -Wall -Werror -Wextra -std=c11 -g -O0 -o print_macro print_macro.c
void print_int(int x) { printf("int: %d\n", x); }

void print_dbl(double x) { printf("double: %g\n", x); }

void print_default() { puts("unknown argument"); }

#define print(X)                                                               \
  _Generic((X), int: print_int, double: print_dbl, default: print_default)(X)

int main(void) {
  print(42);
  print(3.14);
  print("hello, world");
}
