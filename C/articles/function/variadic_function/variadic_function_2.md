## Синтаксис

```c
type va_arg(
   va_list arg_ptr,
   type
);
void va_copy(
   va_list dest,
   va_list src
); // (ISO C99 and later)
void va_end(
   va_list arg_ptr
);
void va_start(
   va_list arg_ptr,
   prev_param
); // (ANSI C89 and later)
void va_start(
   arg_ptr
);  // (deprecated Pre-ANSI C89 standardization version)
```

### Параметры

_`type`_  
Тип аргумента, который требуется извлечь.

_`arg_ptr`_  
Указатель на список аргументов.

_`dest`_  
Указатель на список аргументов, которые нужно инициализировать из параметра _`src`_

_`src`_  
Указатель на инициализированный список аргументов, которые требуется скопировать в параметр _`dest`_.

_`prev_param`_  
Параметр, который предшествует первому необязательному аргументу.

## Возвращаемое значение

**`va_arg`** возвращает текущий аргумент. **`va_copy`**, **`va_start`** и **`va_end`** не возвращайте значения.
## Замечания

Макросы **`va_arg`**, **`va_copy`**, **`va_end`** и **`va_start`** предоставляют переносимый способ получения аргументов функции, которая принимает переменное число аргументов. Существует две версии макросов: макросы, определенные в `STDARG.H` соответствии со стандартом ISO C99; макросы, определенные в `VARARGS.H` нерекомендуемом виде, но сохраняются для обратной совместимости с кодом, написанным до стандарта ANSI C89.

Эти макросы предполагают, что функции принимают фиксированное число обязательных аргументов, за которыми следует переменное число необязательных аргументов. Обязательные аргументы объявляются как обычные параметры для функции и доступ к ним возможен через имена параметров. К необязательным аргументам обращаются макросы (или `VARARGS.H` код, написанный до стандарта ANSI C89), который задает указатель на первый необязательный аргумент в списке аргументов `STDARG.H` , извлекает аргументы из списка и сбрасывает указатель при завершении обработки аргументов.

Стандартные макросы C, определенные в `STDARG.H`, используются следующим образом:

- **`va_start`** задает указатель _`arg_ptr`_ на первый необязательный аргументу в списке аргументов, который передан функции. Аргумент _`arg_ptr`_ должен иметь тип **`va_list`**. Аргумент _`prev_param`_ — это имя обязательного параметра, который непосредственно предшествует первому необязательному аргументу в списке аргументов. Если параметр _`prev_param`_ объявлен в классе регистрового хранения, поведение макроса не определено. **`va_start`** необходимо использовать до первого использования **`va_arg`**.
    
- **`va_arg`** извлекает значение _`type`_ из расположения, которое задано параметром _`arg_ptr`_, и увеличивает значение указателя _`arg_ptr`_, чтобы он указывал на следующий аргумент в списке, используя размер _`type`_ для определения места начала следующего аргумента. **`va_arg`** можно использовать в функции любое количество раз, чтобы получить аргументы из списка.
    
- **`va_copy`** делает копию списка аргументов в текущем состоянии. Параметр _`src`_ должен быть уже инициализирован с помощью **`va_start`**; он может быть обновлен вызовами **`va_arg`**, но не должен быть сброшен с помощью **`va_end`**. Следующий аргумент, который извлекается **`va_arg`** из _`dest`_, совпадает со следующий аргументом, который извлекается из _`src`_.
    
- После получения **`va_end`** всех аргументов сбрасывает указатель `NULL`на . **`va_end`** должен вызываться для каждого списка аргументов, который инициализируется **`va_start`** или **`va_copy`**, до выполнения возврата функцией.
    

Примечание

Макросы в VARARGS.H использовать не рекомендуется; они сохранены только для обратной совместимости с кодом, который написан до появления стандарта ANSI C89. Во всех остальных случаях используйте макросы из файла STDARGS.H.

При компиляции с помощью [`/clr` (компиляция среды CLR)](https://learn.microsoft.com/ru-ru/cpp/build/reference/clr-common-language-runtime-compilation?view=msvc-170) программы, использующие эти макросы, могут создавать непредвиденные результаты из-за различий между системами типов среды CLR. Рассмотрим следующую программу:

```c
#include <stdio.h>
#include <stdarg.h>

void testit (int i, ...)
{
    va_list argptr;
    va_start(argptr, i);

    if (i == 0)
    {
        int n = va_arg(argptr, int);
        printf("%d\n", n);
    }
    else
    {
        char *s = va_arg(argptr, char*);
        printf("%s\n", s);
    }

    va_end(argptr);
}

int main()
{
    testit(0, 0xFFFFFFFF); // 1st problem: 0xffffffff is not an int
    testit(1, NULL);       // 2nd problem: NULL is not a char*
}
```

Обратите внимание — функция **`testit`** ожидает, что второй параметр будет **`int`** или **`char*`**. Передаваемые аргументы имеют значение 0xffffffff (**`unsigned int`**, а не **`int`**) и `NULL` (фактически **`int`**, а не **`char*`**). Когда программа скомпилирована для неуправляемого кода, она дает следующий результат:

Output

```
-1

(null)
```

## Требования

**Заголовок:** `<stdio.h>` и `<stdarg.h>`

**Устаревший заголовок:** `<varargs.h>`

## Библиотеки

Все версии [библиотек времени выполнения языка C](https://learn.microsoft.com/ru-ru/cpp/c-runtime-library/crt-library-features?view=msvc-170).

## Пример

```c
// crt_va.c
// Compile with: cl /W3 /Tc crt_va.c
// The program below illustrates passing a variable
// number of arguments using the following macros:
//      va_start            va_arg              va_copy
//      va_end              va_list

#include <stdio.h>
#include <stdarg.h>
#include <math.h>

double deviation(int first, ...);

int main( void )
{
    /* Call with 3 integers (-1 is used as terminator). */
    printf("Deviation is: %f\n", deviation(2, 3, 4, -1 ));

    /* Call with 4 integers. */
    printf("Deviation is: %f\n", deviation(5, 7, 9, 11, -1));

    /* Call with just -1 terminator. */
    printf("Deviation is: %f\n", deviation(-1));
}

/* Returns the standard deviation of a variable list of integers. */
double deviation(int first, ...)
{
    int count = 0, i = first;
    double mean = 0.0, sum = 0.0;
    va_list marker;
    va_list copy;

    va_start(marker, first);     /* Initialize variable arguments. */
    va_copy(copy, marker);       /* Copy list for the second pass */
    while (i != -1)
    {
        sum += i;
        count++;
        i = va_arg(marker, int);
    }
    va_end(marker);              /* Reset variable argument list. */
    mean = sum ? (sum / count) : 0.0;

    i = first;                  /* reset to calculate deviation */
    sum = 0.0;
    while (i != -1)
    {
        sum += (i - mean)*(i - mean);
        i = va_arg(copy, int);
    }
    va_end(copy);               /* Reset copy of argument list. */
    return count ? sqrt(sum / count) : 0.0;
}
```

Output

```
Deviation is: 0.816497
Deviation is: 2.236068
Deviation is: 0.000000
```

[](https://learn.microsoft.com/ru-ru/cpp/c-runtime-library/reference/va-arg-va-copy-va-end-va-start?view=msvc-170#see-also)

## См. также
