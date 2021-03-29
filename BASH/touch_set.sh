#!/bin/bash
# trouble: сценарий для демонстрации распространенных видов ошибок
number=1
set -x # Включить трассировку
if [ $number = 1 ]; then
    echo "Number is equal to 1."
else
    echo "Number is not equal to 1."
fi
set +x # Выключить трассировку
