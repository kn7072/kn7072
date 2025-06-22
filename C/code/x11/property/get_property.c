#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <X11/Xatom.h>
#include <X11/Xlib.h>

// gcc -g -O0 get_property.c -o get_property -lX11

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

  /*Declare the values, to be returned
      by a call to the XGetWindowProperty
      function. */
  Atom returned_property_type;
  int returned_property_format;
  unsigned long returned_number_data_units;
  unsigned long number_of_bytes_remaining_after_return;
  long *retrieved_data;

  // Getting a property with an invalid name
  int status = XGetWindowProperty(
      display,                                  // The connection
      top_level_window,                         // The window
      XA_WM_NAME,                               // The property name
      0,                                        // offset in 32 bits
      1,                                        // number of elements in 32 bits
      False,                                    // delete
      XA_INTEGER,                               // requested_property_type
      &returned_property_type,                  // returned_property_type
      &returned_property_format,                // returned_property_format
      &returned_number_data_units,              // returned_number_data_units
      &number_of_bytes_remaining_after_return,  // number_of_bytes_remaining_after_return
      (unsigned char **)&retrieved_data /*retrieved_data */);

  printf("Results of getting a property, with an invalid name: \n");
  printf("\tstatus is : %d\n", status);
  /*If returned_property_type is None,
      and both of returned_property_format
      and returned_number_data_units are
      0, then the property name is
      invalid.*/
  printf("\treturned_property_type is : %lu\n", returned_property_type);
  printf("\treturned_property_format is : %d\n", returned_property_format);
  printf("\treturned_number_data_units is : %lu\n\n\n", returned_number_data_units);
  /* Output:
  Results of getting a property, with an invalid name:
      status is : 0
      returned_property_type is : 0
      returned_property_format is : 0
      returned_number_data_units is : 0 */

  // Create an atom for a string
  // which will be used, as our
  // own property name.
  Atom my_prop_atom = XInternAtom(display, "MY_PROPERTY", false);
  int my_prop_data_len = 5;
  long my_prop_data[] = {4294967297, 5, 6, 8, 10};

  // Define a property, on the
  // top level window.
  XChangeProperty(
      display,                        // The connection
      top_level_window,               // The window
      my_prop_atom,                   // atom, Property name
      XA_INTEGER,                     // atom, Property type
      32,                             // Property format
      PropModeAppend,                 // Property mode
      (unsigned char *)my_prop_data,  // Property data
      my_prop_data_len);              // Number of data units

  printf("Results of getting a property, with a valid name: \n");
  long offset = 0;
  long length = 1;
  do {
    status = XGetWindowProperty(
        display,                                  // The connection
        top_level_window,                         // The window
        my_prop_atom,                             // The property name
        offset,                                   // offset in 32 bits
        length,                                   // number of elements in 32 bits
        False,                                    // delete
        XA_INTEGER,                               // requested_property_type
        &returned_property_type,                  // returned_property_type
        &returned_property_format,                // returned_property_format
        &returned_number_data_units,              // returned_number_data_units
        &number_of_bytes_remaining_after_return,  // number_of_bytes_remaining_after_return
        (unsigned char **)&retrieved_data /*retrieved_data */);

    printf("\tstatus is : %d\n", status);
    printf("\treturned_property_type is : %lu\n", returned_property_type);
    printf("\treturned_property_format is : %d\n", returned_property_format);
    printf("\treturned_number_data_units is : %lu\n", returned_number_data_units);
    printf("\tnumber_of_bytes_remaining_after_return is : %lu\n", number_of_bytes_remaining_after_return);
    printf("\tretrieved property data is: %ld\n\n", *retrieved_data);
    offset++;
    XFree(retrieved_data);
  } while (number_of_bytes_remaining_after_return != 0);
  /* Output:
  Results of getting a property, with a valid name:
      status is : 0
      returned_property_type is : 19
      returned_property_format is : 32
      returned_number_data_units is : 1
      number_of_bytes_remaining_after_return is : 16
      retrieved property data is: 1

      status is : 0
      returned_property_type is : 19
      returned_property_format is : 32
      returned_number_data_units is : 1
      number_of_bytes_remaining_after_return is : 12
      retrieved property data is: 5

      status is : 0
      returned_property_type is : 19
      returned_property_format is : 32
      returned_number_data_units is : 1
      number_of_bytes_remaining_after_return is : 8
      retrieved property data is: 6

      status is : 0
      returned_property_type is : 19
      returned_property_format is : 32
      returned_number_data_units is : 1
      number_of_bytes_remaining_after_return is : 4
      retrieved property data is: 8

      status is : 0
      returned_property_type is : 19
      returned_property_format is : 32
      returned_number_data_units is : 1
      number_of_bytes_remaining_after_return is : 0
      retrieved property data is: 10 */

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
