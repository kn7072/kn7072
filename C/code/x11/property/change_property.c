#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <X11/Xatom.h>
#include <X11/Xlib.h>

// gcc -g -O0 change_property.c -o change_property -lX11

int main(int argc, char *argv[]) {
  // get a connection to the server
  char *connection_string = NULL;
  Display *display;
  display = XOpenDisplay(connection_string);
  if (display == NULL) {
    fprintf(stderr, "Error: XOpenDisplay (%s )\n", connection_string == NULL ? "NULL" : connection_string);
    exit(EXIT_FAILURE);
  }

  // create a top level window
  Window top_level_window;
  top_level_window = XCreateSimpleWindow(
      display,
      XDefaultRootWindow(display),  // parent window
                                    //  set the parent of top_level_window to the root window
      0,                            // x position
      0,                            // y position
      300,                          // width
      300,                          // height
      0,                            // border width
      0xFFFFFFFF,                   // border color
      0xFF112233 /*background color .*/);

  XChangeProperty(
      display,                       // The connection
      top_level_window,              // The window
      XA_WM_NAME,                    // atom, Property name
      XA_STRING,                     // atom, Property type
      8,                             // Property format
      PropModeAppend,                // Property mode
      (unsigned char *)"Hey world",  // Property data
      strlen("Hey world"));          // Number of data units

  XSelectInput(display, top_level_window, ExposureMask);
  // select the event, we want to handle
  // In this case, the window being exposed

  XMapWindow(display, top_level_window);
  // Register a window to be
  // exposed later on.

  XEvent xevent;
  while (true) {  // handle events
    XNextEvent(display, &xevent);
    switch (xevent.type) {
      case Expose:
      default:
        break;
    }
  }

  XCloseDisplay(display);
  return 0;
}
