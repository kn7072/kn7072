#include <unistd.h>
#include <X11/Xlib.h>

// gcc 01_simple_window.c -o 01_simple_window -lX11

int main() {
  Display *MainDisplay = XOpenDisplay(0);
  Window RootWindow = XDefaultRootWindow(MainDisplay);

  Window MainWindow = XCreateSimpleWindow(MainDisplay, RootWindow, 0, 0, 800, 600, 0, 0, 0x00aade87);
  XMapWindow(MainDisplay, MainWindow);
  XFlush(MainDisplay);

  for (;;) {
    sleep(1);
  }
}
