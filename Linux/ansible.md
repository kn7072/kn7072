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

# генерация ключа ssh
ssh-keygen
cd ~/.ssh  -ключи по умолчанию тут