#include <assert.h>
#include <stdio.h>
#include <X11/Xlib.h>
#include <X11/Xutil.h>

// https://www.linux.org.ru/forum/development/10260952?ysclid=m9e9ijafhb943335093
// gcc test.c -o test -lX11

int main() {
  XEvent event;
  Display *dis;
  Window root;
  Bool owner_events = False;
  unsigned int modifiers = ControlMask;

  dis = XOpenDisplay(0);
  root = XDefaultRootWindow(dis);
  modifiers = ControlMask;
  unsigned int keycode = XKeysymToKeycode(dis, XK_Y);
  XGrabKey(dis, keycode, modifiers, root, False, GrabModeAsync, GrabModeAsync);
  XEvent e;
  while (1) {
    XNextEvent(dis, &e);
    if (e.type == KeyPress) {
      assert(e.xkey.state == modifiers && e.xkey.keycode == keycode);
      printf(
          "hot key pressed on subwindow %ld, window %ld root %ld resending...\n", e.xkey.subwindow, e.xkey.window,
          e.xkey.root);
      Window w = e.xkey.subwindow;
      static XKeyEvent e;
      e.display = dis;
      e.window = w;
      e.time = CurrentTime;
      e.type = KeyPress;  // ButtonPress  KeyPress;
      e.state = modifiers;
      e.keycode = keycode;
      XSendEvent(dis, w, True, KeyPressMask, (XEvent *)&e);
      XSendEvent(dis, w, True, ButtonPressMask, (XEvent *)&e);
      e.type = KeyRelease;
      XSendEvent(dis, w, True, KeyPressMask, (XEvent *)&e);
    }
  }
}
