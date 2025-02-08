https://askubuntu.com/questions/159833/how-do-i-get-the-kernel-source-code

https://unix.stackexchange.com/questions/46077/where-to-download-linux-kernel-source-code-of-a-specific-version

git clone git://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git
cd linux
git checkout v2.6.36.2

To later switch to another version, it's easy:

git checkout v3.5.2

To update your repository to include all of the latest tags and commits:

git fetch


apt-cache search linux-source

Checking Kernel Version Using uname Command in Linux
uname -r

Checking Kernel Version Using hostnamectl 
hostnamectl

Checking Kernel Version by viewing /proc/version File in Linux
cat /proc/version


установка bpf из исходников конкретного ядра
1 выкачиваем репозиторий ядра
    git clone git://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git
    cd linux
    git checkout Ubuntu-6.8.0-10.10 (tag Ubuntu-6.8.0-10.10)
2 переходим в нужный каталог tools/lib/bpf
3 установливаем bpf
    в качестве примера устанавливаем в /home/stepan/temp/my_bpf_oracul
    sudo make && sudo make install prefix=/home/stepan/temp/my_bpf_oracul

    в каталоге /home/stepan/temp/my_bpf_oracul
    создаются каталоги:
        include/bpf - содержит необходимые заголовочны файлы
        lib64 - тут находятся библиотеки


