## breakpoints
(gdb) break tree.c:insert
(gdb) break tree.c:10
(gdb) break main
(gdb) break func if a == 10
(gdb) b -source /path/file.c -line xxx  9.2.2 Explicit Locations
(gdb) tbreak args  -Set a breakpoint enabled only for one stop.

## Listing currently defined breakpoints
(gdb) info breakpoints

## Saving dprintf commands for a later session
(gdb) save breakpoints my-dprintf-breakpoints

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
    Restore the program state that was saved as checkpoint number checkpoint-id. All program variables, registers, stack frames etc. will be returned to the values that they had when the checkpoint was saved. In essence, gdb will “wind back the clock” to the point in time when the checkpoint was saved.

    Note that breakpoints, GDB variables, command history etc. are not affected by restoring a checkpoint. In general, a checkpoint only restores things that reside in the program being debugged, not in the debugger.
(gdb) delete checkpoint checkpoint-id
    Delete the previously-saved checkpoint identified by checkpoint-id.


## 5.1.2 Setting Watchpoints
(gdb) info watchpoints This command prints a list of watchpoints, using the same format as info break
(gdb) watch [-l|-location] expr [thread thread-id] [mask maskvalue] [task task-id]
    (gdb) watch foo

## Redirecting program output to a file
(gdb) run >my-program-output

(gdb) show paths  Display the list of search paths for executables (the PATH environment variable).

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

    “Quiet”. Do not print the introductory and copyright messages. These messages are also suppressed in batch mode.
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



gdb  -x '/home/stepan/GIT/kn7072/C/code/CPrimerPlus6E/Ch03/my_break' -ex 'run' main

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


