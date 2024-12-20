# Рубрика "Секреты Вим". Прыжки по тексту
Всем привет, с вами еженедельная рубрика про Вим! Сегодня поговорим о прыжках по тексту. Про [прыжки по строке](https://zen.yandex.ru/media/math_notebook/rubrika-sekrety-vim-peremescenie-po-stroke-5f6ef1dadf292d11092d803a?from=editor) уже был материал. Скоро выйдет еще один.

[Оглавление рубрики "Секреты Вим"](https://zen.yandex.ru/media/math_notebook/navigator-po-rubrike-sekrety-vim-5f96cbd224d0d15a66ea3f71)

Мы не рассматриваем здесь поиск, про него была [отдельная заметка](https://zen.yandex.ru/media/math_notebook/rubrika-sekrety-vim-poisk-i-zamena-5ec82e9dd09ebe58a38f0e9e?feed_exp=ordinary_feed&from=channel&rid=557829803.640.1596205186307.40845&integration=site_desktop&place=more&secdata=CNij9PCjLiABMAJQDw%3D%3D). Однако **поиск слова** это не совсем поиск, а именно прыжок: * ищет слово под курсором ниже по тексту, а # ищет выше. Обе команды ищут полное слово, то есть окруженное якорями-границами слова: вместо X ищут \<X\>. Это логично; однако, если вы хотите искать не только полные слова, используйте g* и g# . Так, если вы стоите на слове "sex" и нажмете *, то переместитесь к слову "sex" ниже по тексту, а если нажмете g*, то можете попасть на слово "sexuality" или "asexual", или, скажем "Essex" — но тоже ниже по тексту. Впрочем, при достижении конца поиск обычно начинается сначала.

Переходы на метки тоже уже обсуждались. Можно положить закладку, пометив ее буквой (например, mm или mq), и потом вернуться на ту же строку (соответственно, 'm или 'q) или прямо на то же место (`m или `q).

**Прыгнуть на строку** номер _n_: _n_G. При этом просто G прыгает в конец текста. Синоним 1G это gg. А _n_gg — синоним _n_G.

Отменить переход можно двойной обратной кавычкой, если еще ничего не правили: ``. Эта же команда позволяет вернуться туда, откуда начат поиск. (По сути, это спецметка).

А можно прыгнуть **на байт** номер _n_ в тексте! Команда _n_go. Байты в юникодном мире вещь лукавая, но в целом может быть полезно. Просто go прыгает на начало (_n_=1).

Можно **отмотать** _n_ **процентов текста**: _n_%.

Просто % имеет совсем другой смысл: это **прыжок на парную скобку** (любую: ([{}])), а также на соответствующий /* или */ (комментарий в Си-стиле) или на условные операторы препроцессора.

**Искать скобки** можно и другими командами, основанными на [ и ]. Так, [( и [{ прыгают на предыдущую непарную скобку (можно задать повторитель), а ]) и ]} прыгают вперед.

**Переход на определение переменной**: gd (локальное) и gD (глобальное). Вим немного ориентируется на синтаксис языка Си. В обычном тексте или программе на другом языке эти команды почти идентичны и прыгают на **первое упоминание слова** в файле. Удобно очень! Но надо иметь в виду, что это все-таки придумано для Си. Например,

> //The sin  
> ...  
> int sin=7;  
> ...  
> commit(sin);  
> ...

Поставив курсор на аргумент sin функции commit и нажав gd или gD, мы перенесемся на определение переменной. Хотя первое упоминание — в комментарии — было выше.

Команда g, (g и запятая) перемещает курсор **к месту последней правки**. Удобно, если вы улетели наверх посмотреть определение переменной и надо вернуться, а меточку-закладку поставить забыли. Дополняет команды возврата `` (и еще '', которая возвращается на нужную строку, но на ее начало).

Для прыжкам по тексту (а не коду программ) есть несколько команд. Круглые скобки ( и ) прыгают **на начало предожения**: под курсором или следующего, а фигурные { и } — **на начало абзаца**. Абзац понимается как отрезок текста, отделенный пустой строкой. (Именно так трактуется абзац в ТеХе.) Но и для программистов тоже полезно, если вы разделяете функции и другие важные блоки кода пустыми строками.

Предложение должно кончаться знаком препинания (.!?) и после него — пробел. Все команды можно предварять повторителем: так можно проскочить сколько угодно предложений и абзацев. Это очень удобно при редактировании именно текста: рассказа там или статьи. В ТеХе — особенно.

Еще есть **прыжок на экран текста** (вроде PageDown): C-F, обратно C-B. Можно на полэкрана: C-D и C-U. Курсор окажется на первой/последней строке экрана (в отличие от PageDown).

Очень удобны команды **сдвига экрана**: z<CR> перемещает текущую строку наверх экрана, делая ее первой видимой. Команда z. (z и потом точка) помещает текущую строку в центр экрана. Команда z- (вот ее редко использую) ставит текущую строку последней видимой (внизу экрана).

Можно, наоборот, **поместить курсор на первую видимую строку** (H), строку по центру (M) и последнюю видимую (L). Причем H и L могут предваряться числом _n_, которое укажет, на сколько строк (_n_-1) ниже первой или выше последней надо оказаться.