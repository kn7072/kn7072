#!/bin/bash

start_xclip="start"
start_clipboard="clipboard_"
servis_url="http://192.168.1.53:8088"
servis_url="http://localhost:8088"

while true; do
    primery_clip=$(xclip -o -selection primery)
    clipboard=$(xclip -o -selection clipboard)
    
    if [[ "${primery_clip}" == "${start_xclip}" ]]; then
        if [[ "${clipboard}" != "${start_clipboard}" ]]; then
            start_clipboard=$clipboard
            clear
            request=$(curl -s -X POST -F "word=${primery_clip}" ${servis_url}/word_all_examples)
            printf "$request\n"
        fi
        sleep 2
    else
        # printf "start start_xclip ${start_xclip}\n"
        # printf "start primery_clip ${primery_clip}\n"

	    # озвучиваем слово
        # request=$(curl -s -X POST -F "word=${primery_clip}" ${servis_url}/sound)
        
        start_xclip=$primery_clip
        # printf "${primery_clip}\n"
        clear
        request=$(curl -s -X POST -F "word=${primery_clip}" ${servis_url}/word)
        printf "$request\n"

        # printf "end start_xclip ${start_xclip}\n"
        # printf "end primery_clip ${primery_clip}\n"
        # printf "########################\n"
        # sleep 15
    fi
done

