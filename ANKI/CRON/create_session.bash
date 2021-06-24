#!/bin/bash
PATH_DIR_SESSION=~/LOGS

if [[ ! -d "$PATH_DIR_SESSION" ]]; then
    mkdir "$PATH_DIR_SESSION"
fi


touch ~/LOGS/.Xdbus
chmod 666 ~/LOGS/.Xdbus
env | grep DBUS_SESSION_BUS_ADDRESS > ~/LOGS/.Xdbus
echo 'export DBUS_SESSION_BUS_ADDRESS' >> ~/LOGS/.Xdbus