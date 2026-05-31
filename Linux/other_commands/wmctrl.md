https://unix.stackexchange.com/questions/22854/how-to-switch-x-windows-from-the-command-line

shows all children of the root window. That also includes some stuff your window manager or desktop renders.
xwininfo -root -children
xwininfo -tree -root | grep "celluloid"

wmctrl -l
wmctrl -lp дополнительно pid
wmctrl -l|awk '{$3=""; $2=""; $1=""; print $0}'

wmctrl -a emacs24
wmctrl -a zilla Get a list of open windows in Linux - Super User — Mozilla Fir...
wmctrl -i -a 0x0380000a
wmctrl -r mozilla -b add,shaded
wmctrl -i -r 0x05c0002c -b add,below на задний план

wmctrl -i -r 0x05c0002c -b add,sticky
wmctrl -i -r 0x0380000a

xdotool search --name "Rocket Launcher"
xdotool windowactivate 37748739

http://twiserandom.com/unix/x11/tools/xprop-a-tutorial/index.html
Displaying a specific property
xprop WM_NAME -name nemo

Do not display the type
xprop -notype -name nemo свойства без типов

Continuously monitoring a windows
xprop -spy -name nemo

Adding a property to a window
$ xwininfo -root -tree | grep xcalc
Find the id, and name of
a window, containing the
term xcalc .
0x800011 "Calculator": ("xcalc" "XCalc") 226x394+138+161 +138+161

$ xprop -name Calculator -format WM_NAME 8s -set WM_NAME Calc
set or update a property
on a window named
Calculator.
The name of the window is first
specified using:
-name Calculator
The -format option, is followed
by the property name, and its
format and type.
The format can be 8, for 8
bits, 16, for 16 bits, and
32, for 32 bits.
The type can be for example,
s for a c string, c for
cardinal, i for
an integer ..
The -set option is used,
to set the value for the
property. So in this case,
the property type is a C
string, so the value is
considered a C string.

$ xprop -name Calc -format MY_PROP_1 32i -set MY_PROP_1 898
In the previous example, the
window name of Calculator,
was changed to Calc. This is
why, in this example the
-name Calc option is used.
This example defines a new
property, it has a format of
32 bits, and is of the integer
type, and its value is set
to 898.

$ xprop MY_PROP_1 -name Calc
Display information, about
the property named MY_PROP_1,
associated with the window
having the name of Calc .
MY_PROP_1(INTEGER) = 898

https://superuser.com/questions/382616/detecting-currently-active-window
$ wmctrl -lp | grep $(xprop -root | grep \_NET_ACTIVE_WINDOW | head -1 | \
 awk '{print $5}' | sed 's/,//' | sed 's/^0x/0x0/')

xprop -root | grep \_NET_ACTIVE_WINDOW | head -1 | awk '{print $5}' | sed 's/,//' | sed 's/^0x/0x0/' идентификатор активного окна

wmctrl -lp | grep $(xprop -root | grep \_NET_ACTIVE_WINDOW | head -1 | awk '{print $5}' | sed 's/,//' | sed 's/^0x/0x0/') информация об активном окне

$ for x in $(seq 1 10); do sleep 5; wmctrl -lp | grep $(xprop -root | \
 grep \_NET_ACTIVE_WINDOW | head -1 | awk '{print $5}' | sed 's/,//' | \
 sed 's/^0x/0x0/'); done
