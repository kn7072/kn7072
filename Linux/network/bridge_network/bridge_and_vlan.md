[source](https://www.baeldung.com/linux/vlan-bridged-interfaces)

- [ 1. Overview](#link_1)
- [ 2. Terminologies](#link_2)
- [ 2.1. Bridge](#link_3)
- [ 2.2. Virtual Local Area Network (VLAN)](#link_4)
- [ 2.3. TAP](#link_5)
- [ 3. Bridged Interfaces](#link_6)
- [ 3.1. Linux Bridging](#link_7)
- [ 3.2. Configuration Using the _ip_ Command](#link_8)
- [ 3.3. Persist Configuration Using Netplan](#link_9)
- [ 4. VLAN Tagging](#link_10)
- [ 4.1. VLAN in Linux](#link_11)
- [ 4.2. Configuring VLAN Interface Using the _ip_ Command](#link_12)
- [ 4.3. Persist Configuration Using Netplan](#link_13)
- [ 5. VLAN and Bridges](#link_14)
- [ 6. Configuring TAP](#link_15)
- [ 6.1. Install Toolset](#link_16)
- [ 6.2. TAP Interface Creation](#link_17)
- [ 6.3. TAP Bridging](#link_18)
- [ 7. Conclusion](#link_19)

# Using Bridged Interfaces and VLAN

## 1. Overview <a name="link_1"></a>

Networking plays a crucial role in modern computing. Understanding how to use advanced technologies like bridged interfaces and VLAN (Virtual Local Area Network) in Linux can significantly enhance networking capabilities. Further, depending on network needs, these components enable us to create flexible, secure, and scalable virtual and physical networking setups.

In this tutorial, we’ll explore these technologies and look into their configurations.

## 2. Terminologies <a name="link_2"></a>

[Bridge](https://www.baeldung.com/linux/bridging-network-interfaces), VLAN, and TAP are networking concepts in Linux used to manage and manipulate network traffic.

### 2.1. Bridge <a name="link_3"></a>

**A bridge is a software-based device in Linux that connects multiple network interfaces, enabling them to function as if they are on the same physical network**. It operates at the data link layer (Layer 2) of the OSI model, forwarding traffic based on MAC addresses. A bridge is commonly used in virtualized environments, where multiple virtual machines (VMs) need to communicate with each other or the host machine.

### 2.2. Virtual Local Area Network (VLAN) <a name="link_4"></a>

A [VLAN](https://www.baeldung.com/cs/vlan-intro) logically segments a network into separate broadcast domains, even if the devices are connected to the same physical network. VLANs operate at Layer 2 and use 802.1Q tagging to add a VLAN tag to Ethernet frames, enabling switches and routers to identify and handle traffic from different VLANs.

### 2.3. TAP <a name="link_5"></a>

[TAP](https://www.baeldung.com/linux/create-check-network-interfaces#2-tap-network-interface) interface is a virtual network interface in Linux that operates at the Ethernet layer (Layer 2). It’s software that emulates a physical network card.

## 3. Bridged Interfaces <a name="link_6"></a>

A bridge interface functions like a network switch. It forwards traffic between connected interfaces based on MAC addresses. Bridged interfaces are useful in virtual machines and containers where we need to connect virtualized environments to physical networks.

### 3.1. Linux Bridging <a name="link_7"></a>

**The Linux kernel provides native support for bridging through the _bridge-utils_ package**. This package provides tools to create, manage, and delete bridge interfaces. Linux bridges use BPDU (Bridge Protocol Data Units) to avoid network loops. A network loop occurs when multiple paths exist between network devices, causing data packets to circulate endlessly. Due to this, packets can overwhelm the network with broadcast storms, which degrade performance, and lead to outages.

Specifically, a network bridge mitigates loops using the [Spanning Tree Protocol (STP)](https://www.baeldung.com/cs/rstp-stp-protocols). STP identifies redundant paths and places certain links into a blocking state to prevent loops. This ensures only one active path exists. If the primary path fails, STP reconfigures the network to activate a backup link. By dynamically managing redundancy, network bridges maintain robust connectivity while avoiding disruptive loops, enabling efficient and reliable network operations.

Further, a bridge interface also utilizes the Netlink API which facilitates communication between user-space tools (like _brctl_, _iproute2,_ or _nmcli_) and the bridge kernel module. User-space tools use Netlink to configure the bridge, set up ports, enable or disable STP, and monitor bridge state changes. The kernel module enforces these configurations, dynamically managing bridge interfaces and ensuring loop-free and efficient network operations.

### 3.2. Configuration Using the _ip_ Command <a name="link_8"></a>

Now, let’s look at how to configure a bridged interface.

To begin with, let’s ensure the required tools are installed:

```bash
$ sudo apt update && sudo apt install bridge-utils
```

Next, **we create a bridge interface named _sec0_**:

```bash
$ sudo ip link add name sec0 type bridge
```

Let’s add one physical interface (_enp0s3_) to the bridge:

```bash
$ sudo ip link set enp0s3 master sec0
```

Subsequently, we assign an IP address to the bridge interface. **We can give it the same IP assigned as the _enp0s3_ interface or assign a different IP**:

```bash
$ sudo ip addr add 192.168.2.116/24 dev sec0
$ sudo ip link set dev sec0 up
```

Following, we need to update the default route and then flush the _enp0s3_ interface to remove its current IP address:

```bash
$ sudo ip route append default via 192.168.2.1 dev sec0
$ sudo ip addr del 192.168.2.116/24 dev enp0s3
```

Once we perform the above configuration, let’s verify the results via the _ip_ command:

```bash
$ ip a
2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel master sec0 state UP group default qlen 1000
    link/ether 08:00:27:0b:af:50 brd ff:ff:ff:ff:ff:ff
    inet6 fe80::1a5c:65bf:5561:e8c5/64 scope link noprefixroute
       valid_lft forever preferred_lft forever
3: sec0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
    link/ether 0e:3b:e2:ad:86:3e brd ff:ff:ff:ff:ff:ff
    inet 192.168.2.116/24 scope global sec0
       valid_lft forever preferred_lft forever
    inet6 fe80::c3b:e2ff:fead:863e/64 scope link
       valid_lft forever preferred_lft forever
```

From the snippet above, we can see there are two interfaces: the physical interface _enp0s3,_ and the _bridge_ interface _sec0_. The physical interface is a slave of the bridge. The bridge interface is assigned an IP address for routing traffic.

### 3.3. Persist Configuration Using Netplan <a name="link_9"></a>

The above configuration isn’t persistent and is usually lost once we reboot the computer. To preserve the setup, we can use [Netplan](https://www.baeldung.com/linux/netplan-bridge-two-interfaces).

Let’s edit the network configuration _/etc/netplan/01-network-manager-all.yaml_ file to add lasting configurations by enabling NetworkManager to manage all interfaces:

```bash
$ cat /etc/netplan/01-network-manager-all.yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    enp0s3:
      dhcp4: no

  bridges:
    sec0:
      dhcp4: yes
      interfaces:
        - enp0s3
```

Finally, we apply the changes via _netplan_:

```bash
$ sudo netplan apply
```

Thus, we should have the bridge even after a reboot.

## 4. VLAN Tagging <a name="link_10"></a>

VLANs enable the segmentation of a physical network into multiple logical networks.

### 4.1. VLAN in Linux <a name="link_11"></a>

In Linux, we implement VLANs using the 802.1Q standard, which tags Ethernet frames to distinguish between different VLANs. **This feature enables network interfaces to process tagged packets, isolating and segmenting traffic into virtual networks on a single physical interface**. The _vconfig_ or _ip_ command creates VLAN sub-interfaces, assigning unique VLAN IDs to each. Linux kernel supports VLAN ensuring proper tagging and untagging of packets for communication across VLANs.

Specifically, **VLAN tagging adds a 4-byte header (per IEEE 802.1Q) to Ethernet frames**, identifying the VLAN ID for traffic segregation. Switches and routers use this tag to route packets within specific VLANs. Tagging enables multiple VLANs to share a single physical link.

Additionally, VLAN-aware tools and bridges enable advanced configurations, like inter-VLAN routing and integration with physical network switches.

### 4.2. Configuring VLAN Interface Using the _ip_ Command <a name="link_12"></a>

Now, let’s move on to VLAN configuration.

To begin with, we load the VLAN kernel module:

```bash
$ sudo modprobe 8021q
```

Now, let’s verify it’s loaded:

```bash
$ lsmod | grep 8021q
8021q                  45056  0
garp                   20480  1 8021q
mrp                    20480  1 8021q
```

Furthermore, we can ensure the [module is automatically loaded on boot](https://www.baeldung.com/linux/kernel-module-load-boot):

Next, let’s create a VLAN interface with a VLAN ID of _10_:

```bash
$ sudo ip link add link enp0s3 name vlan10 type vlan id 10
```

Most importantly, we should note that **the above command creates a VLAN subinterface on a physical network interface to tag traffic with a specific VLAN ID**.

Let’s assign an IP address to the VLAN interface:

```bash
$ sudo ip addr add 192.168.150.2/24 dev vlan10
$ sudo ip link set dev vlan10 up
```

Following, we check the configuration using the _ip_ command:

```bash
$ ip a
2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel master sec0 state UP group default qlen 1000
    link/ether 08:00:27:0b:af:50 brd ff:ff:ff:ff:ff:ff
    inet6 fe80::1a5c:65bf:5561:e8c5/64 scope link noprefixroute
       valid_lft forever preferred_lft forever
3: sec0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
    link/ether 0e:3b:e2:ad:86:3e brd ff:ff:ff:ff:ff:ff
    inet 192.168.2.116/24 scope global sec0
       valid_lft forever preferred_lft forever
    inet6 fe80::c3b:e2ff:fead:863e/64 scope link
       valid_lft forever preferred_lft forever
4: vlan10@enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
    link/ether 08:00:27:0b:af:50 brd ff:ff:ff:ff:ff:ff
    inet 192.168.2.150/24 scope global vlan10
       valid_lft forever preferred_lft forever
    inet6 fe80::a00:27ff:fe0b:af50/64 scope link
       valid_lft forever preferred_lft forever
```

From the above snippet, we can see that the VLAN subinterface is up and it has an IP of _192.168.2.150_.

### 4.3. Persist Configuration Using Netplan <a name="link_13"></a>

Similarly, for persistence,  let’s update the Netplan network configuration file:

```bash
$ sudo vi /etc/netplan/01-network-manager-all.yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    enp0s3:
      dhcp4: no
      addresses:
        - 192.168.2.40/24
      routes:
        - to: default
          via: 192.168.2.1
      nameservers:
          addresses: [8.8.8.8, 8.8.4.4]

  vlans:
    vlan10:
      id: 10
      link: enp0s3
      addresses: [192.168.2.20/24]
```

Again we, apply the following changes:

```bash
$ sudo netplan apply
```

This way, the VLAN settings remain after a reboot.

## 5. VLAN and Bridges <a name="link_14"></a>

Of course, bridge and VLAN configurations can be combined.

So, let’s add the VLAN interface to the _bridge_:

```bash
$ sudo ip link set vlan10 master sec0
```

Now that we added _vlan10_ to the bridge, let’s list the bridge interfaces on the system:

```bash
$ bridge link
2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 master sec0 state forwarding priority 32 cost 5
4: vlan10@enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 master sec0 state forwarding priority 32 cost 5
```

The _sudo ip link set vlan10 master sec0_ adds the VLAN interface (_vlan10_) as a slave of the bridge, allowing VLAN traffic to pass through the bridge. This means VLAN is handled externally. Conversely, we can configure VLAN rules to be handled within the bridge. To achieve this we need to enable VLAN filtering on the bridge.

**VLAN filtering is a feature that enables a network bridge (such as a switch or Linux bridge) to filter traffic based on VLAN tags**. It ensures that the bridge only forwards frames belonging to certain VLANs, dropping traffic for unspecified VLANs, and providing network segregation and security.

As mentioned earlier, we use VLAN tags to identify which VLAN a frame belongs to. These tags are added to Ethernet frames (using IEEE 802.1Q) to ensure they are associated with a specific VLAN. Comparatively, when we enabled VLAN filtering on the bridge, the bridge is aware of VLAN tags. It can make forwarding decisions based not only on the MAC address but also on the VLAN tag (identifier).

For instance, to enable VLAN filtering on a bridge, we use _ip_:

```bash
$ sudo ip link set dev sec0 type bridge vlan_filtering 1
```

Assuming the bridge _sec0_ connects multiple network segments, this way we only want it to pass traffic from specific VLANs. **Once we enable VLAN filtering, the bridge ensures that only frames tagged with that specific VLAN are forwarded**, and all others are discarded.

## 6. Configuring TAP <a name="link_15"></a>

We commonly use TAP interfaces in virtualization ([KVM](https://www.baeldung.com/linux/kernel-based-virtual-machine), [Qemu](https://www.baeldung.com/linux/qemu-from-terminal)), VPNs, and container networking to handle Ethernet frames, enable network bridging, or facilitate communication between virtual and physical networks.

So, let’s configure the TAP interface.

### 6.1. Install Toolset <a name="link_16"></a>

First, we ensure all the required packages are installed.

To configure TAP, we need either _tunctl_ or _iproute2_. We use _tunctl_ (currently deprecated) for older systems, but we can install it via the _uml-utilities_ package:

```bash
$ sudo apt-get install uml-utilities
```

Otherwise, we use _iproute2_ which is installed by default in most Linux distros. Thus, we should have access to the TAP subcommands in *ip*.

### 6.2. TAP Interface Creation <a name="link_17"></a>

Next, let’s run the respective _ip_ commands to create a TAP interface:

```bash
$ sudo ip tuntap add dev tap0 mode tap
```

Optionally, we can assign an IP address to the TAP interface:

```bash
$ sudo ip addr add 192.168.2.120/24 dev tap0
```

At this point, we should have _tap0_ available as a TAP interface.

### 6.3. TAP Bridging <a name="link_18"></a>

Next, we add the TAP interface to the _sec0_ bridge:

```bash
$ sudo ip link set tap0 master sec0
```

Lastly, let’s bring up the interface:

```bash
$ sudo ip link set dev tap0 up
```

We often pair TAP with TUN interfaces for IP-level tunneling. TAP interfaces pass raw Ethernet frames, making them suitable for bridging and VLAN configurations.

## 7. Conclusion <a name="link_19"></a>

In this article, we looked at bridges, VLANs, and TAP interfaces. These networking features enable us to manipulate the network to achieve different outcomes. Bridges provide the framework to interconnect interfaces, VLANs segment the traffic, and TAP interfaces enable virtualized networking within the system. Together, they form the backbone of virtual and isolated networking setups in Linux.

Lastly, to access the internet we need to configure DNS properly and ensure we’ve set up packet forwarding for devices behind the bridge.
