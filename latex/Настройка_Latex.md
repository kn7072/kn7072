1.  Установка дистрибутива LaTeX
- Необходимо скачать torrent файл iso образа  c официального сайта
https://www.tug.org/texlive/acquire-iso.html ссылка находится в разделе  Acquiring the ISO using the torrent network
- Необходимо смонтировать образ командой, предварительно создав папку tex2024 по адресу `/mnt/tex2024`. Я переименовал исходный iso файл, что бы не заморачиваться с путями т.к оригинальное название состоит из нескольких слов (я просто убрал все пробелы из названия)
		`mount -t iso9660 -o,loop,noauto /your/texlive.iso /mnt/tex2024`
-  Необходимо перейти в папку `/mnt/tex2024` и выполнить команду 
`sudo perl ./install-tl --no-interaction`  источник информации https://tug.org/texlive/quickinstall.html#running
- Для того чтобы система корректно видела установленный texlive необходимо прописать PATH путь. Необходимо открыть файл `~/.profile` или `~/.bashrc`
и добавить строку `PATH=/usr/local/texlive/2024/bin/x86_64-linux:$PATH`
		



#### Полезные команды

- Посмотреть текущую версию tex live:
	- `tex --version`
	- `latex --version` 
	- `pdflatex --version`
	- `xelatex --version` 
