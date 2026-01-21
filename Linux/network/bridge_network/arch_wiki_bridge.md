[source](https://wiki.archlinux.org/title/Network_bridge)
A network bridge is a virtual network device that forwards packets between two or more network segments. A bridge behaves like a virtual network switch and works transparently. Other machines in the network do not need to know about its existence. Physical network devices (e.g. `eth1`) and virtual network devices (e.g. `tap0`) can be connected to it.

## Creating a bridge

There are a number of ways to create a network bridge. This section outlines the steps required to set up a bridge with at least one ethernet interface. This is useful for things like the bridge mode of [QEMU](https://wiki.archlinux.org/title/QEMU "QEMU"), setting a software based access point, etc.

**Warning** If you are creating a bridge on a remote server, and you plan to add the main network interface to the bridge, make sure you first add the main network interface's IP address on the bridge, set the bridge up, and set up a backup default route, **before** adding the interface to the bridge. Otherwise the server will lose network connectivity and you will not be able to SSH back into it.

### With iproute2

This section describes the management of a network bridge using the _ip_ tool from the [iproute2](https://archlinux.org/packages/?name=iproute2) package, which is required by the [base](https://archlinux.org/packages/?name=base) [meta package](https://wiki.archlinux.org/title/Meta_package "Meta package").

Create a new bridge and change its state to up:

```bash
# ip link add name _bridge_name_ type bridge
# ip link set dev _bridge_name_ up
```

To add an interface (e.g. `eth1`) into the bridge, its state must be up:

```bash
# ip link set eth1 up
```

Adding the interface into the bridge is done by setting its master to `_bridge_name_`:

```bash
# ip link set eth1 master _bridge_name_
```

To show the existing bridges and associated interfaces, use the _bridge_ utility (also part of [iproute2](https://archlinux.org/packages/?name=iproute2)). See [bridge(8)](https://man.archlinux.org/man/bridge.8) for details.

```bash
# bridge link
```

This is how to remove an interface from a bridge:

```bash
# ip link set eth1 nomaster
```

The interface will still be up, so you may also want to bring it down:

```bash
# ip link set eth1 down
```

To delete a bridge issue the following command:

```bash
# ip link delete _bridge_name_ type bridge
```

This will automatically remove all interfaces from the bridge. The slave interfaces will still be up, though, so you may also want to bring them down after.

#### Adding the main network interface

If you are doing this on a remote server, and the plan is to add the main network interface (e.g. `eth0`) to the bridge, first take note of the current network status:

```bash
$ ip address show eth0
$ ip route show dev eth0
```

For this example, this is the relevant info:

- IP address attached to `eth0`: `10.2.3.4/8`
- Default gateway: `10.0.0.1`
- Bridge name: `br0`

Initial setup for the bridge:

```bash
# ip link add name br0 type bridge
# ip link set dev br0 up
# ip address add 10.2.3.4/8 dev br0
# ip route append default via 10.0.0.1 dev br0
```

Then, execute these commands in quick succession. It is advisable to put them in a script file and execute the script:

```bash
# ip link set eth0 master br0
# ip address del 10.2.3.4/8 dev eth0
```

Explanation:

- Once `eth0` is added to the bridge, it won't be used for routing anymore. `br0` will take its place, so it needs an IP and have the default route attached.
- We cannot delete the IP address on `eth0` before adding the interface to `br0`, otherwise network connectivity will be lost.
- However, we need to quickly remove the ip address on `eth0`, otherwise network connectivity will be lost after a short period.
- Linux does not allow two default routes on the same routing table. The easy workaround is just to append the new default route.
- Once the IP address of `eth0` is removed, the default route attached to it is automatically removed.

### With bridge-utils

This section describes the management of a network bridge using the legacy _brctl_ tool from the [bridge-utils](https://archlinux.org/packages/?name=bridge-utils) package. See [brctl(8)](https://man.archlinux.org/man/brctl.8) for full listing of options.

**Note** The use of _brctl_ is deprecated and is considered obsolete. See the Notes section in [brctl(8) § NOTES](https://man.archlinux.org/man/brctl.8#NOTES) for details.

Create a new bridge:

```bash
# brctl addbr _bridge_name_
```

Add a device to a bridge, for example `eth1`:

**Note** Adding an interface to a bridge will cause the interface to lose its existing IP address. If you are connected remotely via the interface you intend to add to the bridge, you will lose your connection. This problem can be worked around by scripting the bridge to be created at system startup.

```bash
# brctl addif _bridge_name_ eth1
```

Show current bridges and what interfaces they are connected to:

$ brctl show

Set the bridge device up:

```bash
# ip link set dev _bridge_name_ up
```

Delete a bridge, you need to first set it to _down_:

```bash
# ip link set dev _bridge_name_ down
# brctl delbr _bridge_name_
```

**Note** To enable the [bridge-netfilter](https://ebtables.netfilter.org/documentation/bridge-nf.html) functionality, you need to manually load the `br_netfilter` module:

```bash
# modprobe br_netfilter
```

You can also [load the module at boot](https://wiki.archlinux.org/title/Load_the_module_at_boot "Load the module at boot").

#### Adding the main network interface

First, take note of the current network status:

```bash
$ ip address show eth0
$ ip route show dev eth0
```

For this example, this is the relevant info:

- IP address attached to `eth0`: `10.2.3.4/8`
- Default gateway: `10.0.0.1`
- Bridge name: `br0`

Initial setup for the bridge:

```bash
# brctl addbr br0
# ip address add 10.2.3.4/8 dev br0
# ip link set dev br0 up
```

Then, execute these commands in quick succession. It is advisable to put them in a script file and execute the script:

```bash
# brctl addif br0 eth0
# ip address del 10.2.3.4/8 dev eth0
```

### With netctl

See [Bridge with netctl](https://wiki.archlinux.org/title/Bridge_with_netctl "Bridge with netctl").

### With systemd-networkd

See [systemd-networkd#Bridge interface](https://wiki.archlinux.org/title/Systemd-networkd#Bridge_interface "Systemd-networkd").

### With NetworkManager

[GNOME](https://wiki.archlinux.org/title/GNOME "GNOME")'s Network settings can create bridges, but currently will not auto-connect to them or slave/attached interfaces. Open Network Settings, add a new interface of type Bridge, add a new bridged connection, and select the MAC address of the device to attach to the bridge.

[KDE](https://wiki.archlinux.org/title/KDE "KDE")'s [plasma-nm](https://archlinux.org/packages/?name=plasma-nm) can create bridges. In order to view, create and modify bridge interfaces open the Connections window either by right clicking the Networks applet in the system tray and selecting _Configure Network Connections..._ or from _System Settings > Connections_. Click the _Configuration_ button in the lower left corner of the module and enable "Show virtual connections". A session restart will be necessary to use the enabled functionality.

[nm-connection-editor](https://archlinux.org/packages/?name=nm-connection-editor) can create bridges in the same manner as GNOME's Network settings. [This](https://www.xmodulo.com/configure-linux-bridge-network-manager-ubuntu.html) page shows these steps with screenshots.

_nmcli_ from [networkmanager](https://archlinux.org/packages/?name=networkmanager) can create bridges. For example, to create a bridge `br0` with [STP](https://en.wikipedia.org/wiki/Spanning_Tree_Protocol "wikipedia:Spanning Tree Protocol") disabled (to avoid the bridge being advertised on the network) run:

```bash
$ nmcli connection add type bridge ifname br0 stp no
```

Make your Ethernet interface (`enp30s0` in this example, see [Network configuration#Network interfaces](https://wiki.archlinux.org/title/Network_configuration#Network_interfaces "Network configuration") for instructions on finding out the name) into a slave to the bridge:

```bash
$ nmcli connection add type bridge-slave ifname enp30s0 master br0
```

Bring the existing connection down (you can acquire the connection name with `nmcli connection show --active`):

```bash
$ nmcli connection down _Connection_
```

Bring the new bridge up:

```bash
$ nmcli connection up bridge-br0
$ nmcli connection up bridge-slave-enp30s0
```

If NetworkManager's default interface for the device you added to the bridge connects automatically, you may want to disable that by clicking the gear next to it in Network Settings, and unchecking _Connect automatically_ under _Identity_ or using the command:

```bash
$ nmcli connection modify _Connection_ connection.autoconnect no
```

## Assigning an IP address

**This article or section needs expansion.**

**Reason:** This section needs to be connected to the link-level part described in [QEMU#Tap networking with QEMU](https://wiki.archlinux.org/title/QEMU#Tap_networking_with_QEMU "QEMU"). For now, see the instructions given there. (Discuss in [Talk:Network bridge](https://wiki.archlinux.org/title/Talk:Network_bridge))

When the bridge is fully set up, it can be assigned an IP address:

### With iproute2

```bash
# ip address add dev _bridge_name_ 192.168.66.66/24
```

### With NetworkManager

Give it the desired address:

```bash
# nmcli connection modify _Connection_ ipv4.addresses _desired_IP_
```

Set up a DNS server (this will also avoid not being able to load any pages after you apply the changes):

```bash
# nmcli connection modify _Connection_ ipv4.dns _DNS_server_
```

Set the IP address to static:

```bash
# nmcli connection modify _Connection_ ipv4.method manual
```

Apply the changes:

```bash
# nmcli connection up _Connection_
```

## Tips and tricks

### Wireless interface on a bridge

To add a wireless interface to a bridge, you first have to assign the wireless interface to an access point or start an access point with [hostapd](https://wiki.archlinux.org/title/Software_access_point "Software access point"). Otherwise the wireless interface will not be added to the bridge.

See also [Debian:BridgeNetworkConnections#Bridging with a wireless NIC](https://wiki.debian.org/BridgeNetworkConnections#Bridging_with_a_wireless_NIC "debian:BridgeNetworkConnections").

### Speeding up traffic destinated to the bridge itself

In some situations the bridge not only serves as a bridge box, but also talks to other hosts. Packets that arrive on a bridge port and that are destinated to the bridge box itself will by default enter the iptables INPUT chain with the logical bridge port as input device. These packets will be queued twice by the network code, the first time they are queued after they are received by the network device. The second time after the bridge code examined the destination MAC address and determined it was a locally destinated packet and therefore decided to pass the frame up to the higher protocol stack.[[1]](https://ebtables.netfilter.org/examples/basic.html#ex_speed)

The way to let locally destinated packets be queued only once is by brouting them in the BROUTING chain of the broute table. Suppose br0 has an IP address and that br0's bridge ports do not have an IP address. Using the following rule should make all locally directed traffic be queued only once:

```bash
# ebtables -t broute -A BROUTING -d $MAC_OF_BR0 -p ipv4 -j redirect --redirect-target DROP
```

The replies from the bridge will be sent out through the br0 device (assuming your routing table is correct and sends all traffic through br0), so everything keeps working neatly, without the performance loss caused by the packet being queued twice.

The redirect target is needed because the MAC address of the bridge port is not necessarily equal to the MAC address of the bridge device. The packets destinated to the bridge box will have a destination MAC address equal to that of the bridge br0, so that destination address must be changed to that of the bridge port.

## Troubleshooting

### No networking after bridge configuration

**This article or section needs language, wiki syntax or style improvements. See [Help:Style](https://wiki.archlinux.org/title/Help:Style "Help:Style") for reference.**

**Reason:** This problem is pointed out as a note in [#With bridge-utils](https://wiki.archlinux.org/title/Network_bridge#With_bridge-utils). It should be made clear in all other sections and running a DHCP client should be added to [#Assigning an IP address](https://wiki.archlinux.org/title/Network_bridge#Assigning_an_IP_address). (Discuss in [Talk:Network bridge](https://wiki.archlinux.org/title/Talk:Network_bridge))

It may help to remove all IP addresses and routes from the interface (e.g. `eth1`) that was added to the bridge and configure these parameters for the bridge instead.

First of all, make sure there is no [dhcpcd](https://wiki.archlinux.org/title/Dhcpcd "Dhcpcd") instance running for `eth1`, otherwise the deleted addresses may be reassigned.

Remove address and route from the `eth1` interface:

```bash
# ip addr del _address_ dev eth1
# ip route del _address_ dev eth1
```

Now IP address and route for the earlier configured bridge must be set. This is usually done by starting a DHCP client for this interface. Otherwise, consult [Network configuration](https://wiki.archlinux.org/title/Network_configuration "Network configuration") for manual configuration.

### No networking on hosted servers after bridge configuration

**This article or section needs language, wiki syntax or style improvements. See [Help:Style](https://wiki.archlinux.org/title/Help:Style "Help:Style") for reference.**

**Reason:** "Hosted server" is not a generally obvious term. (Discuss in [Talk:Network bridge](https://wiki.archlinux.org/title/Talk:Network_bridge))

As the MAC address of the bridge is not necessarily equal to the MAC address of the networking card usually used by the server, the server provider might drop traffic coming out from the bridge, resulting in a loss of connectivity when bridging e.g. the server ethernet interface. Configuring the bridge to clone the mac address of the ethernet interface might therefore be needed for hosted servers.

### Cannot connect to bridge connection after connecting to usual connection

In Network Manager applet, if you have usual ethernet/wireless connection (not a bridge slave connection), and if you first connect to it, and then try to connect to bridged connection (with or without disconnecting from usual connection first), then you are not able to connect to it. For some reason, the bridge slave connection (it is not listed in network applet) is not activated, even when the auto connect checkbox is enabled.

The workaround is to activate it manually via terminal:

nmcli connection up br1\ slave\ 1

Then immediately your bridge connections works.

**This article or section needs expansion.**

**Reason:** Is there a bug report for this? (Discuss in [Talk:Network bridge](https://wiki.archlinux.org/title/Talk:Network_bridge))

### Bridge appears to not be working on one side of the network

See [QEMU#Internal networking](https://wiki.archlinux.org/title/QEMU#Internal_networking "QEMU").

## See also

- [Official documentation for iproute2](https://www.linuxfoundation.org/collaborate/workgroups/networking/iproute2)
- [ebtables/iptables interaction on a Linux-based bridge](https://ebtables.netfilter.org/br_fw_ia/br_fw_ia.html)
