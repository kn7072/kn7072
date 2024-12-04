#include <stdio.h>
#include <sys/sdt.h>
#include <sys/time.h>
#include <unistd.h>

static long myclock() {
  struct timeval tv;
  gettimeofday(&tv, NULL);
  DTRACE_PROBE1(tracetest, testprobe, tv.tv_sec);
  return tv.tv_sec;
}

int main(int argc, char **argv) {
  while (1) {
    myclock();
    sleep(1);
  }
  return 0;
}
