# C atexit() Function

[Leave a Comment](https://www.rameshfadatare.com/c-functions/c-atexit-function/#respond) / By [Ramesh Fadatare](https://www.rameshfadatare.com/author/admin/ "View all posts by Ramesh Fadatare") / July 7, 2024

The `atexit()` function in C is a standard library function that registers a function to be called upon normal program termination. It is part of the C standard library (`stdlib.h`). This function is useful for performing cleanup operations, such as releasing resources or saving state, before the program exits.

## Table of Contents

1. Introduction
2. `atexit()` Function Syntax
3. Understanding `atexit()` Function
4. Examples
    - Registering a Single Function
    - Registering Multiple Functions
5. Real-World Use Case
6. Conclusion

## Introduction

The `atexit()` function allows you to register a function that will be called automatically when the program terminates normally. This is useful for performing cleanup tasks that need to be done before the program exits, such as closing files, freeing memory, or saving data.

## atexit() Function Syntax

The syntax for the `atexit()` function is as follows:

```c
int atexit(void (*func)(void));
```

### Parameters:

- `func`: A pointer to the function to be called upon program termination. This function must take no arguments and return no value.

### Returns:

- The function returns `0` on success and a non-zero value on failure.

## Understanding atexit() Function

The `atexit()` function registers the specified function to be called when the program terminates normally. Multiple functions can be registered with `atexit()`, and they will be called in the reverse order of their registration. The registered functions are called automatically when the `exit()` function is called or when the program returns from the `main()` function.

## Examples

### Registering a Single Function

To demonstrate how to use `atexit()` to register a function to be called upon program termination, we will write a simple program.

#### Example

```c
#include <stdio.h>
#include <stdlib.h>

void cleanup_function(void) {
    printf("Cleanup function called.\n");
}

int main() {
    // Register the cleanup function
    if (atexit(cleanup_function) != 0) {
        printf("Failed to register cleanup function.\n");
        return 1;
    }

    printf("Main function executing.\n");

    // Program will exit normally
    return 0;
}
```

**Output:**

```bash
Main function executing.
Cleanup function called.
```

### Registering Multiple Functions

This example shows how to register multiple functions with `atexit()`.

#### Example

```c
#include <stdio.h>
#include <stdlib.h>

void cleanup_function1(void) {
    printf("Cleanup function 1 called.\n");
}

void cleanup_function2(void) {
    printf("Cleanup function 2 called.\n");
}

int main() {
    // Register the first cleanup function
    if (atexit(cleanup_function1) != 0) {
        printf("Failed to register cleanup function 1.\n");
        return 1;
    }

    // Register the second cleanup function
    if (atexit(cleanup_function2) != 0) {
        printf("Failed to register cleanup function 2.\n");
        return 1;
    }

    printf("Main function executing.\n");

    // Program will exit normally
    return 0;
}
```

**Output:**

```bash
Main function executing.
Cleanup function 2 called.
Cleanup function 1 called.
```

## Real-World Use Case

### Cleaning Up Resources

In real-world applications, the `atexit()` function can be used to ensure that resources are properly released when the program exits. For example, you can register functions to close open files, free dynamically allocated memory, or save the program’s state.

#### Example: Closing a File on Exit

```c
#include <stdio.h>
#include <stdlib.h>

FILE *file;

void close_file(void) {
    if (file != NULL) {
        fclose(file);
        printf("File closed.\n");
    }
}

int main() {
    // Open a file
    file = fopen("example.txt", "w");
    if (file == NULL) {
        printf("Failed to open file.\n");
        return 1;
    }

    // Register the close_file function
    if (atexit(close_file) != 0) {
        printf("Failed to register close_file function.\n");
        return 1;
    }

    printf("Main function executing.\n");

    // Write to the file
    fprintf(file, "Hello, World!\n");

    // Program will exit normally
    return 0;
}
```

**Output:**

```bash
Main function executing.
File closed.
```

## Conclusion

The `atexit()` function is used for ensuring that cleanup operations are performed when a program terminates normally. By understanding and using this function, you can register functions to release resources, save data, or perform other necessary tasks before the program exits. This helps to maintain the integrity and stability of your programs, preventing resource leaks and ensuring that important operations are not overlooked.