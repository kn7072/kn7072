[source](https://dev.to/pemcconnell/docker-overlayfs-network-namespaces-docker-bridge-and-dns-52jo?ysclid=mlp2f04ty6323346426)

- [ LowerDir](#link_1)
- [ UpperDir](#link_2)
- [ MergedDir](#link_3)
- [ Do it yourself](#link_4)

# Docker Overlayfs: How filesystems work in Docker

This is a brief follow up to my article on [Docker networking: Network Namespaces, Docker Bridge and DNS](https://www.petermcconnell.com/posts/linux_networking/)

Docker uses the OverlayFS file system to manage the file system of its containers. When a container is run, Docker creates a new layer for the container's file system on top of the base image. This allows the container to have its own file system that is isolated from the host system and other containers.

Running the `ubuntu:22.04` image we can see the root file system differs from the host where I'm running it. Below you can see there is a file in root called `/.dockerenv`:

```
$ docker run --rm -ti ubuntu:22.04 bash
root@541cc3b62543:/# ls -al /
total 56
drwxr-xr-x   1 root root 4096 Jan 19 11:51 .
drwxr-xr-x   1 root root 4096 Jan 19 11:51 ..
-rwxr-xr-x   1 root root    0 Jan 19 11:51 .dockerenv
lrwxrwxrwx   1 root root    7 Nov 30 02:04 bin -> usr/bin
drwxr-xr-x   2 root root 4096 Apr 18  2022 boot
drwxr-xr-x   5 root root  360 Jan 19 11:51 dev
drwxr-xr-x   1 root root 4096 Jan 19 11:51 etc
drwxr-xr-x   2 root root 4096 Apr 18  2022 home
lrwxrwxrwx   1 root root    7 Nov 30 02:04 lib -> usr/lib
lrwxrwxrwx   1 root root    9 Nov 30 02:04 lib32 -> usr/lib32
lrwxrwxrwx   1 root root    9 Nov 30 02:04 lib64 -> usr/lib64
lrwxrwxrwx   1 root root   10 Nov 30 02:04 libx32 -> usr/libx32
drwxr-xr-x   2 root root 4096 Nov 30 02:04 media
drwxr-xr-x   2 root root 4096 Nov 30 02:04 mnt
drwxr-xr-x   2 root root 4096 Nov 30 02:04 opt
dr-xr-xr-x 491 root root    0 Jan 19 11:51 proc
drwx------   2 root root 4096 Nov 30 02:07 root
drwxr-xr-x   5 root root 4096 Nov 30 02:07 run
lrwxrwxrwx   1 root root    8 Nov 30 02:04 sbin -> usr/sbin
drwxr-xr-x   2 root root 4096 Nov 30 02:04 srv
dr-xr-xr-x  13 root root    0 Jan 19 11:51 sys
drwxrwxrwt   2 root root 4096 Nov 30 02:07 tmp
drwxr-xr-x  14 root root 4096 Nov 30 02:04 usr
drwxr-xr-x  11 root root 4096 Nov 30 02:07 var
```

Which does not exist at root on the host running the container:

```
root@541cc3b62543:/#
root@541cc3b62543:/# exit
exit
$ stat /.dockerenv
stat: cannot statx '/.dockerenv': No such file or directory
```

So ... _where_ does it exist? To inspect the layers of a running container, you can use the "docker inspect" command followed by the container ID or name. This will return a JSON object containing information about the container, including its layers. To view this we'll re-run our `ubuntu:22.04` container, grab the ID and inspect it:

```
$ docker run --rm -d -ti ubuntu:22.04 bash
6a9014d7ebfddb3a107b29aca3764f24e51f64fda1e8b8cec135c18923daefeb
# lower directory
$ docker inspect 6a9014d7ebfddb3a107b29aca3764f24e51f64fda1e8b8cec135c18923daefeb -f '{{.GraphDriver.Data.LowerDir}}'
/dockerstore/overlay2/268eb11c54948d6293aa3947b7a2c83b1395b18509518e26487f0e79997f787a-init/diff:/dockerstore/overlay2/bb9057b4f1980fe004301f181c3313c15c2a75b7c7b7c5a6fe80159d2275f0d3/diff

# upper directory
$ docker inspect 6a9014d7ebfddb3a107b29aca3764f24e51f64fda1e8b8cec135c18923daefeb -f '{{.GraphDriver.Data.UpperDir}}'
/dockerstore/overlay2/268eb11c54948d6293aa3947b7a2c83b1395b18509518e26487f0e79997f787a/diff

# merged directory
$ docker inspect 6a9014d7ebfddb3a107b29aca3764f24e51f64fda1e8b8cec135c18923daefeb -f '{{.GraphDriver.Data.MergedDir}}'
/dockerstore/overlay2/268eb11c54948d6293aa3947b7a2c83b1395b18509518e26487f0e79997f787a/merged
```

I'll keep this container running and we'll dig into these contents shortly.

When a container is run, its layers are stored in the host system's file system, typically in the `/var/lib/docker/overlay2` directory. You can see mine is in `/dockerstore/` as I have manually set `data-root` in `/etc/docker/daemon.json` for the host that I'm testing this on. Each layer is represented by a directory that contains the files and directories that make up that layer. The topmost layer is the one that the container is currently using, and the lower layers are the ones that are inherited from the base image.

The advantages of using layers in Docker include:

- Smaller image size, since multiple containers can share a common base image
- Faster container startup time, since only the changes made to the container are stored in new layers
- Easier to manage and update containers, since changes can be made to a container's layer without affecting the base image
- Greater security, since each container's file system is isolated from other containers and the host system.

Please keep in mind that the information is general and may vary depending on specific scenarios.

Now lets take a deeper look at the filesystem for our running container.

## LowerDir <a name="link_1"></a>

This value is unique in the outputs above in that it's actually two paths, separated by a colon:

```
$ docker inspect 6a9014d7ebfddb3a107b29aca3764f24e51f64fda1e8b8cec135c18923daefeb -f '{{.GraphDriver.Data.LowerDir}}'
/dockerstore/overlay2/268eb11c54948d6293aa3947b7a2c83b1395b18509518e26487f0e79997f787a-init/diff:/dockerstore/overlay2/bb9057b4f1980fe004301f181c3313c15c2a75b7c7b7c5a6fe80159d2275f0d3/diff
```

The first part (left side of `:`) is the path to the init layer of the container. this is the layer that contains the initial filesystem of the container, which is based on the base image. We can take a look at the contents of that layer with `ls`:

```
sudo ls /dockerstore/overlay2/268eb11c54948d6293aa3947b7a2c83b1395b18509518e26487f0e79997f787a-init/diff
dev  etc
```

The second part (right side of `:`) is the path to the layer of the container that includes changes from the rest of the Dockerfile. Again we can take a look:

```
sudo ls /dockerstore/overlay2/bb9057b4f1980fe004301f181c3313c15c2a75b7c7b7c5a6fe80159d2275f0d3/diff
bin  boot  dev  etc  home  lib  lib32  lib64  libx32  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var
```

To better visualise this, lets create our own Dockerfile:

```
FROM ubuntu:22.04

RUN mkdir -p /testinglowerdir/ && echo -n "hellothere" > /testinglowerdir/foo
```

Now, given what we learned above, when we run this container the first part of `LowerDir` should contain _all_ the contents for `ubuntu:22.04` and the second part of `LowerDir` should contain only `/testinglowerdir/`:

```
$ docker build -t=test .
Sending build context to Docker daemon  2.048kB
Step 1/2 : FROM ubuntu:22.04
 ---> 6b7dfa7e8fdb
Step 2/2 : RUN mkdir -p /testinglowerdir/ && echo -n "hellothere" > /testinglowerdir/foo
 ---> Running in e71a7cd5541c
Removing intermediate container e71a7cd5541c
 ---> df924945a2b0
Successfully built df924945a2b0
Successfully tagged test:latest
$ docker run --rm -d -ti test bash
9c9fe0bcd283bc0c9649b77246115e3a09e8885efd53f0e9de09de537bea9188
$ docker inspect 9c9fe0bcd283bc0c9649b77246115e3a09e8885efd53f0e9de09de537bea9188 -f '{{.GraphDriver.Data.LowerDir}}'
/dockerstore/overlay2/5501fd185b14a60317f3e0db485bb8f8c5cf41b7cb1ed0688526ba918938b7bf-init/diff:/dockerstore/overlay2/4d49e9a62bad55c3761ab08ded87f56010b28a40f264896c01e5c1c653b826a8/diff:/dockerstore/overlay2/bb9057b4f1980fe004301f181c3313c15c2a75b7c7b7c5a6fe80159d2275f0d3/diff
$ # show directory contents for second part of LowerDir
$ sudo ls /dockerstore/overlay2/4d49e9a62bad55c3761ab08ded87f56010b28a40f264896c01e5c1c653b826a8/diff
testinglowerdir
```

## UpperDir <a name="link_2"></a>

```
$ docker inspect 6a9014d7ebfddb3a107b29aca3764f24e51f64fda1e8b8cec135c18923daefeb -f '{{.GraphDriver.Data.UpperDir}}'
/dockerstore/overlay2/268eb11c54948d6293aa3947b7a2c83b1395b18509518e26487f0e79997f787a/diff
```

The UpperDir contains changes that we've made at runtime. To see this in action we can exec into our container and create a simple directory with a file in the root directory:

```
docker exec -ti 6a9 bash
root@6a9014d7ebfd:/# mkdir /tutorial
root@6a9014d7ebfd:/# echo 'iseeyou' > /tutorial/ohai
```

We can now see this in our UpperDir directory:

```
$ sudo ls /dockerstore/overlay2/268eb11c54948d6293aa3947b7a2c83b1395b18509518e26487f0e79997f787a/diff/
root  tutorial
$ sudo cat /dockerstore/overlay2/268eb11c54948d6293aa3947b7a2c83b1395b18509518e26487f0e79997f787a/diff/tutorial/ohai
iseeyou
```

Want to quickly see what files are being created by a running container? This is something the `UpperDir` can tell you.

## MergedDir <a name="link_3"></a>

```
$ docker inspect 6a9014d7ebfddb3a107b29aca3764f24e51f64fda1e8b8cec135c18923daefeb -f '{{.GraphDriver.Data.MergedDir}}'
/dockerstore/overlay2/268eb11c54948d6293aa3947b7a2c83b1395b18509518e26487f0e79997f787a/merged
```

I'm sure you've guessed what this one is... This is the merged structure:

```
$ sudo ls /dockerstore/overlay2/268eb11c54948d6293aa3947b7a2c83b1395b18509518e26487f0e79997f787a/merged
bin  boot  dev  etc  home  lib  lib32  lib64  libx32  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  tutorial  usr  var
```

Here you can see all of the directories from the LowerDir and UpperDir together. We can chroot into this directory to "see what docker sees":

```
sudo chroot /dockerstore/overlay2/268eb11c54948d6293aa3947b7a2c83b1395b18509518e26487f0e79997f787a/merged /bin/bash
root@pete:/# ls -al
total 72
drwxr-xr-x  1 root root 4096 Jan 19 12:21 .
drwxr-xr-x  1 root root 4096 Jan 19 12:21 ..
-rwxr-xr-x  1 root root    0 Jan 19 11:56 .dockerenv
lrwxrwxrwx  1 root root    7 Nov 30 02:04 bin -> usr/bin
drwxr-xr-x  2 root root 4096 Apr 18  2022 boot
drwxr-xr-x  1 root root 4096 Jan 19 11:56 dev
drwxr-xr-x  1 root root 4096 Jan 19 11:56 etc
drwxr-xr-x  2 root root 4096 Apr 18  2022 home
lrwxrwxrwx  1 root root    7 Nov 30 02:04 lib -> usr/lib
lrwxrwxrwx  1 root root    9 Nov 30 02:04 lib32 -> usr/lib32
lrwxrwxrwx  1 root root    9 Nov 30 02:04 lib64 -> usr/lib64
lrwxrwxrwx  1 root root   10 Nov 30 02:04 libx32 -> usr/libx32
drwxr-xr-x  2 root root 4096 Nov 30 02:04 media
drwxr-xr-x  2 root root 4096 Nov 30 02:04 mnt
drwxr-xr-x  2 root root 4096 Nov 30 02:04 opt
drwxr-xr-x  2 root root 4096 Apr 18  2022 proc
drwx------  1 root root 4096 Jan 19 12:16 root
drwxr-xr-x  5 root root 4096 Nov 30 02:07 run
lrwxrwxrwx  1 root root    8 Nov 30 02:04 sbin -> usr/sbin
drwxr-xr-x  2 root root 4096 Nov 30 02:04 srv
drwxr-xr-x  2 root root 4096 Apr 18  2022 sys
drwxrwxrwt  2 root root 4096 Nov 30 02:07 tmp
drwxr-xr-x  2 root root 4096 Jan 19 12:20 tutorial
drwxr-xr-x 14 root root 4096 Nov 30 02:04 usr
drwxr-xr-x 11 root root 4096 Nov 30 02:07 var
root@pete:/# cat /tutorial/ohai
iseeyou
root@pete:/#
```

Pretty sweet! Another way / a "better" way that we can get this view is with `nsenter`:

```
$ sudo nsenter --target $(docker inspect --format {{.State.Pid}} 6a9) --mount --uts --ipc --net --pid
root@6a9014d7ebfd:/# cat /tutorial/ohai
iseeyou
root@6a9014d7ebfd:/#
```

## Do it yourself <a name="link_4"></a>

This has been a quick look into how Docker avails of OverlayFS, but you can of course do this yourself. The basic syntax is:

```
mount -t overlay overlay -o lowerdir=lower,upperdir=upper,workdir=workdir target
```

- `lowerdir` is the lower filesystem
- `upperdir` is the upper filesystem
- `workdir` is a directory where the OverlayFS stores metadata about the overlay
- `target` is the mount point where the overlay will be mounted

For example, if you have two directories, /mnt/lower and /mnt/upper, you can create an OverlayFS file system that combines them at /mnt/overlay with the following command:

```
mount -t overlay overlay -o lowerdir=/mnt/lower,upperdir=/mnt/upper,workdir=/mnt/workdir /mnt/overlay
```

To view the contents of the overlay, you can simply navigate to the mount point (in this example, /mnt/overlay) and use standard Linux commands to view the files and directories.

You can also use `lsblk` command to view the mounted overlays in your system and also you can unmount the overlays using umount command.

Please keep in mind that this is a basic example and there are many other options and settings that can be used when creating an OverlayFS file system.
