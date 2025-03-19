#!/usr/bin/env bash

# "$*" стр 472
celluloid "$*" &

# Process ID of the process we just launched
PID=$!

# echo $#
# echo $*

# Window ID of the process...pray that there's     
# only one window! Otherwise this might break.
# We also need to wait for the process to spawn
# a window.

# echo $(wmctrl -lp | grep $(ps -C celluloid  -o pid=) | cut "-d " -f1)
while [ "$WID" == "" ]; do
        WID=$(wmctrl -lp | grep $PID | cut "-d " -f1)
done

echo $WID
# Set the size and location of the window
# See man wmctrl for more info
# gravity,X,Y,width,height
gravity=0
X=2000
Y=100
width=1500
height=900
position="${gravity},${X},${Y},${width},${height}"
wmctrl -i -r $WID -e $position # чтобы окно открылось в нужном месте
sleep 1 # чтобы дождаться пока прогрузится celluloid
wmctrl -i -r $WID -e $position # чтобы размеры окна сработали
