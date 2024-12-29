C provides two functions strtok() and strtok_r() for splitting a string by some delimiter. Splitting a string is a very common task. For example, we have a comma-separated list of items from a file and we want individual items in an array.

## strtok() Function

The strtok() method splits str[] according to given delimiters and returns the next token. It needs to be called in a loop to get all tokens. It returns NULL when there are no more tokens.

### Syntax of strtok()

char ***strtok**(char *_str_, const char *_delims_);

### Parameters

- **str**: It is the pointer to the string to be tokenized.
- **delims**: It is a string containing all delimiters.

### Return Value

- It returns the pointer to the first token encountered in the string.
- It returns NULL if there are no more tokens found.

### Examples of strtok()

**Example 1:** C Program to demonstrate how to split a string using strtok().


```c
// C program for splitting a string
// using strtok()
#include <stdio.h>
#include <string.h>

int main()
{
	char str[] = "Geeks-for-Geeks";

	// Returns first token
	char* token = strtok(str, " - ");

	// Keep printing tokens while one of the
	// delimiters present in str[].
	while (token != NULL) {
		printf(" % s\n", token);
		token = strtok(NULL, " - ");
	}

	return 0;
}

```

**Output**

 Geeks
 for
 Geeks

**Example 2:** Program to demonstrates the use of the strtok() function to tokenize a string based on a delimiter.

```c
// C code to demonstrate working of
// strtok
#include <stdio.h>
#include <string.h>
// Driver function
int main()
{
    // Declaration of string
    char gfg[100] = " Geeks - for - geeks - Contribute";
    // Declaration of delimiter
    const char s[4] = "-";
    char* tok;
    // Use of strtok
    // get first token
    tok = strtok(gfg, s);
    // Checks for delimiter
    while (tok != 0) {
        printf(" %s\n", tok);
        // Use of strtok
        // go through other tokens
        tok = strtok(0, s);
    }
    return (0);
}
```

**Output**

  Geeks 
  for 
  geeks 
  Contribute

### **Practical Application of** strtok()

strtok() can be used to split a string into multiple strings based on some separators. A **simple CSV file** support might be implemented using this function. CSV files have commas as delimiters.

**Example 3:** C Program to demonstrate the use of the strtok() function in C to implement a **simple CSV file.**

```c
// C code to demonstrate practical application of
// strtok
#include <stdio.h>
#include <string.h>
// Driver function
int main()
{
    // Declaration of string
    // Information to be converted into CSV file
    char gfg[100] = " 1997 Ford E350 ac 3000.00";
    // Declaration of delimiter
    const char s[4] = " ";
    char* tok;
    // Use of strtok
    // get first token
    tok = strtok(gfg, s);
    // Checks for delimiter
    while (tok != 0) {
        printf("%s, ", tok);
        // Use of strtok
        // go through other tokens
        tok = strtok(0, s);
    }
    return (0);
} 
```

**Output**

1997, Ford, E350, ac, 3000.00, 

## strtok_r() Function

Just like strtok() function in C, strtok_r() does the same task of parsing a string into a sequence of tokens. strtok_r() is a [reentrant](https://www.geeksforgeeks.org/reentrant-function/) version of strtok(), hence it is thread safe.

### Syntax of strtok_r()

char ***strtok_r**(char *_str_, const char *_delim_, char **_saveptr_);

### Parameters

- **str**: It is the pointer to the string to be tokenized.
- **delims**: It is a string containing all delimiters.
- **saveptr**: It is a pointer to a char * variable that is used internally by strtok_r() in order to maintain context between successive calls that parse the same string.

### Return Value

- It returns the pointer to the first token encountered in the string.
- It returns NULL if there are no more tokens found.

### Examples of strtok_r()

**Example 1:** a Simple C program to show the use of strtok_r().

```c
// C program to demonstrate working of strtok_r()
// by splitting string based on space character.
#include <stdio.h>
#include <string.h>
int main()
{
    char str[] = "Geeks for Geeks";
    char* token;
    char* rest = str;
    while ((token = strtok_r(rest, " ", &rest)))
        printf("%s\n", token);
    return (0);
}
```

**Output**

Geeks
for
Geeks

### Nested-Tokenization in C

**Example 2:** The below C program demonstrates the use of strtok_r() function for Nested Tokenization.

```c
#include <stdio.h>
#include <string.h>
int main()
{
    char str[] = "Hello, World! Geeks for Geeks.";
    const char outer_delimiters[] = "!.";
    const char inner_delimiters[] = " ,";
    char* token;
    char* outer_saveptr = NULL;
    char* inner_saveptr = NULL;
    token = strtok_r(str, outer_delimiters, &outer_saveptr);
    while (token != NULL) {
        printf("Outer Token: %s\n", token);
        char* inner_token = strtok_r(
            token, inner_delimiters, &inner_saveptr);
        while (inner_token != NULL) {
            printf("Inner Token: %s\n", inner_token);
            inner_token = strtok_r(NULL, inner_delimiters,
                                   &inner_saveptr);
        }
        token = strtok_r(NULL, outer_delimiters,
                         &outer_saveptr);
    }
    return 0;
}
```

**Output**

Outer Token: Hello, World
Inner Token: Hello
Inner Token: World
Outer Token:  Geeks for Geeks
Inner Token: Geeks
Inner Token: for
Inner Token: Geeks

## Difference Between strtok() and strtok_r()

Let us see the differences between strtok() and strtok_r() functions in a tabular form as shown below:

|S.No.|strtok()|strtok_r()|
|---|---|---|
|1.|It is used to break string str into a series of tokens.|It is used to decode a string into a pattern for tokens.|
|2.|The syntax is as follows:<br><br>**char *strtok(char *str, const char *delim)**|Its syntax is as follows:  <br>**char *strtok_r(char *string, const char *limiter, char **context);**|
|3.|It uses the delimiter to proceed.|It is a re-entered variant of strtok().|
|4.|It takes two parameters.|It takes three parameters.|
|5.|It returns a pointer to the first token found in the string.|It returns a pointer to the first token found in the string.|
|6.|It is not thread-safe.|It is thread-safe.|
