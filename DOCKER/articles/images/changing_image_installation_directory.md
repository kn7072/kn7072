[source](https://www.baeldung.com/ops/docker-image-change-installation-directory)

- [ 1. Overview](#link_1)
- [ 2. Setting up an Example](#link_2)
- [ 3. Changing the Image Installation Directory](#link_3)
  - [ 3.1. Using the Daemon Configuration File](#link_4)
  - [ 3.2. Restoring the Default Configuration](#link_5)
  - [ 3.3. Using the _systemd_ Configuration File](#link_6)
  - [ 3.4. Limitation](#link_7)
- [ 4. Migrating the Persistent Objects](#link_8)
  - [ 4.1. Copying Data Using the _rsync_ Command](#link_9)
  - [ 4.2. Restoring the Default Configuration](#link_10)
- [ 5. Conclusion](#link_11)

## 1. Overview <a name="link_1"></a>

While working with [Docker](https://www.docker.com/) containers, we often need to create various persistent objects, such as volumes and images. By default, these objects occupy disk space from the boot disk. This default configuration might cause some significant data issues, such as low disk space for other applications or data loss in case of hardware failure.

In this tutorial, we’ll discuss how to configure the Data Root Directory in a Docker. This allows us to change the image installation directory and mitigate the problems mentioned above.

## 2. Setting up an Example <a name="link_2"></a>

Let’s create a few persistent Docker objects to use as an example.

First, we’ll pull the [NGINX](https://www.nginx.com/) and [Redis](https://redis.io/) images:

```bash
$ docker image pull nginx
$ docker image pull redis
```

Let’s verify they’re pulled ok:

```bash
$ docker image list
REPOSITORY   TAG       IMAGE ID       CREATED       SIZE
nginx        latest    76c69feac34e   2 weeks ago   142MB
redis        latest    c2342258f8ca   2 weeks ago   117MB
```

Next, we’ll create a volume and find its mount point:

```bash
$ docker volume create dangling-volume

$ docker volume inspect dangling-volume -f '{{ .Mountpoint }}'
/var/lib/docker/volumes/dangling-volume/_data
```

Finally, let’s create a sample file inside a */var/lib/docker/volumes/dangling-volume/\_data* directory:

```bash
$ echo "Dangling volume" | sudo tee /var/lib/docker/volumes/dangling-volume/_data/sample.txt

$ sudo cat /var/lib/docker/volumes/dangling-volume/_data/sample.txt
Dangling volume
```

In the next section, we’ll see how to change the Docker Root Directory to store such persistent objects at a different location.

## 3. Changing the Image Installation Directory <a name="link_3"></a>

In Docker, the **image installation directory is denoted by the _DockerRootDir_ property**. We can find its value using the _[info](https://docs.docker.com/engine/reference/commandline/info/)_ child command:

```bash
$ docker info -f '{{ .DockerRootDir }}'
/var/lib/docker
```

In this example, the _/var/lib/docker_ directory from the boot disk represents the Docker Root Directory.

Now, let’s discuss the various methods to change this default root directory.

### 3.1. Using the Daemon Configuration File <a name="link_4"></a>

We can change the default root directory by updating the daemon configuration file. The **default location of this configuration file on Linux is _/etc/docker/daemon.json_**.

So, let’s create a new directory and configure it as the root directory by editing the daemon configuration file:

```bash
$ mkdir -p /tmp/new-docker-root
$ sudo vi /etc/docker/daemon.json
```

Then we edit the file so it has a _data-root_ pointing to the newly created directory. When we’ve saved it:

```bash
$ sudo cat /etc/docker/daemon.json
{
   "data-root": "/tmp/new-docker-root"
}
```

Finally, we must restart the docker service and check the updated root directory using the *info* child command:

```bash
$ sudo systemctl restart docker
$ docker info -f '{{ .DockerRootDir}}'
/tmp/new-docker-root
```

Now, we can see that Docker Root Directory is set to _/tmp/new-docker-root_.

### 3.2. Restoring the Default Configuration <a name="link_5"></a>

In the previous section, we changed the default configuration by updating the daemon configuration file. However, we must restore it to the previous state before moving to the next section.

First, we reset the settings to default by removing the daemon configuration file and _/tmp/new-docker-root_ directory:

```bash
$ sudo rm /etc/docker/daemon.json
$ sudo rm -rf /tmp/new-docker-root/
```

Next, we must restart the docker service for changes to take effect:

```bash
$ sudo systemctl restart docker
```

Finally, we can verify that the Docker Root Directory is set to its default location:

```bash
$ docker info -f '{{ .DockerRootDir}}'
/var/lib/docker
```

### 3.3. Using the _systemd_ Configuration File <a name="link_6"></a>

Similarly, we can also modify the [systemd](https://www.baeldung.com/linux/create-remove-systemd-services) configuration of the docker service to achieve the same result. Docker uses the**_/lib/systemd/system/docker.service_ unit file to store its configuration**. Let’s look at how to update this file.

First, we’ll create a new directory and update the _ExecStart_ property from the _/lib/systemd/system/docker.service_ file*:*

```bash
$ mkdir -p /tmp/new-docker-root/
$ sudo vi /lib/systemd/system/docker.service
```

Now, the updated file looks like this:

```bash
$ grep ExecStart /lib/systemd/system/docker.service
ExecStart=/usr/bin/dockerd --data-root /tmp/new-docker-root -H fd:// --containerd=/run/containerd/containerd.sock
```

In this example, we have **configured the Docker Root Directory using the _–data-root /tmp/new-docker-root_** property.

Next, we must reload the unit file and restart the docker service for changes to take effect:

```bash
$ sudo systemctl daemon-reload
$ sudo systemctl restart docker
```

Finally, let’s check the updated data root directory using the _info_ child command:

```bash
$ docker info -f '{{ .DockerRootDir}}'
/tmp/new-docker-root
```

Here, we can see that the data root directory is pointing to the _/tmp/new-docker-root_ location*.*

### 3.4. Limitation <a name="link_7"></a>

In the previous sections, we saw how to change the Docker Data Root directory. However, just changing the data root properly is not sufficient. Because this configuration **doesn’t locate previously created persistent objects**.

To understand this, let’s list the images and volumes:

```bash
$ docker image list
REPOSITORY   TAG       IMAGE ID   CREATED   SIZE

$ docker volume list
DRIVER    VOLUME NAME
```

As we can see, Docker is unable to locate images and volumes from the previous data root directory.

## 4. Migrating the Persistent Objects <a name="link_8"></a>

For a complete solution to changing our persistent object location, we may also wish to migrate the existing objects.

### 4.1. Copying Data Using the _rsync_ Command <a name="link_9"></a>

_[rsync](https://www.baeldung.com/linux/rsync-transfer-files)_ is a command line utility that copies and synchronizes files and directories in an efficient way. We can use this command to copy the contents from the \_/var/lib/docke_r directory:

Let’s copy the data using the _rsync_ command and restart the docker service:

```bash
$ sudo rsync -aqxP /var/lib/docker/ /tmp/new-docker-root
$ sudo systemctl restart docker
```

In this example, we have used the following:

- –_a_ option to enable the archive mode
- –_q_ option to suppress non-error messages
- –_x_ option to avoid crossing a filesystem boundary while copying directories recursively
- –_P_ option to preserve partially copied files/directories

Now, let’s list the images and volumes:

```bash
$ docker image list
REPOSITORY   TAG       IMAGE ID       CREATED       SIZE
nginx        latest    76c69feac34e   3 weeks ago   142MB
redis        latest    c2342258f8ca   3 weeks ago   117MB

$ docker volume list
DRIVER    VOLUME NAME
local     dangling-volume
```

As we can see, Docker is now able to identify the previously created persistent object.

### 4.2. Restoring the Default Configuration <a name="link_10"></a>

First, let’s stop the docker service and remove the _–data-root_ property from the _/lib/systemd/system/docker.service_ unit file:

```bash
$ sudo systemctl stop docker
$ sudo vi /lib/systemd/system/docker.service
```

After modification, the unit file looks like this:

```bash
$ grep ExecStart /lib/systemd/system/docker.service
ExecStart=/usr/bin/dockerd -H fd:// --containerd=/run/containerd/containerd.sock
```

Now, we’ll reload the unit file, restart the docker service, and check the updated data root directory:

```bash
$ sudo systemctl daemon-reload
$ sudo systemctl restart docker

$ docker info -f '{{ .DockerRootDir}}'
/var/lib/docker
```

## 5. Conclusion <a name="link_11"></a>

In this article, we saw how to change the image installation directory in Docker by configuring the _data-root_ property.

First, we used the daemon configuration file to change the Docker Root Directory. Next, we discussed how to achieve the same result using the _systemd_ unit file. Then, we discussed the limitation imposed by these methods.

Finally, we discussed how to overcome these limitations by migrating persistent objects.
