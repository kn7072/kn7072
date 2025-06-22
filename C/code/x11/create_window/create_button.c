/*This program c r e a t e s a button,
    l a b e l l e d ’ qui t ’ l o c a t e d in a
                window.Clicking *the mouse on t h i s button t e r m i n a t e s
   the execution of t h i s program.The *button has a red background and the l a
   b e l l i n g i s in a yellow font.The *window i t s e l f has a d e f a u l
   t white background.*/

// gcc -g -O0 -Wall -Werror -Wextra create_button.c -o create_button -lX11

#include <string.h>
#include <X11/Xlib.h>
#include <X11/Xutil.h>

int main(void) {
  Display *mydisplay;
  XSetWindowAttributes myat, buttonat;
  Window mywindow, button;
  XSizeHints wmsize;
  XWMHints wmhints;
  XTextProperty windowName, iconName;
  XEvent myevent;
  XColor exact, closest;
  GC mygc;
  XGCValues myvalues;
  char *window_name = "Quit";
  char *icon_name = "Qt";
  int screen_num, done;
  unsigned long valuemask;
  /* 1.open connection to the server */
  mydisplay = XOpenDisplay("");
  /* 2. create a top−level window */
  screen_num = DefaultScreen(mydisplay);
  myat.background_pixel = WhitePixel(mydisplay, screen_num);
  myat.border_pixel = BlackPixel(mydisplay, screen_num);
  valuemask = CWBackPixel | CWBorderPixel;
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
  /* 4. establish window resources */
  XAllocNamedColor(mydisplay, XDefaultColormap(mydisplay, screen_num), "yellow", &exact, &closest);
  myvalues.foreground = exact.pixel;
  XAllocNamedColor(mydisplay, XDefaultColormap(mydisplay, screen_num), "red", &exact, &closest);
  myvalues.background = exact.pixel;
  valuemask = GCForeground | GCBackground;
  mygc = XCreateGC(mydisplay, mywindow, valuemask, &myvalues);
  /* 5. create all the other windows needed */
  valuemask = CWBackPixel | CWBorderPixel | CWEventMask;
  buttonat.border_pixel = BlackPixel(mydisplay, screen_num);
  buttonat.background_pixel = myvalues.background;
  buttonat.event_mask = ButtonPressMask | ExposureMask;
  button = XCreateWindow(
      mydisplay, mywindow, 10, 10, 100, 20, 2, DefaultDepth(mydisplay, screen_num), InputOutput,
      DefaultVisual(mydisplay, screen_num), valuemask, &buttonat);
  /* 6. select events for each windows */
  /* 7. map the windows */
  XMapWindow(mydisplay, mywindow);
  XMapWindow(mydisplay, button);
  /* 8. enter the event loop */
  done = 0;
  while (done == 0) {
    XNextEvent(mydisplay, &myevent);
    switch (myevent.type) {
      case Expose:
        XDrawImageString(mydisplay, button, mygc, 35, 15, "quit", strlen("quit"));
        break;
      case ButtonPress:
        XBell(mydisplay, 100);
        done = 1;
        break;
    }
  }
  /* 9. clean up before exiting */
  XUnmapWindow(mydisplay, mywindow);
  XDestroyWindow(mydisplay, mywindow);
  XCloseDisplay(mydisplay);
}
