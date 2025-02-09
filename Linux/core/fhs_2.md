# A Detailed Guide to Linux Filesystem Hierarchy Standard (FHS)

The directory(folder) structure in Linux-based operating systems follows the Linux **[Filesystem Hierarchy Standard](https://www.linuxfordevices.com/tutorials/linux/detect-filesystem-of-unmounted-partition)** (**FHS**) defined and maintained by the [Linux](https://www.linuxfordevices.com/tutorials/how-to-install-tradingview-on-linux) Foundation. Having a well-defined standard makes it easier for the users and software developers to know the location of installed binaries, system files, system information, etc. This way Linux applications don’t have to be tailored for a particular distribution and can be used universally.

In this article, we will have a detailed look at the directory structure in Linux and discuss the roles of all of the directories one by one with examples.

## Linux Filesystem Hierarchy Standard

The l[atest rendition of FHS](https://refspecs.linuxfoundation.org/FHS_3.0/fhs-3.0.pdf) was released by the Linux Foundation in 2015. This is the FHS-compliant directory structure.

![File Heirarchy System Graphic1](fhs_2_images/File-heirarchy-system-graphic1-724x1024.png)

### / (root)

This is the beginning of the Linux filesystem hierarchy. All the file paths originate from the root. The directories listed above or symbolic links to those directories are required / otherwise, the file structure isn’t FSH compliant.

### /bin

- Stores essential command binaries which can be used by both system administrator and the user such as cat,ls,mv,ps,mount etc.
- These commands are used to boot up a system (access boot files, mount drives) and can be used while repairing a system when the binaries in /usr aren’t available

![Bin Directory](fhs_2_images/bin_directory.png)

**NOTE**: In the above screenshot, you might see that /bin does not only contain the essential binaries but also non-essential ones like 7z. **For the full explanation check the /usr merge section**

### /boot

- This directory contains all the files necessary for the system to boot up
- This includes the kernel files, initrd, initramfs, bootloader etc.

![Boot Directory 1](fhs_2_images/boot_directory-1.png)

### /dev

- Contains device files for all the physical and virtual devices mounted in the system.
- Device files aren’t files in the traditional sense. They are a way for device drivers to access and interact with the said device
- Usually, the primary storage is called `sda` (/dev/sda)

![Dev Directory](fhs_2_images/dev_directory.png)

### /etc

- This directory contains configuration files of your system.
- The name of your device, your passwords, your network configuration, DNS, crontabs, date and time ..etc are stored here in configuration files.
- This directory cannot contain any binary executable files according to FHS.
- These configuration files affect all users on the system. If you want to make config changes for a specific user, `~/.conf/` should be used instead of `/etc/`

![Etc Directory](fhs_2_images/etc_directory.png)

### /home

- The home contains all the personal user-specific files. It contains separate directories for each user which can be accessed by cd /home/username
- This is where you do most of your work. All the downloads, pictures, music, etc on your system are in /home.
- The user-specific configuration file for each application can be found in /home/[username]/.conf
- You can go to any user’s home directory by executing cd ~[username]. If there is only one user on the system, just `cd ~` works.

### /lib

- Libraries are standard code files that define the commands used in a programming language. During compilation, a compiler looks up these libraries to make sense of the code just as we might look up a dictionary to understand the meaning of words while reading a book.
- This directory contains all the libraries needed to boot up the system and for commands in /bin and /sbin to run.
- This also contains kernel modules which control a lot of your hardware and device functioning
- A lot of times, there are different 32-bit and 64-bit libraries with the same name. To avoid any collusion, these binaries are kept in two separate directories accordingly named /lib32 and /lib64**.**

![Lib Directory](fhs_2_images/lib_directory-1024x459.png)

### /media

- This directory contains several sub-directories where the system mounts removable devices such as USB drives.

### /mnt

- This directory can be used by a user to manually mount a device. (as opposed to /media which is only used by the system)
- The current convention among users is making a separate subdirectory under /mnt and mounting the device in that subdirectory, while the older tradition is mounting the device directly in /mnt.

### /opt

- /opt contains libraries and binaries related to packages which are not installed by your system’s package managers but are installed through third-party means like using Discord’s in-application update button.
- /opt is a less popular alternative to /usr/local . It is the vendor who decided where the libraries and binaries go but usually more monolithic and proprietary software like zoom use /opt .

![Opt Directory](fhs_2_images/opt_directory.png)

### /run

- This directory contains the metadata of the device since the last boot.
- This includes data of all the system processes and daemons that were executed in the current session.
- Files under this directory are cleared (removed or truncated) at the beginning of the boot process.

![Run Directory](fhs_2_images/run_directory.png)

### /sbin

- Just like /bin, /sbin also contains essential system binaries. However, these binaries are only meant to be used by a system administrator rather than a normal user.
- These binaries are mostly used for device management. For example, fdisk, fsck, mkfs, ifconfig, reboot.

![Sbin Directory](fhs_2_images/sbin_directory.png)

**NOTE**: In the above screenshot, you might see that /sbin does not only contain the essential binaries but also non-essential ones. **For the full explanation check the /usr merge section**

### /srv

- You will only ever use this directory if your device is acting as a webserver, as this directory contains all the files regarding web servers.
- For example if host a FTP connection, all the files that need to be shared should by default go in a /srv/ftp.

### /tmp

- Contains temporary files of the currently running processes.
- This data is also flushed after every boot.

![Tmp Directory](fhs_2_images/tmp_directory.png)

### /proc

- Just like /dev which provides devices as files, this folder contains system information and kernel information as files.
- This includes information regarding memory, partitions, hardware (battery, temperature etc), all loaded kernel modules etc.

![Proc Directory](fhs_2_images/proc_directory-1024x287.png)

### /sys (distro specific)

- It contains information similarly held in /proc/, but displays a hierarchical view of specific device information in regards to hot-plug devices.

![Sys Directory](fhs_2_images/sys_directory.png)

### /var

- Contains variable data regarding the running processes.
- This includes the **logs, cache and _spools_** for all applications.
- Spools are the data which are waiting for further processing. For example, A document waiting in the printer queue or an email header waiting to be sent.

![Var Directory](fhs_2_images/var_directory.png)

### /lost+found (ext4 feature)

- While not listed in the FHS, this directory is automatically generated by fsck.
- It stores all the orphaned and corrupted files in this folder.
- This includes the files you couldn’t save because of a power cut, files corrupted due to a failed upgrade process etc.

### /root (optional)

- This is supposed to be the home directory for the root user, as opposed to /home which is the home directory for the non-root [users](https://www.linuxfordevices.com/news/essential-online-security-tools-for-linux-users).

### /usr

The /usr directory has very interesting origins. At the time of formation, it was supposed to act like the /home directory, but when people ran out of space on /bin, they started storing the non-essential binaries in /usr. You can read the whole story [here](https://twitter.com/foone/status/1059310938354987008).

Over time, this directory has been fashioned to store the binaries and libraries for the applications that are installed by the user. So for example, while bash is in /bin (since it can be used by all users) and fdisk is in /sbin (since it should only be used by administrators), user-installed applications like `vlc` are in /usr/bin.

This way `/usr` has its own hierarchy just like the / (root) did.

#### /usr/bin

- This is the primary directory of executable commands on the system.
- Contains all user-installed command binaries and
- If you want to execute your scripts using a single command, you usually place them in /usr/bin/

#### /usr/sbin

- This contains user-installed command binaries that can only be used by system administrators.

#### /usr/lib

- This contains the essential libraries for packages in /usr/bin and /usr/sbin just like /lib.

#### /usr/local

- This is used for all packages which are compiled manually from the source by the system administrator.
- This directory has its own hierarchy with all the bin, sbin and lib folders which contain the binaries and applications of the compiled software.

#### /usr/share

- Contains several architecture-independent miscellaneous files
- Man files, word lists (dictionaries) and definition files are all included in this.

### The case for /usr merge – Is there really a difference between /bin and /usr/bin?

The need for moving non-essential binaries to a different folder historically arose from a lack of space in the /[bin](https://www.linuxfordevices.com/tutorials/linux/error-sub-process-usr-bin-dpkg-returned-error) hard disk. However, that was 1971. Today over 50 years later, we no longer face the same size problems. This has rendered two separate folders for default and user-installed binaries useless. Over time this has also caused a hodge-podge in the filesystems, with both the directory having redundant binaries which makes it confusing.

For this reason**, over the years, many distributions (Debian, Fedora, Ubuntu, Arch etc.) have merged /usr/bin and /bin in the same directory.**

**Similarly /usr/sbin – /sbin and /usr/lib – /lib have been merged into the same directory to simplify the directory structure. Now the /bin folder is just a symlink to the /usr/bin directory and the same for other merges.**

You can read more about the discussion regarding these merges [here](https://www.freedesktop.org/wiki/Software/systemd/TheCaseForTheUsrMerge/) and [here](https://www.linux-magazine.com/Issues/2019/228/Debian-usr-Merge).

![Usr Merge](fhs_2_images/usr_merge.png)

/bin , /sbin and /lib (including its variants) are symlinked to their /usr counterparts

## Conclusion

Since 1993, the Filesystem Hierarchy Standard has been the guideline for Unix-like directory structures. It requires the root directory partition to contain all the files the system needs for booting and mounting additional partitions.

In 2015, FHS was integrated into the Linux Standard Base (LSB) and is now maintained by the Linux Foundation. To read more about the current FHS standard, I highly recommend checking out the [full text](https://refspecs.linuxfoundation.org/FHS_3.0/fhs/index.html) of the last release in 2015. Keep exploring!

### **What is FHS?**

The **Filesystem Hierarchy Standard (FHS)** is a **hierarchy standard** for **Linux** organizing the **file system** structure. It defines the structure and content of directories that contain files, along with their associated permissions and ownership.

### **Why is FHS important for System Administrators?**

**System administrators** follow the **FHS document** as the **authoritative standard** to ensure the **system** functions properly. Adhering to this standard is **essential for the system** to function optimally and maintain consistency across **Linux distributions**.

### **What does FHS cover?**

The **Filesystem Hierarchy Standard** specifies the **parts of the file system** that are within the **root file system**. It provides a detailed **overview of the standard** and a description of each level of the hierarchy.

### **Are all aspects of the file system covered by FHS?**

While the **FHS document** covers many aspects of the **file system**, the **standard leaves many areas undefined**. As a result, there are still **parts of the file system** that are not specified by the standard.

### **What is the significance of FHS-compliant directories?**

**Directories** that are compliant with the **Filesystem Hierarchy Standard** are crucial for the **system to function properly**. They ensure that the **system entries** which represent **devices** and other vital components are correctly structured.

### Who is responsible for maintaining the FHS?

The FHS is maintained by the Linux Foundation and is widely used by many Linux distributions like Red Hat.

### What is the role of each file within the Linux Filesystem Hierarchy?

Each file within the hierarchy serves a specific purpose, such as configuration files, system binaries, logs, and more, to ensure the smooth functioning of the system.

### Why is it important to adhere to the FHS when installing software?

Adhering to the FHS ensures that the software is installed in the correct directories, and it helps system administrators maintain a standardized and organized approach to software installation.

### Why is understanding the FHS important for a system administrator?

Understanding the FHS makes it easier for a system administrator to navigate the filesystem, execute commands accurately, and maintain system integrity.
