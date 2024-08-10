#!/bin/bash

execute_file="flatpak run io.github.xiaoyifang.goldendict_ng ${word}"
start_message="Введите слово:"
while true; do
    echo -n "$start_message"
    read word
    nohup flatpak run io.github.xiaoyifang.goldendict_ng ${word} &
done

