#!/bin/bash

start_xclip="start"
servis_url="http://192.168.1.54:8088"
# servis_url="http://localhost:8088"

while true; do
    primery_clip=$(xclip -o primery)
    
    if [[ "${primery_clip}" == "${start_xclip}" ]]; then
        sleep 2
    else
        # printf "start start_xclip ${start_xclip}\n"
        # printf "start primery_clip ${primery_clip}\n"

        start_xclip=$primery_clip
        # printf "${primery_clip}\n"
        request=$(curl -s -X POST -F "word=${primery_clip}" ${servis_url}/info)
        printf "$request\n"

        # printf "end start_xclip ${start_xclip}\n"
        # printf "end primery_clip ${primery_clip}\n"
        # printf "########################\n"
        # sleep 15
    fi
done

