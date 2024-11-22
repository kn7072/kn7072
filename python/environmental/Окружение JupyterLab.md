Для того чтобы jupyterlab запускался в нашем окружении необходимо, чтобы он был добавлен в наши зависимости
 ```bash
poetry add -D jupyterlab
```
 1. Кликаем на меню в верхней части окна
  ![](../images/jplab_1.png)
  2. Выбираем отмеченный на скрине 2 пункт меню.
  ![](../images/jplab_2.png)
  3. Выбираем из существующих окружений.![](../images/jplab_3.png)
  4. Выбираем python из нашего окружения![](../images/jplab_4.png)
  5. Жмем на кнопку с отображением текущего имени окружения и выбираем из списка то которое создали.![](../images/jplab_5.png)

##### Существует еще один вариант создания свое ядра для jupyter.

Для этого нужно добавить еще одну dev зависимость в poetry.
```bash
poetry add -D ipykernel
```
и выполнить команду
```bash
poetry run python -m ipykernel install --user --name che-project
```
После это при <u>запуске jupyter lab через poetry</u> мы сможем выбирать нужное нам ядро (если отрывать jupyter lab не через poetry, то ничего работать не будет)
```bash
poetry run jupyter lab
```

**У нас откроется jupyter lab в браузере.** После этого при создании нового таба должно отображаться созданное ядро![](../images/jplab_6.png)

Можно изменить ядро в уже отрытом файле.![](../images/jplab_7.png)

#### Настройка debug
В папке где активировано виртуальное окружение python (т.е где вызываем команду poetry shell) вызываем команду ([источник](https://ipython.readthedocs.io/en/stable/config/intro.html))
 ```
 ipython profile create
```
Я не указываю имени профиля, поэтому конфиги будут созданы в дефолтной папке по пути `~/.ipython/profile_default/`.
Мы открываем файл `ipython_kernel_config.py` и в конец файла вносим строку 
`c.Kernel.debug_just_my_code=False` - этим мы говорим, что хотим отлаживать не только наш код, но код сторонних модулей.

#### Полезные ссылки:
https://www.alexanderjunge.net/blog/pyenv-virtualenv-poetry-jupyter/