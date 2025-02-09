Linux looks for shared libraries in several standard locations, and the process is called dynamic linking. Here are the standard locations where Linux looks for shared libraries:

1. /lib: This directory contains the shared libraries that are essential for running the system and the binaries in /bin and /sbin.

2. /usr/lib: This directory contains the shared libraries that are used by user programs.

3. /usr/local/lib: This directory contains the shared libraries that are installed locally by the user or administrator.

4. LD_LIBRARY_PATH environment variable: This variable specifies additional directories that the linker should search for shared libraries.

5. /etc/ld.so.conf file: This file specifies additional directories that the linker should search for shared libraries.

6. /etc/ld.so.cache file: This file contains a cached list of all the shared libraries found in the standard locations.

When a program is executed, the linker searches for the required shared libraries in the standard locations in the order listed above. If a library is not found, the linker looks in the directories specified in the LD_LIBRARY_PATH environment variable, and then looks in the directories specified in the /etc/ld.so.conf file. If the library is still not found, the program will fail to run with an error message indicating that a required shared library is missing.

## How do I see loaded shared libraries in Linux?

You can see the list of loaded shared libraries in Linux using the following steps:

1. Open a terminal window.  
2. Type in the command "**lsof**" and hit enter. This will display a list of open files, including the shared libraries.  
3. To display only the shared libraries, type in the following command: "**lsof | grep DEL**". This will display a list of all the shared libraries loaded by the processes currently running on your system.  
4. Another method to see the shared libraries is to use the "**ldd**" command, which lists the shared libraries required by a particular binary. For example, if you want to see the shared libraries required by the "**ls**" command, type in the following command: "**ldd /bin/ls**".

By using these commands, you can get a better understanding of the dependencies and library files required by different processes running on your Linux system.

## Where do I find shared library?

Shared libraries are a commonly used component in software development. They are collections of code, data, and resources that can be shared across multiple programs. Here are the steps to find shared libraries:

1. Determine the operating system and platform you are using, as different systems have different methods of managing shared libraries.

2. Check the relevant documentation for the programming language and development tools you are using, as they may provide guidelines on how to locate and use shared libraries.

3. Search for shared libraries in the appropriate directories on your system. On Unix-based systems, for example, shared libraries are typically stored in the /usr/lib or /usr/local/lib directories.

4. Use package management systems or repositories to obtain shared libraries. Many programming languages and platforms have package managers that allow you to easily download and install shared libraries that are commonly used.

5. Consider building and packaging your own shared libraries if they are not available through other means. This can be a more complex process, but it allows for greater flexibility and customization.

By using these steps, you can find and use shared libraries in your software development projects.


## Where does GCC look for shared libraries?

GCC (GNU Compiler Collection) looks for shared libraries in standard locations and user-defined locations. Here are the steps GCC follows to find shared libraries:

1. GCC first looks for shared libraries in the standard system directories, such as /lib, /usr/lib, /usr/local/lib, depending on the operating system and its configuration.

2. If the required library is not found in the standard directories, GCC checks the directories specified in the LD_LIBRARY_PATH environment variable. This variable contains a colon-separated list of directories to search for shared libraries.

3. If the library is still not found, GCC looks in the directories specified in the /etc/ld.so.conf file and its included files. These files define additional directories to search for shared libraries.

4. Finally, GCC may check user-defined directories that are specified using the -rpath or -rpath-link options during the link stage of compilation.

Overall, GCC follows a hierarchical search order for shared libraries, starting with standard system directories and moving to user-defined locations as necessary to find the required libraries.

## How does Linux search for libraries?

Linux searches for libraries using a specific order or path set by the environment variable LD_LIBRARY_PATH. The search path is as follows:

1. The runtime linker looks for libraries in the directories listed in LD_LIBRARY_PATH.  
2. If the library is not found in the directories listed in LD_LIBRARY_PATH, the linker looks for the library in the standard system directories.  
3. The linker also checks for dependencies specified in the library itself and loads them accordingly.

It is important to note that the order of the LD_LIBRARY_PATH directories can affect which libraries are used, as libraries found in the earlier directories take precedence over those found in later directories. This can be useful for testing new libraries without affecting the system-wide libraries.

In addition, the ldconfig command can be used to update the system’s cache of shared libraries and their paths, allowing the linker to find libraries more efficiently. This usually updates the cache located in /etc/ld.so.cache.


## Where does Ubuntu look for shared libraries?

Ubuntu, like other Linux-based operating systems, looks for shared libraries in specific locations in the file system. In general, shared libraries are located in the /lib, /usr/lib, and /usr/local/lib directories.

However, depending on the specific version of Ubuntu and the software being used, there may be additional directories searched for shared libraries. These directories are defined in the ld.so.conf file. This file is located in the /etc directory and contains a list of directories that the operating system will search for shared libraries.

If a required shared library is not found, Ubuntu will issue an error message indicating that the library cannot be found. To resolve the issue, the appropriate library must be installed or its location must be added to the ld.so.conf file. This can be done using the apt package manager or by manually installing the library and updating the ld.so.conf file.

In summary, Ubuntu looks for shared libraries in specific directories such as /lib, /usr/lib, and /usr/local/lib. Additional directories can be added to the ld.so.conf file. If a required library is not found, it must be installed or its location must be added to the ld.so.conf file.

vi /etc/ld.so.conf 

The line(s) in this file instruct the kernel to load file in **/etc/ld.so.conf.d**. This way, package maintainers or programmers can add their custom library directories to the search list.

If you look into the **/etc/ld.so.conf.d** directory, you’ll see **.conf** files for some common packages (kernel, mysql, and postgresql in this case):

**# ls /etc/ld.so.conf.d**

kernel-2.6.32-358.18.1.el6.x86_64.conf  
kernel-2.6.32-696.1.1.el6.x86_64.conf  
mariadb-x86_64.conf
kernel-2.6.32-642.6.2.el6.x86_64.conf  
kernel-2.6.32-696.6.3.el6.x86_64.conf  
postgresql-pgdg-libs.conf

If you take a look at the mariadb-x86_64.conf, you will see an absolute path to package libraries.

**# cat mariadb-x86_64.conf**

/usr/lib64/mysql

The method above sets the library path permanently. To set it temporarily, use the **LD_LIBRARY_PATH** environment variable on the command line. If you want to keep the changes permanent, then add this line in the shell initialization file **/etc/profile** (global) or **~/.profile** (user-specific).

export LD_LIBRARY_PATH=/path/to/library/file

## How to check shared library version in Linux?

In Linux, shared libraries are an essential component of software packages. They serve as common resources that applications use to avoid redundancy and improve efficiency. Knowing how to verify the shared library version is necessary for maintaining and troubleshooting the system.

Here are the steps for checking the shared library version in Linux:

1. Identify the library name: Before checking the shared library version in Linux, you need first to know the library name. You can list all the available libraries in the system by using this command: ‘ls /usr/lib’, ‘ls /usr/local/lib’ or ‘ls /lib’.

2. Use the ldd command: The ldd command on Linux system is used to identify the shared libraries required by a program or library. To check the shared library version information, use the following syntax in the terminal:  
‘ldd LIBRARY-NAME | grep VERSION’

Replace the "**LIBRARY-NAME**" with the actual name of the shared library, and "**VERSION**" with the version number of the shared library that you want to check.

3. Check package version number: If you are interested to know the library version number of an already installed package, you can use the package manager to get the details. For instance, on Ubuntu, you can use the following command: ‘dpkg -l | grep LIBRARY-NAME’

Replace the "**LIBRARY-NAME**" with the actual name of the shared library that you want to check, and it will provide the version number for the package.

By following these steps, you can easily check the shared library version in Linux.


#### Managing Shared Libraries in Linux

Let us now look at how to deal with shared libraries. To get a list of all shared library dependencies for a binary file, you can use the **ldd utility**. The output of **ldd** is in the form:
```bash
ibrary name =>  filename (some hexadecimal value)
OR
filename (some hexadecimal value)  #this is shown when library name can’t be read

```

This command shows all shared library dependencies for the [ls command](https://www.tecmint.com/tag/linux-ls-command/).
```bash
ldd /usr/bin/ls
OR
ldd /bin/ls
 ```
##### Sample Output
```bash
linux-vdso.so.1 =>  (0x00007ffebf9c2000)
	libselinux.so.1 => /lib64/libselinux.so.1 (0x0000003b71e00000)
	librt.so.1 => /lib64/librt.so.1 (0x0000003b71600000)
	libcap.so.2 => /lib64/libcap.so.2 (0x0000003b76a00000)
	libacl.so.1 => /lib64/libacl.so.1 (0x0000003b75e00000)
	libc.so.6 => /lib64/libc.so.6 (0x0000003b70600000)
	libdl.so.2 => /lib64/libdl.so.2 (0x0000003b70a00000)
	/lib64/ld-linux-x86-64.so.2 (0x0000561abfc09000)
	libpthread.so.0 => /lib64/libpthread.so.0 (0x0000003b70e00000)
	libattr.so.1 => /lib64/libattr.so.1 (0x0000003b75600000)
	```
	
Because shared libraries can exist in many different directories, searching through all of these directories when a program is launched would be greatly inefficient: which is one of the likely disadvantages of dynamic libraries. Therefore a mechanism of caching is employed, performed by the program **ldconfig**.

By default, **ldconfig** reads the content of **/etc/ld.so.conf**, creates the appropriate symbolic links in the dynamic link directories, and then writes a cache to **/etc/ld.so.cache** which is then easily used by other programs.

This is very important especially when you have just installed new shared libraries or created your own, or created new library directories. You need to run the **ldconfig** command to effect the changes.

```bash
# ldconfig
OR
# ldconfig -v 	#shows files and directories it works with
```
After creating your shared library, you need to install it. You can either move it into any of the standard directories mentioned above and run the **ldconfig** command.

Alternatively, run the following command to create symbolic links from the **soname** to the filename:
```bash
# ldconfig -n /path/to/your/shared/libraries

```
To get started with creating your own libraries, check out this guide from [The Linux Documentation Project(TLDP)](http://tldp.org/HOWTO/Program-Library-HOWTO/shared-libraries.html).