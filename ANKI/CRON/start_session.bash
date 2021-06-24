#!/bin/bash
if [ -f ~/LOGS/.Xdbus ]
then
    # source ~/LOGS/.Xdbus;
    source ~/LOGS/.Xdbus; dbus-send --session --type=method_call --dest=org.mpris.MediaPlayer2.clementine /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.PlayPause
else
    echo "File doesn't exist"
fi