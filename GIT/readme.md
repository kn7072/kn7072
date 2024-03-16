1 файлы extDiff и extMerge должны находиться в /usr/local/bin
2 файлы должны быть исполняемыми
    sudo chmod +x /usr/local/bin/extDiff
    sudo chmod +x /usr/local/bin/extMerge
3 .gitconfig должен находиться в каталоге пользоватля на пример /home/stepan
4 для работы скриптов необходима утилита p4merge - ее необходимо скачать отдельно (оф сайт https://www.perforce.com/downloads/visual-merge-tool)
(в скриптах утилита находится по адресу /usr/local/bin/p4v-2023.2.2467475/bin/p4merge, если утилита находится в другом месте, 
значит нужно изменить адрес на актуальный)

