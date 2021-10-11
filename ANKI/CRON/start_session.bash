#!/bin/bash
if [ -f ~/LOGS/.Xdbus ]; then
    # source ~/LOGS/.Xdbus;
    # Pause, Play, Stop, PlayPause
	echo "$1"
    # clementine
    source ~/LOGS/.Xdbus; dbus-send --session --type=method_call --dest=org.mpris.MediaPlayer2.clementine /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.$1
    
    # vlc
    # source ~/LOGS/.Xdbus; dbus-send --session --type=method_call --dest=org.mpris.MediaPlayer2.vlc /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.$1
else
    echo "File doesn't exist"
fi
