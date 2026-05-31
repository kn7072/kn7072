# Узнать тип графического интерфейса Ubuntu
__ls /usr/bin/*session__ 
пример вывода 
/usr/bin/dbus-run-session /usr/bin/gnome-session /usr/bin/gnome-session-custom-session 
из примера видно, что установлен gnome

# Если вам нужно узнать установлен ли X server в принципе выполните 
__dpkg -l | grep xserver__

# Эту же команду можно использовать для определения типа 
__dpkg -l|egrep -i "(kde|gnome|lxde|xfce|mint|unity|fluxbox|openbox)" | grep -v library__
Информации будет довольно много, но почти во всех строках будет упоминаться тип иксов
В выводе на моей Ubuntu есть например такая строка 
…
ii    gdm3    3.36.3-0ubuntu0.20.04.2    amd64    __GNOME Display Manager__
…