https://unix.stackexchange.com/questions/22854/how-to-switch-x-windows-from-the-command-line

shows all children of the root window. That also includes some stuff your window manager or desktop renders.
xwininfo -root -children
xwininfo -tree -root | grep  "celluloid"

wmctrl -l
wmctrl -lp дополнительно pid
wmctrl -l|awk '{$3=""; $2=""; $1=""; print $0}'

wmctrl -a emacs24
wmctrl -a zilla    Get a list of open windows in Linux - Super User — Mozilla Fir...
wmctrl -i -a 0x0380000a
wmctrl -r mozilla -b add,shaded
wmctrl -i -r 0x05c0002c -b add,below на задний план


wmctrl -i -r 0x05c0002c -b add,sticky
wmctrl -i -r 0x0380000a


https://superuser.com/questions/382616/detecting-currently-active-window
$ wmctrl -lp | grep $(xprop -root | grep _NET_ACTIVE_WINDOW | head -1 | \
    awk '{print $5}' | sed 's/,//' | sed 's/^0x/0x0/')

xprop -root | grep _NET_ACTIVE_WINDOW | head -1 |  awk '{print $5}' | sed 's/,//' | sed 's/^0x/0x0/' идентификатор активного окна

wmctrl -lp | grep $(xprop -root | grep _NET_ACTIVE_WINDOW | head -1 |  awk '{print $5}' | sed 's/,//' | sed 's/^0x/0x0/')  информация об активном окне


$ for x in $(seq 1 10); do sleep 5; wmctrl -lp | grep $(xprop -root | \
    grep _NET_ACTIVE_WINDOW | head -1 | awk '{print $5}' | sed 's/,//' | \
    sed 's/^0x/0x0/'); done
