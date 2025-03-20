#include <stdbool.h>
#include <stdio.h>

// gcc -g3 -Wall -O0 -o void_pointer void_pointer.c

void test_asterix(void **a) {
  void *x = a;
  printf("x %d\n", **(int **)x);
  printf("a %d\n", **(int **)a);
}

int main(void) {
  int a = 1;
  int a2 = 2;
  const char *s = "abc";
  bool b = 0;
  bool equil_ptr;
  void *vp;
  void **vpp;
  int *intp;
  int **intpp;

  vp = &a;
  vpp = &vp;

  intp = &a;
  intpp = &intp;

  test_asterix(vpp);

  printf("a = %d, s = %s, b = %b\n", a, s, b);
  printf("vp a = %d, addr (int *)vp = %p, addr a = %p\n", *(int *)vp, (int *)vp,
         &a);

  printf("vpp a = %d\n", *(int *)(vpp));
  printf("vpp a = %d, addr *(int **)vpp = %p, (int **)vpp = %p, vpp = %p, addr "
         "a = %p\n",
         **(int **)vpp, *(int **)vpp, (int **)vpp, vpp, &a);

  if (vpp == (void **)vpp) {
    printf("%s\n", "ok");
  }

  equil_ptr = 1 ? (vpp == ((void **)vpp)) : 0;
  printf("vpp is (void **)vpp %d\n", equil_ptr);

  printf("intp a  value = %d, addr &intp = %p, addr intp = %p, addr a = %p\n",
         *(int *)intp, &intp, intp, &a);
  intp = &a2;
  printf("intp a2 value = %d, addr &intp = %p, addr intp = %p, addr a2 = %p\n",
         *(int *)intp, &intp, intp, &a2);

  printf("intpp value = %d, addr *intpp = %p, addr intpp(&intp) = %p, addr "
         "&intp = "
         "%p, addr intp(a2) = %p\n",
         **intpp, *intpp, intpp, &intp, intp);
  return 0;
}
