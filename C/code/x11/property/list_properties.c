#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <X11/Xlib.h>

#define strsize(args...) (snprintf(NULL, 0, args) + sizeof('\0'))

// clang-format off
/*
gcc-14 -g -O0 -Wall -Werror -Wextra list_properties.c -o list_properties -lX11
gcc-14 -g3 -O0 -Wall -Werror -Wextra list_properties.c -o list_properties -lX11

Опция Clang для перехвата чтения неинициализированной памяти: -fsanitize=memory. Эту опцию нельзя комбинировать с -fsanitize=address

gcc-14 -g3 -O0 -Wall -Werror -Wextra -fsanitize=leak -fsanitize=address -fsanitize=undefined -fno-sanitize-recover=all -fsanitize=float-divide-by-zero -fsanitize=float-cast-overflow -fno-sanitize=null -fno-sanitize=alignment list_properties.c -o list_properties -lX11

gcc-14 -g3 -O0 -Wall -Werror -Wextra -fsanitize=address  list_properties.c -o list_properties -lX11

valgrind --leak-check=full --leak-resolution=med ./list_properties
valgrind -s --leak-check=full --track-origins=yes ./list_properties

--log-file="filename"

By default, Valgrind writes its output to stderr. So you need to do something like:
valgrind -s --leak-check=full --track-origins=yes ./list_properties > valgrind_log 2>&1

p (int)XGetWindowProperty( disp, win, prop, 0, 1024, False, AnyPropertyType, &type, &form, &len, &remain, &list)

*/
// clang-format on

Status getGeometry(Display *display, Window win) {
  Window root_return;
  int x_return, y_return;
  unsigned int width_return, height_return;
  unsigned int border_width_return;
  unsigned int depth_return;
  Status status;
  status = XGetGeometry(
      display, win, &root_return, &x_return, &y_return, &width_return, &height_return, &border_width_return,
      &depth_return);
  return status;
}

char *printAttributesWindow(Display *display, Window win) {
  // https://www.tronche.com/gui/x/xlib/window-information/XGetWindowAttributes.html
  XWindowAttributes wattr;
  static char properties[1024];

  XGetWindowAttributes(display, win, &wattr);
  // printf(
  //     "x %d y %d\nwidth %d height %d\ndepth %d\nroot_window %lu\nclass(InputOutput 1, InputOnly 2) %d\nbit_gravity "
  //     "%d\nwin_gravity %d\ncolormap %lu\n"
  //     "map_installed %d\nall_event_masks %lb\nyour_event_mask %lb\n",
  //     wattr.x, wattr.y, wattr.width, wattr.height, wattr.depth, wattr.root, wattr.class, wattr.bit_gravity,
  //     wattr.win_gravity, wattr.colormap, wattr.map_installed, wattr.all_event_masks, wattr.your_event_mask);

  snprintf(
      properties, sizeof properties / sizeof properties[0],
      "x %d y %d\nwidth %d height %d\ndepth %d\nroot_window %lu\nclass(InputOutput 1, InputOnly 2) %d\nbit_gravity "
      "%d\nwin_gravity %d\ncolormap %lu\n"
      "map_installed %d\nall_event_masks %ld\nyour_event_mask %ld\n",
      wattr.x, wattr.y, wattr.width, wattr.height, wattr.depth, wattr.root, wattr.class, wattr.bit_gravity,
      wattr.win_gravity, wattr.colormap, wattr.map_installed, wattr.all_event_masks, wattr.your_event_mask);

  return properties;
}

Window *getWindowList(Display *disp, unsigned long *len) {
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

char *string_copy(char *output, char const *input) {
  char const *x = input;
  char *y = output;
  for (; *x; x++, y++) *y = *x;
  *y = '\0';
  return y;
}

char *printWinProperty(Display *disp, Window win, Atom prop, char *prop_str) {
  // Atom prop = XInternAtom(disp, atom_name, False), type;
  Atom type;
  int form;
  // int size = 1024;
  unsigned long remain, len;
  unsigned char *list;
  char temp_str[1024];
  char storage_str[1024];
  char *val_prop = prop_str;
  char *atom_name;
  // long val;

  if (XGetWindowProperty(
          disp, win, prop, 0, 1024, False, AnyPropertyType, &type, &form, &len, &remain,
          &list) != Success) {  // XA_STRING
    printf("Warning\n");
  }
  // printf("\tname %lu type %lu format %d len %lu remain %lu\n", prop, type, form, len, remain);
  // snprintf(
  //     temp_str, sizeof temp_str / sizeof temp_str[0], "\tname %lu type %lu format %d len %lu remain %lu\n", prop,
  //     type, form, len, remain);
  atom_name = XGetAtomName(disp, prop);
  snprintf(
      temp_str, sizeof temp_str, "\tname %s %lu type %lu format %d len %lu remain %lu\n", atom_name, prop, type, form,
      len, remain);
  XFree(atom_name);
  strcat(storage_str, temp_str);

  // if (len == 0) {
  //   printf("len = 0 %s\n", "0");
  // }
  // http://twiserandom.com/unix/x11/what-is-a-property-in-x11/index.html
  switch (form) {
    case 32:
      // snprintf(temp_str, sizeof(temp_str), "\tretrieved 32 property data is: %d\n\n", *(int *)list);
      // snprintf(temp_str, sizeof(temp_str), "\tretrieved 32 property data is: %d\n\n", ((int *)list)[0]);
      snprintf(temp_str, sizeof(temp_str), "\tretrieved 32 property data is: %d\n\n", len > 0 ? ((int *)list)[0] : -1);

      // snprintf(temp_str, sizeof temp_str / sizeof(long), "\tretrieved 32 property data is: %ld\n\n", *(long *)list);
      //  val = *(int *)list;
      //  snprintf(
      //      temp_str, size, "\tretrieved 32 property data is: %cu\n\n",
      //      *list);  // sizeof temp_str / sizeof temp_str[0]
      break;
    case 8:
      // printf("\tretrieved 8 property data is: %s\n\n", (char *)list);
      snprintf(temp_str, sizeof temp_str / sizeof temp_str[0], "\tretrieved 8 property data is: %s\n\n", (char *)list);
      break;
  }
  // strcat(val_prop, temp_str);
  strcat(storage_str, temp_str);
  memcpy(val_prop, storage_str, sizeof storage_str);
  XFree(list);
  return val_prop;
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

int main(void) {
  // get a connection to the server
  char *connection_string = NULL;
  unsigned long len;
  Display *display;
  Window *list_windows, window_i;
  int i, j = 0;
  char prop_str[1024];

  display = XOpenDisplay(connection_string);
  if (display == NULL) {
    fprintf(stderr, "Error: XOpenDisplay (%s )\n", connection_string == NULL ? "NULL" : connection_string);
    exit(EXIT_FAILURE);
  }

  list_windows = (Window *)getWindowList(display, &len);

  // List the properties of the root window
  Atom *root_window_properties, property_i;
  int number_returned_properties;
  FILE *pointer_file;
  char file_name[1024];
  char *WindowclassName, *properties_window;

  for (i = 0; i < (int)len; i++) {
    window_i = list_windows[i];
    WindowclassName = getClassName(display, window_i);
    snprintf(file_name, sizeof file_name / sizeof file_name[0], "./prop_windows/%s", WindowclassName);
    j++;

    printf("\nWindow name %s\n\n", WindowclassName);
    if (strcmp(WindowclassName, "nemo") == 0) {
      printf("\t\t\t%s\n", "Debug");
    }
    XFree(WindowclassName);

    getGeometry(display, window_i);
    properties_window = printAttributesWindow(display, window_i);

    pointer_file = fopen(file_name, "w");
    if (pointer_file == NULL) {
      fprintf(stderr, "Error message: file not found %s\n", file_name);
      exit(EXIT_FAILURE);
    }
    fputs(properties_window, pointer_file);

    root_window_properties = XListProperties(
        display,                       // The display
        window_i,                      // DefaultRootWindow(display),    // The root window
        &number_returned_properties);  // The number of returned properties.

    if (root_window_properties != NULL) {
      // printf("-------------\n");
      // printf("atom\tname\n");
      fputs("-------------\n", pointer_file);
      fputs("atom\tname\n", pointer_file);
      for (int i = 0; i < number_returned_properties; i++) {
        property_i = root_window_properties[i];
        // printf("%4lu\t%4s\t\n", property_i, XGetAtomName(display, property_i));
        // fputs(properties_window, pointer_file);

        properties_window = printWinProperty(display, window_i, property_i, prop_str);
        // printf("%s\n", "x");
        fputs(properties_window, pointer_file);
        // XFree(properties_window);
      }
    }
    fclose(pointer_file);
    XFree(root_window_properties);
  }
  XFree(list_windows);
  XCloseDisplay(display);
  return 0;
}

/* Output:
atom    name
 241    __NET_DESKTOP_NAMES
 240    _NET_NUMBER_OF_DESKTOPS
 239    _NET_CURRENT_DESKTOP
 243    _NET_SUPPORTED
  38    WM_ICON_SIZE
 232    _XKB_RULES_NAMES
*/
