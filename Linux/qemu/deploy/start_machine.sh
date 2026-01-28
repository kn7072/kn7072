#!/bin/bash

set -x
echo "machine name $1"
printf -v macaddr "52:54:%02x:%02x:%02x:%02x" $(($"RANDOM" & 0xff)) $(($"RANDOM" & 0xff)) $(($"RANDOM" & 0xff)) $(($"RANDOM" & 0xff))
echo "mac address $macaddr"
# путь к каталогу где находятся образы виртуальных машин
path_to_machine_dir="/media/stepan/ac42ce01-eaac-4d80-a195-8aba8fbb24dd/virtual_machine"
# путь к каталогу где находится скрипт для создания tap интерфейсов
path_to_tap_script="/home/stepan/git_repos/kn7072/Linux/qemu/deploy/create_tap.sh"

if [ -n "$1" ]; then
  nohup qemu-system-x86_64 -hda "$path_to_machine_dir"/"$1" -m 2048 -smp 4 -enable-kvm -device e1000,netdev=net0,mac="$macaddr" -netdev tap,id=net0,script="$path_to_tap_script" &
else
  echo "Error: no virtual machine name"
  exit 1
fi
