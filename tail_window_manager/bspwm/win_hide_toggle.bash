#!/bin/bash

# скрывает текущее окно или восстанавливает скрытые
hidden=$(bspc query -N -n .hidden -d focused)

if [ -z "$hidden" ]; then
  # скрывает текущее окно
  bspc node focused -g hidden=on
else
  for id in $hidden; do
    # отображает все скрытые окна
    bspc node "${id}" -g hidden=off
  done
fi
