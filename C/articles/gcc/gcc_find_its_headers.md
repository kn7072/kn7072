# Where Does GCC Look to Find its Header Files?
[источник](https://commandlinefanatic.com/cgi-bin/showarticle.cgi?article=art026)

Partly by convention and partly by design, C programs are split into source files that describe the functionality of the program itself and header files that describe how to invoke that functionality from other source files. Technically speaking, you can write a complete and useful C program without ever creating or referring to a header file — this is actually feasible when writing embedded apps — but practically, you're going to probably need to at least import a few. You can't even read a file or write to the console without importing <stdio.h>, for example.

`include`-ing a header file in a C program actually means copying the contents of another file in the current one. The strange-looking construct in listings 1 and 2 compile and work correctly:

```c
printf( "%d\n", i );
```

Listing 1: increment.c

```c
#include <stdio.h>  

int main( int argc, char *argv[] ) 
    {   
        int i = 0;   
        for ( i = 0; i < 10; i++ ) { 
            #include "increment.c"
        } 
    }
```

Listing 2: count.c

Nobody ever codes this way (I hope...) but since the C preprocessor's `#include` directive just means "copy the contents of the named file into this one before compiling", you could.

In practical use, though, `#include` is used to copy in _header_ files that describe other modules which will be linked and referred to within the current source file. C includes dozens of standard header files for I/O, math, concurrency, string manipulation, etc. If you refer to one, its contents must be copied into the current source file before it can be processed. So, where does the compiler look to find these files? The earliest description of the C programming language, Kernighan and Ritchie's book "The C Programming Language" (AKA K&R), talks about the preprocessor in chapter 4:

File inclusion makes it easy to handle collections of #defines and declarations (among other things). Any source line of the form

```c
#include "filename"
```

or

```c
#include <filename>
```

is replaced by the contents of the file _filename_. If the _filename_ is quoted, searching for the file typically begins where the source program was found; if it is not found there, or if the name is enclosed in < and >, seaching follows an implementation-defined rule to find the file.

While not an official standard, K&R suggested two different ways to indicate to the compiler where to look for a header file. The first was to enclose the name of the header file in double quotes, e.g. `"header.h"`. In this case, the compiler should (typically) look for the header in the same directory as the source file. Otherwise, the search should be "implementation-defined". Well, that's not very informative. K&R was published in 1978, but C was standardized by ANSI in 1983. So what does the standard say about header file inclusion?

The [official C standard](http://www.open-std.org/jtc1/sc22/WG14/www/docs/n1256.pdf) in section 6.10.2, "Source file inclusion", states:

> A preprocessing directive of the form
> 
> ```
> #include "q-char-sequence" new-line
> ```
> 
> causes the replacement of that directive by the entire contents of the source file identified by the specified sequence between the " delimiters. The named source file is searched for in an implementation-defined manner.

The standard actually says _less_ about where to look for header files than K&R does! Technically speaking, it's impossible to write a portable C program consisting of less than one source file, since the compiler can be standards compliant while searching for header files anywhere it cares to.

Although Apple seems to have nudged the world in the direction of LLVM, for decades, GCC was the de facto standard for C compilation until very recently. Sometimes you had to use a vendor-specific compiler like Microsoft's, but GCC mostly blazed the trail for standardizing the non-standard parts of the C progamming language. So what is the "implementation-defined" GCC manner for header file incluion? As it turns out, although it mostly does what you want it to in most cases, it can be pretty complex and compiler flags can make radical changes to it.

In the simplest (theoretical) case, you have a single source file and a single header file, both in the same directory. In this case, GCC's job seems easy; it just looks in the current directory, finds the header file, and compiles. But actually, there's even a bit of a twist here. This complexity arises because the behavior differs when you use quotes vs. angle brackets. If you use quotes, the current directory is searched first. If the header file isn't found, then the angle-bracket search path is used. You can verify this by actually "overriding" `stdio.h`

```
#define SEEK_SET  12
```

Listing 3: overridden stdio.h

If you include this file in the same directory as `source.c`:
```c 
#include <stdio.h>  

int main( int argc, char *argv[] ) 
{   
    printf( "SEEK_SET = %d\n" ); 
}
```

Listing 4: system search path

And compile and run this, you'll see:`$ ./a.out SEEK_SET = 0`
The compiler found the system copy of `stdio.h` instead of my "override". However, if I change the `#include` to use single quotes:
```c
#include "stdio.h"  

int main( int argc, char *argv[] ) 
{   
    printf( "SEEK_SET = %d\n" ); 
}
```

Listing 5: system search path

The output becomes:`$ ./a.out SEEK_SET = 12`

I also got a compiler warning about an incompatible implicit declaration of built-in function 'printf' — my new `stdio.h` didn't declare it, but of course the linker still found it.

So, if a header file is not found in the current directory, where does it look? The [GCC documentation](http://gcc.gnu.org/onlinedocs/cpp/Search-Path.html) states:

> GCC looks in several different places for headers. On a normal Unix system, if you do not instruct it otherwise, it will look for headers requested with `#include` <_file_> in:
> 
>   /usr/local/include
>   _libdir_/_gcc_/_target_/_version_/include
>   /usr/target/include
>   /usr/include

but that's sort of a wishy-washy answer (and also incomplete). Surely there must be a way to get GCC to tell you exactly where it's going to end up looking for its header files? Well, although it's convenient to think of GCC as a single monolithic application that takes in source code files and spits out working programs, it's technically a collection of other programs which chain together to produce the final compiled object file. The first of these is `CPP`, short for _C Pre-Processor_, whose job is to look for compiler directives like `#include` and modify the source code as specified by them; in the case of include, by copying the contents of another file into the current one. You can see where it looks for these files by passing it the `-v` flag:
```bash
$ cpp -v 
... 
#include "..." search starts here: 
#include <...> search starts here:
/usr/local/include  
/usr/lib/gcc/x86_64-linux-gnu/4.4.5/include  
/usr/lib/gcc/x86_64-linux-gnu/4.4.5/include-fixed  
/usr/include/x86_64-linux-gnu  
/usr/include
```
this path is actually built into CPP (which is part of GCC) at compile time; if for whatever reason you end up deleting one of those directories, it will still be checked for on each compile. Each directory is searched in the order it's listed here; if a file is found in `/usr/local/include`, the next three directories won't be checked. This behavior is important — notice the `include-fixed` directory in the search path? On my system, it includes two files: `limits.h` and `syslimits.h`. Both of these files also appear in `/usr/include`; however, GCC will not operate correctly if it finds the copies from the `/usr/include` directory later in its search path.

There are a couple of ways you can manipulate this directory structure. The simplest is by providing the compiler flag `-I`. `-I` is followed by an absolute or relative (to the current directory) path, with no spaces, and inserts the named directory at the _beginning_ of the "angle-bracket" search path. Thus, if you create a directory `headers`, copy the "overridden" `stdio.h` from listing 3 into it, and invoke `gcc` with:

```
gcc -Iheaders source.c
```

the output will show SEEK_SET as 12 even if you `#include stdio.h` with angle brackets as in listing 4. `cpp -v` verifies that the `-I`'ed directory is first in the search path:
```bash
$ cpp -Iheaders -v 
...
#include "..." search starts here: 
#include <...> search starts here:  
headers  
/usr/local/include  
/usr/lib/gcc/x86_64-linux-gnu/4.4.5/include  
/usr/lib/gcc/x86_64-linux-gnu/4.4.5/include-fixed  
/usr/include/x86_64-linux-gnu  
/usr/include
```
But wait — earlier I said that GCC will not compile correctly if it picks up `limits.h` from `/usr/include`. So what happens if I try to force `/usr/include` to be the first directory in the list via:`$ cpp -I/usr/include`
? As it turns out, GCC will ignore me in this case:
```bash
$ cpp -I/usr/include -v 
...
ignoring duplicate directory "/usr/include"  
as it is a non-system directory that duplicates a system directory 
#include "..." search starts here: 
#include <...> search starts here:  
/usr/local/include  
/usr/lib/gcc/x86_64-linux-gnu/4.4.5/include  
/usr/lib/gcc/x86_64-linux-gnu/4.4.5/include-fixed  
/usr/include/x86_64-linux-gnu  
/usr/include
```

There is no way to change this search order other than to recompile GCC itself. You _can_ pass in the `-nostdinc` option which will remove all of these directories from the search path:
```bash
$ cpp -nostdinc -v 
... 
#include "..." search starts here: 
#include <...> search starts here:
```
But there are only a few good reasons why you'd want to do that (compiling the Linux kernel is one example). Other than `-nostdinc`, GCC does not give you a way to _remove_ a directory from the search path once it's been added.

If you want to add multiple directories to the search path, you specify the `-I` directory multiples times. These new directories are added to the beginning of the search path, in the order that they're presented on the command line. If you have a lot of paths that you need to specify repeatedly, GCC looks for an environment variable called `CPATH` that has the same effect as include `-I` multiple times, once for each colon- separated path in the declaration:

```bash
$ EXPORT CPATH=hdr1:hdr2
$ cpp -v
...
#include <...> search starts here:
 hdr1
 hdr2
 /usr/local/include
...
```

If you combine `CPATH` with `-I` flags, `-I` takes precedence:
```bash
$ EXPORT CPATH=hdr1:hdr2 
$ cpp -Ihdr3 -v
... 
#include <...> search starts here:  
hdr3  
hdr1  
hdr2  
/usr/local/include 
...

```
In general, though, you should probably never use the `CPATH` environment variable, since you'll end up creating non-portable source code; specify a `Makefile` instead.

If you look at all of the CPP search directory examples here, you'll notice that they always start with:

```
#include "..." search starts here:
```

And immediately jumping down to the angle-bracket search path, implying that nothing is searched for quoted includes. As we know from experimentation, however, this search does include the current directory; GCC actually does allow you to modify this search path as well, with the `-iquote` compiler flag.
```bash
$ cpp -iquote hdr1 -v 
... 
#include "..." search starts here:  
hdr1
#include <...> search starts here:  
/usr/local/include  
/usr/lib/gcc/x86_64-linux-gnu/4.4.5/include  
/usr/lib/gcc/x86_64-linux-gnu/4.4.5/include-fixed  
/usr/include/x86_64-linux-gnu  
/usr/include
```

Here's an edge case that bit me last week. Consider this directory structure:

base/Makefile
base/shared.c
base/core.h
base/core.c
override/Makefile
override/core.c
override/core.h

What I'm trying to do here is to generate two different executables - `base` and `override`. I want a different version of `core.h` in each, but I want to reuse `shared.c` in each. So my Makefile in override looks like this:
```c
override: ../base/shared.c core.c core.h   
    gcc -o override ../base/shared.c core.c`

The top of `shared.c` looks like this:
#include "core.h"
```
Naively, I assumed that `shared.c` would compile with the version of `core.h` from the `override` directory, since that's the "current working directory". As it turns out, no — `GCC` considers `../base` the current working directory for that compilation unit because that's where it was found. I spent a lot of time banging my head against the keyboard trying to figure out what was going on here, since the problem manifested itself as a memory corruption quite a ways into the execution of the application. One solution would be the `-iquote` compiler directive... although I think if you find yourself manipulating the quote search path this way, it's time to rethink your application structure (and, in my case, I did).
