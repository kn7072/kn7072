# создание диска
qemu-img create -f qcow2 test.qcow 10G

# устанавливаем операционную систему на созданный диск
qemu-system-x86_64 -hda test.qcow -boot d -cdrom /home/stapan/debian-11.3.0-amd64-netinst.iso -m 2048

# запуск виртуалкизш
qemu-system-x86_64 -hda /home/stapan/test.qcow -m 2048 -enable-kvm

su root
apt update
apt upgrade
apt install sudo

# выдаем не рутовому пользователю - stepan права на запуск sudo
sudo usermod -aG sudo stepan
# установливаем графическую среду i3
sudo apt install x-window-system i3 i3status dmenu 
# запускаем x сервер
startx

# узнаем разрешение монитора и имя монитора
sudo xrandr
# изменим разрешение монитора (Virtual-1 из команды выше)
sudo xrandr --output Virtual-1 --mode 1440x900

# горячие клавищи где alt - mod клавиша принятая при установке i3
alt + enter      -открыть терминал
alt + shift + q  -закрыть окно

sudo apt install qemu qemu-kvm libvirt-clients libvirt-daemon-system virtinst bridge-utils
