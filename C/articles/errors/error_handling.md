[source](https://www.scaler.com/topics/c/error-handling-in-c/)

## Overview

We don't have any direct support of error handling in C language but there are some functional methods used to handle errors while performing file operations: **perror(), strerror(), ferror(), feof(), clearerr() and Exit status**. The errors are very common when we try to read a file that doesn't even exist or when we try to use a file that has not been opened. To identify the type of error, we can refer to **errno**. It is a global variable, automatically initialized with a numeric value whenever we call a function.

## Error Handling in C Language

Ever wondered while performing file operations what if we try to open a file for reading data that doesn't even exist? Obviously, we will get some errors and these errors are very common in practical life.

### Example of Error handling in C

We all must have encountered so many common errors either while reading data from a file or while writing data to a file. These errors arise usually:

- When we try to read from a file that doesn't exist.
- When we use a file that has not been opened.
- When we try to write data to a file that has been opened only for reading mode.

In this C program, we are trying to open test.txt file in reading mode to read data from the file. Considering in case if such file doesn't exists, we have taken care of error handling using some methods defined in errno.h header file. If such file doesn't exists, error message will be printed and otherwise, it will read and print the data from the file.

**We will study errno values and error handling methods in the later course of the article.**

```c
#include <stdio.h>       
#include <errno.h>       
#include <string.h> 
 
int main(){
    FILE *fp;                                //File Pointer
    fp = fopen("test.txt","r");
    if(fp==NULL){                           //If file doesn't exists 
        printf("Value of errno: %d",errno);
        printf("\nError Message: %s",strerror(errno));
        perror("Message from perror");
    }
    else{
        int num;
        fscanf(fp,"%d",&num);             //Reading integer data from the file
        printf("File Data: %d",num);
        fclose(fp); 
    }
    return 0;
}
```

Here, we have declared a file pointer and using it, we have opened "test.txt" file. If fp pointer is NULL, that means the file doesn't exists and we print error message.

**Output:**

```c
If "test.txt" file doesn't exists: (Output)
    Value of errno: 2
    Message from perror: No such file or directory
    Error Message: No such file or directory
    
If "test.txt" file exists and (integer) 100 is the data in it: (Output)
    File Data: 100
```

Assuming the data present in the file is integer 100 and therefore, in presence of file we have printed the file data. We have also taken care of error handling and thus, in absence of file we are printing error message.

## What is Errno?

When we call a function in C language, a variable is automatically initialized with a numeric value and we can use that to identify the type of error if encountered while writing the code. This variable is called **errno value.** It is a global variable that is defined in **errno.h** header file. There are a total of 13 errno values in C language and each errno has an error message associated with it. These are illustrated below: **(Different types of possible error messages):**

|Errno Value|Error Message|
|---|---|
|1|Operation not permitted|
|2|No such file or directory|
|3|No such process|
|4|Interrupted system call|
|5|I/O error|
|6|No such device or address|
|7|Argument list too long|
|8|Exec format error|
|9|Bad file number|
|10|No child processes|
|11|Try again|
|12|Out of memory|
|13|Permission denied|

**1. Operation not permitted:** Sometimes while performing operations of file handling in C, we try to read from a file or change permissions of a file by accessing it. If we don't have ownership rights or system rights to access a file, then we get this particular error message.

**2. No such file or directory:** This error message occurs whenever we try to access a file or directory that doesn't exists. It also occurs when we specify wrong file destination path.

**3. No such process:** When we perform some operations that are not supported during file handling in C, it gives **no such process** error.

**4. Interrupted System call:** If we try to read user's input and if there is no input present, then the system calling process will not return any value and will be blocked forever. This results in interrupted system calls.

**5. I/O error:** I/O stands for input/output errors that occur when system is not able to perform basic operations like reading from a file or copying data from one file to another.

**6. No such device or address:** When we specify incorrect device path or address while opening or accessing them, this error occurs.

For example: If we are trying to access a device driver using its path but in actual, it has been removed from the system.

**7. Argument list too long:** This error generally occurs when we work with large number of files.

For example: If we need to get count of no. of files in a directory (consisting of large number of files) that starts with string - "Scaler", then due to limited buffer space it will show an error message - "Argument list too long" as no. of files in that directory will be equal to the arguments list.

**8. Exec format error:** This error occurs when we try to execute a file that is not executable or has an invalid executable-file format.

**9. Bad file number:** This error occurs generally when we try to write to a file which is opened for read-only purpose.

**10. No child process:** If a process has no further sub-process or child process, then the code returns -1 value and we get no child process error message.

**11. Try again:** An attempt to create a process fails, when there are no more process slots or not enough memory available. We then get **try again** error.

**12. Out of memory:** This error occurs when there is not enough memory available to execute a process.

**13. Permission denied:** This error occurs when we try to read from a file that is not opened. It suggests that an attempt was made to access a file in a way that is incompatible with the file's attributes.

## Methods of Error Handling in C

If we do not keep a check on errors, then it may result in either termination for the program or it may result in giving incorrect outputs. These errors can also change the logical flow of the code. Therefore, it is very important for the programmers to keep an eye on the unchecked errors if present in the code. Below are some funtional methods of error handling in C Library that are helpful while performing file operations:

### 1. perror()

- perror() function stands for **print error** and when called by the user, it displays a message describing about the most recent error that occured in the code.
- perror() function is contained in **stdio.h** header file.

**Syntax:**

```c
void perror(const char *str1)
```

Here, str1 is a string containing a custom message that is to be printed before the error message itself.

- User-defined message is printed firstly, followed by a colon and then the error message is printed.
- We can call perror() function even if no error has encountered and in that case, it will display **'No Error'** message.

**C Program to illustrate the use of perror() function:** In this program with the help of perror() function, we are displaying an error message when there is no file available naming "test.txt".

```c
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
  
int main(){
    FILE* fp;
    fp = fopen("test.txt","r");
    
    if(fp==NULL){          //Error handling in case if the file doesn't exists 
        perror("Message from perror "); 
        //User-Defined message passed as an argument string in perror() function
        return -1;
    }
    fclose(fp);
    return 0;
}
```

We have declared a file pointer 'fp' and using it, we are trying to open "test.txt" file in read only mode. If file doesn't exists i.e. fp is NULL, we call perror() function to print the error message.

**Output:**

```c
Assuming "test.txt" file doesn't exists: (Output):
    Message from perror : No such file or directory
```

Here, string - "Message from perror" is user-defined parameter passed in the function that is printed before the actual error message.

### 2. strerror()

- strerror() function is contained in **string.h** header file.
- It takes **'errno'** as an argument and returns the string error message of currently passed errno.

**Syntax:**

```c
char *strerror(int errnum)
```

Here, errnum is the error number (errno value) using which, respective error message will be displayed accordingly.

**C Program to illustrate the use of strerror() function:** In this program with the help of strerror() function, we are displaying an error message using errno value when there is no file available naming "test.txt".

```c
#include <errno.h>
#include <stdio.h>
#include <string.h>
  
int main(){
    FILE* fp;
    fp = fopen("test.txt","r");
    
    if(fp==NULL){          //Error handling in case if the file doesn't exists 
        printf("Error: %s\n",strerror(errno)); 
        //errno passed as an argument to display respective order error message
    }
    fclose(fp);
    return 0;
}
```

After opening the file in read only mode using file pointer fp, we check that if fp is NULL i.e. the file doesn't exists and then we pass errno as parameter in strerror() function that will print respective error message.

**Output:**

```c
Assuming "test.txt" file doesn't exists: (Output):
    Error: No such file or directory
```

As the file doesn't exists, we have printed errno-2 error message i.e. No such file or directory.

### 3. ferror()

- ferror() function is contained in **stdio.h** header file.
- This function basically checks for error in the file stream. It returns zero value if there is no error or else, it returns a positive non-zero value in case of error.
- File pointer stream is passed as an argument to the function. It will check for the error until the file is closed or we call clearerr() function.
- To identify the type of error, we can further use perror() function.

**Syntax:**

```c
int ferror(FILE *stream);
```

**C Program to illustrate the use of ferror() function:** In this program, we are trying to read data from the file but has opened the file in the wrong access mode i.e, writing mode. Now, ferror() function will detect this error in the file stream and using perror() function, we will display the error message.

```c
#include <stdio.h>

int main(){
   FILE *fp;
   fp = fopen("test.txt","w");

   char ch = fgetc(fp);  //Trying to read data, despite of writing mode opened 
   if(ferror(fp)){      //Error detected in the file stream pointer
      printf("File is opened in writing mode!");
      printf("\nError in reading from the file!");
      perror("Error Message from perror");
      //Identifying the type of error using perror() function
   }
   fclose(fp);
   return(0);
}
```

**Output:**

```c
 File is opened in writing mode!
 Error Message from perror: Bad file descriptor
 Error in reading from the file!
```

Here, we are printing error messages both user-defined and from perror() function as well.

### 4. feof()

- feof() function is contained in **stdio.h** header file.
- This function tests for end-of-file (eof indicator) for the file pointer stream passed as an argument to the function.
- On detecting that the end-of-file indicator associated with the file stream is set, it returns a non-zero positive value or else, zero is returned.

**Syntax:**

```c
int feof(FILE *stream);
```

Here, file pointer stream is passed as an argument and on detecting the end-of-file, this function will return a non-zero positive value.

**C Program to illustrate the use of feof() function:** In this program, we are trying to read data from the file and to avoid printing the garbage value characters, we are using feof() function. On detecting the end-of-file, it will return a non-zero value and hence, breaks the loop.

```c
#include <stdio.h>
#include <stdbool.h>

int main(){
   FILE *fp;
   fp = fopen("test.txt","r");
   if(fp==NULL){
      perror("Message from perror");
      return -1;
   }
   while(true){
      char ch = fgetc(fp); //Reading data from the file
      if(feof(fp)){       
      //On detecting the end-of-file, feof() function will return non-zero value   
      //hence, it will break the loop
         break;
      }
      printf("%c",ch);
   }
   fclose(fp);
   return 0;
}
```

**Output:** Assuming there's some data present in the "test.txt" file, it will read and print:

```c
 Scaler Topic: Error Handling in C during File Operations
```

**In absence of feof() function, it will further print the garbage value characters.**

### 5. clearerr()

- clearerr() function is contained in **stdio.h** header file.
- This function clears the end-of-file and the error indicators from the file stream.
- Error indicators are not automatically cleared and they continue to return the errors until clearerr() function is called.

**Syntax:**

```c
void clearerr(FILE *stream)
```

**C Program to illustrate the use of clearerr() function:** In this program, we are trying to read data from the file but has opened the file in the wrong access mode i.e, writing mode. Now, we will clear the error indicators using clearerr() function from the file stream and hence, ferror() couldn't then detect that error again.

```c
#include <stdio.h>

int main(){
   FILE *fp;
   fp = fopen("test.txt","w");
   char ch = fgetc(fp); //Trying to read data but the file is opened in writing mode
   if(ferror(fp)) {    //ferror() will detect error in file pointer stream
      printf("Error in reading from file!");
   }
   clearerr(fp);      //clearerr() will clear error-indicators from the file stream
   if(ferror(fp)){   //No error will be detected now
      printf("Error again in reading from file!");
   }
   fclose(fp);
   return 0;
}
```

After opening the file in writing mode, we are trying to read data from it using fgetc() and therefore, using ferror() function we can detect the error. After using clearerr() function, it will remove the error in the file pointer stream and further, we won't get any error on checking through ferror() function.

**Output:**

```c
 Error in reading from file!
```

**In absence of clearerr() function, output will be:**

```c
 Error in reading from file!
 Error again in reading from file!
```

### 6. Exit Status

- The macros of exit status() functional method are defined in **stdlib.h** header file. They are used to inform calling function about the error.
- There are two constant exit status values available for the exit() function: EXIT_STATUS and EXIT_FAILURE.
- When program code comes out after a successful operation, then EXIT_SUCCESS is used to show successful exit. Its value is defined as 0.
- We use EXIT_FAILURE in case of failures or abrupt termination of the program. Its value is defined as -1.

**Syntax:**

```c
exit(EXIT_SUCCESS);  //successful termination
exit(EXIT_FAILURE); //unsuccessful termination
```

**C Program to illustrate the use of Exit Status function:** In this program, we are illustrating the use of two exit function constant values: EXIT_SUCCESS and EXIT_FAILURE depending upon how the program code is terminated.

```c
#include <stdio.h>
#include <errno.h>
#include <string.h>
#include <stdlib.h>
  
int main(){
    FILE *fp;
    fp = fopen ("test.txt","r");
    if(fp==NULL){
        printf("Value of errno: %d",errno);
        perror("Error printed by perror");
        exit(EXIT_FAILURE); //Good practice to exit the program using exit status
        printf("This message will not be printed!"); 
        //This won't be printed due to exit above
    }
    else{
        fclose (fp);
        exit(EXIT_SUCCESS); //Successful exit from the program
        printf("This message will not be printed!"); 
        //This won't be printed due to exit above
    }
    return 0;
}
```

After opening a file using file pointer fp, if it doesn't exists then we will print the error messages and exit from the function (EXIT_FAILURE). If file exists, then we will exit from the program by executing else condition here (EXIT_SUCCESS). **Output:** In case, if "test.txt" file doesn't exists: **exit(EXIT_FAILURE)**

```c
 Error printed by perror: No such file or directory
 Value of errno: 2
```

### 7. Division by zero

- If we divide a number by zero, C programming language will give warnings and also give runtime error.
- To avoid such an undefined behaviour, there is no construct or method in C.
- To avoid such situations, we can check the value of divisor before using it for division purposes. This can be done using if-else conditions and whenever we encounter such a situation, we can simply print error message.

**C Program to illustrate the error of Division by zero:** In this program, we are keeping a check if in case we get zero number value for division that can produce errors and can also abruptly terminate the program.

```c
#include <stdio.h>
#include <stdlib.h>

void division(int x){
    if(x==0){ //Checking if divisor is zero, to avoid errors
        printf("Division by Zero is not allowed!");
        exit(EXIT_FAILURE); //unsuccessful termination
    }
    else{
        float fx = 10/x;
        printf("f(x) is: %.5f",fx);
    }
}
  
int main(){
    int x = 0; 
    division(x); //Calling function to perform division
    return 0;
}
```

Here, we have passed the value x in division function. Using if condition we check if it is 0, then we can't perform division using it. Using else condition, we divide 10 by x and then print the resultant value. **Output:**

```c
 Division by Zero is not allowed!
```

## Conclusion

- In C language when we call a function, a variable called **errno** is assigned with a numeric value and we can use that to identify the type of error if encountered while writing the code.
- When we perform operations of file handling in C, there are some common errors that we may encounter such as reading a file that doesn't even exists or using a file that has not been opened.
- To avoid errors while performing file operations, we have some helpful functional methods for error handling in C language: **perror(), strerror(), ferror(), feof(), clearerr() and Exit status**.
