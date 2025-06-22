#include <X11/Xlib.h>
#include <X11/Xutil.h>

// https://hereket.com/posts/linux_creating_x11_windows/
// gcc 03_create_window_with_events.c -o 03_create_window_with_events -lX11

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

  int AttributeValueMask = CWBackPixel | CWEventMask;
  XSetWindowAttributes WindowAttributes = {};
  WindowAttributes.background_pixel = 0xffffccaa;
  WindowAttributes.event_mask = StructureNotifyMask | KeyPressMask | KeyReleaseMask | ExposureMask;

  Window MainWindow = XCreateWindow(
      MainDisplay, RootWindow, WindowX, WindowY, WindowWidth, WindowHeight, BorderWidth, WindowDepth, WindowClass,
      WindowVisual, AttributeValueMask, &WindowAttributes);

  XMapWindow(MainDisplay, MainWindow);

  int IsWindowOpen = 1;
  while (IsWindowOpen) {
    XEvent GeneralEvent = {};
    XNextEvent(MainDisplay, &GeneralEvent);

    switch (GeneralEvent.type) {
      case KeyPress:
      case KeyRelease: {
        XKeyPressedEvent *Event = (XKeyPressedEvent *)&GeneralEvent;
        if (Event->keycode == XKeysymToKeycode(MainDisplay, XK_Escape)) {
          IsWindowOpen = 0;
        }
      } break;
    }
  }
}
