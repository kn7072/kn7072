https://github.com/linuxmint/Cinnamon/issues/4871
https://manpages.ubuntu.com/manpages/bionic/en/man1/gsettings.1.html - документация
gsettings list-recursively | sort | uniq | grep -i cursor

io.github.celluloid-player.Celluloid always-autohide-cursor false
io.github.celluloid-player.Celluloid controls-unhide-cursor-speed 0.0
io.github.GnomeMpv always-autohide-cursor false
org.cinnamon.desktop.interface cursor-blink-time 1200
org.cinnamon.desktop.interface cursor-blink-timeout 10
org.cinnamon.desktop.interface cursor-blink true
org.cinnamon.desktop.interface cursor-size 24
org.cinnamon.desktop.interface cursor-theme 'Bibata-Modern-Classic'
org.gnome.desktop.interface cursor-blink-time 1200
org.gnome.desktop.interface cursor-blink-timeout 10
org.gnome.desktop.interface cursor-blink true
org.gnome.desktop.interface cursor-size 24
org.gnome.desktop.interface cursor-theme 'Bibata-Modern-Classic'
org.gnome.yelp show-cursor false
org.mate.interface cursor-blink-time 1200
org.mate.interface cursor-blink true
org.x.editor.preferences.editor restore-cursor-position true
x.dm.slick-greeter cursor-theme-name 'Bibata-Modern-Classic'
x.dm.slick-greeter cursor-theme-size 24


gsettings set org.cinnamon.desktop.interface cursor-blink-time 2000
gsettings set org.cinnamon.desktop.interface cursor-blink-timeout 1200


gsettings list-schemas
gsettings monitor org.cinnamon.desktop.interface отслеживает изменения для данной схемы
gsettings describe org.cinnamon.desktop.interface cursor-blink описание ключа (Whether the cursor should blink.)
gsettings range org.cinnamon.desktop.interface cursor-blink  узнать допустимые значения для ключа, type b означает булево
gsettings get org.cinnamon.desktop.interface cursor-blink узнать значение (в данном примере true)
gsettings reset org.cinnamon.desktop.interface cursor-blink-time сбросить ключ к значению по умолчанию

