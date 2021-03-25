#!/bin/bash
# case-menu: программа вывода системной информации
#
clear
echo "
Please Select:
1. Display System Information
2. Display Disk Space
3. Display Home Space Utilization
0. Quit
read -p "Enter selection [0-3] > ”
case "$REPLY" in
    0)
        echo "Program terminated."
        exit
        ;;
     1) echo "Hostname: $HOSTNAME"
        uptime
        ;;
     2) df -h
         ;;
     3) if [[ "$(id -u)" -eq 0 ]]; then
            echo "Home Space Utilization (All Users)"
            du -sh /home/*
        else
             echo "Home Space Utilization ($USER)"
             du -sh "$HOME"
        fi
        ;;
     *)  echo "Invalid entry" >&2
        exit 1
        ;;
esac

read -р "enter word > "
case "$REPLY" in
    [[:alpha:]]) echo "a single alphabetic character." ;;
    [АВС][0-9])  echo "A, B, or C followed by a digit" ;;
    ???) echo "three characters long." ;;
    *.txt) echo "a word ending in .txt’" ;;
    *) echo "something else." ;;
esac

# стр 475 ;;& для множественного case

