[source](https://blogs.cisco.com/developer/container-images-2?ccid=&dtid=devblog&oid=crippa-containerimage3-ww)

- [ Understanding Container Images, Part 2: Optimizing Your Images](#link_1)
  - [ Hello world app – Take 2](#link_2)
  - [ The builder pattern](#link_3)
  - [ Simplyfing the build process](#link_4)

# Understanding Container Images, Part 2: Optimizing Your Images <a name="link_1"></a>

[Francisco Sedano Crippa](https://blogs.cisco.com/author/franciscosedanocrippa "Posts by Francisco Sedano Crippa")

In the first post of this series we discussed [how container images are built](https://blogs.cisco.com/developer/container-image-layers-1). We talked about layers, reusing them, and how to make your Dockerfiles build faster.

We also started to build a container containing our shiny ‘Hello World’ C application.

## Hello world app – Take 2 <a name="link_2"></a>

What is the ultimate goal of our container? In this case, we want to be able to build our application in an automated and consistent way, and then use it in our environment.

The first Dockerfile we wrote to build our Hello world app is:

```
FROM ubuntu:18.04
RUN apt-get update
RUN apt-get install -y build-essential
WORKDIR /app
COPY app/hello.c /app/
RUN gcc -o hello hello.c
ENTRYPOINT [ "/app/hello" ]
```

After building it, you can notice the size of the final container:

```
$ docker build -t stage0 .
```

```
$ docker image ls
REPOSITORY   TAG       IMAGE ID       CREATED         SIZE
stage0       latest    87a0e7eb81da   4 minutes ago   319MB
ubuntu       18.04     2c047404e52d   7 weeks ago     63.3MB
$
```

319 Mb (a delta of 255 Mb over the ubuntu image) for a minimal hello world C app. Not exactly optimal. Additionally, if we jump into the container, we can see all our source code, compilation artifacts, etc. Not something you want to include in your shipping product.

## The builder pattern <a name="link_3"></a>

![](./optimizing_images_images/b9f945a45b4c5ab4bc35e49e3feacb87_MD5.jpg)

One of the problems with this approach is we’re doing two very different things with our container: we’re using it to build a product, and we’re using the same one to ship it. Not optimal.

One common approach to solve this problem is to use two dockerfiles; one for building and one for shipping the product. During build, you can extract the built application to a local directory, and copy the files to the shipping container. This is called “**the builder pattern**“.

Please read on, but **don’t apply this … yet**. There are better ways!

The first dockerfile is almost identical to our first approach, except for the last line where ENTRYPOINT is defined:

**Dockerfile.build**:

```
FROM ubuntu:18.04
RUN apt-get update
RUN apt-get install -y build-essential
WORKDIR /app
COPY app/hello.c /app/
RUN gcc -o hello hello.c
```

You can now build this container and, after it’s completed, extract the application from it. To build it, you need to specify the filename you want to use as your Dockerfile – Dockerfile.build on this example. Also, we’re adding a name to the built image (build_step).

```
$ docker build . -f Dockerfile.build -t build_step
```

```
$ docker image ls
REPOSITORY   TAG       IMAGE ID       CREATED            SIZE
build_step   latest    f0e92c66ae80   About a minute ago 308MB
ubuntu       18.04     c090eaba6b94   10 hours ago       63.3MB
$
```

Now you need to create a container from this image, extract the compiled application, and copy it to your filesystem:

```
$ docker create --name extract build_step
```

```
$ docker ps -a
CONTAINER ID    IMAGE      COMMAND        CREATED          STATUS    PORTS    NAMES
f22b7931ece6    build_step "/bin/bash"    6 seconds ago    Created            extract
```

```
$ mkdir built-app
```

```
$ docker cp extract:/app/hello built-app/
```

And finally you have your compiled application:

```
$ ls -l built-app
total 24
-rwxr-xr-x 1 fsedanoc staff 8304 Jan 21 15:03 hello
$
```

Now you can build a simple Dockerfile to create the minimal environment to run your app:

**Dockerfile**

```
FROM ubuntu:18.04
WORKDIR /app
COPY built-app/hello /app/
ENTRYPOINT ["/app/hello"]
```

```
$ docker run ship_step
Hello from the container!
$
```

If you look at the size of the images, the shippable one is much smaller – Actually it’s just the base image plus our final application:

```
$ docker image ls
REPOSITORY   TAG       IMAGE ID       CREATED         SIZE
ship_step    latest    25cebe417392   5 minutes ago   63.3MB
build_step   latest    f0e92c66ae80   19 minutes ago  308MB
ubuntu       18.04     c090eaba6b94   11 hours ago    63.3MB
$
```

## Simplyfing the build process <a name="link_4"></a>

![](./optimizing_images_images/627601b523ec94c0bda6c15ff00917a4_MD5.jpg)

While the ‘Builder pattern’ works, keeping two separate Dockerfiles, plus scripts to extract the application from one to the host directory, etc, can become difficult to manage. There’s a better way!

**Multi-stage docke\*\***rfiles!\*\*

If you read the [documentation](https://docs.docker.com/engine/reference/builder/) for the Dockerfile, you can see the COPY file accepts an extra parameter:

**--from**

Per the documentation:

Optionally `COPY` accepts a flag `--from=<name>` that can be used to set the source location to a previous build stage (created with `FROM .. AS <name>`) that will be used instead of a build context sent by the user

This flag allows you to compress the two steps in the Builder pattern in a single Dockerfile:

```
FROM ubuntu:18.04 as build_step
RUN apt-get update
RUN apt-get install -y build-essential
WORKDIR /app
COPY app/hello.c /app/
RUN gcc -o hello hello.c

FROM ubuntu:18.04
WORKDIR /app
COPY --from=build_step /app/hello /app
ENTRYPOINT [ "/app/hello" ]
```

```
$ docker build -t multistep .
```

After the build, you can see the final image, with the correct size, and as lean as it can be. You’re ready to push your final image to the repository and use it to run your app!

```
$ docker image ls
REPOSITORY   TAG       IMAGE ID       CREATED         SIZE
multistep    latest    31ddecae27b8   9 minutes ago   63.3MB
<none>       <none>    c301e0bb00e0   9 minutes ago   308MB
ubuntu       18.04     c090eaba6b94   11 hours ago    63.3MB
```

```
$ docker run multistep
Hello from the container!
$
```

Multi step builds are a great tool that will improve the quality of your containers. A smaller container means faster pushes and pulls, and that’s crucial in a CI/CD/CD environment
