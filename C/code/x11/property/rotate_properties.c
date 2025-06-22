#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <X11/Xlib.h>

// gcc -g -O0 rotate_properties.c -o rotate_properties -lX11

int main(int argc, char *argv[]) {
  // get a connection to the server
  char *connection_string = NULL;
  Display *display;
  display = XOpenDisplay(connection_string);
  if (display == NULL) {
    fprintf(stderr, "Error: XOpenDisplay (%s )\n", connection_string == NULL ? "NULL" : connection_string);
    exit(EXIT_FAILURE);
  }

  Atom atom_prop_1 = XInternAtom(display, "prop_1", false);
  Atom atom_prop_2 = XInternAtom(display, "prop_2", false);
  Atom atom_prop_3 = XInternAtom(display, "prop_3", false);

  int number_properties = 3;
  Atom properties[] = {atom_prop_1, atom_prop_2, atom_prop_3};

  Atom atom_type_int = XInternAtom(display, "type_int", false);

  // Store some properties, on the root window
  for (long i = 0; i < number_properties; i++)
    XChangeProperty(
        display,                     // The connection
        DefaultRootWindow(display),  // The window
        properties[i],               // atom, Property name
        atom_type_int,               // atom, Property type
        32,                          // Property format
        PropModeReplace,             // Property mode
        (unsigned char *)&i,         // Property data
        1);                          // Number of data units

  XRotateWindowProperties(
      display, DefaultRootWindow(display), properties, number_properties,
      1);  // rotate properties by 1

  /* Extract the rotated property values */
  Atom returned_property_type;
  int returned_property_format;
  unsigned long returned_number_data_units;
  unsigned long number_of_bytes_remaining_after_return;
  long *retrieved_data;

  printf("%-18s%-18s%-18s\n", "Property", "Old Value", "New Value");
  for (long i = 0; i < number_properties; i++) {
    XGetWindowProperty(
        display,                                  // The connection
        DefaultRootWindow(display),               // The window
        properties[i],                            // The property name
        0,                                        // offset in 32 bits
        1,                                        // number of elements in 32 bits
        False,                                    // delete
        atom_type_int,                            // requested_property_type
        &returned_property_type,                  // returned_property_type
        &returned_property_format,                // returned_property_format
        &returned_number_data_units,              // returned_number_data_units
        &number_of_bytes_remaining_after_return,  // number_of_bytes_remaining_after_return
        (unsigned char **)&retrieved_data /*retrieved_data */);
    printf("atom_prop_%-8ld  %-18ld %-18ld\n", i, i, *retrieved_data);
  }
  /* Output
      Property          Old Value         New Value
      atom_prop_0         0                  2
      atom_prop_1         1                  0
      atom_prop_2         2                  1 */

  XRotateWindowProperties(
      display, DefaultRootWindow(display), properties, number_properties,
      -1);  // Reset the previous rotation

  XRotateWindowProperties(display, DefaultRootWindow(display), properties, number_properties,
                          2);  // Rotate by 2

  printf("\n\n%-18s%-18s%-18s\n", "Property", "Old Value", "New Value");
  for (long i = 0; i < number_properties; i++) {
    XGetWindowProperty(
        display,                                  // The connection
        DefaultRootWindow(display),               // The window
        properties[i],                            // The property name
        0,                                        // offset in 32 bits
        1,                                        // number of elements in 32 bits
        False,                                    // delete
        atom_type_int,                            // requested_property_type
        &returned_property_type,                  // returned_property_type
        &returned_property_format,                // returned_property_format
        &returned_number_data_units,              // returned_number_data_units
        &number_of_bytes_remaining_after_return,  // number_of_bytes_remaining_after_return
        (unsigned char **)&retrieved_data /*retrieved_data */);
    printf("atom_prop_%-8ld  %-18ld %-18ld\n", i, i, *retrieved_data);
  }
  /* Output:
      Property          Old Value         New Value
      atom_prop_0         0                  1
      atom_prop_1         1                  2
      atom_prop_2         2                  0*/

  for (long i = 0; i < number_properties; i++) XDeleteProperty(display, DefaultRootWindow(display), properties[i]);

  XCloseDisplay(display);
  return 0;
}
