#include <stdio.h>
#include <X11/Xlib.h>
#include <X11/Xutil.h>

// https://hereket.com/posts/linux_creating_x11_windows/
// gcc 04_rectangles_and_action.c -o 04_rectangles_and_action -lX11

typedef struct {
  int X;
  int Y;
  int Width;
  int Height;
} entity;

int main() {
  Display *MainDisplay = XOpenDisplay(0);
  Window RootWindow = XDefaultRootWindow(MainDisplay);

  int DefaultScreen = DefaultScreen(MainDisplay);
  GC Context = XDefaultGC(MainDisplay, DefaultScreen);

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
  WindowAttributes.event_mask = StructureNotifyMask | KeyPressMask | KeyReleaseMask | ExposureMask | FocusChangeMask;

  Window MainWindow = XCreateWindow(
      MainDisplay, RootWindow, WindowX, WindowY, WindowWidth, WindowHeight, BorderWidth, WindowDepth, WindowClass,
      WindowVisual, AttributeValueMask, &WindowAttributes);

  XMapWindow(MainDisplay, MainWindow);

  XStoreName(MainDisplay, MainWindow, "Moving rectangle. Use arrow keys to move.");

  Atom WM_DELETE_WINDOW = XInternAtom(MainDisplay, "WM_DELETE_WINDOW", False);
  if (!XSetWMProtocols(MainDisplay, MainWindow, &WM_DELETE_WINDOW, 1)) {
    printf("Couldn't register WM_DELETE_WINDOW property \n");
  }

  entity Box = {};
  Box.Width = 50;
  Box.Height = 80;
  Box.X = WindowWidth / 2 - Box.Width / 2;
  Box.Y = WindowHeight / 2 - Box.Height / 2;
  int StepSize = 5;

  int IsWindowOpen = 1;
  while (IsWindowOpen) {
    XEvent GeneralEvent = {};

    XNextEvent(MainDisplay, &GeneralEvent);

    switch (GeneralEvent.type) {
      case FocusIn: {
        printf("focus_in\n");
      } break;
      case FocusOut: {
        printf("focus_out\n");

      } break;

      case KeyPress:
      case KeyRelease: {
        XKeyPressedEvent *Event = (XKeyPressedEvent *)&GeneralEvent;
        if (Event->keycode == XKeysymToKeycode(MainDisplay, XK_Escape)) {
          IsWindowOpen = 0;
        }

        if (Event->keycode == XKeysymToKeycode(MainDisplay, XK_Down)) {
          Box.Y += StepSize;
          printf("down\n");
        } else if (Event->keycode == XKeysymToKeycode(MainDisplay, XK_Up)) {
          Box.Y -= StepSize;
        } else if (Event->keycode == XKeysymToKeycode(MainDisplay, XK_Right)) {
          Box.X += StepSize;
        } else if (Event->keycode == XKeysymToKeycode(MainDisplay, XK_Left)) {
          Box.X -= StepSize;
        }
      } break;

      case ClientMessage: {
        XClientMessageEvent *Event = (XClientMessageEvent *)&GeneralEvent;
        if ((Atom)Event->data.l[0] == WM_DELETE_WINDOW) {
          XDestroyWindow(MainDisplay, MainWindow);
          IsWindowOpen = 0;
        }
      } break;
    }

    XClearWindow(MainDisplay, MainWindow);
    XFillRectangle(MainDisplay, MainWindow, Context, Box.X, Box.Y, Box.Width, Box.Height);
  }
}
