# What’s on the stack?
[](https://oskarth.com/unix02/)
_2015-07-10_

This is the third post in my series on Grokking xv6. We will use GDB to understand how the stack works in detail. At the end of the post there’s a video where we trace a system call from user space to kernel space and back.

## Introduction

I want to begin with a word of warning. In this article there’ll be a lot of things that you’ll see that we won’t explain. Instead, we are going to learn how to squint at the code, suppress detail and focus on what we want to do. There are a lot of guides out there that present a fluffy view of reality, but I want to stay as faithful as possible to what you would actually see using GDB and a real code base.

One of the hardest parts so far [going through xv6](http://oskarth.com/unix00/) was not having a good mental model of the _stack_ and how it operates, I will attempt to communicate at least a part of this to you.

## Code

We are going to look at some _assembly code_. I do not expect you to understand everything. Instead we will look at a few things and see what they can teach us about the stack.

When we type `ls` in a terminal, the shell takes care of parsing the input and then passes the control to the `ls` program, `ls.c`, which is written in C. Here’s the _main function_ of that file:

```c
int
main(int argc, char *argv[])
{
  int i;

  if(argc < 2){
    ls(".");
    exit();
  }
  for(i=1; i<argc; i++)
    ls(argv[i]);
  exit();
}
```

This is the main entry point of the `ls` program. `argc` stands for _argument count_, and if main doesn’t get a second argument (`ls` counts as the first argument to main) it will call the function `ls` with the argument `.`. After that it will call the `exit` function.

We can get the assembly code for our main function with the `disassemble` command in _GDB_. GDB is a debugger that allows us to see what is going on inside a program when it executes. We will see a lot of “code boxes” as we move on. Lines starting with `(gdb)` are lines that we write as input, and the other lines are things GDB shows us.

```bash
(gdb) disassemble main
Dump of assembler code for function main:
=> 0x00000304 <+0>:     push   %ebp
0x00000305 <+1>:     mov    %esp,%ebp
0x00000307 <+3>:     and    $0xfffffff0,%esp
0x0000030a <+6>:     sub    $0x20,%esp
0x0000030d <+9>:     cmpl   $0x1,0x8(%ebp)
0x00000311 <+13>:    jg     0x324 <main+32>
0x00000313 <+15>:    movl   $0xb5f,(%esp)
0x0000031a <+22>:    call   0xb0 <ls>
0x0000031f <+27>:    call   0x5cb <exit>
0x00000324 <+32>:    movl   $0x1,0x1c(%esp)
0x0000032c <+40>:    jmp    0x34d <main+73>
0x0000032e <+42>:    mov    0x1c(%esp),%eax
0x00000332 <+46>:    lea    0x0(,%eax,4),%edx
0x00000339 <+53>:    mov    0xc(%ebp),%eax
0x0000033c <+56>:    add    %edx,%eax
0x0000033e <+58>:    mov    (%eax),%eax
0x00000340 <+60>:    mov    %eax,(%esp)
0x00000343 <+63>:    call   0xb0 <ls>
0x00000348 <+68>:    addl   $0x1,0x1c(%esp)
0x0000034d <+73>:    mov    0x1c(%esp),%eax
0x00000351 <+77>:    cmp    0x8(%ebp),%eax
0x00000354 <+80>:    jl     0x32e <main+42>
0x00000356 <+82>:    call   0x5cb <exit>
```

This is a lot of code, and we are not going to understand all of it in this post. Here’s how to read it. The first line is the following:

```bash
=> 0x00000304 <+0>:     push   %ebp
```

`=>` means that this is the instruction we are about to execute, but haven’t yet. `0x00000304` is the _address_ of the _instruction_ written in _base 16_ or _hexadecimal_ or _hex_ - this is where the instruction lives in memory. `<+0>` is an offset that we are going to ignore. `push` is a _mnemonic_ or an _instruction_, and its argument in this case is `%ebp`. We will talk more about instructions and what their arguments mean in later sections.

How does hexadecimal work? The _decimal_ alphabet consists of the numbers 0 through 9, and the _binary_ alphabet consists of 0 and 1. Similarly, the hexadecimal alphabet has 16 “numbers” - 0 through 9 and then A through F. For example, 14 would be written simply as “E”, and 17 as “11”. To differentiate between hexadecimal numbers and decimal we use the _prefix_ “0x”, so 11 is 11 but “0x11” is 17. _Addresses_ in the computer’s memory can be very long, so instead of writing `0x00000304` we can omit the leading zeroes and write `0x304` instead.

Without knowing anything about assembly, you might notice that the `call` instruction occurs several times, and that its arguments is either `<ls>` or `<exit>`. These `call` instructions correspond to the four function calls we see in our main function.

## The Stack

If we follow the execution of a program by pointing at the screen we might say “this calls this, which calls this, then it returns here”. The stack is how the computer keeps track of things like this - where it came from, what the arguments of a function are, etc.

Let’s have a look at what’s on the stack before we have executed a single instruction. We can do this using GDB’s `x` command, which allows us to inspect memory at a given address. It takes two arguments: a format and an address.

```bash
(gdb) x /x $esp
0x2fe8: 0xffffffff
```

In this case `/x` is the format and `$esp` is the address. We see that $esp is set to `0x2fe8` and the content of it is `0xffffffff`. This is what’s on top of the stack. We can see a bit more of what’s on the stack with the following.

```bash
(gdb) x /4x $esp
0x2fe8: 0xffffffff      0x00000001      0x00002ff4      0x00002ffc
```

Here the format `/4x` means “show me 4 _words_ in hex”. In GDB, a word is 4 _bytes_ (and a byte is always 8 bits). Addresses are one word, or 32 bits, which is why it’s called a _32-bit architecture_. _Registers_ are also 32 bits.

Registers store data for the _CPU_ for easy access. `esp` is a special _register_ called _(extended) stack pointer_, and `$esp` is the way you reference it in GDB.

At any given time, the stack pointer points to the top of the stack. In the above output, `$esp` is set to `0x2fe8`, and it points to `0xffffffff`. We can also write the above in a slightly more verbose way, for clarity. Each address on the left is offset by four from the one above it.

```bash
0x2fe8: 0xffffffff <--- ESP
0x2fec: 0x00000001
0x2ff0: 0x00002ff4
0x2ff4: 0x00002ffc
```

In the abstract sense, a stack is a _LIFO_ (last in first out) data structure that supports two primary operations: _push_ and _pop_. It is normally conceptualized as a stack of plates, growing upwards. What might be confusing in this context is that the top of the stack has the lowest address. The stack grows down, in terms of addresses, but the last touched entry is still called the top of the stack. This might be counterintuitive, but “top” is an abstract term and it doesn’t become less of a stack because it’s growing down.

Recall that the four lines above show what’s on the stack before we have even executed a single instruction in our main function. What do they mean? Before a function is called, its arguments are pushed onto the stack, in reverse order, followed by the return address (also known as as the return program counter or return PC). This way of modifying the stack is part of a _calling convention_. There are other calling conventions, but this is the most common one for C.

Our main function takes two arguments, argc and argv, whose values are:

```bash
0x2fe8: 0xffffffff    <- -1, return address for main
0x2fec: 0x00000001    <- 1, argc value 
0x2ff0: 0x00002ff4    <- argv, pointer to argv[0]
0x2ff4: 0x00002ffc    <- "ls", value of argv[0]
```

We can cast `0x00002ffc` to a `char*` (a string) to see its human readable representation. Likewise, we can do the same for main’s return address, `0xffffffff`:

```bash
(gdb) print (char*)0x00002ffc
$83 = 0x2ffc "ls"
(gdb) print (int)0xffffffff
$88 = -1
```

`main` has a fake return address. Since it has no place to return to, it is simply set to -1.

## One instruction at a time

We are now going to step through the beginning of the program, instruction by instruction. We can see the first four instructions to be executed:

```
(gdb) x /4i $eip
=> 0x304 <main>:        push   %ebp
   0x305 <main+1>:      mov    %esp,%ebp
   0x307 <main+3>:      and    $0xfffffff0,%esp
   0x30a <main+6>:      sub    $0x20,%esp
```

We use the `/4i` format to interpret the content of the four addresses, starting at `$eip`, as instructions. There are no guardrails here - GDB doesn’t care if you read memory that represents, say, a number as an instruction.

`$eip` is a register that’s called an _(extended) instruction pointer_. This points to the next instruction we are about to execute. These four instructions are called the _function prologue_. What does the stack look like after we perform these instructions?

Let’s do it one by one using GDB’s `stepi` function. After `push %ebp` this is the stack:

```
0x2fe4: 0x00003fb8  <--- ESP
0x2fe8: 0xffffffff
0x2fec: 0x00000001
0x2ff0: 0x00002ff4
```

Two things have happened: we have moved the stack pointer up an address, and put a new value there. The push instruction does both of those things one after another. This is slightly tricky as there’s no mention of `$esp` in that instruction, but yet it changed our stack pointer. There are only a few instructions like these though: `push`, `pop`, `call`, `ret` and a few others. Another way to write `push $ebp` is as follows:

```
sub $0x4 $esp
mov $ebp ($esp)
```

This subtracts 4 from the stack pointer and puts `$ebp` in whatever the stack pointer is pointing to. `$esp` is the address of the stack pointer, and `($esp)` is what the stack pointer points to (just like with pointers in C):

What is `$ebp`? It stands for _(extended) base pointer_ (or sometimes it’s called a frame pointer, depending on the architecture). The idea is that the stack pointer changes throughout the function as variables and registers are pushed and popped, but the base pointer stays the same throughout. That means that we can use the base pointer as an anchor to find parameters and local variables. For example, if you look at the first assembly code listing, you can see that there are things like `0x8(%ebp)`. This takes the content of `%ebp` but offset by 8, which is two words, and in this case that’s where argc is located.

The next instruction after the `push` instruction is `mov %esp, %ebp` nothing changes on the stack. This moves our stack pointer into the _base pointer_ address.

The third instruction is `and $0xfffffff0,%esp`, and it’s a so called stack alignment (`0xfffffff0` is -16 in hex, using two’s complement). It ensures that the stack pointer will be at its current position in memory, or at a lower one, but more importantly that it will be at a 16-byte boundary. Why this is done is outside of the scope of this article, but it has to do with performance and being able to do several instructions in parallel on certain architectures with something called _SIMD_. We can see that the stack pointer is evenly divided by 16 with `print 0x2fe0 % 16` (or just by looking at the last position in the hex number, since that’s the “16”-th position). This is what the stack looks like now:

```
0x2fe0: 0x00000000  <--- ESP
0x2fe4: 0x00003fb8
0x2fe8: 0xffffffff
0x2fec: 0x00000001
```

After `sub $0x20,%esp`, which subtracts `0x20` (2 times 16 is 32 in decimal) from our stack pointer, we’ve made room for 32 bytes on the stack. This is used for local variables in main.

```
(gdb) x /12x $esp
0x2fc0: 0x00000000      0x00000000      0x00000000      0x00000000
0x2fd0: 0x00000000      0x00000000      0x00000000      0x00000000
0x2fe0: 0x00000000      0x00003fb8      0xffffffff      0x00000001
```

We will show the stack using the more concise format from now on.

We’ve now performed four instructions in main and this is the end of the _function prologue_. Something similar to this is done in every function. There’s also an _function epilogue_ - and of course the main meat of the function in between.

## Calling ls

If we step two more instructions (`stepi 2`) we get to:

```
movl   $0xb5f,(%esp)
```

which puts 0xb5f on the stack without changing the stack pointer (good thing we made room for local variables before so we didn’t overwrite our stack!) What is that? Just like was done to `main` in the very beginning, before we call `ls` (the function, not the program - henceforth we will just talk about the function `ls` inside the `ls` program) we push the argument on the stack. We know there’s only one argument and that it should be a string, and we can see the true nature of it by casting it to a char*:

```
print (char*)0xb5f
$2 = 0xb5f "."
(gdb) x /4x $esp
0x2fc0: 0x00000b5f      0x00000000      0x00000000      0x00000000
```

The next instruction is `call 0xb0 <ls>`. `call` does two things, it pushes the address of the next instruction in `main` onto the stack, and then it _jumps_ to a subprogram (which is just another address in memory, but since our program was compiled with debug information on we can see that it says `<ls>`). A jump changes the instruction pointer to its argument. After executing that instruction our stack and our upcoming four instructions to execute looks like this:

```
(gdb) x /4x $esp
0x2fbc: 0x0000031f      0x00000b5f      0x00000000      0x00000000
(gdb) x /4i $eip
=> 0xb0 <ls>:   push   %ebp
   0xb1 <ls+1>: mov    %esp,%ebp
   0xb3 <ls+3>: push   %edi
   0xb4 <ls+4>: push   %esi
```

We are now in the `ls` function, and `0xb0`, which was an argument to call, is what our instruction pointer is set to. You might recognize the two first lines from the prologue in our main function.

What about `0x0000031f` that is now on top of our stack? It’s the address where the program should keep executing once the ls function returns. We can confirm this by looking at it’s memory location as instructions. These are exactly the instructions that come after the call to ls (see the code section above).

```
(gdb) x /4i 0x0000031f
   0x31f <main+27>:     call   0x5cb <exit>
   0x324 <main+32>:     movl   $0x1,0x1c(%esp)
   0x32c <main+40>:     jmp    0x34d <main+73>
   0x32e <main+42>:     mov    0x1c(%esp),%eax
```

We are still in ls though. Let’s step two more instructions, pushing the base pointer onto the stack and moving (or “saving”) the stack pointer to the base pointer.

```
(gdb) x /4x $esp
0x2fb8: 0x00002fe4      0x0000031f      0x00000b5f      0x00000000
```

The new address on the stack is our old base pointer from main. We’ve seen this before, but let’s take a look again.

```
(gdb) x /4x 0x00002fe4
0x2fe4: 0x00003fb8      0xffffffff      0x00000001      0x00002ff4
```

This is exactly our stack at the beginning of main, so we now have easy access to that state for when we want to go back to it.

## Skipping until the end of ls

There’s a lot that happens in `ls` and the functions it calls. We are going to skip all that by going to the very last line of the C code in the ls function ([code](https://github.com/oskarth/xv6/blob/master/ls.c)), line 71. We do this with the GDB command `until 71`. When we are at the end of `ls`, what’s about to happen now and what does the stack look like?

```
(gdb) x /6i $eip
=> 0x2f9 <ls+585>:      add    $0x25c,%esp
   0x2ff <ls+591>:      pop    %ebx
   0x300 <ls+592>:      pop    %esi
   0x301 <ls+593>:      pop    %edi
   0x302 <ls+594>:      pop    %ebp
   0x303 <ls+595>:      ret
(gdb) x /4x $esp
0x2d50: 0x00000003      0x00002d88      0x00000010      0x00000001
```

We don’t know what those things on the stack are, but presumably they come from something ls did - in fact, we would have to run `x /170x $esp` to begin to see addresses that we recognize on our stack. That’s okay though, we are about the clean that stack up with the function epilogue. Essentially the five first instructions are the opposite of subtracting and pushing things onto the stack. If we step through them with `stepi 5` we get:

```
(gdb) x /4x $esp
0x2fbc: 0x0000031f      0x00000b5f      0x00000000      0x00000000
```

Before we did that our stack pointer was set to `0x2d50`, and now it’s back to `0x2fbc`. As a sanity check on what’s going on, we can see that everything seems OK: we just cleaned up 620 bytes, of which the first `add $0x25c, %esp` took care of 604. `pop` was called four times, and 4 times 4 bytes (the size of each register that we popped) is 16, which takes care of the rest.

```
print  0x2fbc - 0x2d50
$3 = 620
print 0x25c
$4 = 604
```

Our stack pointer is now back at `0x2fbc`, which is where it was at the very beginning of the `ls` function. The next instruction is a simple `ret`. What does `ret` do? It’s the opposite of `call`: it pops off an address, and jumps to it. So without single stepping, we should expect it to jump to `0x31f` and set the stack pointer to `0x2fbc + 4` = `0x2fc0`. What is `0x31f` again? It’s the next line in `main` after calling `ls`. After single stepping it:

```
x /4x $esp
0x2fc0: 0x00000b5f      0x00000000      0x00000000      0x00000000
x /4i $eip
=> 0x31f <main+27>:     call   0x5cb <exit>
   0x324 <main+32>:     movl   $0x1,0x1c(%esp)
   0x32c <main+40>:     jmp    0x34d <main+73>
   0x32e <main+42>:     mov    0x1c(%esp),%eax
```

Indeed, we are now back in `main` and are about to call `exit`, and our stack is back to the same state it was just before it was about to call `ls`.

## Stack traces

When you program in a high-level language you might come across _stack traces_ that show who called a function and with which arguments. GDB also has support for this, and if we were executing in the middle of the `ls` function we could see the following:

```
(gdb) info stack
#0  ls (path=path@entry=0xb5f ".") at ls.c:33
#1  0x0000031f in main (argc=1, argv=0x2ff4) at ls.c:79
```

Here we have two _stack frames_. A stack frame is created at every function invocation and contains arguments to the function, its return address, and space for local variables.

In this case we are in stack frame #0 (the inner frame), executing instructions in `ls`, and we came from main. Notice that the base pointer we talked about earlier, `0x31f`, is there as the start of the other stack frame (the outer frame).

You can see a stack trace just shows you all the stack frames, which we have meticulously (our rather, our compile has) constructed at the lower level. There’s no magic.

## Conclusion and demo

We started off looking at a simple piece of C code and its equivalent assembly code. We then inspected the stack before a single instruction had been executed, and we then carefully went through the first few instructions in that function to see how the stack frame was set up. Then we saw how another function, ls, was called and how that changed the stack, preserving the stack state of the calling function. We then skipped a whole bunch of code only to catch our stack being cleaned up, and finally getting returned to the main function again with its stack frame intact.

Here’s the video that was promised. In it we trace a system call from user space to kernel space and back.