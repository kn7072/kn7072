[source](https://linux-kvm.org/page/Networking)

# Networking

Jump to:[navigation](https://linux-kvm.org/page/Networking#mw-navigation), [search](https://linux-kvm.org/page/Networking#p-search)

## Contents

1. [User Networking](#link_1)
2. [Private Virtual Bridge](#link_2)
3. [Public Bridge](#link_3)
4. [Routing with iptables](#link_4)
5. [VDE](#link_5)
6. [Performance](#link_6)
7. [Compatibility](#link_7)

Guest (VM) networking in kvm is the same as in qemu, so it is possible to refer to other documentation about networking in qemu. This page will try to explain how to configure the most frequent types of networking needed.

## User Networking <a name="link_1"></a>

**Use case:**

- You want a simple way for your virtual machine to access to the host, to the internet or to resources available on your local network.
- You don't need to access your guest from the network or from another guest.
- You are ready to take a huge performance hit.
- Warning: User networking does not support a number of networking features like ICMP. Certain applications (like ping) may not function properly.

**Prerequisites:**

- You need kvm up and running
- If you don't want to run as root, then the user needs to have rw access to /dev/kvm
- In order for the guest to be able to access the internet or a local network, the host system must be able to access these resources as well

**Solution:**

- Simply run your guest without specifying network parameters, which by default will create user-level (a.k.a slirp) networking:

```bash
qemu-system-x86_64 -hda /path/to/hda.img
```

**Notes:**

- The IP address can be automatically assigned to the guest thanks to the DHCP service integrated in QEMU
- If you run multiple guests on the host, you don't need to specify a different MAC address for each guest
- The default is equivalent to this explicit setup:

```bash
qemu-system-x86_64 -hda /path/to/hda.img -netdev user,id=user.0 -device e1000,netdev=user.0
```

- The user.0 identifier above is just to connect the two halves into one. You may use any identifier you wish, such as "n" or "net0".
- Use rtl8139 instead of e1000 to get an rtl8139-based network interface.
- You can still access one specific port on the guest using the "hostfwd" option. This means e.g. if you want to transport a file with scp from host to guest, start the guest with **"-device e1000,netdev=user.0 -netdev user,id=user.0,hostfwd=tcp::5555-:22"**. Now you are forwarding the host port 5555 to the guest port 22. After starting up the guest, you can transport a file with e.g. "scp -P 5555 file.txt root@localhost:/tmp" from host to guest. Or you can also use the other address of the host to connect to.

## Private Virtual Bridge <a name="link_2"></a>

**Use case:**

- You want to set up a private network between 2 or more virtual machines. This network won't be seen from the other virtual machines nor from the real network.

**Prerequisites:**

- You need kvm up and running
- If you don't want to run as root, then the user needs to have rw access to /dev/kvm
- The following commands must be installed on the host system and executed as root:

```bash
ip
brctl (deprecated). Use ip link instead
tunctl (deprecated). Use ip tuntap and ip link instead
```

**Solution:**

- You need to create a bridge, e-g:

```bash
    # ip link add br0 type bridge ; ifconfig br0 up
    # brctl addbr br0 (deprecated)
```

- You need a qemu-ifup script containing the following (run as root):

```bash
    #!/bin/sh
set -x

switch=br0

if [ -n "$1" ];then
        # tunctl -u `whoami` -t $1 (use ip tuntap instead!)
        ip tuntap add $1 mode tap user `whoami`
        ip link set $1 up
        sleep 0.5s
        # brctl addif $switch $1 (use ip link instead!)
        ip link set $1 master $switch
        exit 0
else
        echo "Error: no interface specified"
        exit 1
fi
```

- Generate a MAC address, either manually or using:

```bash
    #!/bin/bash
    # generate a random mac address for the qemu nic
    printf -v macaddress 'DE:AD:BE:EF:%02X:%02X\n' $((RANDOM%256)) $((RANDOM%256))
```

- Run each guest with the following, replacing $macaddress with the value from the previous step

```bash
qemu-system-x86_64 -hda /path/to/hda.img -device e1000,netdev=net0,mac=$macaddress -netdev tap,id=net0
```

**Notes:**

- If you don't want to run qemu-ifup as root, then consider using sudo
- You can either create a system-wide qemu-ifup in /etc/qemu-ifup or use another one. In the latter case, run

```bash
qemu-system-x86_64 -hda /path/to/hda.img -device e1000,netdev=net0,mac=$macaddress -netdev tap,id=net0,script=/path/to/qemu-ifup
```

- Each guest on the private virtual network must have a different MAC address

## Public Bridge <a name="link_3"></a>

**WARNING:** The method shown here will not work with all wireless drivers as they might not support bridging.

**Use case:**

- You want to assign IP addresses to your virtual machines and make them accessible from your local network
- You also want performance out of your virtual machine

**Prerequisites:**

- You need kvm up and running
- If you don't want to run kvm as root, then the user must have rw access to /dev/kvm
- The following commands must be installed on the host system and executed as root:

```bash
ip
brctl (deprecated, use ip link instead)
tunctl (deprecated, use ip tuntap instead)
```

- Your host system must be able to access the internet or the local network

**Solution 1: Using Distribution-Specific Scripts**

| RedHat                                                                                                                                                                                                                                               | Debian                                                                                                                                                                                                                                          | SuSE                                                                                                                         |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| - Edit /etc/sysconfig/network-scripts/ifcfg-eth0<br> - comment out BOOTPROTO<br> - Add BRIDGE=br0<br>- Create /etc/sysconfig/network-scripts/ifcfg-br0<br> - The content should be:<br><br>DEVICE=br0<br>BOOTPROTO=dhcp<br>ONBOOT=yes<br>TYPE=Bridge | /etc/network/interfaces<br><br># Replace old eth0 config with br0<br>auto eth0 br0<br><br># Use old eth0 config for br0, plus bridge stuff<br>iface br0 inet dhcp<br> bridge_ports eth0<br> bridge_stp off<br> bridge_maxwait 0<br> bridge_fd 0 | - Start YaST<br>- Go to Network Configuration<br>- Add new device -> Bridge<br>- Tick your existing network device<br>- done |

- /etc/init.d/networking restart
- The bridge br0 should get the IP address (either static/dhcp) while the physical eth0 is left without an IP address.

**VLANs**

Please note that the rtl8139 virtual network interface driver does not support VLANs. If you want to use VLANs with your virtual machine, you must use another virtual network interface like virtio.

When using VLANs on a setup like this and no traffic is getting through to your guest(s), you might want to do:

```bash
    # cd /proc/sys/net/bridge
    # ls
    bridge-nf-call-arptables  bridge-nf-call-iptables
    bridge-nf-call-ip6tables  bridge-nf-filter-vlan-tagged
    # for f in bridge-nf-*; do echo 0 > $f; done
```

**Solution 2: Manual Configuration**

- You need to create a bridge, e-g:

```bash
    # ip link add br0 type bridge
    # brctl addbr br0 (deprecated, use ip link instead!)
```

- Add one of your physical interface to the bridge, e-g for eth0:

```bash
    # ip link set eth0 master br0
    # brctl addif br0 eth0 (deprecated, use ip link instead!)
```

- You need a qemu-ifup script containing the following (run as root):

```bash
    #!/bin/sh
set -x

switch=br0

if [ -n "$1" ];then
        #tunctl -u `whoami` -t $1
        ip tuntap add $1 mode tap user `whoami`
        ip link set $1 up
        sleep 0.5s
        #brctl addif $switch $1
        ip link set $1 master $switch
        exit 0
else
        echo "Error: no interface specified"
        exit 1
fi
```

- Generate a MAC address, either manually or using:

```bash
    #!/bin/sh
    # generate a random mac address for the qemu nic
printf -v macaddress 'DE:AD:BE:EF:%02X:%02X\n' $((RANDOM%256)) $((RANDOM%256))
```

- Run each guest with the following, replacing $macaddress with the value from the previous step

```bash
qemu-system-x86_64 -hda /path/to/hda.img -device e1000,netdev=net0,mac=$macaddress -netdev tap,id=net0
```

**Notes:**

- If you don't want to run qemu-ifup as root, then consider using sudo
- Each guest on the network must have a different MAC address
- You can either create a system-wide qemu-ifup in /etc/qemu-ifup or use another one. In the latter case, run

```bash
qemu-system-x86_64 -hda /path/to/hda.img -device e1000,netdev=net0,mac=$macaddress -netdev tap,id=net0,script=/path/to/qemu-ifup
```

## Routing with iptables <a name="link_4"></a>

With this method, you can connect your guest vm to a tap device in your host. Then you can set iptables rules in your host so that it acts as a router and firewall for your guest.

Routing is done simply by setting the default route on the client to the IP address of the host, allowing IP forwarding, and setting a route to the tap device of the client on the host.

- Host-side: Allow IPv4 forwarding and add a route to the guest (could be put in a script, but the route has to be added after the guest has started):

```bash
sysctl -w net.ipv4.ip_forward=1                 # allow forwarding of IPv4
route add -host <ip-of-client> dev <tap-device> # add route to the client
```

- Guest-side: Set the default gateway to the IP address of the host (make sure the host and guest IP addresses are in the same subnet):

```bash
route add default gw <ip-of-host>
```

- Note: If the host is not on the same subnet as the guest, then you must manually add the route to the host before you create the default route:

```bash
route add -host <ip-of-host> dev <network-interface>
route add default gw <ip-of-host>
```

## VDE <a name="link_5"></a>

Another option is using VDE (Virtual Distributed Ethernet).

More information will be provided later.

## Performance <a name="link_6"></a>

Data on benchmarking results should go in here. There's now a page dedicated to ideas for improving [Networking Performance](https://linux-kvm.org/page/Networking_Performance "Networking Performance").

Some 10G NIC performance comparisons between VFIO passthrough and virtio are discussed in [VFIO vs virtio](https://linux-kvm.org/page/VFIO_vs_virtio "VFIO vs virtio").

## Compatibility <a name="link_7"></a>

There's another, old and obsolete syntax of specifying network for virtual machines. Above examples uses -netdev..-device model, old way used -net..-net pairs. For example,

```
-netdev tap,id=net0 -device e1000,netdev=net0,mac=52:54:00:12:34:56
```

is about the same as old

```
-net tap,vlan=0 -net nic,vlan=0,model=e1000,macaddr=52:54:00:12:34:56
```

(note mac => macaddr parameter change as well; vlan=0 is the default).

Old way used the notion of "VLANs" - these are QEMU VLANS, which has nothing to do with 802.1q VLANs. Qemu VLANs are numbered starting with 0, and it's possible to connect one or more devices (either host side, like -net tap, or guest side, like -net nic) to each VLAN, and, in particular, it's possible to connect more than 2 devices to a VLAN. Each device in a VLAN gets all traffic received by every device in it. This model was very confusing for the user (especially when a guest has more than one NIC).

In new model, each host side correspond to just one guest side, forming a pair of devices based on -netdev id= and -device netdev= parameters. It is less confusing, it is faster (because it's always 1:1 pair), and it supports more parameters than old -net..-net way.

However, -net..-net is still supported, used widely, and mentioned in lots of various HOWTOs and guides around the world. It is also a bit shorter and so faster to type.
