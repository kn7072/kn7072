#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

// gcc -g -O0 -Wall -Werror -Wextra struct_fields.c -o struct_fields

struct One {
  int type;
  char *name;
  bool is_one;
};

struct Two {
  int type;
  char *name;
  unsigned unsign;
};

typedef struct One One;
typedef struct Two Two;

union U {
  One one;
  Two two;
};

int main(void) {
  union U myUnion;
  One one = {.type = 1, .name = "one", .is_one = 1};
  Two two = {.type = 2, .name = "two", .unsign = 100};
  myUnion.two = two;
  printf("myUnion.two.type %d, myUnion.two.name %s\n", myUnion.two.type, myUnion.two.name);
  printf("myUnion.one.type %d  myUnion.two.name %s\n", myUnion.one.type, myUnion.one.name);

  // printf("myUnion.two.is_one %d, myUnion.two.unsign %s\n", myUnion.two.is_one, myUnion.two.unsign);

  myUnion.one = one;
  printf("myUnion.two.type %d, myUnion.two.name %s\n", myUnion.two.type, myUnion.two.name);
  printf("myUnion.one.type %d  myUnion.two.name %s\n", myUnion.one.type, myUnion.one.name);
  return EXIT_SUCCESS;
}
