// C program to demonstrate snprintf()
#include <stdio.h>

// clang-format off

/*
gcc-14 -g3 -O0 -Wall -Werror -Wextra example_1.c -o example_1 -lX11

gcc-14 -g3 -O0 -Wall -Werror -Wextra  -fsanitize=address -fsanitize=undefined -fno-sanitize-recover=all -fsanitize=float-divide-by-zero -fsanitize=float-cast-overflow -fno-sanitize=null -fno-sanitize=alignment example_1.c -o example_1 -lX11


valgrind --leak-check=full --leak-resolution=med ./example_1
valgrind -s --leak-check=full --track-origins=yes ./example_1

https://www.linux.org.ru/forum/development/2415080?ysclid=macq4ibwao19455801 - пример как исключить ошибки
*/
// clang-format on

void print_str(char* text, int len) {
  int i;
  char c;
  for (i = 0; i < len; i++) {
    // printf("%c", *(text + i));
    c = *(text + i);
    putchar(c);
  }
}

int main() {
  char buffer[50];

  // join two or more strings
  char* str1 = "QUICK";
  char* str2 = "BROWN";
  char* str3 = "LAZY";
  int max_len = sizeof buffer;

  int j = snprintf(buffer, max_len, "12345 %s %s fox jumped over the %s dog.", str1, str2, str3);
  print_str(buffer, max_len);
  printf("%s\n", "");
  buffer[4] = '\0';
  print_str(buffer, max_len);
  puts(buffer);

  printf(
      "\nThe number of bytes printed to 'buffer' "
      "(excluding the null terminator) is %d\n",
      j);
  if (j >= max_len) fputs("Buffer length exceeded; string truncated", stderr);
  puts("Joined string:");
  puts(buffer);

  snprintf(buffer, max_len, "New %s %s %s dog.!", str1, str2, str3);
  print_str(buffer, max_len);

  printf("%s\n", "");
  puts(buffer);
  return 0;
}
