#include "multiple_arg.h"
#include <stdio.h>
#include <stdlib.h>

// clang-format off
// gcc -Wall -Werror -Wextra -std=c11 -g -O0 -o multiple_arg multiple_arguments.c
// clang-format on

int AddStrInt(const char *x, int y) { return atoi(x) + y; }

int AddStrStr(const char *x, const char *y) { return atoi(x) + atoi(y); }

int AddIntInt(int x, int y) { return x + y; }

int AddIntStr(int x, const char *y) { return x + atoi(y); }

int main(void) {
  int result = 0;
  result = Add(100, 999);
  result = Add(100, "999");
  result = Add("100", 999);
  result = Add("100", "999");
  const int a = -123;
  char b[] = "4321";
  result = Add(a, b);
  printf("%d\n", result);

  int c = 1;
  const char d[] = "0";
  result = Add(d, ++c);

  printf("%d\n", result);

  return 0;
}
