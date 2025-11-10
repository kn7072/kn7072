# Install the Latest Version tof Nmap From Source on Linux Mint

## How to install the latest version of Nmap from source code on Linux ( Mint )

1. First create a directory in the /opt directory.

```bash
cd /opt
sudo mkdir /opt/nmap
```

2. Next change to the /tmp directory and download the source via Github [here](https://github.com/nmap/nmap.git).

```bash
cd /tmp
git clone https://github.com/nmap/nmap.git
```

3. Now cd to the /tmp/nmap directory and run the configure script. Note: If the **configure** script fails try removing the **--with-localdirs** flag. Depends on how your libs are installed if you need it or not.

```bash
cd /tmp/nmap ./configure --with-localdirs
```

If configure is successful you should end up with something that looks like the following:
```bash
.       .            \`-"'"-'/              } 6 6 {            ==. Y ,==              /^^^\  .             /     \  )  Ncat: A modern interpretation of classic Netcat            (  )-(  )/            -""---""---   /           /   Ncat    \_/          (     ____           \_.=|____E Configuration complete.           :================:         /||# nmap -A _   ||        / ||              ||       |  ||              ||        \ ||              ||          ==================   ........... /      \.............   :\        ############            \   : ---------------------------------   : |  *   |__________|| ::::::::::  |   \ |      |          ||   .......   |     --------------------------------- 8   NMAP IS A POWERFUL TOOL -- USE CAREFULLY AND RESPONSIBLY Configured with: ndiff zenmap nping openssl zlib libssh2 lua ncat Configured without: localdirs Type make (or gmake on some *BSD machines) to compile.
```

4. Now run **make**.

```bash
make
```

5. Next copy the compiled nmap binary to the /opt/nmap directory.

```bash
sudo cp nmap /opt/nmap/
```


1. Now run **make install**.

```bash
sudo make install
```

6. Confirm your new nmap binary is installed and executable.

```bash
nmap --version
Nmap version 7.93SVN ( https://nmap.org ) Platform: x86_64-unknown-linux-gnu Compiled with: liblua-5.3.3 openssl-1.1.1f nmap-libssh2-1.10.0 libz-1.2.11 libpcre-8.39 libpcap-1.9.1 nmap-libdnet-1.12 ipv6 Compiled without: Available nsock engines: epoll poll select
```
```bash
nmap -p 22 localhost

Starting Nmap 7.93SVN ( https://nmap.org ) at 2022-09-15 09:38 EDT Nmap scan report for localhost (127.0.0.1) Host is up (0.00011s latency). PORT   STATE  SERVICE 22/tcp closed ssh Nmap done: 1 IP address (1 host up) scanned in 0.12 seconds
```
## What next?

If you're not that familar using nmap check out a previous post on [my list of most useful nmap scans and one-liners](https://nfosec.co/posts/most-useful-nmap-scans-and-one-liners/).