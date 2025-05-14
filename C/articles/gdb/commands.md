## breakpoints

(gdb) break tree.c:insert
(gdb) break tree.c:10
(gdb) break main
(gdb) break func if a == 10
(gdb) b -source /path/file.c -line xxx 9.2.2 Explicit Locations
примеры точек останова которые монжно использовать в файле my-dprintf-breakpoints
break -source /path/file.c -line 127
break -source /path/file.c -line 148 if j>3

(gdb) tbreak args -Set a breakpoint enabled only for one stop.

## printf

https://sourceware.org/gdb/current/onlinedocs/gdb.html/Output.html#Output
printf "x is %d\n",x

## Listing currently defined breakpoints

(gdb) info breakpoints

## Saving dprintf commands for a later session

(gdb) save breakpoints my-dprintf-breakpoints (создаст файл my-dprintf-breakpoints в текущем каталоге)

## loading breakbpoints

(gdb) source my-dprintf-breakpoints

## Logging GDB's output to a file

(gdb) set logging file my-gdb-log
(gdb) set logging enabled on

(gdb) run
(gdb) set logging enabled off
As shown in the example, both program output and GDB's output are still sent to the console. (The set logging debugredirect on command can be used to send GDB's output only to the log file.)

## 4.12 Setting a Bookmark to Return to later

(gdb) checkpoint
Save a snapshot of the debugged program’s current execution state. The checkpoint command takes no arguments, but each checkpoint is assigned a small integer id, similar to a breakpoint id.

(gdb) info checkpoints
List the checkpoints that have been saved in the current debugging session. For each checkpoint, the following information will be listed:

    Checkpoint ID
    Process ID
    Code Address
    Source line, or label

(gdb) restart checkpoint-id
Restore the program state that was saved as checkpoint number checkpoint-id. All program variables, registers, stack frames etc. will be returned to the values that they had when the checkpoint was saved. In essence, gdb will "wind back the clock" to the point in time when the checkpoint was saved.

    Note that breakpoints, GDB variables, command history etc. are not affected by restoring a checkpoint. In general, a checkpoint only restores things that reside in the program being debugged, not in the debugger.

(gdb) delete checkpoint checkpoint-id
Delete the previously-saved checkpoint identified by checkpoint-id.

## 5.1.2 Setting Watchpoints

(gdb) info watchpoints This command prints a list of watchpoints, using the same format as info break
(gdb) watch [-l|-location] expr [thread thread-id] [mask maskvalue] [task task-id]
(gdb) watch foo

## Redirecting program output to a file

(gdb) run >my-program-output

(gdb) show paths Display the list of search paths for executables (the PATH environment variable).

(gdb) show environment [varname] Print the value of environment variable varname to be given to your program when it starts. If you do not supply varname, print the names and values of all environment variables to be given to your program. You can abbreviate environment as env

(gdb) set environment varname [=value] Set environment variable varname to value
set env USER = foo

(gdb) info terminal
Displays information recorded by GDB about the terminal modes your program is using.

(gdb) info threads [-gid] [thread-id-list]
Display information about one or more threads. With no arguments displays information about all threads. You can specify the list of threads that you want to display using the thread ID list syntax (see thread ID lists).

    GDB displays for each thread (in this order):

        the per-inferior thread number assigned by GDB
        the global thread number assigned by GDB, if the ‘-gid’ option was specified
        the target system’s thread identifier (systag)
        the thread’s name, if one is known. A thread can either be named by the user (see thread name, below), or, in some cases, by the program itself.
        the current stack frame summary for that thread

## 8.2 Backtraces

(gdb) backtrace [option]… [qualifier]… [count]
(gdb) bt [option]… [qualifier]… [count]

(gdb) bt
(gdb) bt -full Print the values of the local variables also. This can be combined with the optional count to limit the number of frames shown.

## 8.3 Selecting a Frame

(gdb) frame [ frame-selection-spec ]
(gdb) f [ frame-selection-spec ]

(gdb) up n
Move n frames up the stack; n defaults to 1

(gdb) down n
Move n frames down the stack; n defaults to 1

(gdb) info frame
(gdb) info f
This command prints a verbose description of the selected stack frame, including:
the address of the frame
the address of the next frame down (called by this frame)
the address of the next frame up (caller of this frame)
the language in which the source code corresponding to this frame is written
the address of the frame’s arguments
the address of the frame’s local variables
the program counter saved in it (the address of execution in the caller frame)
which registers were saved in the frame

    The verbose description is useful when something has gone wrong that has made the stack format fail to fit the usual conventions.

(gdb) info locals [-q]
Print the local variables of the selected frame, each on a separate line.

(gdb) show listsize
Display the number of lines that list prints.

(gdb) set listsize count
(gdb) set listsize unlimited
Make the list command display count source lines (unless the list argument explicitly specifies some other number). Setting count to unlimited or 0 means there’s no limit

## All the options and command line arguments you give are processed in sequential order. The order makes a difference when the -x option is used.

--help
-h

    List all options, with brief explanations.

--symbols=file
-s file

    Read symbol table from file.

--write

    Enable writing into executable and core files.

--exec=file
-e file

    Use file as the executable file to execute when appropriate, and for examining pure data in conjunction with a core dump.

--se=file

    Read symbol table from file and use it as the executable file.

--core=file
-c file

    Use file as a core dump to examine.

--command=file
-x file

    Execute GDB commands from file.

--eval-command=command
-ex command

    Execute given GDB command.

--init-eval-command=command
-iex

    Execute GDB command before loading the inferior.

--directory=directory
-d directory

    Add directory to the path to search for source files.

--nh

    Do not execute commands from ~/.config/gdb/gdbinit, ~/.gdbinit, ~/.config/gdb/gdbearlyinit, or ~/.gdbearlyinit

--nx
-n

    Do not execute commands from any .gdbinit or .gdbearlyinit initialization files.

--quiet
--silent
-q

    "Quiet". Do not print the introductory and copyright messages. These messages are also suppressed in batch mode.

--batch

    Run in batch mode. Exit with status 0 after processing all the command files specified with -x (and .gdbinit, if not inhibited). Exit with nonzero status if an error occurs in executing the GDB commands in the command files.

    Batch mode may be useful for running GDB as a filter, for example to download and run a program on another computer; in order to make this more useful, the message

    Program exited normally.

    (which is ordinarily issued whenever a program running under GDB control terminates) is not issued when running in batch mode.

--batch-silent

    Run in batch mode, just like --batch, but totally silent. All GDB output is suppressed (stderr is unaffected). This is much quieter than --silent and would be useless for an interactive session.

    This is particularly useful when using targets that give ‘Loading section’ messages, for example.

    Note that targets that give their output via GDB, as opposed to writing directly to stdout, will also be made silent.

--args prog [arglist]

    Change interpretation of command line so that arguments following this option are passed as arguments to the inferior. As an example, take the following command:

    gdb ./a.out -q

    It would start GDB with -q, not printing the introductory message. On the other hand, using:

    gdb --args ./a.out -q

    starts GDB with the introductory message, and passes the option to the inferior.

--pid=pid

    Attach GDB to an already running program, with the PID pid.

--tui

    Open the terminal user interface.

--readnow

    Read all symbols from the given symfile on the first access.

--readnever

    Do not read symbol files.

--return-child-result

    GDB’s exit code will be the same as the child’s exit code.

--configuration

    Print details about GDB configuration and then exit.

--version

    Print version information and then exit.

--cd=directory

    Run GDB using directory as its working directory, instead of the current directory.

--data-directory=directory
-D

    Run GDB using directory as its data directory. The data directory is where GDB searches for its auxiliary files.

--fullname
-f

    Emacs sets this option when it runs GDB as a subprocess. It tells GDB to output the full file name and line number in a standard, recognizable fashion each time a stack frame is displayed (which includes each time the program stops). This recognizable format looks like two ‘\032’ characters, followed by the file name, line number and character position separated by colons, and a newline. The Emacs-to-GDB interface program uses the two ‘\032’ characters as a signal to display the source code for the frame.

-b baudrate

    Set the line speed (baud rate or bits per second) of any serial interface used by GDB for remote debugging.

-l timeout

    Set timeout, in seconds, for remote debugging.

--tty=device

    Run using device for your program’s standard input and output.

gdb -x '/home/stepan/GIT/kn7072/C/code/CPrimerPlus6E/Ch03/my_break' -ex 'run' main

gdb -q -batch -x /home/stepan/GIT/kn7072/C/code/CPrimerPlus6E/Ch03/my_break main

gdb -batch --nh -q -ex 'dprintf 10, "%u %u\n", i, r' -ex 'run' ./main

gdb -q -x tree-debugging-commands
где tree-debugging-commands содержит следующие команды
file tree
source my-dprintf-breakpoints
source my-insert-breakpoint
set dprintf-style call

    the file my-dprintf-breakpoints contains three lines:

    dprintf /home/kev/ctests/tree.c:41,"Allocating node for data=%s\n", data
    dprintf /home/kev/ctests/tree.c:47,"Recursing left for %s at node %s\n", data, tree->data
    dprintf /home/kev/ctests/tree.c:49,"Recursing right for %s at node %s\n", data, tree->data

It should also be possible to achieve the same effect, but without needing to interact with GDB, by using the following command:
$ gdb -q -x tree-debugging-commands -ex 'run >my-program-output' -ex quit

info functions [-q] [-n] [-t type_regexp] [regexp]
info fun ^step
i func SetB

17.5 Calling Program Functions
print expr
Evaluate the expression expr and display the resulting value. The expression
may include calls to functions in the program being debugged.

call expr
Evaluate the expression expr without displaying void returned values.
You can use this variant of the print command if you want to execute a function
from your program that does not return anything (a.k.a. a void function), but
without cluttering the output with void returned values that gdb will otherwise
print. If the result is not void, it is printed and saved in the value history.

list function_name - посмотреть листинг ее исходного кода

Symbol table
Run the command

```bash
info address <symbol name>    to see the address of that symbol.
info address displayBits
Symbol "displayBits" is a function at address 0x5555555556f1.
```

Now since you know the address you can reverse lookup the symbol name with the command

```bash
info symbol <address>
dap> info symbol 0x5555555556f1
displayBits in section .text of /home/stepan/git_repos/kn7072/C/code/bitwise_operations/bit_tricks_1
```

Working with Variables

```bash
info locals
val = 0xa

```

It says the value of the variable val is 0xa. We can also print the values with the command print (or just p).

```bash
p val
$1 = 0xa
p/d val
$2 = 10
```

By default, the value will be in hex, but we can specify /d to display in decimal. Here are other formats:
format description
x hexadecimal
d signed decimal
u unsigned decimal
o octal
t binary
a address, absolute and relative
c character
f floating-point

// https://sourceware.org/gdb/current/onlinedocs/gdb.html/Assignment.html#Assignment

```bash
set variable val=5   or set var val=5
p/d val
$3 = 5
```

You can also use the 'set' command to change memory locations.

```bash
(gdb) l
6       {
7           int i;
8           struct file *f, *ftmp;
9
(gdb) set variable i = 10
(gdb) p i
$1 = 10

(gdb) p &i
$2 = (int *) 0xbfbb0000
(gdb) set *((int *) 0xbfbb0000) = 20
(gdb) p i
$3 = 20
```

10.6 Examining Memory

You can use the command x (for "examine") to examine memory in any of several formats, independently of your program’s data types.

x/nfu addr
x addr
x

    Use the x command to examine memory.

n, f, and u are all optional parameters that specify how much memory to display and how to format it; addr is an expression giving the address where you want to start displaying memory. If you use defaults for nfu, you need not type the slash ‘/’. Several commands set convenient defaults for addr.

n, the repeat count

    The repeat count is a decimal integer; the default is 1. It specifies how much memory (counting by units u) to display. If a negative number is specified, memory is examined backward from addr.

f, the display format

    The display format is one of the formats used by print (‘x’, ‘d’, ‘u’, ‘o’, ‘t’, ‘a’, ‘c’, ‘f’, ‘s’), ‘i’ (for machine instructions) and ‘m’ (for displaying memory tags). The default is ‘x’ (hexadecimal) initially. The default changes each time you use either x or print.

u, the unit size

    The unit size is any of

    b

        Bytes.
    h

        Halfwords (two bytes).
    w

        Words (four bytes). This is the initial default.
    g

        Giant words (eight bytes).

    Each time you specify a unit size with x, that size becomes the default unit the next time you use x. For the ‘i’ format, the unit size is ignored and is normally not written. For the ‘s’ format, the unit size defaults to ‘b’, unless it is explicitly given. Use x /hs to display 16-bit char strings and x /ws to display 32-bit strings. The next use of x /s will again display 8-bit strings. Note that the results depend on the programming language of the current compilation unit. If the language is C, the ‘s’ modifier will use the UTF-16 encoding while ‘w’ will use UTF-32. The encoding is set by the programming language and cannot be altered.

addr, starting display address

    addr is the address where you want GDB to begin displaying memory. The expression need not have a pointer value (though it may); it is always interpreted as an integer address of a byte of memory. See Expressions, for more information on expressions. The default for addr is usually just after the last address examined—but several other commands also set the default address: info breakpoints (to the address of the last breakpoint listed), info line (to the starting address of a line), and print (if you use it to display a value from memory).

For example, ‘x/3uh 0x54320’ is a request to display three halfwords (h) of memory, formatted as unsigned decimal integers (‘u’), starting at address 0x54320. ‘x/4xw $sp’ prints the four words (‘w’) of memory above the stack pointer (here, ‘$sp’; see Registers) in hexadecimal (‘x’).

You can also specify a negative repeat count to examine memory backward from the given address. For example, ‘x/-3uh 0x54320’ prints three halfwords (h) at 0x5431a, 0x5431c, and 0x5431e

All the defaults for the arguments to x are designed to make it easy to continue scanning memory with minimal specifications each time you use x. For example, after you have inspected three machine instructions with ‘x/3i addr’, you can inspect the next seven with just ‘x/7’. If you use RET to repeat the x command, the repeat count n is used again; the other arguments default as for successive uses of x.

When examining machine instructions, the instruction at current program counter is shown with a => marker. For example:

(gdb) x/5i $pc-6
0x804837f <main+11>: mov %esp,%ebp
0x8048381 <main+13>: push %ecx
0x8048382 <main+14>: sub $0x4,%esp
=> 0x8048385 <main+17>: movl $0x8048460,(%esp)
0x804838c <main+24>: call 0x80482d4 <puts@plt>

If the architecture supports memory tagging, the tags can be displayed by using ‘m’. See Memory Tagging.

10.14 Registers
You can refer to machine register contents, in expressions, as variables with names starting with ‘$’. The names of registers are different for each machine; use info registers to see the names used on your machine.

info registers

    Print the names and values of all registers except floating-point and vector registers (in the selected stack frame).

info all-registers

    Print the names and values of all registers, including floating-point and vector registers (in the selected stack frame).

info registers reggroup …

    Print the name and value of the registers in each of the specified reggroups. The reggroup can be any of those returned by maint print reggroups (see Maintenance Commands).

info registers regname …

    Print the relativized value of each specified register regname. As discussed in detail below, register values are normally relative to the selected stack frame. The regname may be any register name valid on the machine you are using, with or without the initial ‘$’.

GDB has four "standard" register names that are available (in expressions) on most machines—whenever they do not conflict with an architecture’s canonical mnemonics for registers.

The register names $pc and $sp are used for the program counter register and the stack pointer. 
$fp is used for a register that contains a pointer to the current stack frame, and
$ps is used for a register that contains the processor status. For example, you could print the program counter in hex with

pc
Счётчик инструкций или program counter - это специальный регистр процессора, который указывает на следующую инструкцию в программе, которую надо исполнить. Программа состоит из инструкций лежащих в памяти. С помощью этого счётчика компьютер проходит вдоль всего кода попутно извлекая и исполняя эти инструкции

p/x $pc

or print the instruction to be executed next with

x/i $pc

or add four to the stack pointer12 with

set $sp += 4

Whenever possible, these four standard register names are available on your machine even though the machine has different canonical mnemonics, so long as there is no conflict. The info registers command shows the canonical names. For example, on the SPARC, info registers displays the processor status register as $psr but you can also refer to it as $ps; and on x86-based machines $ps is an alias for the EFLAGS register.

GDB always considers the contents of an ordinary register as an integer when the register is examined in this way. Some machines have special registers which can hold nothing but floating point; these registers are considered to have floating point values. There is no way to refer to the contents of an ordinary register as floating point value (although you can print it as a floating point value with ‘print/f $regname’).

Some registers have distinct "raw" and "virtual" data formats. This means that the data format in which the register contents are saved by the operating system is not the same one that your program normally sees. For example, the registers of the 68881 floating point coprocessor are always saved in "extended" (raw) format, but all C programs expect to work with "double" (virtual) format. In such cases, GDB normally works with the virtual format only (the format that makes sense for your program), but the info registers command prints the data in both formats.

Some machines have special registers whose contents can be interpreted in several different ways. For example, modern x86-based machines have SSE and MMX registers that can hold several values packed together in several different formats. GDB refers to such registers in struct notation:

(gdb) print $xmm1
$1 = {
v4_float = {0, 3.43859137e-038, 1.54142831e-044, 1.821688e-044},
v2_double = {9.92129282474342e-303, 2.7585945287983262e-313},
v16_int8 = "\000\000\000\000\3706;\001\v\000\000\000\r\000\000",
v8_int16 = {0, 0, 14072, 315, 11, 0, 13, 0},
v4_int32 = {0, 20657912, 11, 13},
v2_int64 = {88725056443645952, 55834574859},
uint128 = 0x0000000d0000000b013b36f800000000
}

To set values of such registers, you need to tell GDB which view of the register you wish to change, as if you were assigning value to a struct member:

(gdb) set $xmm1.uint128 = 0x000000000000000000000000FFFFFFFF

Normally, register values are relative to the selected stack frame (see Selecting a Frame). This means that you get the value that the register would contain if all stack frames farther in were exited and their saved registers restored. In order to see the true contents of hardware registers, you must select the innermost frame (with ‘frame 0’).

    bt - backtrace: show stack functions and args
    info frame - show stack start/end/args/locals pointers
    x/10gx $sp - show stack memory
