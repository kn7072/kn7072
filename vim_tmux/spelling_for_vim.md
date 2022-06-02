## Проверка орфографии в vim

##### Водим в консоль:
1. mkdir -p ~/.vim/spell
2. cd ~/.vim/spell
3. `Словари для русского языка`
   1.  wget http://ftp.vim.org/vim/runtime/spell/ru.utf-8.sug
   2.  wget http://ftp.vim.org/vim/runtime/spell/ru.utf-8.spl
4. `Словари для английскоо языка`
   1. wget http://ftp.vim.org/vim/runtime/spell/en.utf-8.spl
   2. wget http://ftp.vim.org/vim/runtime/spell/en.utf-8.sug
5. Переходим в папку с конфигурационный файл vim -> **~/.config/nvim**
6. Добавляем строки в файл **init.vim** строку `set spell spelllang=ru,en_us`

##### Вкл/выкл проверку орфографии:
`:set spell/spell!`

##### Некоторые команды:

Следующее слово с ошибкой: 
]s
Предыдущее слово с ошибкой:
[s
Добавить в словарь:
zg
Убрать из словаря:
zw
Игнорировать слово:
zG

Источники:
1. https://blog.amet13.name/2013/08/vim_14.html
2. https://neovim.io/doc/user/spell.html


