// #include <errno.h>
#include <assert.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <X11/X.h>
#include <X11/Xatom.h>
#include <X11/Xlib.h>
#include <X11/Xutil.h>

/* clang-format off
gcc -g -O0 -Wall -Werror -Wextra main.c -o main -lX11

gcc-14 -g3 -O0 -Wall -Werror -Wextra -fsanitize=leak -fsanitize=address -fsanitize=undefined -fno-sanitize-recover=all -fsanitize=float-divide-by-zero -fsanitize=float-cast-overflow -fno-sanitize=null -fno-sanitize=alignment main.c -o main -lX11

clang-format on
*/
// функции для работы с окнами X11
Window *getWindowList(Display *disp, unsigned long *len) {
  // xprop -root _NET_CLIENT_LIST
  Atom prop = XInternAtom(disp, "_NET_CLIENT_LIST", False), type;
  int form;
  unsigned long remain;
  unsigned char *list;

  if (XGetWindowProperty(disp, XDefaultRootWindow(disp), prop, 0, 1024, False, 33, &type, &form, len, &remain, &list) !=
      Success) {
    return 0;
  }
  // XFree(&prop);
  return (Window *)list;
}

int main(void) {
  unsigned long len = 0;
  char *connection_string = NULL;
  Display *disp = NULL;
  Window *window_list = NULL;
  Window root = 0;

  disp = XOpenDisplay(connection_string);
  if (disp == NULL) {
    fprintf(stderr, "Error: XOpenDisplay (%s )\n", connection_string == NULL ? "NULL" : connection_string);
    exit(EXIT_FAILURE);
  }

  root = XDefaultRootWindow(disp);
  unsigned int modifiers = ControlMask;
  unsigned int keycode = XKeysymToKeycode(disp, XK_Y);
  XGrabKey(disp, keycode, modifiers, root, False, GrabModeAsync, GrabModeAsync);
  unsigned int keycode_f = XKeysymToKeycode(disp, XK_F);
  XGrabKey(disp, keycode_f, modifiers, root, False, GrabModeAsync, GrabModeAsync);

  // настройки для дочерних окон
  int window_x = 0;
  int window_y = 0;
  int window_width = 150;   // 800;
  int window_height = 150;  // 600;
  int border_width = 0;
  int window_depth = CopyFromParent;
  int window_class = InputOutput;  // CopyFromParent;
  Visual *window_visual = CopyFromParent;

  int attribute_value_mask =
      CWBackPixel | CWBorderPixel | CWEventMask;  //| CWSaveUnder | CWBackPixmap |
                                                  // CWBorderPixmap;  // CWBackPixel | CWEventMask;
  XSetWindowAttributes window_attributes = {};
  window_attributes.background_pixel = 0xFF112233;
  window_attributes.event_mask = StructureNotifyMask | KeyPressMask | KeyReleaseMask | ExposureMask | FocusChangeMask;

  window_list = getWindowList(disp, &len);
  // char symbol_array_used[len];
  char *symbol_array[] = {"a", "b", "c", "d", "e", "f", "g", "x", "x", "x", "x", "x", "x", "x", "x", "x"};

  for (unsigned long i = 0; i < len; i++) {
    Window window_i = window_list[i];
    Window child_window = 0;
    GC gc; /* Графический контекст */

    fprintf(stdout, "window_id %lu\n", window_i);

    child_window = XCreateWindow(
        disp, window_list[i], window_x, window_y, window_width, window_height, border_width, window_depth, window_class,
        window_visual, attribute_value_mask, &window_attributes);
    fprintf(stdout, "child_window_id %lu\n", child_window);

    gc = XCreateGC(disp, child_window, 0, NULL);

    XFontStruct *fontInfo;
    /* Загружаем шрифт */
    // "-sony-*-*-*-*-*-24-*-*-*-*-*"
    // "*-courier-*"
    if ((fontInfo = XLoadQueryFont(disp, "-sony-*-*-*-*-*-24-*-*-*-*-*")) == NULL) {
      printf("Font not found!\n");
      exit(1);
    }

    XSetForeground(disp, gc, WhitePixel(disp, 0));
    XSetFont(disp, gc, fontInfo->fid);

    // int l = 0;
    // char **x = XListFonts(disp, "*courier*", 9999999, &l);
    // for (int i = 0; i < l; i++) {
    //   fprintf(stdout, "%s\n", x[i]);
    // };
    // Font font = XLoadFont(disp, "-*-tahoma-*-*-*-*-*-*-*-*-*-*");

    XMapWindow(disp, child_window);
    int result = XDrawString(disp, child_window, gc, 70, 70, symbol_array[i], strlen(symbol_array[i]));  // strlen("A")
    if (result == BadValue) printf("   bad value!!!\n");
    if (result == BadWindow) printf("   bad window!!!\n");
    XFreeGC(disp, gc);
    XFlush(disp);
    // XMapWindow(disp, child_window);
  }

  int done = 0;
  int res_send_event = 0;
  Atom prop = XInternAtom(disp, "_NET_ACTIVE_WINDOW", False);
  XEvent event;
  XEvent send_event;
  XWindowAttributes wattr;

  while (done == 0) {
    XNextEvent(disp, &event);
    switch (event.type) {
      case ButtonPress:
        printf("button press\n");
        break;
        // case KeyPress:
        //   printf("key press %d\n", event.xkey.keycode);
        //   break;

      case KeyPress:
        assert(event.xkey.state == modifiers && (event.xkey.keycode == keycode || event.xkey.keycode == keycode_f));
        printf("key_press\n");

        printf(
            "hot key pressed on subwindow %ld, window %ld root %ld keycode %u resending...\n", event.xkey.subwindow,
            event.xkey.window, event.xkey.root, event.xkey.keycode);
        // Window w = event.xkey.subwindow;
        // ekey.display = dis;
        // ekey.window = w;
        // ekey.time = CurrentTime;
        // ekey.type = KeyPress;  // ButtonPress  KeyPress;
        // ekey.state = modifiers;
        // ekey.keycode = keycode;
        // XSendEvent(dis, w, True, KeyPressMask, (XEvent *)&ekey);
        // ekey.type = KeyRelease;
        // XSendEvent(dis, w, True, KeyPressMask, (XEvent *)&ekey);

        // 2 - два окна заняты - это фоновые окна мониторов - для cinnamon
        // int r = (rand() % (len - 2)) + 2;

        // для bspwm
        int r = rand() % len;
        printf("rand index %d\n", r);

        Window test_window = window_list[r];

        memset(&send_event, 0, sizeof(send_event));
        send_event.type = ClientMessage;
        send_event.xclient.display = disp;
        send_event.xclient.window = test_window;
        send_event.xclient.message_type = prop;
        send_event.xclient.format = 32;
        send_event.xclient.data.l[0] = 2L; /* 2 == Message from a window pager */
        send_event.xclient.data.l[1] = CurrentTime;

        XGetWindowAttributes(disp, test_window, &wattr);
        res_send_event =
            XSendEvent(disp, wattr.screen->root, False, SubstructureNotifyMask | SubstructureRedirectMask, &send_event);

        printf("res_send_event %d\n", res_send_event);
        // XSetInputFocus(dis, test_window, RevertToNone, CurrentTime);
        // XRaiseWindow(dis, test_window);
        // XFlush(dis);

        break;

      case PropertyNotify:
        /*Print the name of the property, which is being modified .*/
        // printf("Property modified is : %s\n", XGetAtomName(disp, event.xproperty.atom));
        break;
      case EnterNotify:
        break;
      default:
        break;
    }
  }

  // очистка
  XFree(window_list);
  XCloseDisplay(disp);
  return EXIT_SUCCESS;
}
