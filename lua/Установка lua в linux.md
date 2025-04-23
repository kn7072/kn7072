1. Следуем инструкции с [официального сайта](https://www.lua.org/download.html)
```bash
curl -L -R -O https://www.lua.org/ftp/lua-5.4.7.tar.gz
tar zxf lua-5.4.7.tar.gz
cd lua-5.4.7
make all test
```
2. Вызываем команду в этой же папке
```bash
 sudo make install
```
3. Установить менеджер пакетов 
```bash
sudo apt-get -y install luarocks
```