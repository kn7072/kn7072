[источник](https://dzen.ru/a/YQxD5jnHZ2bdAESD)
Есть в Вим есть большое число опций, которые я называю иногда переменными или флагами. Опция может быть _логической_ (флаг), _числовой_ или _текстовой_. Например, _number_ логическая, _textwidth_ числовая, а _statusline_ текстовая. Опции позволяют настраивать работу в Вим, делая ее более удобной. Выставляет их команда _set_, которая таит довольно много секретов.

Редактор опций. Они сгруппированы по темам, можно перемещаться по группам, читать кратко, подробно, выставлять значения. См. ниже.

Помимо выставления заданного значения опции, команда может сообщить текущее или выставить значение по умолчанию.

Так, просто _:set_ **выведет значения** всех опций, которые имеют другое значение, не по умолчанию. А _set all_ и _set termcap_ выведут ВСЕ опции, кроме терминальных, и все терминальные опции.

Это массовка. Теперь индивидуальная работа. Команда _set опция?_ **выведет значение** опции. Это работает со всеми тремя типами (логическим, числовым, текстовым), но полезно для флагов. Сейчас станет ясно, почему.

Потому что _set опция_ для флага **выставит флаг** в истину, а для числовых и текстовых опций **покажет значение**. Чтобы **сбросить флаг**, добавьте no перед опцией, то есть выставьте флаг _noопция_. Например, _set nonumber_.

Еще **флаги можно переключать**: _set опция!_ Восклицательный знак и означает "выключить включенное, включить выключенное". Как вариант, можно добавить перед опцией inv: _set invnumber_.

Можно **вернуть значение по умолчанию**. Конечно, можно посмотреть в Справке и выставить его, но Вим же знает сам, какое значение по умолчанию: _set опция&_

Ну и вариант массовки: _set all&_ вернет **все опции к заводским значениям**. На самом деле, не все, есть исключения: терминальные опции, метод и ключ шифрования, кодировка... И эффект может быть довольно резким, так что осторожнее, пожалуйста.

Нюанс: _set опция&_ вернет опцию к значению по умолчанию Вим. Но если выставлен флаг _compatible_, то Вим старается походить на vi, ну и сами понимаете. Можно уточнить, чего вы хотите: _set опция&vim_ (или _set опция&vi_).

> Если выставлено ненулевое значение опции verbose, то на запрос значения опции будет дано сообщение, где оно было выставлено. Может быть иногда полезно.

Это все хорошо, но мы не добрались еще собственно до задания опций. Только флаги можем выставлять и сбрасывать. Числовую или текстовую **переменную зададим так**: _set опция=значение_. Вместо знака = можно поставить двоеточие. Пробел перед = или : допустим, после — нет. Числовое значение может быть десятичным, семеричным (в начале 0) или шестнадцатеричным (0x). Дойдя до знака равенства, можно нажать табуляцию и подставится старое значение. Если набрать часть имени опции и нажать таб, появятся варианты.

Можно не просто задать переменную, но добавить к ней что-то, **изменить переменную относительно**. Для чисел это сумма в стиле x=x+a (или x+=a), для текста — конкатенация, но умная. Команда _set опция+=значение_. Если, например, опция есть список чего-то, разделенного запятыми или чем-то еще, то set отработает правильно: добавит запятую, если она нужна, и не будет добавлять просимое, если оно уже присутствует. Главное, добавлять сущности по одной, а не сразу пачками.

Примеры:  
_set shiftwidth+=2_  
_set path+=/home/myself/_  
_set formatoptions+=a_

Аналогично, можно **уменьшить числовую переменную** или **удалить текст** из текстовой: _set опция-=значение_. Для текста команда работает интеллектуально. Так, если в опции список через запятую а,б,в и вы вычтите б, то все отработает как надо. Получится а,в

Есть еще и третий, малоизвестный вариант: _set опция^=значение_. Для чисел это **умножение опции на число**, для строк **конкатенация спереди**. Например, пути проверяются, начиная с начала, и если надо вставить более приоритетный путь, то это самое оно.

Примеры:  
_set shiftwidth^=2_  
_set path^=/home/myself/_

> А вот деления нет, отменить содеянное для числовых опций так просто не получится! Для текстовых списков получится: вычитание удалит просимое, даже если оно не в конце.

Можно **задавать сразу много опций** одной командой:_set nu sw=4 nosi ts=3 tw=80_

Если допущена ошибка, Вим о ней сообщит и все, что после ошибочного аргумента, не обработает.

> Как вы заметили, имена опций можно сокращать.

Для текстовых опций, если вам нужны пробелы и другие спецсимволы, их надо экранировать слешем. Например, _set titlestring=I\ love\ Vim_. Сам слеш тоже экранируется и действует правило: число идущих подряд слешей преобразуется в половину, с округлением вниз. Так, \\\ и \\ одинаково дадут \, а \\\\ и \\\\\ дадут \\. Двойную кавычку надо экранировать, так как она начинает комментарий.

И последнее: есть **удобный интерфейс** для изучения и выставления **опций**! Он включается командами _:options_ или _:browse set_ и выводит группы опций (см. скриншот выше), которые можно раскрывать. Дана и справка по опциям, что полезно и для изучения, и для настройки Вим в удобном режиме. Потом [сессия](https://zen.yandex.ru/media/math_notebook/rubrika-sekrety-vim-sessii-603a9bbb732f3c7f6211b201?from=editor) или mkvimrc позволят вам сохранить достигнутое.

Это всё касалось либо глобальных опций, либо относящихся к данному окну или файлу. Обычно интуитивно все ясно. Но иногда есть разница между локальными и глобальными опциями. О ней в другой раз