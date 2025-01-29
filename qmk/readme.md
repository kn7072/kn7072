https://getreuer.info/posts/keyboards/triggers/index.html

организация проекта
https://docs.qmk.fm/#/hardware_keyboard_guidelines?id=ltkeyboard_namehgt

# buffer overflow / empty elf
https://github.com/qmk/qmk_firmware/issues/21720?ysclid=lq6x6ob87t524695899

https://www.rigacci.org/wiki/doku.php/doc/appunti/linux/sa/remap_keyboard_keys
sudo apt install evtest
sudo evtest

если возникла ошибка как показано ниже, необходимо установить sudo apt install gcc-arm-none-eab
⚠ avalanch_2040/v4: RGBLED_SPLIT in config.h is overwriting rgblight.split_count in info.json
/bin/sh: 1: arm-none-eabi-gcc: not found
/bin/sh: 1: arm-none-eabi-gcc: not found
sh: 1: arm-none-eabi-gcc: not found
sh: 1: arm-none-eabi-gcc: not found
gmake: *** [builddefs/common_rules.mk:370: .build/obj_avalanch_2040_v4_test_1/compiler.txt] Error 127


sudo chown $USER:$USER /dev/hidraw1

qmk list-keyboards | grep "iris" -найти полное название клавиатуры

export LANGUAGE=en -ВАЖНО - необходимо выполнить данную команду прежде чем выполнять команды идущие ниже

qmk new-keymap -kb keebio/iris/rev4        создаем keymap - на пример via
qmk compile -kb keebio/iris/rev4 -km via   компилирует клавиатуры с нужным keymap=via
qmk flash -kb keebio/iris/rev4 -km via     заливает бинарник в контроллер клавиатуры

When another key is held
https://getreuer.info/posts/keyboards/triggers/index.html


qmk new-keymap -kb avalanche/v4   /home/stepan/qmk_firmware/keyboards/avalanche/v4/keymaps/stepan
qmk compile -kb avalanche/v4 -km stepan
qmk flash -kb avalanche/v4 -km stepan


qmk new-keymap -kb bastardkb/tbkmini/v2/splinky_3 test_0
qmk compile -kb bastardkb/tbkmini/v2/splinky_3 -km test_0
qmk flash -kb bastardkb/tbkmini/v2/splinky_3 -km test_0

qmk new-keymap -kb avalanche/splinky_3  test_1
qmk compile -kb avalanche/splinky_3  -km test_1
qmk flash -kb avalanche/splinky_3  -km test_1

qmk new-keymap -kb avalanch_2040/v4  test_1
qmk compile -kb avalanch_2040/v4 -km test_1
qmk flash -kb avalanch_2040/v4  -km test_1



qmk new-keymap -kb tbkmini/v2/splinky_3 test_1
qmk compile -kb tbkmini/v2/splinky_3 -km test_1
qmk flash -kb tbkmini/v2/splinky_3  -km test_1

qmk new-keymap -kb bastardkb/scylla/v2/splinky_3
qmk compile -kb bastardkb/scylla/v2/splinky_3 -km test_1

необходимо установить qmk под админом
сначала выполнить sudo su, а дальше согласно официальной инструкции
qmk console -l
qmk console -d CEE2:0004:1

which qmk -получаем адрес
cd /home/stepan/.pyenv/shims
sudo /home/stepan/.pyenv/shims/qmk console -l
sudo /home/stepan/.pyenv/shims/qmk console -d CEE2:0004:1

showkey -a
You could try, and Ctrl + D to exit:

/home/stepan/qmk_firmware/keyboards/work_louder/micro


make avalanch_2040/v4:vial
make avalanch_2040/v4:vial:flash

make avalanch_2040/v4:test_1
make avalanch_2040/v4:vial:test_1


qmk compile -kb avalanch_2040/v4 -km vial
qmk flash -kb avalanch_2040/v4 -km vial
