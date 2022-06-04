# создание диска
qemu-img create -f qcow2 test.qcow 10G

# устанавливаем операционную систему на созданный диск
qemu-system-x86_64 -hda test.qcow -boot d -cdrom /home/stapan/debian-11.3.0-amd64-netinst.iso -m 2048


# запуск виртуалкизш
qemu-system-x86_64 -hda /home/stapan/VIRTUAL_MACHINE/test.qcow -m 2048 -enable-kvm -net user,hostfwd=tcp::10022-:22 -net nic

https://unix.stackexchange.com/questions/124681/how-to-ssh-from-host-to-guest-using-qemu
-net user,hostfwd=tcp::10022-:22 -net nic
ssh stepan@localhost -p 10022

# подключение по ssh
ssh -i ~/.ssh/for_virtual/id_rsa stepan@localhost -p 10022

предварительно создав ключ
__ssh-keygen -t rsa ~/.ssh/for_virtual/id_rsa__
и закинув публичную часть на сервер
__ssh-copy-id -i ~/.ssh/for_virtual/id_rsa.pub stepan@localhost -p 10022__
далее можно подключаться
__ssh -i ~/.ssh/for_virtual/id_rsa stepan@localhost -p 10022__

если создать файл config, по адресу ~/.ssh/config [https://www.cyberciti.biz/faq/create-ssh-config-file-on-linux-unix/]
и добавить:

Host virtual1
        HostName localhost
        User stepan
        Port 10022
        IdentityFile ~/.ssh/for_virtual/id_rsa
        IdentitiesOnly yes
то можно будет подключаться просто указав название хоста, не вводя ни каких дополнительных параметров
__ssh virtual1__

su root
apt update
apt upgrade
apt install sudo

# выдаем не рутовому пользователю - stepan права на запуск sudo
__sudo usermod -aG sudo stepan__
# установливаем графическую среду i3
__sudo apt install x-window-system i3 i3status dmenu__
# запускаем x сервер
__startx__

# узнаем разрешение монитора и имя монитора
__sudo xrandr__
# изменим разрешение монитора (Virtual-1 из команды выше)
__sudo xrandr --output Virtual-1 --mode 1440x900__

# горячие клавищи где alt - mod клавиша принятая при установке i3
alt + enter      -открыть терминал
alt + shift + q  -закрыть окно

sudo apt install qemu qemu-kvm libvirt-clients libvirt-daemon-system virtinst bridge-utils
