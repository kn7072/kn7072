extern void print_data(int);

char *message = "Hello";

int main(void) {
    print_data(22);
    return 0;
}

// gcc -c app_for_shared.c -o app_for_shared.o
// Вторая команда передает линковщику объектный файл app_for_shared.o и файл
// библиотеки hello.so и создает исполняемый файл приложения - файл
// app_for_shared
// gcc app_for_shared.o hello.so -o app_with_shared
//
// ldd app_with_shared
// linux-vdso.so.1 (0x00007fff90520000)
// hello.so => not found   <-------- НЕ НАЙДЕНА
// libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007d8e78e00000)
// /lib64/ld-linux-x86-64.so.2 (0x00007d8e79181000)
//
// export LD_LIBRARY_PATH=.
// ./app_with_shared

// ldd app_with_shared
// linux-vdso.so.1 (0x00007fffef315000)
// hello.so => ./hello.so (0x00007f7dcbc30000) <---- В текущем каталоге
// libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f7dcba00000)
// /lib64/ld-linux-x86-64.so.2 (0x00007f7dcbc3c000)
//
// ldconfig -p | grep -i "hello"
