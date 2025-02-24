#ifndef INCLUDE_MACROS_MACROS_TRICKS_H_
#define INCLUDE_MACROS_MACROS_TRICKS_H_

/*
## Гигиена

- Параметры в месте раскрытия ставим в скобки

    ```c
    #define DOUBLE(x) (x)*2
    ```

- Одного раза достаточно — это про параметры

    ```c
    #define SQUARE(x) do { int r = (x); r *= r; } while(0);
    ```

- Весь раскрывающий текст прячем в блоки
- Следим за `;`
- Следуем традициям именования (`E`, капс, `_`)
- Перед `#define` ставим `#undef`
- Следим за запятыми

    ```c
    #define ALERT(x) printf("%s\n", #x);
    ```
 * */

//  Склейка значений двух макросов
#define CONCAT(x, y) x##y

// Превращение макроса в строку
#define STR(x) #x

// Подсчёт количества аргументов (`##` даст и 0)
#define _COUNT_ARGS(_1, _2, _3, _4, _5, _6, _7, N, ...) N
#define COUNT_ARGS(...) _COUNT_ARGS(__VA_ARGS__, 7, 6, 5, 4, 3, 2, 1, 0)

// Повторялка кода
#define REPEAT_3(macro, data) macro(data) macro(data) macro(data)
#define PRINT(x) printf("%s\n", x);
// REPEAT_3(PRINT, "Hello!")

#define PR(...) printf(__VA_ARGS__)
// PR("weight = %d, shipping = $%.2f\n", wt, sp);
// printf("weight = %d, shipping = $%.2f\n", wt, sp);

// Выбрать N-й аргумент макроса
#define SELECT_NTH(N, ...) SELECT_NTH_HELPER(N, __VA_ARGS__)
#define SELECT_NTH_HELPER(N, _1, _2, _3, _4, _5, ...) _##N
// printf("%d\n", SELECT_NTH(3, 10, 20, 30, 40, 50)); // 30

#define SELECT_NTH_HELPER_TEST(N, _1, _2, _3, _4, _5, ...) _##N##__VA_ARGS__

// Выбрать последний аргумент макроса
#define GET_LAST(...) GET_LAST_HELPER(__VA_ARGS__, dummy)
#define GET_LAST_HELPER(_1, _2, _3, _4, _5, last, ...) last
// printf("%d\n", GET_LAST(10, 20, 30, 40, 50)); // 50

// Применить «нечто» (ну тоже макрос, да) к каждому аргументу макроса
#define APPLY(macro, ...) __VA_ARGS__
#define PRINT_2(x)                 \
    do {                           \
        printf("PRINT_2 %s\n", x); \
    } while (0);
// APPLY(PRINT_2, "one", "two", "three");

// Проверить и вернуть что сказано (работает и с пустым значением!)
#define CHECK(x, y) \
    if (!(x)) {     \
        return (y); \
    }

// Показать переменную и её значение
#define TRACE(x, y) printf(#x ": %" #y, (x))

#endif  // INCLUDE_MACROS_MACROS_TRICKS_H_
