[source](https://benjamintoll.com/2022/08/08/on-unsharing-namespaces-part-one/)

- [ On Unsharing Namespaces, Part One](#link_0)
  - [ Namespaces](#link_1)
    - [ Unix Timesharing System](#link_2)
    - [ Process IDs](#link_3)
    - [ Mount points](#link_4)
  - [ Summary](#link_5)
  - [ References](#link_6)
- [ On Unsharing Namespaces, Part Two](#link_62)
  - [ Namespaces](#link_7)
    - [ Network](#link_8)
      - [ Sharing](#link_9)
      - [ Unsharing](#link_10)
      - [ Connectivity](#link_11)
    - [ User](#link_12)
      - [ Rootless Containers](#link_13)
      - [ Capabilities](#link_14)
      - [ /etc/sub{u,g}id](#link_15)
      - [ nsswitch.conf](#link_16)
  - [ Summary](#link_17)
  - [ References](#link_18)

# On Unsharing Namespaces, Part One <a name="link_0"></a>

---

This is the first part in a two part series that will be looking at [Linux namespaces](https://en.wikipedia.org/wiki/Linux_namespaces) and the [`unshare`](https://www.man7.org/linux/man-pages/man1/unshare.1.html) command which is used to create them. Using this new knowledge, we’ll create a container by hand, piece by piece.

The `unshare` tool is used to run a program in a process with some namespaces unshared from its parent, meaning that it doesn’t share the namespaces with the parent, instead having its own. The namespaces to be unshared are listed as options to the `unshare` command.

So, what’s the big deal about this? Why learn about it? Can’t I just use Docker?

Well, you could, if you want to be just like everyone else. But you don’t, do you? You want to be unique, your own person.

We’ll be learning how to create a container from scratch using some foundational knowledge that we probably already have. It’s just a matter of putting all of the pieces together. And, no matter your container technology of choice (Docker, Podman, `systemd-nspawn`, et al.), doing this exercise will improve and enhance your understanding of how these higher-level abstractions create Linux containers under the hood. That’s always a good thing.

Back to the task at hand. Again, we’re going to be primarily looking at the `unshare` command and creating new, unshared namespaces.

As for the name, the child process inherits all of its parent namespaces, but sometimes the child shouldn’t **share** those inherited namespaces, instead opting to create new namespaces that are not **shared** (or, if you will, _unshared_) with the parent.

So, let’s get on with it.

> There are more namespaces than just the ones we’re looking at in this series.

---

Before we start, here is the syntax of the command:

```bash
unshare [options] [program [arguments]]
```

---

## Namespaces <a name="link_1"></a>

You can get a sense of all of the defined [namespaces](https://www.man7.org/linux/man-pages/man7/namespaces.7.html) for all users on your system by listing them:

```bash
$ sudo lsns
```

Running the command as an unprivileged user will only get your own namespaces:

```bash
$ lsns
```

> Always run [`lsns`](https://www.man7.org/linux/man-pages/man8/lsns.8.html) as a privileged user, because it reads its information from the [`/proc`](https://man7.org/linux/man-pages/man5/proc.5.html) pseudo-filesystem!

On mine, there are a whole bunch, mostly Firefox web browser tabs that I have open. After all, modern browsers use namespacing and cgroups to create a sandboxed environment!

### Unix Timesharing System <a name="link_2"></a>

The `uts` [Unix Timesharing System namespace](https://www.man7.org/linux/man-pages/man7/uts_namespaces.7.html) is basically the hostname namespace, which allows us to set a hostname in the `uts` namespace which can be different from that of the host.

As a simple example, observe the following:

```bash
# On host, the following command puts us in a new Bourne shell.
$ sudo unshare --uts sh

# So, now we're inside the "container" process.
$ hostname
kilgore-trout
$ hostname doody
$ hostname
doody
$ exit

# Now, back on host.
$ hostname
kilgore-trout
```

First, we launched a Bourne shell with its own `uts` namespace. We then list out the hostname inherited from the parent, and then change it to “doody”, because I’m a child. Then, we verify that it took and exited the shell (and the namespace). Lastly, we verify that the hostname on the host has not been changed.

Ok, pretty simple stuff. Let’s move on to a more interesting example.

> Note that not giving a command to `unshare` will result in it opening a shell by default (determined by the value of the `SHELL` environment variable).

### Process IDs <a name="link_3"></a>

The [`pid` namespace](https://www.man7.org/linux/man-pages/man7/pid_namespaces.7.html) is interesting because we first have to know something about [`chroot`](https://man7.org/linux/man-pages/man2/chroot.2.html)s and the [`/proc`](https://man7.org/linux/man-pages/man5/proc.5.html) filesystem. Let’s talk about `/proc` first.

`/proc` is a pseudo-filesystem that is created by the kernel and is an interface to kernel data structures. Essentially, this means that user space can get information from the kernel and set properties that are read from the kernel by reading from and writing to these files.

We’re interested in the `/proc` filesystem because of its detailed information about all of the running processes. When, for example, the [`ps`](https://www.man7.org/linux/man-pages/man1/ps.1.html) command is executed, it reads its information from `/proc`. So, when creating an unshared `pid` namespace, it’s not enough to simply specify the option as part of the `unshare` command (i.e., `unshare --pid`); we also need to tell the kernel to create a new `/proc` filesystem, in which it will write **only** process information for the new namespace.

> This is crucially important because we don’t want a child namespace to have a view of its parents `pid` namespace and all of its running processes. Allowing this would be giving away a lot of unintended information that could perhaps be used for nefarious purposes.

But, wait, there is _already_ a `/proc` filesystem! Won’t a new `/proc` filesystem interfere or conflict with this older one? Indeed it would, observant grasshopper.

What we need is to create another, different view of the filesystem for the new process. Perhaps we could install another [`rootfs`](https://en.wikipedia.org/wiki/Filesystem_Hierarchy_Standard) within this filesystem, and then **change the root** of the filesystem to this new `rootfs`.

This will change the root of what the process can see, essentially restricting its access and what it can do (for example, the new root filesystem may only have a small fraction of the binaries that are available in the main root filesystem). There are many upsides to this (for example, greater security), as evidenced by the fact that `chroot`s have been used in the Unix world for decades.

Let’s download a `rootfs` from Alpine. Let’s get the latest as of this writing, [version 3.9](http://dl-cdn.alpinelinux.org/alpine/v3.9/releases/x86_64/alpine-minirootfs-3.9.0-x86_64.tar.gz):

```bash
$ sudo su -
# mkdir rootfs
# curl http://dl-cdn.alpinelinux.org/alpine/v3.9/releases/x86_64/alpine-minirootfs-3.9.0-x86_64.tar.gz | tar -xz -C rootfs/
```

> We’re running as a privileged user for all commands simply out of convenience.

And `unshare` the `pid` namespace and change the root in the same fell command:

```bash
# unshare --pid --fork chroot rootfs sh
/ # ls
bin    dev    etc    home   lib    media  mnt    opt    proc   root   run    sbin   srv    sys    tmp    usr    var
```

> Note my prompt. Yours may be different.

This is doing the following:

- unsharing the `pid` namespace
- creating a `chroot` rooted in the `rootfs/` filesystem that was just downloaded and installed
- putting us into the new `chroot`
- starting a new Bourne shell in the `chroot`

> Why `--fork`? From the `unshare` man page:
>
> > Fork the specified program as a child process of `unshare` rather than running it directly. This is useful when creating a new PID namespace.
>
> Every time you unshare the `pid` namespace, you should use the `--fork` option.

Let’s [`sleep`](https://www.man7.org/linux/man-pages/man1/sleep.1.html) in the container process and then inspect the process ID from the host.

In the container process:

```bash
/ # sleep 1000
```

In another terminal on the host:

```bash
$ ps -C sleep
    PID TTY          TIME CMD
2290330 pts/1    00:00:00 sleep
```

Now, using its `pid`, let’s see what the kernel tells us about its `root`, that is, its view of the filesystem:

```bash
$ sudo ls -l /proc/2290330/root
lrwxrwxrwx 1 root root 0 Aug  8 01:52 /proc/2290330/root -> /root/rootfs
```

From the host, we can see that the `sleep` process indeed has a different view of the filesystem (that is, the kernel is informing us that the `root` of process ID 2290330 is `/root/rootfs`). Its `root` is the new `rootfs` in the `rootfs` directory, and the process only sees this subsystem of the entire host filesystem. In other words, its world is very limited, and this is a good thing.

For fun, let’s see what a host process reports as its `root`:

```bash
$ sudo ls -l /proc/$$/root
lrwxrwxrwx 1 btoll btoll 0 Apr 21 13:40 /proc/574264/root -> /
```

This is another way we can fortify our learning by actively demonstrating that a host process **not** running in a `chroot` has a very different view of the filesystem than a “container” process running in a `chroot`.

If you’re unfamiliar with `bash` internal variable [`$$`](https://codefather.tech/blog/bash-dollar-dollar-variable/), it is the `pid` of the current shell.

> Note that the process only has a high number from the perspective of the host. In the chroot (the “container”), it would have a different and lower number.

However, `ps` still isn’t working in the container process. You may receive an error or it may just return the column headers with no running processes listed:

```bash
/ # ps
Error, do this: mount -t proc proc /proc
```

Or:

```bash
/ # ps
PID   USER     TIME  COMMAND
```

Why isn’t it reporting on any running processes? We know that it should have at least one in the container process, PID 1, which will be `/bin/sh` in this case, since we launched the process with the `sh` shell command.

Listing out the `/proc` directory tells us why. It’s empty, of course.

```bash
/ # ls /proc
/ #
```

Either way, we need to mount the `/proc` pseudo-filesystem before we’re able to see anything. Just as with the main `/proc` filesystem in the `/` root, it will contain information written to it by the kernel about the running processes, but, importantly, **only** those running in this `chroot`:

```bash
/ # mount -t proc proc /proc
```

Now, `ps` should be able to list the running processes:

```bash
/ # ps
    PID TTY          TIME CMD
      1 ?        00:00:00 sh
     46 ?        00:00:00 ps
```

Sweet, that worked! And, as expected, the `sh` process is `pid` 1. With one simple command and an easily downloaded `rootfs`, we’ve gone a fair way toward making a running container!

> Note that we’ll get a similar error when executing the `mount` command in the container process before the `/proc` filesystem is mounted:
>
> ```
> / # mount
> mount: failed to read mtab: No such file or directory
> / # mount -t proc proc /proc
> / # mount
> /dev/sda2 on /target type ext4 (rw,relatime,errors=remount-ro)
> proc on /proc type proc (rw,relatime)
> ```
>
> More on this in the next section.
>
> ---
>
> **Note** that I’ve also received the following, so your mileage may vary:
>
> ```bash
> / # mount
> mount: no /proc/mounts
> ```
>
> Either ways, the result is the same: the `chroot` isn’t reporting any `mount` points.

Weeeeeeeeeeeeeeeeeeeeeeee

### Mount points <a name="link_4"></a>

[`mnt` namespaces](https://www.man7.org/linux/man-pages/man7/mount_namespaces.7.html) allow a process to see only its own mount points and not that of any other `mnt` namespace, like its parent’s.

Creating a `mnt` namespace is important so the parent `mnt` namespace isn’t shared with child processes and subsequently the host mount table isn’t littered with entries that had been mounted in child container processes and not unmounted, leaving a relic that hangs around like your next-door neighbor.

Since the `mnt` namespace is otherwise inherited and shared, any `mount` created in the “container” will be seen from the host and will appear in its mount table.

Imagine having a host that continually spawns hundreds, if not thousands, of containers whose needs include bind mounting directories from the host and/or mounting (pseudo-)filesystems in the container, like `/proc`. Of course, if the container process remembers to clean up after itself by umounting any mount points before exiting (or in a [`trap`](https://linuxhandbook.com/bash-trap-command/)), then the mount entries are removed, but who remembers to do that? Well, I do, of course, but other people that aren’t me? No way.

Also, and more importantly, sharing the same `mnt` namespace with the host is a huge security risk. Remember, once the host is compromised by a process breaking out of a container, which is bad enough, then the attacker has access to every container running on the kernel. Depending on the shared hosting and its infrastructure, this could be really bad (although I assume, and hope, that cloud providers run the containers in virtual machines, but that only partly mitigates it. For example, if there are multiple containers running in the same VM, that would be the same problem). So, not only do you have to worry about your own security, you have to worry about your neighbor’s.

First, let’s take a look at mounting from within the container process that inherits (shares) its `mnt` namespace with its parent:

```bash
$ sudo unshare bash
# mkdir source
# touch source/HELLO
# mkdir target
# mount --bind source target
# ls target
HELLO
# exit
exit
```

Back on the host, we can still see the mount point listed by the `mount` command:

```bash
$ mount | ag target
/dev/sda2 on /home/btoll/target type ext4 (rw,relatime,errors=remount-ro)
```

This is unfortunate but easily fixed.

You’ll notice that in the example below that we don’t need to recreate the `source` and `target` directories. This is because the `bash` process has the same root filesystem (`/`) as that of the host, and so the directories created in the “container” were created on the host’s root filesystem (which, of course, persist when exiting the subprocess (the “container”)).

This would be a different story if the the new process had `chroot`ed to a subdirectory on the host filesystem. In that scenario, the `rootfs` used as the subprocess' filesystem in the `chroot` would be entirely separate from the host, and any files and directories created in the `chroot` will not be on the host.

Back to our story, to remove the `mount` point entry from the host’s list of `mount` points, simply run the same command as before and unmount the bind mount:

```bash
$ sudo unshare bash
$ umount target
```

And, on the host, it’s gonzo:

```bash
$ mount | ag target
$
```

> Of course, you can always remote the `mount` point from the host:
>
> ```bash
> $ sudo umount /path/to/target
> ```

Now, let’s do this properly. Create an unshared process with its own `mnt` namespace:

```bash
$ sudo unshare --mount bash
# mount --bind source target
# ls target
HELLO
# exit
exit
```

And, on the host:

```bash
$ mount | ag target
$
```

Even though the container process didn’t tidy up by unmounting the mount point before exiting, it still didn’t create the mount point in the parent namespace because it had its own `mnt` namespace, established by the `--mount` option.

Weeeeeeeeeeeeeeeeeeeeeee

---

Before moving on to the last section of this very generous article, let’s take a look at some information made available to us by the kernel in `/proc` that is interesting and instructive.

Each process in `/proc` has a `mounts` file that informs us what mounts, if any, were created by any process. For example, to see the mount points for PID 1 (on my system that is `systemd`), you can do:

```bash
$ sudo cat /proc/1/mounts
```

You’ll see a list that is strikingly similar, or perhaps the same, as that of the `mount` command.

Now, let’s take a look at an example where a process is created with its own unshared `mnt` namespace. We’ll issue the same commands as before:

```bash
$ sudo unshare --mount bash
# mkdir source
# touch source/HELLO
# mkdir target
# mount --bind source target
# ls target
HELLO
```

So far, so good. We need to look at the process information on the host in `/proc`, so let’s get the PID number from the container environment:

```bash
# echo $$
2521485
```

> As aforementioned, the [Bash and Bourne special parameter](https://www.gnu.org/software/bash/manual/html_node/Special-Parameters.html) `$$` expands to the process ID of the shell (in a subshell, it’s always the PID of the invoking shell).

As expected, it’s a high number because the process has inherited the `pid` namespace of its parent. We can use `ps` to confirm that:

```bash
# ps
    PID TTY          TIME CMD
2521380 pts/1    00:00:00 sudo
2521485 pts/1    00:00:00 bash
2521847 pts/1    00:00:00 ps
```

Armed with the PID of the [Bourne-Again SHell](<https://en.wikipedia.org/wiki/Bash_(Unix_shell)>) process, we can now see its mount points.

> Since the container process has unshared its `mnt` namespace from its parent, the mount point entry won’t show by running `mount` on the host, so the following method is the only way to see from the host what is in a container process' `mnt` namespace.

First, just as a sanity check, we’ll make sure that that process can be seen from the host:

```bash
$ ps -C bash
    PID TTY          TIME CMD
   1891 tty1     00:00:00 bash
   2200 pts/0    00:00:00 bash
 965293 pts/1    00:00:22 bash
2353178 pts/0    00:00:00 bash
2521485 pts/1    00:00:00 bash
```

Yes, there it is, listed last. Of course it would be, but I am, well, paranoid. Now, let’s look at the method with which we can see what is in a process’s unshared `mnt` namespace. The expectation is that we’ll only see what has been mounted (`source`, in this case).

```bash
$ sudo cat /proc/2521485/mounts
sysfs on /sys type sysfs (rw,nosuid,nodev,noexec,relatime)
proc on /proc type proc (rw,nosuid,nodev,noexec,relatime)
udev on /dev type devtmpfs (rw,nosuid,noexec,relatime,size=8039820k,nr_inodes=2009955,mode=755)
devpts on /dev/pts type devpts (rw,nosuid,noexec,relatime,gid=5,mode=620,ptmxmode=000)
tmpfs on /run type tmpfs (rw,nosuid,nodev,noexec,relatime,size=1613876k,mode=755)
/dev/sda2 on / type ext4 (rw,relatime,errors=remount-ro)
securityfs on /sys/kernel/security type securityfs (rw,nosuid,nodev,noexec,relatime)
...
/dev/sda2 /home/btoll/target ext4 rw,relatime,errors=remount-ro 0 0
```

Wait, what?!? In addition to the mount point created by the process that we expected to see (the last one listed), we also see all of the other of the host’s mount points. What is going on here?

Well, it’s because the mount information for each process is contained in `/proc` within each PID’s directory entry, as we’ve seen above. And, because we haven’t unshared the `pid` namespace **and** (most importantly) created the process in its own `chroot`, its view of the world will still be that of its parent, and it will get all of its mount information from `/proc` on the host.

> Of course, running the `mount` command in the “container” will also list all of the host’s mounts for the same reason.

So let’s create **its** own `pid` namespace and `chroot` to get only the information we expect.

```bash
$ sudo unshare --pid --fork --mount chroot rootfs bash
# echo $$
1
# ps
Error, do this: mount -t proc proc /proc
# mount -t proc proc /proc
# ls -l /proc/$$/exe
lrwxrwxrwx 1 root root 0 Aug  8 23:30 /proc/1/exe -> /bin/busybox
# mkdir -p source
# touch source/CIAO
# mkdir -p target
# mount --bind source target
# ls target/
CIAO HELLO
# sleep 1000
```

> Remember, since we didn’t create a `chroot`, the `source` and `target` directories and any contents will still be present on the host machine, and thus listing the entries of one of them will also produce our old friend `HELLO`.

And on the host:

```bash
$ ps -C sleep
    PID TTY          TIME CMD
    2528091 pts/1    00:00:00 sleep
$ cat /proc/2528091/mounts
proc /proc proc rw,relatime 0 0
/dev/sda2 /target ext4 rw,relatime,errors=remount-ro 0 0
```

And there we have it, it’s only listing the two mount points that we just created in the container, and nothing from its parent `mnt` namespace.

So, we don’t need to `cat` out the mount points for the parent `bash` process (PID 1) and instead can look at any process in the process tree that hasn’t unshared its `mnt` namespace (because all other processes will have the same shared view of the mount points).

Here is the proof they’re sharing the same namespace (the first is `bash` and the second is `sleep`):

```bash
$ sudo ls -l /proc/2528059/ns/ | ag mnt
lrwxrwxrwx 1 root root 0 Aug  8 20:57 mnt -> mnt:[4026533227]
$ sudo ls -l /proc/2528091/ns/ | ag mnt
lrwxrwxrwx 1 root root 0 Aug  8 20:57 mnt -> mnt:[4026533227]
```

As this is starting to get fairly long, I will stop rambling on and continue in [On Unsharing Namespaces, Part Two](https://benjamintoll.com/2022/12/14/on-unsharing-namespaces-part-two/) where we’ll cover the `net` and `user` namespaces.

## Summary <a name="link_5"></a>

I hope you have found this article scintillating and that you’ve been titillated. I know that I have.

## References <a name="link_6"></a>

- [On Unsharing Namespaces, Part Two](https://benjamintoll.com/2022/12/14/on-unsharing-namespaces-part-two/)
- [Container Security by Liz Rice](https://containersecurity.tech/)
- [Containers From Scratch - Liz Rice - GOTO 2018](https://www.youtube.com/watch?v=8fi7uSYlOdc)
- [Trivy](https://github.com/aquasecurity/trivy)
- [Index of /alpine/](http://dl-cdn.alpinelinux.org/alpine/)

# On Unsharing Namespaces, Part Two <a name="link_62"></a>

---

This is the second installment in a riveting series. Be sure to have read the [first part](https://benjamintoll.com/2022/08/08/on-unsharing-namespaces-part-one/), which covers the `uts`, `pid` and `mnt` namespaces!

> There are more [namespaces](https://www.man7.org/linux/man-pages/man7/namespaces.7.html) than just the ones we’re looking at in this series.

---

## Namespaces <a name="link_7"></a>

### Network <a name="link_8"></a>

Unsharing the `net` [network namespace](https://www.man7.org/linux/man-pages/man7/network_namespaces.7.html) allows for the process to have its own IPv4 and IPv6 stacks, network links, firewall rules and IP routing tables (among others).

Let’s look at the difference between sharing, or inheriting, the `net` namespace from the parent process and unsharing it.

#### Sharing <a name="link_9"></a>

In the absence of the `--net` option to `unshare`, the `bash` program running in the forked process below will inherit the `--net` namespace from its parent, and we can see this by listing out the processes `ns` directory in `/proc`:

```bash
# On the host.
$ unshare bash

# In the container process.
$ ls -l /proc/$$/ns | ag net
lrwxrwxrwx 1 btoll btoll 0 Aug  9 17:52 net -> net:[4026532008]
```

Then, on the host, we demonstrate that `pid` 1 (`systemd` on my Debian `bullseye` distro) indeed has the same `net` namespace, which the containing process inherited:

```bash
# On the host, where PID 1 is `systemd`.
$ sudo ls -l /proc/1/exe
lrwxrwxrwx 1 root root 0 Aug  2 15:21 /proc/1/exe -> /lib/systemd/systemd
$ sudo ls -l /proc/1/ns | ag net
lrwxrwxrwx 1 root root 0 Aug  7 20:19 net -> net:[4026532008]
```

Further, back in the container process, since it inherited the same `net` namespace we can show that the new process can see all of the same namespaced network interfaces as the host and accesses the same routing table:

```bash
$ ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: enp2s0f1: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc fq_codel state DOWN group default qlen 1000
    link/ether 80:fa:5b:53:fb:82 brd ff:ff:ff:ff:ff:ff
3: wlp3s0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
    link/ether e4:70:b8:b4:22:a6 brd ff:ff:ff:ff:ff:ff
    inet 192.168.1.10/24 brd 192.168.1.255 scope global dynamic noprefixroute wlp3s0
       valid_lft 196879sec preferred_lft 196879sec
    inet6 fe80::2308:ab5:dc8:cdae/64 scope link noprefixroute
       valid_lft forever preferred_lft forever
$
$ ip r
default via 192.168.1.1 dev wlp3s0 proto dhcp metric 600
169.254.0.0/16 dev wlp3s0 scope link metric 1000
172.17.0.0/16 dev docker0 proto kernel scope link src 172.17.0.1 linkdown
192.168.1.0/24 dev wlp3s0 proto kernel scope link src 192.168.1.10 metric 600
```

#### Unsharing <a name="link_10"></a>

Ok, now, let’s create a process with its own `net` namespace. Immediately, we can see that the `net` namespaces are not the same, using the same steps as before:

```bash
# On the host.
$ sudo unshare --net bash

# In the container process.
# ls -l /proc/$$/ns | ag net
lrwxrwxrwx 1 root root 0 Aug  9 17:58 net -> net:[4026533295]
```

```bash
# Again, on the host, where PID 1 is `systemd`.
$ sudo ls -l /proc/1/exe
lrwxrwxrwx 1 root root 0 Aug  2 15:21 /proc/1/exe -> /lib/systemd/systemd
$ sudo ls -l /proc/1/ns | ag net
lrwxrwxrwx 1 root root 0 Aug  7 20:19 net -> net:[4026532008]
```

More, back in the container process, we can show that the new process only has a [`loopback`](https://benjamintoll.com/2019/09/23/on-loopback/) interface and has no routing table information:

```bash
# ip a
1: lo: <LOOPBACK> mtu 65536 qdisc noop state DOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
# ip route
Error: ipv4: FIB table does not exist.
Dump terminated
```

> Note that not giving a command to `unshare` will result in it opening a shell by default (determined by the value of the `SHELL` environment variable).
>
> We could have omitted the `bash` program name from all of the above examples.

Weeeeeeeeeeeeeeeeeeeeeeeeeeee

#### Connectivity <a name="link_11"></a>

Let’s now establish network connectivity between the host and the container process by creating two virtual Ethernet ([`veth`](https://man7.org/linux/man-pages/man4/veth.4.html)) interfaces.

Conceptually, we can think of this as a cable that connects the default `net` network namespace with the new `net` network namespace of the container.

Here are some characteristics of `veth` devices (from the manpage):

- they can act as tunnels between network namespaces to create a bridge to a physical network device in another namespace, but can also be used as standalone network devices
- always created in interconnected pairs, such as:
  ```bash
  $ sudo ip link add p1-name type veth peer name p2-name
  ```
  - `p1-name` and `p2-name` are the names assigned to the two connected end points
- packets transmitted on one device in the pair are immediately received on the other device
- when either device is down the link state of the pair is down

> Anyone with an interest in container networking should pay particular attention to these little fellas.
>
> `veth` devices have a particularly interesting use case: placing one end of a `veth` pair in one network namespace and the other end in another network namespace allows for communicating between network namespaces.
>
> Here is another example (using the `netns` parameter):
>
> ```bash
> $ sudo ip link add p1-name netns p1-ns type veth peer p2-name netns p2-ns
> ```

We’ll start by creating the new process with its own unshared `net` network namespace:

```bash
$ sudo unshare --net bash
```

Again, we can see that the new process has its own `net` namespace that is distinct from the host. This time, we’ll show the difference by using the [`lsns`](https://www.man7.org/linux/man-pages/man8/lsns.8.html) command with custom columns:

```bash
# lsns --type net -o NS,PID,COMMAND | ag "systemd|bash"
4026532008       1 /lib/systemd/systemd --system --deserialize 18
4026532801 2561438 bash
```

As we can see from the column options passed to the output parameter (`-o`), the first column is the `net` namespace, the second the process ID and the third the command that created the process (notably, the first column has different values).

> If there were no accessible namespaces, the result would be empty.

You could also list all of the namespaces of a process by passing the `-p` option the `pid`:

```bash
# lsns -p $$
        NS TYPE   NPROCS      PID USER COMMAND
4026531834 time       99        1 root /sbin/init
4026531835 cgroup     99        1 root /sbin/init
4026531836 pid        99        1 root /sbin/init
4026531837 user       99        1 root /sbin/init
4026531838 uts        97        1 root /sbin/init
4026531839 ipc        99        1 root /sbin/init
4026531840 mnt        94        1 root /sbin/init
4026532160 net         2  2561438 root bash
```

Let’s look at networking information. Note that there are no entries in the routing table yet in the container, and the only device is `loopback`:

```bash
# ip route
Error: ipv4: FIB table does not exist.
Dump terminated
#
# ip link
1: lo: <LOOPBACK> mtu 65536 qdisc noop state DOWN mode DEFAULT group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
```

Let’s now connect the new `net` namespace to the default `net` namespace with that `pid`. Run the following command on the host, first getting the `pid` of the new process which we’ll need to create its virtual network interface (we can also get it inside the container by echoing out the current process ID using a [special Bash parameter](https://www.gnu.org/software/bash/manual/html_node/Special-Parameters.html)):

```bash
# echo $$
2561438
$ sudo ip link add ve1 netns 2561438 type veth peer name ve2 netns 1
```

Let’s break that down like a hip beat:

- We’re adding a new virtual Ethernet interface called `ve1` and binding it to the process with ID 2561438.
  - Note that we called have called this anything, it doesn’t have to be `ve1`. It could have been called `poop1`.
- The type `veth` is a virtual Ethernet interface.
- The `peer` keyword means that we’re joining the two new interfaces together.
- We’re adding a new virtual Ethernet interface called `ve2` and binding it to the process with ID 1.
  - Note that we called have called this anything, it doesn’t have to be `ve2`. It could have been called `poop2`.

In the container, we can now see that the new virtual Ethernet device has indeed been added:

```bash
# ip link
1: lo: <LOOPBACK> mtu 65536 qdisc noop state DOWN mode DEFAULT group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
2: ve1@if3: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN mode DEFAULT group default qlen 1000
    link/ether 26:c2:b6:f3:aa:3d brd ff:ff:ff:ff:ff:ff link-netnsid 0
```

And we’ll bring it up:

```bash
# ip link set ve1 up
# ip l
1: lo: <LOOPBACK> mtu 65536 qdisc noop state DOWN mode DEFAULT group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
2: ve1@if3: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state LOWERLAYERDOWN mode DEFAULT group default qlen 1000
    link/ether 26:c2:b6:f3:aa:3d brd ff:ff:ff:ff:ff:ff link-netnsid 0
```

We’ll do the same on the host:

```bash
$ ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
...
3745: ve2@if2: <BROADCAST,MULTICAST> mtu 1500 qdisc noqueue state DOWN group default qlen 1000
    link/ether 9e:ea:69:72:e3:1e brd ff:ff:ff:ff:ff:ff link-netnsid 3
$
$ sudo ip link set ve2 up
$ ip a
...
3745: ve2@if2: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
    link/ether 9e:ea:69:72:e3:1e brd ff:ff:ff:ff:ff:ff link-netnsid 3
    inet6 fe80::9cea:69ff:fe72:e31e/64 scope link
       valid_lft forever preferred_lft forever
```

> Bringing an interface `UP` means to enable it. What does `LOWER_UP` mean, then?
>
> It signals that it is a physical layer link flag. `LOWER_UP` indicates that an `Ethernet` cable was plugged in and that the device is connected to the network, that is, it can send and receive encoded and decoded information from its physical medium source, be it electricity, light or radio waves.

Of course, in order to be able to send traffic to the devices, both need to be assigned an IP address on the same network.

First, in the container:

```bash
# ip addr add 192.168.1.100/24 dev ve1
# ip a
1: lo: <LOOPBACK> mtu 65536 qdisc noop state DOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
2: ve1@if3745: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
    link/ether 1e:93:3b:e3:8f:32 brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 192.168.1.100/24 scope global ve1
       valid_lft forever preferred_lft forever
    inet6 fe80::1c93:3bff:fee3:8f32/64 scope link
       valid_lft forever preferred_lft forever
```

As soon as the IP is associated, a route has been added to the container’s routing table (since its using [`CIDR`](https://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing) notation, the kernel automatically adds a routing entry):

```bash
# ip route
192.168.1.0/24 dev ve1 proto kernel scope link src 192.168.1.100
```

And on the host:

```bash
$ sudo ip addr add 192.168.1.200/24 dev ve2
$ ip a
...
3745: ve2@if2: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
    link/ether 9e:ea:69:72:e3:1e brd ff:ff:ff:ff:ff:ff link-netnsid 3
    inet 192.168.1.200/24 scope global ve2
       valid_lft forever preferred_lft forever
    inet6 fe80::9cea:69ff:fe72:e31e/64 scope link
       valid_lft forever preferred_lft forever
```

Likewise, when the IP address was associated with the host’s virtual Ethernet device, a new route was added to its routing table (again, because `CIDR` notation was used):

```bash
$ ip route
default via 192.168.1.1 dev wlp3s0 proto dhcp metric 20600
...
192.168.1.0/24 dev ve2 proto kernel scope link src 192.168.1.200
192.168.1.0/24 dev wlp3s0 proto kernel scope link src 192.168.1.10 metric 600
```

Let’s test it!

In the container:

```bash
# ping -c4 192.168.1.200
PING 192.168.1.200 (192.168.1.200) 56(84) bytes of data.
64 bytes from 192.168.1.200: icmp_seq=1 ttl=64 time=0.097 ms
64 bytes from 192.168.1.200: icmp_seq=2 ttl=64 time=0.095 ms
64 bytes from 192.168.1.200: icmp_seq=3 ttl=64 time=0.096 ms
64 bytes from 192.168.1.200: icmp_seq=4 ttl=64 time=0.094 ms

--- 192.168.1.200 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3067ms
rtt min/avg/max/mdev = 0.094/0.095/0.097/0.001 ms
```

On the host:

```bash
$ ping -c4 192.168.1.100
PING 192.168.1.100 (192.168.1.100) 56(84) bytes of data.
64 bytes from 192.168.1.100: icmp_seq=1 ttl=64 time=0.081 ms
64 bytes from 192.168.1.100: icmp_seq=2 ttl=64 time=0.074 ms
64 bytes from 192.168.1.100: icmp_seq=3 ttl=64 time=0.067 ms
64 bytes from 192.168.1.100: icmp_seq=4 ttl=64 time=0.068 ms

--- 192.168.1.100 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3060ms
rtt min/avg/max/mdev = 0.067/0.072/0.081/0.005 ms
```

Weeeeeeeeeeeeeeeeeeeeeeee

> At this point, the container can only send traffic to addresses in the 192.168.1.0/24 range.

Note that the `veth` device and the route in the routing table will both be removed automatically from the host when the container is exited.

If the two processes can’t communicate, i.e., the `ping`s don’t work, make sure that the new network you configured for the container processes doesn’t conflict with any others.

Check out the following two resources for more information:

- [On Linux Container Networking](https://benjamintoll.com/2023/11/28/on-linux-container-networking/)
- [Linux Networking GitHub Repository](https://github.com/btoll/linux-networking)

### User <a name="link_12"></a>

The [`user` namespace](https://www.man7.org/linux/man-pages/man7/user_namespaces.7.html) is the only one that can be created by a non-privileged user. This allows for running [rootless containers](https://blog.aquasec.com/rootless-containers-boosting-container-security), which greatly mitigates one of the best-known security implications of containers: running containers as root. Not needing to run containers as a privileged user is a good security practice, but unfortunately not all popular container runtimes allow for this.

Does this mean that a container shouldn’t ever have a `root` user? No, of course not. Containers need to have a privileged user to do whatever nefarious things containers do.

The critical difference is that you don’t want a `root` user in a container **also** mapping to/running as the `root` user on the host. This is very bad, because if the `root` user breaks out of the container and the `user` namespace, then they are also `root` on the host.

This would mean, to put it mildly, that you would be fucked. Remember that the host can see everything that runs on it, including containers? The attacker could then do whatever they wanted, and most likely, do it gleefully.

Sadly, most people who run containers use Docker, and Docker was not built with security in mind. It was an afterthought. Maybe a Docker Captain can tell you about it someday.

So, what does one do? Curse the decision to promote Docker? Well, yes. Alias docker to [`podman`](https://podman.io/)? Also, yes. But, further, _critically_, use the `user` namespace to map the `root` user in the container to a non-privileged account on the host. That way, if an attacker breaks out of the container, the worst they can do is delete the poems in your home directory.

In addition, the effective user on the host can have greater capabilities inside the container running as `root`.

Let’s see how that mapping is done.

#### Rootless Containers <a name="link_13"></a>

Let’s create a process that inherits all of its parent’s namespaces and check out the user information:

```bash
$ unshare bash
$ id
uid=1000(btoll) gid=1000(btoll) groups=1000(btoll)
```

Ok, it’s running in the same `user` namespace as the PPID (parent process ID) and has inherited the effective user that created the child process.

How about when creating the child process as a privileged user?

```bash
$ sudo unshare bash
# id
uid=0(root) gid=0(root) groups=0(root)
```

That’s interesting and to be expected. Let’s now create a process with an unshared `user` namespace:

```bash
$ unshare --user bash
$ id
uid=65534(nobody) gid=65534(nogroup) groups=65534(nogroup)
```

Ok, the `nobody` user. Let’s confirm that the process has a `user` namespace distinct from the host:

On the host:

```bash
$ lsns -t user | ag "systemd|bash"
4026531837 user      57    1881 btoll /lib/systemd/systemd --user
4026533574 user       1 2713100 btoll bash
```

> Why can’t we run the `lsns` as an unprivileged user in the container as before?
>
> Great question, Eagle Eye. Since we’re now using an unshared `user` namespace, the user in the container is `nobody`, **not** `btoll`, the effective user that created the process.
>
> So, the `nobody` user can only see its own `user` namespace, and the `btoll` user doesn’t exist in that namespace.

Ok, let’s now do the mapping.

The `/proc/PID/uid_map` and `/proc/PID/gid_map` are the kernel interfaces for the user and group IDs, respectively, for each process.

First, we need to get the `pid` of the “container” (really, the `bash` process):

In the container:

```bash
$ echo $$
2713100
```

On the host:

```bash
$ sudo echo "0 1000 1" >> /proc/2713100/uid_map
```

> These special `/proc` files can only be written to once.

Let’s break that down (`0 1000 1`):

1. (0) The first number is the start of the range of the user IDs that will be used **in the container**.
2. (1000) The second number is the start of the range of the user IDs that will be mapped to **on the host**.
3. (1) The last number states the number of user IDs (the length of the range) that will be mapped in the container. Only one user ID is given, since we only expect one user for this container. That’s a good thing.

This example is doing the following, in plain English: “Map the effective user ID on the host with user ID 1000 to the user ID of 0 in the container, and only allocate one user ID.”

The end result is that my `btoll` (1000) user on the host is now seen as `root` in the new `user` namespace in the container.

[Kool moe dee](ttps://en.wikipedia.org/wiki/Kool_Moe_Dee).

After running the mapping command above, we see that the mapping has taken effect in the container:

```bash
$ id
uid=0(root) gid=65534(nogroup) groups=65534(nogroup)
```

> The user may still say `nobody` in the prompt, but this is expected since the shell init scripts like `.bash_profile` haven’t been run again. Rest assured, though, the user is the privileged `root` user in the container.

After having gone through all of those contortions to write to the `/proc/PID/uid_map` after the container has been created to set up the `root` user mapping, let’s now look at a very simple way to do it as a switch to the `unshare` command:

```bash
$ unshare --map-root-user bash
# id
uid=0(root) gid=0(root) groups=0(root),65534(nogroup)
# cat /proc/$$/uid_map
         0       1000          1
```

Of course, the `--map-root-user` switch implies the creation of a new `user` namespace:

In the container:

```bash
# lsns -t user
        NS TYPE  NPROCS     PID USER COMMAND
4026533651 user       2 2935027 root bash
```

On the host:

```bash
$ sudo ls -l /proc/1/ns | ag user
lrwxrwxrwx 1 root root 0 Dec 17 16:42 user -> user:[4026531837]
```

Weeeeeeeeeeeeeeeeeeeee

Lastly, let’s prove to ourselves that this is indeed a rootless container. In other words, let’s show that, although the container is running as a `root` user, it actually maps to a non-privileged user on the host:

In the container:

```bash
$ unshare --map-root-user bash
# sleep 12345 &
[1] 2945562
# id
uid=0(root) gid=0(root) groups=0(root),65534(nogroup)
# whoami
root
# touch fooby
# ls -li fooby
6038245 -rw-rw-r-- 1 root root 0 Dec 17 17:20 fooby
```

On the host:

```bash
$ ps -ft5
UID          PID    PPID  C STIME TTY          TIME CMD
btoll    2690597    2294  0 Dec16 pts/5    00:00:00 -bash
btoll    2944466 2690597  0 17:14 pts/5    00:00:00 bash
btoll    2945562 2944466  0 17:16 pts/5    00:00:00 sleep 12345
$ ls -li /home/btoll/fooby
6038245 -rw-rw-r-- 1 btoll btoll 0 Dec 17 17:20 /home/btoll/fooby
```

Told you so.

#### Capabilities <a name="link_14"></a>

Note that the [capabilities](https://man7.org/linux/man-pages/man7/capabilities.7.html) may be augmented depending on the mapping. Below we see an example of a process not being able to create a `mnt` namespace because the effective user does not have the correct permissions:

```bash
$ unshare --mount sh
unshare: unshare failed: Operation not permitted
$ id
uid=65534(nobody) gid=65534(nogroup) groups=65534(nogroup)
```

However, if we give the user in that container escalated privileges by running the now-familiar mapping command on the host, we can effect that by mapping the non-privileged user on the host to the `root` user in the container. This will allow us to do what we want. Remember, if the `root` user does find a way to break out of the `user` namespace, the damage will be limited to only what the `btoll` user is permitted to do on the host.

> And, although dangerously handsome and charming, the `btoll` user won’t be able to do any effective damage on the host due to lack of permissions.

Again, this will look like the following, if the new container process has the PID 2713100:

```bash
$ sudo echo "0 1000 1" >> /proc/2713100/uid_map
```

Back in the container, we see that the user is now `root` and now has the capabilites needed to unshare any other namespace:

```bash
$ id
uid=0(root) gid=65534(nogroup) groups=65534(nogroup)
$ unshare --mount sh
\u@\h:\w$
```

Let’s wrap up this section by looking at the capabilities for a rootless container:

On the host:

```bash
$ capsh --print | ag "Current|uid"
Current: =
Bounding set =cap_chown,cap_dac_override,cap_dac_read_search,cap_fowner,cap_fsetid,cap_kill,cap_setgid,cap_setuid,cap_setpcap,cap_linux_immutable,cap_net_bind_service,cap_net_broadcast,cap_net_admin,cap_net_raw,cap_ipc_lock,cap_ipc_owner,cap_sys_module,cap_sys_rawio,cap_sys_chroot,cap_sys_ptrace,cap_sys_pacct,cap_sys_admin,cap_sys_boot,cap_sys_nice,cap_sys_resource,cap_sys_time,cap_sys_tty_config,cap_mknod,cap_lease,cap_audit_write,cap_audit_control,cap_setfcap,cap_mac_override,cap_mac_admin,cap_syslog,cap_wake_alarm,cap_block_suspend,cap_audit_read
 secure-no-suid-fixup: no (unlocked)
uid=1000(btoll) euid=1000(btoll)
```

In the container:

```bash
# capsh --print | ag "Current|uid"
Current: =ep
Bounding set =cap_chown,cap_dac_override,cap_dac_read_search,cap_fowner,cap_fsetid,cap_kill,cap_setgid,cap_setuid,cap_setpcap,cap_linux_immutable,cap_net_bind_service,cap_net_broadcast,cap_net_admin,cap_net_raw,cap_ipc_lock,cap_ipc_owner,cap_sys_module,cap_sys_rawio,cap_sys_chroot,cap_sys_ptrace,cap_sys_pacct,cap_sys_admin,cap_sys_boot,cap_sys_nice,cap_sys_resource,cap_sys_time,cap_sys_tty_config,cap_mknod,cap_lease,cap_audit_write,cap_audit_control,cap_setfcap,cap_mac_override,cap_mac_admin,cap_syslog,cap_wake_alarm,cap_block_suspend,cap_audit_read
 secure-no-suid-fixup: no (unlocked)
uid=0(root) euid=0(root)
#
# cat /proc/$$/uid_map
         0       1000          1
```

Note that the privileges have been escalated in the container, and the last `cat` command shows indeed that the mapping of `root` in the container is to `btoll(1000)` on the host.

Weeeeeeeeeeeeeeeeeeeeeeeeeee

#### /etc/sub{u,g}id <a name="link_15"></a>

You may be thinking to yourself, “hey, the format of the `/proc/PID/uid_map` looks suspiciously like the files `/etc/subuid` and `/etc/subgid` that I’ve configured to map users when using Docker”, or something to that effect.

And you’d be right. Unfortunately, I haven’t been able to ascertain the provenance of those files.

Are they an implementation detail of an [OCI spec](https://opencontainers.org/)? Do they predate the burgeoning popularity and ubiquity of containers? After all, the files are listed in the [`useradd` man page](https://www.man7.org/linux/man-pages/man8/useradd.8.html#FILES) in the `FILES` section, and the [`getuid`](https://www.man7.org/linux/man-pages/man2/getuid.2.html) and [`getgid`](https://www.man7.org/linux/man-pages/man2/getgid.2.html) system calls, et al., also use them.

Does [the Shadow](https://en.wikipedia.org/wiki/The_Shadow) know?

I think it’s safe to say that regardless of its origin, these files allow for an easier way to map users within a `user` namespace than what we’ve seen in the examples above.

#### nsswitch.conf <a name="link_16"></a>

Interestingly, I stumbled across the [subuid(5) man page](https://www.man7.org/linux/man-pages/man5/subuid.5.html) when trying to find the provenance of the `/etc/sub{u,g}id` files, and it states the following:

> The delegation of the subordinate uids can be configured via the subid field in /etc/nsswitch.conf file. Only one value can be set as the delegation source. Setting this field to files configures the delegation of uids to /etc/subuid.

I have not tested this, but this would be a great area to explore.

## Summary <a name="link_17"></a>

Um.

## References <a name="link_18"></a>

- [On Unsharing Namespaces, Part One](https://benjamintoll.com/2022/08/08/on-unsharing-namespaces-part-one/)
- [Container Security by Liz Rice](https://containersecurity.tech/)
- [Containers From Scratch - Liz Rice - GOTO 2018](https://www.youtube.com/watch?v=8fi7uSYlOdc)
- [On Linux Container Networking](https://benjamintoll.com/2023/11/28/on-linux-container-networking/)
- [Linux Networking GitHub Repository](https://github.com/btoll/linux-networking)
- [Trivy](https://github.com/aquasecurity/trivy)
- [Index of /alpine/](http://dl-cdn.alpinelinux.org/alpine/)
- [Linux Bridges, IP Tables & CNI Plug-Ins: A Container Networking Deep Dive](https://www.youtube.com/watch?v=z-ITjDQT7DU)

- [](https://gohugo.io/)
