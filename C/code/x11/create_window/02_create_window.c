#include <X11/Xlib.h>

// https://hereket.com/posts/linux_creating_x11_windows/
// gcc 02_create_window.c -o 02_create_window -lX11

int main() {
  Display *MainDisplay = XOpenDisplay(0);
  Window RootWindow = XDefaultRootWindow(MainDisplay);

  int WindowX = 0;
  int WindowY = 0;
  int WindowWidth = 800;
  int WindowHeight = 600;
  int BorderWidth = 0;
  int WindowDepth = CopyFromParent;
  int WindowClass = CopyFromParent;
  Visual *WindowVisual = CopyFromParent;

  int AttributeValueMask = CWBackPixel;
  XSetWindowAttributes WindowAttributes = {};
  WindowAttributes.background_pixel = 0xffafe9af;

  Window MainWindow = XCreateWindow(
      MainDisplay, RootWindow, WindowX, WindowY, WindowWidth, WindowHeight, BorderWidth, WindowDepth, WindowClass,
      WindowVisual, AttributeValueMask, &WindowAttributes);

  XMapWindow(MainDisplay, MainWindow);

  for (;;) {
    XEvent GeneralEvent = {};
    XNextEvent(MainDisplay, &GeneralEvent);
  }
}
