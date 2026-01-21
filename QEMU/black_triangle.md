# создание диска

qemu-img create -f qcow2 test.qcow 10G

# устанавливаем операционную систему на созданный диск

qemu-system-x86_64 -hda test.qcow -boot d -cdrom /home/stapan/debian-11.3.0-amd64-netinst.iso -m 2048

# запуск виртуалки

qemu-system-x86_64 -hda /home/stapan/VIRTUAL_MACHINE/test.qcow -m 2048 -enable-kvm -net user,hostfwd=tcp::10022-:22 -net nic

https://unix.stackexchange.com/questions/124681/how-to-ssh-from-host-to-guest-using-qemu
-net user,hostfwd=tcp::10022-:22 -net nic
ssh stepan@localhost -p 10022

# подключение по ssh

ssh -i ~/.ssh/for_virtual/id_rsa stepan@localhost -p 10022

предварительно создав ключ
**ssh-keygen -t rsa ~/.ssh/for_virtual/id_rsa**
и закинув публичную часть на сервер
**ssh-copy-id -i ~/.ssh/for_virtual/id_rsa.pub stepan@localhost -p 10022**
далее можно подключаться
**ssh -i ~/.ssh/for_virtual/id_rsa stepan@localhost -p 10022**

если создать файл config, по адресу ~/.ssh/config [https://www.cyberciti.biz/faq/create-ssh-config-file-on-linux-unix/]
и добавить:

Host virtual1
HostName localhost
User stepan
Port 10022
IdentityFile ~/.ssh/for_virtual/id_rsa
IdentitiesOnly yes
то можно будет подключаться просто указав название хоста, не вводя ни каких дополнительных параметров
**ssh virtual1**

su root
apt update
apt upgrade
apt install sudo

# выдаем не рутовому пользователю - stepan права на запуск sudo

**sudo usermod -aG sudo stepan**

# установливаем графическую среду i3

**sudo apt install x-window-system i3 i3status dmenu**

# запускаем x сервер

**startx**

# узнаем разрешение монитора и имя монитора

**sudo xrandr**

# изменим разрешение монитора (Virtual-1 из команды выше)

**sudo xrandr --output Virtual-1 --mode 1440x900**

# горячие клавищи где alt - mod клавиша принятая при установке i3

alt + enter -открыть терминал
alt + shift + q -закрыть окно
alt + ctrcl + g -захват клавиатуры и мыши

sudo apt install qemu-kvm libvirt-clients libvirt-daemon-system virtinst bridge-utils, virt-manager
