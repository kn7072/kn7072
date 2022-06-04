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
ansible all -m ping

если подключения осуществляются не через ssh
будет ошибка
__"msg": "to use the 'ssh' connection type with passwords or pkcs11_provider, you must install the sshpass program"__
чтобы ошибка ичезла необходимо установить sshpass 
__sudo apt install sshpass__
