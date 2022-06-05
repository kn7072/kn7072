# установка Ansible
sudo apt update
sudo apt upgrade
cat /etc/os-release

// sudo apt install git python3-pip
// update-alternatives --install /usr/bin/python python /usr/bin/python3 2
// python --version

pip3 install ansible
ansible --version

cd ~ && touch ansible.cfg && nvim ansible.cfg

# создаем пароль для пользователя
useradd -m -s /bin/bash xxx
passwd xxx
--вводим пароль

awk -F: '{ print $1}' /etc/passwd
проверим пользователей 
grep -E '^UID_MIN|^UID_MAX' /etc/login.defs
getent passwd {1000..60000}

# генерация ключа ssh
ssh-keygen
cd ~/.ssh  -ключи по умолчанию тут

ssh-copy-id -i ~/.ssh/id_rsa.pub user@host
ssh-copy-id -i ~/.ssh/for_virtual/id_rsa.pub stepan@localhost -p 10022

# команды 
команды запускаются из каталог, в котором находится конфиг ansible.cfg
__ansible all -m ping__ -для всех хостов
__ansible virt -m ping__ -для virt

если подключения осуществляются не через ssh
будет ошибка
__"msg": "to use the 'ssh' connection type with passwords or pkcs11_provider, you must install the sshpass program"__
чтобы ошибка ичезла необходимо установить sshpass 
__sudo apt install sshpass__


__ansible test -m ping__ запуск для всех хостов в группе test
__ansible all_groups -m ping__ -для хостов объединенной группы

__ansible all -m setup__ выдает всю возможную информацию о наших клиентах
__ansible all -m shell -a "uptime" -выполнить команду uptime, -a для передачи аргументов в shell 
команты модуля shell выполняются без проверки

__ansible all -m command -a "uptime"__ то же что и выше, только через модуль command
__ansible all -m file -a "path=~/ansible_test.txt state=touch" -создать файл

        если возникают проблемы с правами у пользователя user_x на хосте y, заходим на хост y и выполняем команду 
        __sudo visudo__
        добавляем строку - команда отключает запрос пароля при вооде команды sudo для пользователя user_x

        user_x  ALL=(ALL:ALL) NOPASSWD:ALL
__ansible group2 -m copy -a "src=file123 dest=/home mode=777"__ -b -скопиторовать файл file123 из текущей машины на хосты указанные в group2


