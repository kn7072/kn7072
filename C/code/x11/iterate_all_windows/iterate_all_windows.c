#include <stdbool.h>
#include <stdio.h>
#include <X11/Xatom.h>
#include <X11/Xlib.h>

// gcc -g -O0 iterate_all_windows.c -o iterate_all_windows -lX11

Display *dpy;

int x11_get_property_int32(const char *property_name, Display *dpy, Window root_window);
int x11_window_get_pid(Display *dpy, Window wnd);

int x11_get_property_int32(const char *property_name, Display *dpy, Window root_window) {
  // https://gist.github.com/caiorss/639df76864d014ead12936fbd361be73
  Atom p = XInternAtom(dpy, property_name, false);
  Atom actual_type;
  int format;
  unsigned long num_items, bytes_after;
  unsigned char *data = NULL;

  int status = XGetWindowProperty(
      dpy, root_window, p, 0L, 1024L, false, XA_CARDINAL, &actual_type, &format, &num_items, &bytes_after, &data);

  if (status != 0 || num_items < 1) {
    // throw std::runtime_error("Error: failed to get property");
    return -1;
  }
  int value = data[0] | (data[1] << 8) | (data[2] << 16) | (data[3] << 24);
  XFree(data);
  return value;
}

void pwn(Window win) {
  unsigned int nchildren, i;
  Window rw, pw, *cw;
  char *name;

  if (XFetchName(dpy, win, &name)) {
    int pid = x11_window_get_pid(dpy, win);

    printf("%s %d\n", name, pid);
    XFree(name);
  }
  if (XQueryTree(dpy, win, &rw, &pw, &cw, &nchildren)) {
    for (i = 0; i < nchildren; ++i) pwn(cw[i]);
    XFree(cw);
  }
}

//   Note: It only works for X-client applications running on local machine.
int x11_window_get_pid(Display *dpy, Window wnd) {
  return x11_get_property_int32("_NET_WM_PID", dpy, wnd);
}

int main() {
  Window root;

  if ((dpy = XOpenDisplay(NULL))) {
    if ((root = DefaultRootWindow(dpy))) pwn(root);
    XCloseDisplay(dpy);
  }
  return 0;
}
