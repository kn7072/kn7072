#!/bin/bash

set -x
echo "machine name $1"
printf -v macaddr "52:54:%02x:%02x:%02x:%02x" $(($"RANDOM" & 0xff)) $(($"RANDOM" & 0xff)) $(($"RANDOM" & 0xff)) $(($"RANDOM" & 0xff))
echo "mac address $macaddr"

if [ -n "$1" ]; then
  nohup qemu-system-x86_64 -hda /media/stepan/ac42ce01-eaac-4d80-a195-8aba8fbb24dd/virtual_machine/"$1".qcow -m 2048 -smp 4 -enable-kvm -device e1000,netdev=net0,mac="$macaddr" -netdev tap,id=net0,script=//media/stepan/ac42ce01-eaac-4d80-a195-8aba8fbb24dd/virtual_machine/create_tap.sh &
#&
else
  echo "Error: no vintual machine name"
  exit 1
fi
