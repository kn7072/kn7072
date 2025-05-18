1. `curl -L https://sw.kovidgoyal.net/kitty/installer.sh | sh /dev/stdin` Бинарные файлы будут установлены в `~/.local/kitty.app`
2.  Для того чтобы kitty можно было вызывать как из терминала так и из меню приложений, необходимо выполнить команды:

```bash
# Create symbolic links to add kitty and kitten to PATH (assuming ~/.local/bin is in
# your system-wide PATH)
ln -sf ~/.local/kitty.app/bin/kitty ~/.local/kitty.app/bin/kitten ~/.local/bin/

# Place the kitty.desktop file somewhere it can be found by the OS
cp ~/.local/kitty.app/share/applications/kitty.desktop ~/.local/share/applications/

# If you want to open text files and images in kitty via your file manager also add the kitty-open.desktop file
cp ~/.local/kitty.app/share/applications/kitty-open.desktop ~/.local/share/applications/

# Update the paths to the kitty and its icon in the kitty desktop file(s)
sed -i "s|Icon=kitty|Icon=$(readlink -f ~)/.local/kitty.app/share/icons/hicolor/256x256/apps/kitty.png|g" ~/.local/share/applications/kitty*.desktop
sed -i "s|Exec=kitty|Exec=$(readlink -f ~)/.local/kitty.app/bin/kitty|g" ~/.local/share/applications/kitty*.desktop

# Make xdg-terminal-exec (and hence desktop environments that support it use kitty)
echo 'kitty.desktop' > ~/.config/xdg-terminals.list
```
3. Для того чтобы осуществлять поиск без учета регистра необходимо выполнить команду: 
```bash
echo 'set completion-ignore-case On' >> ~/.inputrc
````
4. Конфиг и цветовая схема для kitty уже настроены и лежат в папке `configs`. Содержимое папки нужно скопировать и вставить в папку
`~/.config/kitty`
5. Для корректного отображения цветовой схемы необходимо проверить строку `xterm-color|*-256color) color_prompt=yes;;` в файле `~/.bashrc`
и добавить в нее `xterm-kitty` чтобы получилось
`xterm-color|*-256color|xterm-kitty) color_prompt=yes;;`
`
Источники:
- https://sw.kovidgoyal.net/kitty/binary/
- https://askubuntu.com/questions/87061/can-i-make-tab-auto-completion-case-insensitive-in-bash