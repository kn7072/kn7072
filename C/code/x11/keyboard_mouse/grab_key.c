#include <assert.h>
#include <stdio.h>
#include <string.h>
#include <X11/Xlib.h>
#include <X11/Xutil.h>

// https://www.linux.org.ru/forum/development/10260952?ysclid=m9e9ijafhb943335093
// gcc -g -O0 -Wall -Werror -Wextra grab_key.c -o grab_key -lX11

int main() {
  // XEvent event;
  Display *dis;
  Window root;
  Window test_window;
  // Bool owner_events = False;
  unsigned int modifiers = ControlMask;

  dis = XOpenDisplay(0);
  root = XDefaultRootWindow(dis);
  modifiers = ControlMask;
  unsigned int keycode = XKeysymToKeycode(dis, XK_Y);
  XGrabKey(dis, keycode, modifiers, root, False, GrabModeAsync, GrabModeAsync);
  unsigned int keycode_f = XKeysymToKeycode(dis, XK_F);
  XGrabKey(dis, keycode_f, modifiers, root, False, GrabModeAsync, GrabModeAsync);

  XEvent e;
  XEvent xev;
  // static XKeyEvent ekey;
  static XButtonEvent ebutton;
  Atom prop = XInternAtom(dis, "_NET_ACTIVE_WINDOW", False);
  XWindowAttributes wattr;
  int ret = 0;

  test_window = XCreateSimpleWindow(
      dis,
      root,        // parent window
                   //  set the parent of child_window to the root window
      0,           // x position
      0,           // y position
      300,         // width
      300,         // height
      0,           // border width
      0xFFFFFFFF,  // border color
      0xFFDF0000 /*background color .*/);
  Window w = test_window;

  XMapWindow(dis, test_window);
  XSelectInput(
      dis, test_window,
      PropertyChangeMask | EnterWindowMask | ExposureMask | StructureNotifyMask | ButtonPressMask | ButtonReleaseMask);
  while (1) {
    XNextEvent(dis, &e);
    switch (e.type) {
      case ButtonRelease:
      case ButtonPress:
        /*
         type
        ButtonPress   4
        ButtonRelease 5

        xbutton.button
        1 левая кнопка мыши
        2 колесико
        3 привая
        4 колесико вперед
        5 колесико назад

        6 колесо прокрутки вниз
        7 колесо прокрутки вверх
        8 нижняя кнопка рядом с колесом прокрутки
        9 вверхняя кнопка рядом с колесом прокрутки

         */
        printf("mouse %d state %u, button(detail) %u\n", e.xbutton.type, e.xbutton.state, e.xbutton.button);
        break;
      case EnterNotify:
        printf(
            "enter notify window = %ld root = %ld subwindow = %ld x = %d y = %d focus = %d\n", e.xcrossing.window,
            e.xcrossing.root, e.xcrossing.subwindow, e.xcrossing.x, e.xcrossing.y, e.xcrossing.focus);
        w = test_window;
        ebutton.display = dis;
        ebutton.window = w;
        ebutton.time = CurrentTime;
        ebutton.type = ButtonPress;
        ebutton.state = Button1Mask;
        ebutton.button = Button1;
        XSendEvent(dis, w, True, ButtonPressMask, (XEvent *)&ebutton);
        break;

      case KeyPress:
        assert(e.xkey.state == modifiers && (e.xkey.keycode == keycode || e.xkey.keycode == keycode_f));
        printf("test_window %ld\n", test_window);

        printf(
            "hot key pressed on subwindow %ld, window %ld root %ld keycode %u resending...\n", e.xkey.subwindow,
            e.xkey.window, e.xkey.root, e.xkey.keycode);
        // Window w = e.xkey.subwindow;
        w = test_window;
        // ekey.display = dis;
        // ekey.window = w;
        // ekey.time = CurrentTime;
        // ekey.type = KeyPress;  // ButtonPress  KeyPress;
        // ekey.state = modifiers;
        // ekey.keycode = keycode;
        // XSendEvent(dis, w, True, KeyPressMask, (XEvent *)&ekey);
        // ekey.type = KeyRelease;
        // XSendEvent(dis, w, True, KeyPressMask, (XEvent *)&ekey);

        memset(&xev, 0, sizeof(xev));
        xev.type = ClientMessage;
        xev.xclient.display = dis;
        xev.xclient.window = test_window;
        xev.xclient.message_type = prop;
        xev.xclient.format = 32;
        xev.xclient.data.l[0] = 2L; /* 2 == Message from a window pager */
        xev.xclient.data.l[1] = CurrentTime;

        XGetWindowAttributes(dis, test_window, &wattr);
        ret = XSendEvent(dis, wattr.screen->root, False, SubstructureNotifyMask | SubstructureRedirectMask, &xev);

        printf("ret %d\n", ret);
        // XSetInputFocus(dis, test_window, RevertToNone, CurrentTime);
        // XRaiseWindow(dis, test_window);
        // XFlush(dis);

        break;
    }
  }
  XCloseDisplay(dis);
  return (0);
}
