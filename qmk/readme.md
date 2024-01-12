
# buffer overflow / empty elf
https://github.com/qmk/qmk_firmware/issues/21720?ysclid=lq6x6ob87t524695899


qmk list-keyboards | grep "iris" -найти полное название клавиатуры

export LANGUAGE=en -ВАЖНО - необходимо выполнить данную команду прежде чем выполнять команды идущие ниже

qmk new-keymap -kb keebio/iris/rev4        создаем keymap - на пример via
qmk compile -kb keebio/iris/rev4 -km via   компилирует клавиатуры с нужным keymap=via
qmk flash -kb keebio/iris/rev4 -km via     заливает бинарник в контроллер клавиатуры 




