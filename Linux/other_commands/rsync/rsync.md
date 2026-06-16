rsync -av /home/stepan/.config/nvim /home/stepan/GIT/kn7072/vim_tmux

в .bashrc
alias backup='sudo rsync -av /home/stepan/.config/nvim /home/stepan/GIT/kn7072/vim_tmux

перенести файлы из phrasal*verb(внутри находтся каталоги с файлами) в каталог WORDS с той же структурой как в
каталоге phrasal_verb
rsync -avm --include='*/' --include='\_' --exclude='\*' /home/stepan/temp/phrasal_verb/ /home/stepan/git_repos/kn7072/ANKI/WORDS/

Как это работает:

    -a — архивный режим (сохраняет права и атрибуты).
    -v — показывает процесс (можно убрать для тишины).
    -m (--prune-empty-dirs) — самое важное: не создает пустые папки в каталог_2. Если в каталог_1/x есть только файлы, папка x будет создана в каталог_2. Если бы в x была только пустая папка y, она бы не скопировалась.
    --include='*/' — разрешает заходить внутрь всех подкаталогов.
    /путь/к/каталог_1/ — обязательно со слэшем на конце! Это означает "копировать содержимое каталога", а не сам каталог целиком.
