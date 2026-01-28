[source](https://www.golinuxcloud.com/ip-route-command-in-linux/)

- [ Introduction](#link_1)
- [ Syntax and Supported Options](#link_2)
- [ Differences Between `ip route` and Other Commands (`route`, `netstat`)](#link_3)
- [ Understanding the Routing Table Output](#link_4)
- [ Managing routes with ip route command](#link_5)
  - [ 1. Adding Routes](#link_6)
  - [ 2. Deleting Routes](#link_7)
  - [ 3. Modifying Routes](#link_8)
  - [ 4. Special Routes](#link_9)
  - [ 5. Using Metrics and Priorities](#link_10)
  - [ 6. Multihomed Network Configuration](#link_11)
- [ Understanding Advanced Routing Options](#link_12)
- [ Troubleshooting with the `ip route command`](#link_13)
- [ Conclusion](#link_14)
- [ Further Reading Resources](#link_15)

## Introduction <a name="link_1"></a>

`ip route` command in Linux used to manage the IP routing table of the operating system. This table determines how packets are forwarded and routed through the various interfaces on a system. By manipulating the routing table, you can dictate how data is transmitted, to which interface, and on what path.

Here's a basic breakdown of what `ip route` does:

- **View Routing Table**: By simply using `ip route show` or `ip route list`, you can view the entire routing table. This will show you all routes, their associated next-hop gateways, and the interfaces they use.
- **Add Routes**: You can add new routes, determining where packets with a particular destination IP should be sent.
- **Delete Routes**: Routes that are no longer valid or needed can be removed from the routing table.
- **Modify Routes**: Existing routes can be changed to adjust for network changes.
- **Special Routes**: `ip route` allows you to set specific kinds of routes like "blackhole" (where packets are discarded) or "prohibit" (where packets are denied and an error is sent to the sender).

The command is part of the IPROUTE2 utility suite in Linux, a set of programs that replaces older tools like `route` and provides much more functionality, especially in modern network configurations.

## Syntax and Supported Options <a name="link_2"></a>

Here is a basic syntax to use `ip route` command:

bash

```bash
ip route { add | del | change | append | replace | show | flush } SELECTOR ROUTE-OPTIONS
```

**Commands**:

- `add`: Used to add a new route.
- `del`: Deletes a specific route.
- `change`: Modifies an existing route.
- `append`: Appends a new path to an existing route.
- `replace`: Replaces an existing route.
- `show`: Displays routes (can be filtered).
- `flush`: Removes routes as per the given criteria.

**SELECTOR**:

- This determines which routes to display or modify. For example, you can select all routes (`all`), or specific ones based on address type (like `unicast`, `local`, `broadcast`, etc.).

**ROUTE-OPTIONS**:

- This is where you define the specifics of the route, such as the destination, gateway, device, metric, etc.

**Commonly Used Parameters**:

- `dst PREFIX`: The destination prefix of the route. For example, `192.168.1.0/24`.
- `via ADDRESS`: The next hop IP address. In other words, it's the IP address of the next device (usually a router) that the packet should be sent to.
- `dev NAME`: The name of the outgoing network interface to use, like `eth0` or `wlan0`.
- `src ADDRESS`: The source IP address to use when sending packets.
- `metric NUMBER`: This sets the route metric, which is a value that helps determine the priority of a route. Lower values have higher priority.
- `table TABLE_ID`: This specifies the routing table ID to use. It's used for advanced routing.
- `proto PROTOCOL`: The routing protocol identifier. This can be values like `boot` (for routes set during boot), `static` (for manually added routes), or other dynamic routing protocols.
- `scope SCOPE_VAL`: The scope of the routes. It can be values like `host`, `link`, `global`, etc.
- `realm REALM`: Routing realms are used for policy routing. This is an advanced feature.

## Differences Between `ip route` and Other Commands (`route`, `netstat`) <a name="link_3"></a>

While the `ip route command` is a staple in modern networking on Linux systems, older utilities like `route` and `netstat` once held its place. Here's how they differ:

1. **Unified vs. Fragmented Approach**:
   - The `ip route command` is part of the IPROUTE2 suite, offering a unified approach to networking tasks. It's a one-stop solution where you can manage routes, addresses, and links, among others.
   - In contrast, older commands are fragmented. While `route` specifically deals with routes, `netstat` focuses on network connections, routing tables, interface statistics, and more.
2. **Feature Set**:
   - The `ip route command` provides a more extensive set of features, allowing for advanced routing options, including policy routing, multipath routing, and more.
   - Older commands like `route` have a limited set, often missing out on the newer kernel's routing features.
3. **Output and Syntax**:
   - `ip route` offers a more structured and consistent output, making it easier for parsing, especially in scripts.
   - The older utilities, especially `netstat`, tend to have verbose outputs, which can be harder to decipher and utilize in automated tasks.
4. **Deprecation**:
   - As Linux systems evolve, tools like `route` and `netstat` are being marked as deprecated in favor of the `ip route command` and its counterparts. This means they might not be available or maintained in future Linux distributions.

## Understanding the Routing Table Output <a name="link_4"></a>

- **Destination**: Specifies the network or subnet being targeted, such as `192.168.1.0/24`.
- **Gateway**: Shows the device's IP address if data needs forwarding before reaching its destination, often a router's IP.
- **Genmask**: An older term essentially denoting the Subnet Mask, defining the IP address range of a network.
- **Flags**: Quick insights into the route's status, with common flags like `U` for an active route and `G` indicating use of a gateway.
- **MSS**: Represents the maximum [packet size before fragmentation](https://www.golinuxcloud.com/packet-fragmentation-wireshark/ "Troubleshoot Packet Fragmentation Issues with Wireshark") becomes necessary.
- **Window**: A value occasionally displayed for controlling network congestion.
- **IRTT**: Stands for Initial Round Trip Time, offering an estimated time for packet round trips.
- **Interface**: Reveals which network interface the rule is associated with, such as `eth0` or `wlan0`.
- **Default Routes**: Pathways the system takes to communicate with unknown networks, typically appearing as `default via 192.168.0.1 dev eth0`.
- **Connected Routes**: Routes to networks directly linked to your device via specific interfaces.
- **Static Routes**: Manually set pathways pointing to distinct networks.

## Managing routes with ip route command <a name="link_5"></a>

### 1. Adding Routes <a name="link_6"></a>

To ensure that data packets find their correct path in a network, the `ip route command` offers ways to specify routing instructions. This is vital when there are multiple paths in a network or when redirecting traffic through specific routes.

```bash
# Adding a Default Route:
# This sets the default gateway to ensure that any unspecified traffic gets directed to a particular path.
ip route add default via 192.168.1.1

# Adding a Route to a Specific Subnet:
# Directs traffic for a specific subnet through a defined route.
ip route add 192.168.2.0/24 via 192.168.1.2

# Adding a Route via a Specific Gateway:
# Routes traffic to a particular network via a specific gateway.
ip route add 192.168.3.0/24 via 192.168.1.3 dev eth1
```

### 2. Deleting Routes <a name="link_7"></a>

Over time, certain routes may become obsolete or there might be a need to reset the routing table. The `ip route command` enables such modifications, ensuring that the routing tables remain current and efficient.

```bash
# Removing a Specific Route:
# Deletes a specific route, preventing traffic from being directed along that path.
ip route del 192.168.2.0/24 via 192.168.1.2

# Flushing or Clearing All Routes:
# This is an advanced operation that clears all routes, essentially resetting the routing table. Caution is advised when using this command.
ip route flush table main
```

### 3. Modifying Routes <a name="link_8"></a>

Routing decisions often need adjustments due to changing network requirements. The `ip route command` provides the capability to modify existing routes, ensuring the efficient flow of data packets.

```bash
# Changing the Gateway for a Specific Route:
# This alters the gateway for a specified route.
ip route change 192.168.2.0/24 via 192.168.1.4

# Modifying Metric Values:
# Metrics influence routing decisions. By adjusting metric values, you can influence the preference of one route over another.
ip route add 192.168.2.0/24 via 192.168.1.2 metric 5
```

### 4. Special Routes <a name="link_9"></a>

Special routes are a set of routes that don't follow the usual pattern of forwarding traffic to a destination based on the best possible match. Instead, they define specific behaviors or treatments for the packets that match these routes. These are incredibly useful for advanced networking scenarios, security, or specific types of traffic treatment.

- **Blackhole Routes:** When traffic is sent to a blackhole route, it is silently discarded without any error message to the sender. It’s like sending packets into a black hole where they disappear. It can be used to prevent unwanted traffic from consuming resources on the host or network.
- **Unreachable Routes:** Any traffic matching an unreachable route results in the host sending an ICMP destination unreachable message back to the sender. It is used to indicate that a specific destination is not reachable, ensuring that sending hosts are quickly informed rather than waiting for a timeout.
- **Prohibit Routes:** Similar to unreachable routes, but instead of a destination unreachable message, the host sends back an ICMP prohibited message. This can be useful for indicating that a route is administratively prohibited, perhaps due to security policies.

The `ip route command` facilitates the management of these special routes, enhancing the versatility of network configurations.

```bash
# Blackhole Routes:
# Traffic directed to a blackhole route is silently discarded. Useful in preventing unwanted traffic.
ip route add blackhole 192.168.4.0/24

# Unreachable Routes:
# This informs the system that certain destinations are not reachable, generating an error message in response to attempted access.
ip route add unreachable 192.168.5.0/24

# Prohibit Routes:
# This prevents traffic to specified routes, issuing an error when such traffic is detected.
ip route add prohibit 192.168.6.0/24
```

### 5. Using Metrics and Priorities <a name="link_10"></a>

In networking, especially when dealing with multiple routes and gateways, it becomes vital to distinguish which routes should be prioritized over others. That's where metrics and priorities come into play. They allow for fine-tuned control over route selection. The `ip route command` empowers administrators to set and tweak these values, optimizing network efficiency.

**Understanding Route Metrics**

Metrics are numerical values associated with specific routes. They help in distinguishing which routes are more preferable when there are multiple paths to a destination. A lower metric value is generally preferred over a higher one. It's a way to dictate which path a packet should take when multiple paths are available to the same destination.

```bash
ip route add 192.168.80.0/24 via 10.0.0.1 metric 10
ip route add 192.168.80.0/24 via 10.0.0.2 metric 20
```

In the scenario above, traffic heading to the 192.168.80.0/24 subnet will prefer the gateway 10.0.0.1 over 10.0.0.2 due to the lower metric value.

**Setting and Modifying Route Metrics**

Sometimes, based on network conditions or administrative decisions, there might be a need to change the metric of an existing route to alter its preference.

The `ip route command` can both establish new metric values and modify existing ones. This flexibility allows for dynamic adjustments based on network conditions or administrative preferences.

```bash
# Adding a route with a metric
ip route add 192.168.90.0/24 via 10.0.0.3 metric 5

# Modifying the metric of the existing route
ip route change 192.168.90.0/24 via 10.0.0.3 metric 15
```

The above commands first set a route with a metric of 5 and then modify it to have a metric of 15.

### 6. Multihomed Network Configuration <a name="link_11"></a>

Multihoming, or the practice of connecting a host to the internet via multiple ISPs, ensures enhanced reliability and redundancy. With the `ip route command`, configuring and managing routes in a multihomed environment becomes a straightforward process.

Multihoming refers to the scenario where a device (like a computer or router) is connected to more than one network. This can be for redundancy, load balancing, or other purposes. If one internet connection fails, the other(s) can take over, ensuring uninterrupted connectivity.

**Configuring and Managing Multiple Routes in a Multihomed Setup:** In a multihomed scenario, the `ip route command` is instrumental in setting up multiple routes, each corresponding to a different ISP or connection.

```bash
# Adding a route for the first ISP:
ip route add default via 192.168.0.1 metric 10

# Adding a route for the second ISP:
ip route add default via 192.168.1.1 metric 20
```

In this example, if the connection through 192.168.0.1 fails, the system will automatically route traffic through 192.168.1.1, given its slightly higher metric value.

## Understanding Advanced Routing Options <a name="link_12"></a>

The `ip route command` is not limited to just basic routing operations; it is versatile enough to handle advanced routing concepts that cater to specific network scenarios and requirements.

**Equal-cost multi-path (ECMP) Routing:** ECMP is a routing strategy where packet forwarding to a single destination can occur over multiple best paths with equal cost. This aids in load balancing and redundancy.

```bash
# Adding two ECMP routes to the same destination:
ip route add 10.0.0.0/24 via 192.168.0.1
ip route add 10.0.0.0/24 via 192.168.0.2
```

In the example above, traffic to 10.0.0.0/24 will be balanced between two paths, via 192.168.0.1 and 192.168.0.2.

**Policy-based Routing with `ip route`:** This allows administrators to route packets based on defined policies, not just by destination IP. It can consider other packet attributes, such as source IP or port.

```bash
# Create a routing table named 'custom':
echo "100 custom" >> /etc/iproute2/rt_tables

# Add a rule that uses the custom table for packets from a specific source:
ip rule add from 192.168.1.100 table custom

# Define the route in the custom table:
ip route add default via 192.168.0.1 table custom
```

In this setup, traffic from 192.168.1.100 would use the route defined in the 'custom' table.

## Troubleshooting with the `ip route command` <a name="link_13"></a>

Routing issues can range from minor hiccups to major network outages. Using the `ip route command`, one can efficiently identify and address these problems.

These can include missing routes, incorrect gateway settings, or wrong metric values.

**Using `ip route` to Identify and Resolve Issues:**

```bash
# Display the routing table to check for anomalies:
ip route show

# If a required route is missing:
ip route add 192.168.2.0/24 via 192.168.0.1

# If a route's gateway is incorrect:
ip route change 192.168.2.0/24 via 192.168.0.2
```

## Conclusion <a name="link_14"></a>

Having delved deep into the versatile and powerful `ip route command`, it's evident that this tool is indispensable for network administrators and enthusiasts. From basic operations like viewing and modifying routes to advanced features such as policy-based routing and troubleshooting, the `ip route command` is a comprehensive solution for routing tasks.

**Key Takeaways:**

- The `ip route command` offers a more extensive set of functionalities compared to its older counterparts.
- Beyond simple route additions or deletions, it provides advanced options like ECMP, policy-based routing, and specific route types like blackhole or unreachable routes.
- Troubleshooting network issues becomes significantly streamlined with the insights and controls the command offers.

## Further Reading Resources <a name="link_15"></a>

- [Linux Advanced Routing & Traffic Control HOWTO](https://lartc.org/)
- [Man Page for ip-route](http://man7.org/linux/man-pages/man8/ip-route.8.html)
- [Linux Network Administrators Guide](https://tldp.org/LDP/nag2/index.html)
