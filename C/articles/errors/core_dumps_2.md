[](https://opensource.com/article/20/8/linux-dump)

# Creating and debugging Linux dump files

Knowing how to deal with dump files will help you find and fix hard-to-reproduce bugs in an application.

Crash dump, memory dump, core dump, system dump … all produce the same outcome: a file containing the state of an application's memory at a specific time—usually when the application crashes.

Knowing how to deal with these files can help you find the root cause(s) of a failure. Even if you are not a developer, dump files created on your system can be very helpful (as well as approachable) in understanding software.

This is a hands-on article, and can you follow along with the example by cloning the sample application repository with:

```bash
git clone https://github.com/hANSIc99/core_dump_example.git
```

## How signals relate to dumps

Signals are a kind of interprocess communication between the operating system and the user applications. Linux uses the signals defined in the [POSIX standard](https://en.wikipedia.org/wiki/POSIX). On your system, you can find the standard signals defined in `/usr/include/bits/signum-generic.h`. There is also an informative [man signal](https://man7.org/linux/man-pages/man7/signal.7.html) page if you want more on using signals in your application. Put simply, Linux uses signals to trigger further activities based on whether they were expected or unexpected.

When you quit a running application, the application will usually receive the `SIGTERM` signal. Because this type of exit signal is expected, this action will not create a memory dump.

The following signals will cause a dump file to be created (source: [GNU C Library](https://www.gnu.org/software/libc/manual/html_node/Program-Error-Signals.html#Program-Error-Signals)):

- SIGFPE: Erroneous arithmetic operation
- SIGILL: Illegal instruction
- SIGSEGV: Invalid access to storage
- SIGBUS: Bus error
- SIGABRT: An error detected by the program and reported by calling abort
- SIGIOT: Labeled archaic on Fedora, this signal used to trigger on `abort()` on a [PDP-11](https://en.wikipedia.org/wiki/PDP-11) and now maps to SIGABRT

## Creating dump files

Navigate to the `core_dump_example` directory, run `make`, and execute the sample with the `-c1` switch:

```text
./coredump -c1
```

The application should exit in state 4 with an error:

![](core_dumps_2_images/e51c61201048dcddada930e6da399fee_MD5.webp)

(Stephan Avenwedde, [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/))

"Abgebrochen (Speicherabzug geschrieben)" roughly translates to "Segmentation fault (core dumped)."

Whether it creates a core dump or not is determined by the resource limit of the user running the process. You can modify the resource limits with the `ulimit` command.

Check the current setting for core dump creation:

```bash
ulimit -c
```

If it outputs `unlimited`, then it is using the (recommended) default. Otherwise, correct the limit with:

```bash
ulimit -c unlimited
```

To disable creating core dumps' type:

```bash
ulimit -c 0
```

The number specifies the resource in kilobytes.

## What are core dumps?

The way the kernel handles core dumps is defined in:

```text
/proc/sys/kernel/core_pattern
```

I'm running Fedora 31, and on my system, the file contains:

```text
/usr/lib/systemd/systemd-coredump %P %u %g %s %t %c %h
```

This shows core dumps are forwarded to the `systemd-coredump` utility. The contents of `core_pattern` can vary widely between the different flavors of Linux distributions. When `systemd-coredump` is in use, the dump files are saved compressed under `/var/lib/systemd/coredump`. You don't need to touch the files directly; instead, you can use `coredumpctl`. For example:

```text
coredumpctl list
```

shows all available dump files saved on your system.

Let’s unpack that compressed file to an handy location and inspect it a bit :

```bash
zstd --uncompress /var/lib/systemd/coredump/core.badprogram.1000.9d49cca5818645e4baacc1ddddd7a9e8.4269.1712308425000000.zst -o badprogram.core
/var/lib/systemd/coredump/core.badprogram.1000.9d49cca5818645e4baacc1ddddd7a9e8.4269.1712308425000000.zst: 475136 bytes

ls -l
-rwxr-xr-x 1 andrea andrea  21152 apr  5 11:08 badprogram*
-rw-r--r-- 1 andrea andrea    240 apr  5 09:30 badprogram.c
-rw-r----- 1 andrea andrea 475136 apr  5 11:13 badprogram.core
```

Now we run again the faulty program, only this time we do with the help of Gnu Debugger and passing also the coredump file:

```bash
gdb ./badprogram -c badprogram.core
```

With `coredumpctl dump`, you can retrieve information from the last dump file saved:

```bash
[stephan@localhost core_dump_example]$ ./coredump 
Application started…

(…….)

Message: Process 4598 (coredump) of user 1000 dumped core.

Stack trace of thread 4598:
#0 0x00007f4bbaf22625 __GI_raise (libc.so.6)
#1 0x00007f4bbaf0b8d9 __GI_abort (libc.so.6)
#2 0x00007f4bbaf664af __libc_message (libc.so.6)
#3 0x00007f4bbaf6da9c malloc_printerr (libc.so.6)
#4 0x00007f4bbaf6f49c _int_free (libc.so.6)
#5 0x000000000040120e n/a (/home/stephan/Dokumente/core_dump_example/coredump)
#6 0x00000000004013b1 n/a (/home/stephan/Dokumente/core_dump_example/coredump)
#7 0x00007f4bbaf0d1a3 __libc_start_main (libc.so.6)
#8 0x000000000040113e n/a (/home/stephan/Dokumente/core_dump_example/coredump)
Refusing to dump core to tty (use shell redirection or specify — output).
```

This shows that the process was stopped by `SIGABRT`. The stack trace in this view is not very detailed because it does not include function names. However, with `coredumpctl debug`, you can simply open the dump file with a debugger ([GDB](https://www.gnu.org/software/gdb/) by default). Type `bt` (short for backtrace) to get a more detailed view:

```bash
Core was generated by `./coredump -c1'.
Program terminated with signal SIGABRT, Aborted.
#0  __GI_raise (sig=sig@entry=6) at ../sysdeps/unix/sysv/linux/raise.c:50
50  return ret;
(gdb) bt
#0  __GI_raise (sig=sig@entry=6) at ../sysdeps/unix/sysv/linux/raise.c:50
#1  0x00007fc37a9aa8d9 in __GI_abort () at abort.c:79
#2  0x00007fc37aa054af in __libc_message (action=action@entry=do_abort, fmt=fmt@entry=0x7fc37ab14f4b "%s\n") at ../sysdeps/posix/libc_fatal.c:181
#3  0x00007fc37aa0ca9c in malloc_printerr (str=str@entry=0x7fc37ab130e0 "free(): invalid pointer") at malloc.c:5339
#4  0x00007fc37aa0e49c in _int_free (av=<optimized out>, p=<optimized out>, have_lock=0) at malloc.c:4173
#5  0x000000000040120e in freeSomething(void*) ()
#6  0x0000000000401401 in main ()
```

The memory addresses: `main()` and `freeSomething()` are quite low compared to subsequent frames. Due to the fact that shared objects are mapped to an area at the end of the virtual address space, you can assume that the `SIGABRT` was caused by a call in a shared library. Memory addresses of shared objects are not constant between invocations, so it is totally fine when you see varying addresses between calls.

The stack trace shows that subsequent calls originate from `malloc.c`, which indicates that something with memory (de-)allocation could have gone wrong.

In the source code, you can see (even without any knowledge of C++) that it tried to free a pointer, which was not returned by a memory management function. This results in undefined behavior and causes the `SIGABRT`:

```c
void freeSomething(void *ptr){
    free(ptr);
}
int nTmp = 5;
int *ptrNull = &nTmp;
freeSomething(ptrNull);
```

The systemd coredump utility can be configured under `/etc/systemd/coredump.conf`. Rotation of dump file cleaning can be configured in `/etc/systemd/system/systemd-tmpfiles-clean.timer`.

You can find more information about `coredumpctl` on its [man page](https://man7.org/linux/man-pages/man1/coredumpctl.1.html).

## Compiling with debug symbols

Open the `Makefile` and comment out the last part of line 9. It should now look like:

```text
CFLAGS =-Wall -Werror -std=c++11 -g
```

The `-g` switch enables the compiler to create debug information. Start the application, this time with the `-c2` switch:

```bash
./coredump -c2
```

You will get a floating-point exception. Open the dump in GDB with:

```bash
coredumpctl debug
```

This time, you are pointed directly to the line in the source code that caused the error:

```bash
Reading symbols from /home/stephan/Dokumente/core_dump_example/coredump…
[New LWP 6218]
Core was generated by `./coredump -c2'.
Program terminated with signal SIGFPE, Arithmetic exception.
#0 0x0000000000401233 in zeroDivide () at main.cpp:29
29 nRes = 5 / nDivider;
(gdb)
```

Type `list` to get a better overview of the source code:

```c
(gdb) list
24	int zeroDivide(){
25	    int nDivider = 5;
26	    int nRes = 0;
27	    while(nDivider > 0){
28	        nDivider--;
29	        nRes = 5 / nDivider;
30	    }
31	    return nRes;
32	}
```

Use the command `info locals` to retrieve the values of the local variables from the point in time when the application failed:

```c
(gdb) info locals
nDivider = 0
nRes = 5
```

In combination with the source code, you can see that you ran into a division by zero:

```c
nRes = 5 / 0
```

## Conclusion

Knowing how to deal with dump files will help you find and fix hard-to-reproduce random bugs in an application. And if it is not your application, forwarding a core dump to the developer will help her or him find and fix the problem.
