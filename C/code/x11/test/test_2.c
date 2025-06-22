#include <stdbool.h>
#include <X11/Xlib.h>

// gcc -g -O0 -Wall -Werror -Wextra test_2.c -o test_2 -lX11
// https://groups.google.com/g/comp.windows.x/c/tZhWUJamK_A?pli=1#b73ef31b88abaa05
enum { _NET_WM_STATE_REMOVE = 0, _NET_WM_STATE_ADD = 1, _NET_WM_STATE_TOGGLE = 2 };

int main() {
  Display* pDisplay = XOpenDisplay(NULL);
  int screen = DefaultScreen(pDisplay);

  XSetWindowAttributes attr;
  attr.border_pixel = 0;
  attr.background_pixel = 0;
  attr.event_mask = ExposureMask | StructureNotifyMask;

  Window parentWindow = RootWindow(pDisplay, screen);
  Window window = XCreateWindow(
      pDisplay, parentWindow, 0, 0,  // left top
      640, 480, 0, 0, InputOutput, CopyFromParent, CWBackPixel | CWBorderPixel | CWEventMask, &attr);

  XWarpPointer(pDisplay, None, window, 0, 0, 0, 0, 100, 100);
  XGrabKeyboard(pDisplay, window, True, GrabModeAsync, GrabModeAsync, CurrentTime);
  XMapRaised(pDisplay, window);

  XSelectInput(pDisplay, window, KeyPressMask | ButtonPressMask);
  bool fullScreen = false;
  bool run = true;
  while (run) {
    XEvent event;
    // KeySym keySym;

    while (XPending(pDisplay) > 0) {
      XNextEvent(pDisplay, &event);

      switch (event.type) {
        case KeyPress: {
          fullScreen = !fullScreen;

          Atom wmState = XInternAtom(pDisplay, "_NET_WM_STATE", False);
          Atom fullScreen = XInternAtom(pDisplay, "_NET_WM_STATE_FULLSCREEN", False);

          XEvent xev;
          xev.xclient.type = ClientMessage;
          xev.xclient.serial = 0;
          xev.xclient.send_event = True;
          xev.xclient.window = window;
          xev.xclient.message_type = wmState;
          xev.xclient.format = 32;
          xev.xclient.data.l[0] = (fullScreen ? _NET_WM_STATE_ADD : _NET_WM_STATE_REMOVE);
          xev.xclient.data.l[1] = fullScreen;
          xev.xclient.data.l[2] = 0;

          XSendEvent(
              pDisplay, DefaultRootWindow(pDisplay), False, SubstructureRedirectMask | SubstructureNotifyMask, &xev);
          break;
        }
        case ButtonPress: {
          run = false;
          break;
        }
        default: {
          break;
        }
      }
    }
  }
  XCloseDisplay(pDisplay);
}
