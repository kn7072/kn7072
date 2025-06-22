#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <X11/Xatom.h>
#include <X11/Xlib.h>

// gcc -g -O0 -Wall -Werror -Wextra property_notify_event.c -o property_notify_event -lX11

int main(void) {
  // get a connection to the server
  char* connection_string = NULL;
  Display* display;
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

  XSelectInput(display, top_level_window, ExposureMask | PropertyChangeMask);
  /* Using XSelectInput, register to receive
      notifications, about the Expose and
      PropertyNotify events, using the
      event masks ExposureMask and
      PropertyChangeMask .*/

  XMapWindow(display, top_level_window);
  /* Map the window to be exposed
      later on .*/

  XEvent xevent;
  while (true) {  // handle events
    XNextEvent(display, &xevent);
    switch (xevent.type) {
      case Expose:
        /*When the window is shown,
            change its title .*/
        XChangeProperty(
            display,                      // The connection
            top_level_window,             // The window
            XA_WM_NAME,                   // atom, Property name, set the title
            XA_STRING,                    // atom, Property type
            8,                            // Property format
            PropModeAppend,               // Property mode
            (unsigned char*)"Hey world",  // Property data
            strlen("Hey world"));         // Number of data units
        break;
      case PropertyNotify:
        /*Print the name of the
            property, which is being
            modified .*/
        printf("Property modified is : %s\n", XGetAtomName(display, xevent.xproperty.atom));
        break;
      default:
        break;
    }
  }

  XCloseDisplay(display);
  return 0;
}

/* Output:
Property modified is : WM_NAME
Property modified is : _WINDOWSWM_NATIVE_HWND
Property modified is : WM_STATE */
