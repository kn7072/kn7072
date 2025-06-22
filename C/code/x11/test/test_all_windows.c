#include <errno.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <X11/X.h>
#include <X11/Xatom.h>
#include <X11/Xlib.h>
#include <X11/Xutil.h>

// gcc -g -O0 -Wall -Werror -Wextra test_all_windows.c -o test_all_windows -lX11

// функции для работы с окнами X11
Window *getWindowList(Display *disp, unsigned long *len) {
  // xprop -root _NET_CLIENT_LIST
  Atom prop = XInternAtom(disp, "_NET_CLIENT_LIST", False), type;
  int form;
  unsigned long remain;
  unsigned char *list;

  if (XGetWindowProperty(
          disp, XDefaultRootWindow(disp), prop, 0, 1024, False, 33, &type, &form, len, &remain,
          &list) != Success) {  // XA_WINDOW
    return 0;
  }

  return (Window *)list;
}

char *getWindowName(Display *disp, Window win) {
  Atom prop = XInternAtom(disp, "WM_NAME", False), type;
  int form;
  unsigned long remain, len;
  unsigned char *list;

  if (XGetWindowProperty(
          disp, win, prop, 0, 1024, False, AnyPropertyType, &type, &form, &len, &remain,
          &list) != Success) {  // XA_STRING
    return NULL;
  }

  return (char *)list;
}

char *getClassName(Display *disp, Window win) {
  Atom prop = XInternAtom(disp, "WM_CLASS", False), type;
  int form;
  unsigned long remain, len;
  unsigned char *list;

  if (XGetWindowProperty(
          disp, win, prop, 0, 1024, False, AnyPropertyType, &type, &form, &len, &remain,
          &list) != Success) {  // XA_STRING

    return NULL;
  }

  return (char *)list;
}

Window getActiveWindow(Display *disp, Window win) {
  Atom prop = XInternAtom(disp, "_NET_ACTIVE_WINDOW", False), type;
  int form;
  unsigned long remain, len;
  unsigned char *list;
  Window root = DefaultRootWindow(disp);

  if (XGetWindowProperty(
          disp, root, prop, 0, 0x7fffffff, False, XA_WINDOW, &type, &form, &len, &remain,
          &list) != Success) {  // XA_STRING
    printf("null %ld\n", win);
    return 0;
  };
  Window active_win = ((Window *)list)[0];
  printf("current_win %ld, active_win %ld\n", win, active_win);
  return active_win;
}

int main(void) {
  // теперь пройдёмся по открытым окнам в ОС
  int i, done;
  int revert_to_return = -1;
  unsigned long len;
  XEvent myevent;
  Display *disp = XOpenDisplay(0);
  Window *list;
  Window child_window;
  Window test_window;
  Window RootWindow = XDefaultRootWindow(disp);
  int DefaultScreen = DefaultScreen(disp);

  char *name, *class_name;
  Window isActiveWindow;
  // Time time = 3;
  int WindowX = 0;
  int WindowY = 0;
  int WindowWidth = 70;   // 800;
  int WindowHeight = 70;  // 600;
  int BorderWidth = 5;
  int WindowDepth = CopyFromParent;
  int WindowClass = InputOutput;  // CopyFromParent;
  Visual *WindowVisual = CopyFromParent;

  int AttributeValueMask = CWBackPixel | CWBorderPixel | CWEventMask | CWSaveUnder | CWBackPixmap |
                           CWBorderPixmap;  // CWBackPixel | CWEventMask;
  XSetWindowAttributes WindowAttributes = {};
  WindowAttributes.background_pixel = 0xFF112233;
  WindowAttributes.event_mask = StructureNotifyMask | KeyPressMask | KeyReleaseMask | ExposureMask | FocusChangeMask;
  Pixmap back;
  // Atom prop = XInternAtom(disp, "_NET_ACTIVE_WINDOW", False);

#define result_width 50
#define result_height 50
  static char result_bits[] = {
    0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x08,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x08,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x40,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x40, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x08,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00};

  list = (Window *)getWindowList(disp, &len);
  for (i = 0; i < (int)len; i++) {
    name = getWindowName(disp, list[i]);
    class_name = getClassName(disp, list[i]);
    isActiveWindow = getActiveWindow(disp, list[i]);

    XMoveResizeWindow(disp, list[i], 100 + i * 50, 100 + i * 50, 500, 700);  // изменяет размер и положение окна
    // XSetWindowBorder(disp, list[i], BlackPixel(disp, DefaultScreen));
    // XSetWindowBorder(disp, list[i], WhitePixel(disp, DefaultScreen));
    // XSetWindowBorderWidth(disp, list[i], 15);
    //
    //
    // child_window = XCreateSimpleWindow(
    //     disp,
    //     list[i],        // parent window
    //                     //  set the parent of child_window to the root window
    //     0,              // x position
    //     0,              // y position
    //     result_width,   // width
    //     result_height,  // height
    //     0,              // border width
    //     0xFFFFFFFF,     // border color
    //     0xFF112233 /*background color .*/);

    XSetWindowAttributes WindowAttributes_new = {};
    // WindowAttributes_new.background_pixel = 0xFF112233;
    WindowAttributes_new.event_mask = StructureNotifyMask | KeyPressMask | KeyReleaseMask | ExposureMask |
                                      FocusChangeMask | CWBackPixmap | CWColormap;

    child_window = XCreateWindow(
        disp, list[i], WindowX, WindowY, WindowWidth, WindowHeight, BorderWidth, WindowDepth, WindowClass, WindowVisual,
        AttributeValueMask, &WindowAttributes_new);

    back = XCreatePixmapFromBitmapData(
        disp, child_window, result_bits, result_width, result_height, BlackPixel(disp, DefaultScreen),
        WhitePixel(disp, DefaultScreen), DefaultDepth(disp, DefaultScreen));
    // WindowAttributes_new.background_pixmap = ParentRelative;
    // XSetWindowBackgroundPixmap(disp, child_window, back);

    XMapWindow(disp, child_window);
    XSelectInput(disp, child_window, KeyPressMask | PropertyChangeMask | EnterWindowMask | ButtonPressMask);

    // XSelectInput(disp, list[i], KeyPressMask);

    // XGetInputFocus(disp, &list[i], &revert_to_return);
    /* revert_to_return содежит константу определяющую куда будет возвращен фокус когда
      окно перестанет быть видимым
      Returns the current focus state (RevertToParent, RevertToPointerRoot, or RevertToNone).
     определены в X.h
     RevertToParent		2

     • If revert_to is RevertToParent, the focus reverts to the parent (or the closest viewable
        ancestor), and the new revert_to value is taken to be RevertToNone.
     • If revert_to is RevertToPointerRoot or RevertToNone, the focus reverts to PointerRoot
        or None, respectively. When the focus reverts, the X server generates FocusIn and Focu-
        sOut ev ents, but the last-focus-change time is not affected.
    */
    // free(name);
    printf(
        "name %s | class name %s | is_active %s | revert_to_return %d\n", name, class_name,
        isActiveWindow == list[i] ? "on" : "off", revert_to_return);
  }

  // test_window = XCreateSimpleWindow(
  //     disp,
  //     XDefaultRootWindow(disp),  // parent window
  //                                //  set the parent of child_window to the root window
  //     0,                         // x position
  //     0,                         // y position
  //     100,                       // width
  //     100,                       // height
  //     0,                         // border width
  //     0xFFFFFFFF,                // border color
  //     0xFFDF0000 /*background color .*/);
  test_window = XCreateWindow(
      disp, RootWindow, WindowX, WindowY, WindowWidth, WindowHeight, BorderWidth, WindowDepth, WindowClass,
      WindowVisual, AttributeValueMask, &WindowAttributes);

  XMapWindow(disp, test_window);
  XSelectInput(
      disp, test_window,
      KeyPressMask | KeyReleaseMask | PropertyChangeMask | EnterWindowMask | ExposureMask | StructureNotifyMask);
  XMapWindow(disp, test_window);
  XSelectInput(disp, test_window, KeyPressMask | PropertyChangeMask | EnterWindowMask | ButtonPressMask);

  back = XCreatePixmapFromBitmapData(
      disp, test_window, result_bits, result_width, result_height, BlackPixel(disp, DefaultScreen),
      WhitePixel(disp, DefaultScreen), DefaultDepth(disp, DefaultScreen));
  XSetWindowBackgroundPixmap(disp, test_window, back);

  // XSelectInput(disp, test_window, StructureNotifyMask | KeyPressMask | KeyReleaseMask | ExposureMask |
  // FocusChangeMask);

  // | ButtonPressMask
  printf("error before focus %d %s\n", errno, strerror(errno));
  // for (i = 0; i < (int)len; i++) {
  //   sleep(2);
  //   XSetInputFocus(disp, list[i], RevertToNone, CurrentTime);  // CurrentTime
  //   XRaiseWindow(disp, list[i]);
  //   XFlush(disp);
  //
  //   if (errno != 0) {
  //     printf("%d %s\n", errno, strerror(errno));
  //   }
  // }
  printf("len %d after for \n", (int)len);

  done = 0;
  while (done == 0) {
    XNextEvent(disp, &myevent);
    switch (myevent.type) {
      case ButtonPress:
        printf("button press\n");

        break;
      case KeyPress:
        printf("key press %d\n", myevent.xkey.keycode);
        break;
      case PropertyNotify:
        /*Print the name of the
            property, which is being
            modified .*/
        // printf("Property modified is : %s\n", XGetAtomName(disp, myevent.xproperty.atom));
        break;
      case EnterNotify:
        printf("test_window %ld\n", test_window);
        printf(
            "enter notify window = %ld root = %ld subwindow = %ld x = %d y = %d focus = %d\n", myevent.xcrossing.window,
            myevent.xcrossing.root, myevent.xcrossing.subwindow, myevent.xcrossing.x, myevent.xcrossing.y,
            myevent.xcrossing.focus);
        XSetInputFocus(disp, test_window, RevertToNone, CurrentTime);
        XRaiseWindow(disp, test_window);

        XFlush(disp);
        // XChangeProperty(
        //     disp,                           // The connection
        //     test_window,                    // The window
        //     prop,                           // atom, Property name
        //     XA_WINDOW,                      // atom, Property type
        //     32,                             // Property format
        //     PropModeReplace,                // PropModeReplace PropModeAppend Property mode
        //     (unsigned char *)&test_window,  // Property data
        //     8);                             // sizeof(test_window));          // Number of data units

        break;
      default:
        break;
    }
  }

  /* 9. clean up before exiting*/
  // XUnmapWindow(mydisplay, mywindow);
  // XDestroyWindow(mydisplay, mywindow);
  XCloseDisplay(disp);

  return 0;
}

/*
 https://ubuntuincident.wordpress.com/2013/01/10/find-window-by-its-name-and-activate-it-bring-to-foreground/
xdotool search --name "Rocket Launcher"
xdotool windowactivate 37748739
 *
 * */
