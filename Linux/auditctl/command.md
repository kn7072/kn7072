auditctl -a exit,always -S open -F path=/home/stepan/.local/share/nvim/mason/packages/luaformatter/bin -F perm=axw
/.local/share/nvim/mason/packages/luaformatter/bin


/etc/init.d/auditd restart  перезагрузка демона
```
sudo service auditd restart
```

# если возникла ошибка
WARNING - 32/64 bit syscall mismatch, you should specify an arch

необходимо добавить ключ -F arch=b64
(архитектуру можно проверить с помощью команды arch)

sudo auditctl -a always,exit -F exe=/home/stepan/.local/share/nvim/mason/packages/luaformatter/bin/lua-format -F arch=b64 -S execve -k execution_bin_id
sudo aureport -f -i --start today | grep "lua-format" 
sudo ausearch -a 4123
# проверить правила
sudo auditctl -l

 если указать флаг '--summary', который заставляет aureport выводить не все случаи доступа к файлом, а только их общее количество по отношению к каждому из файлов:
sudo aureport -f -i --start recent --summary

# Создание и удаление каталогов
sudo auditctl -a exit,always -F arch=b64 -S mkdir -S rmdir

# Наблюдение за конфигурационными файлами системы аудита 
-w /etc/audit/auditd.conf -p wa 
-w /etc/audit/audit.rules -p wa

# Наблюдение за журнальными файлами 
-w /var/log/audit/ 
-w /var/log/audit/audit.log 

# Настройки и задания at 
-w /var/spool/at 
-w /etc/at.allow 
-w /etc/at.deny 

# Файлы паролей и групп 
-w /etc/group -p wa 
-w /etc/passwd -p wa 
-w /etc/shadow 

# Конфигурационные и журнальные файлы входа в систему 
-w /etc/login.defs -p wa 
-w /etc/securetty 
-w /var/log/faillog 
-w /var/log/lastlog 

# Список и имена хостов 
-w /etc/hosts -p wa 

# Стартовые скрипты демонов 
-w /etc/init.d/ 
-w /etc/init.d/auditd -p wa 

# Настройки сервера SSH 
-w /etc/ssh/sshd_config 

# Изменение прав доступа к файлам 
-a entry,always -S chmod -S fchmod -S chown -S chown32 -S fchown -S fchown32 -S lchown -S lchown32 

# Создание, открытие или изменение размеров файлов 
-a entry,always -S creat -S open -S truncate -S truncate64 -S ftruncate -S ftruncate64 

# Создание и удаление каталогов 
-a entry,always -S mkdir -S rmdir 

# Удаление или создание ссылок 
-a entry,always -S unlink -S rename -S link -S symlink 

# Монтирование файловых систем 
-a entry,always -S mount -S umount -S umount2
