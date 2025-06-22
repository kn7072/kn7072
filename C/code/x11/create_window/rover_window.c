#include <unistd.h>
#include <X11/Xlib.h>
#include <X11/Xutil.h>

// gcc -g -O0 -Wall -Werror -Wextra rover_window.c -o rover_window -lX11

int main(void) {
  char *connection_string = NULL;

  Display *mydisplay;
  XSetWindowAttributes myat;
  Window mywindow, rover;
  XWindowChanges alter;
  XSizeHints wmsize;
  XWMHints wmhints;
  XTextProperty windowName, iconName;
  XEvent myevent;
  char *window_name = "Walking";
  char *icon_name = "Wk";
  int screen_num, done;
  unsigned long valuemask;
  int x, y;
  /* 1. open connection to the server */
  mydisplay = XOpenDisplay(connection_string);
  /* 2. create a top−level window */
  screen_num = DefaultScreen(mydisplay);
  myat.background_pixel = WhitePixel(mydisplay, screen_num);
  myat.border_pixel = BlackPixel(mydisplay, screen_num);
  myat.event_mask = ExposureMask | StructureNotifyMask;
  valuemask = CWBackPixel | CWBorderPixel | CWEventMask;
  mywindow = XCreateWindow(
      mydisplay, RootWindow(mydisplay, screen_num), 200, 200, 350, 250, 2, DefaultDepth(mydisplay, screen_num),
      InputOutput, DefaultVisual(mydisplay, screen_num), valuemask, &myat);
  /* 3. give the Window Manager hints */
  wmsize.flags = USPosition | USSize;
  XSetWMNormalHints(mydisplay, mywindow, &wmsize);
  wmhints.initial_state = NormalState;
  wmhints.flags = StateHint;
  XSetWMHints(mydisplay, mywindow, &wmhints);
  XStringListToTextProperty(&window_name, 1, &windowName);
  XSetWMName(mydisplay, mywindow, &windowName);
  XStringListToTextProperty(&icon_name, 1, &iconName);
  XSetWMIconName(mydisplay, mywindow, &iconName);
  /*4. establish window resources*/
  myat.background_pixel = BlackPixel(mydisplay, screen_num);
  /*5. create all the other window sneeded*/
  rover = XCreateWindow(
      mydisplay, mywindow, 100, 30, 50, 70, 2, DefaultDepth(mydisplay, screen_num), InputOutput,
      DefaultVisual(mydisplay, screen_num), valuemask, &myat);

  // rover = XCreateSimpleWindow(
  //     mydisplay,
  //     mywindow,    // parent window
  //                  //  set the parent of top_level_window
  //                  //  to the root window
  //     0,           // x position
  //     0,           // y position
  //     40,          // width
  //     40,          // height
  //     0,           // border width
  //     0xFFFFFFFF,  // border color
  //     0xFFDF0000 /*background color .*/);

  /*6. select events for each window */
  valuemask = CWX | CWY;

  /*7. map the windows*/
  XMapWindow(mydisplay, mywindow);
  // XMapWindow(mydisplay, rover);

  /*8. enter the event loop*/
  // done = 0;
  // while (done == 0) {
  //   XNextEvent(mydisplay, &myevent);
  //   switch (myevent.type) {
  //     case ButtonPress:
  //       break;
  //   }
  // }

  done = 0;
  x = 11;
  y = 12;

  XMapWindow(mydisplay, rover);

  // sleep(20);

  while (done == 0) {
    alter.x = x;
    alter.y = y;
    XConfigureWindow(mydisplay, rover, valuemask, &alter);
    XFlush(mydisplay);
    XNextEvent(mydisplay, &myevent);
    switch (myevent.type) {
      case Expose:
        break;
      case ConfigureNotify:
        XMapWindow(mydisplay, rover);
        sleep(3);
        x += 25;
        y += 6;
    }
  }

  /* 9. clean up before exiting*/
  XUnmapWindow(mydisplay, mywindow);
  XDestroyWindow(mydisplay, mywindow);
  XCloseDisplay(mydisplay);
  return 0;
}
