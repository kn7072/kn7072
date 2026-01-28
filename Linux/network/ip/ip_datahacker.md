[source](https://datahacker.blog/industry/technology-menu/networking/routes-and-rules/iproute-and-routing-tables#master_routing_table)

- [ iproute and Routing Tables](#link_1)
- [ Routes](#link_2)
  - [ Routing Rules](#link_3)
  - [ The Master Routing Table](#link_4)
- [ Default (Built-in) Routing Tables](#link_5)
- [ Examining Existing Routes](#link_6)
- [ IP Route Syntax](#link_7)
- [ Adding New Routes](#link_8)
- [ Main Routing Table Best Practices](#link_9)
- [ Adding New Routes to Existing Routing Tables](#link_10)
- [ Route Priority Processing](#link_11)
- [ IP Route Command Examples](#link_12)
  - [ Point Destination to Gateway Router](#link_13)
  - [ Set Default Route to Gateway Router](#link_14)
  - [ Point Destination to Next Hop](#link_15)
  - [ Assign Route to an Interface](#link_16)
  - [ Set Default Route to Specific Interface](#link_17)
  - [ Policy Routing (Routing Tables)](#link_18)
  - [ Automatic Fallback/Down Detection and Redirection](#link_19)
- [ Deleting Routes](#link_20)
- [ Creating Additional Routing Tables](#link_21)
- [ How To Create a New Routing Table](#link_22)

## iproute and Routing Tables <a name="link_1"></a>

    Category: Routes, Rules, and Tables
    Published: Friday, 19 July 2019 18:38
    Written by David Guyton

We will begin the detailed discussion of the first component of the Routing Policy DataBase (RPDB) triad: routes (the other two components are ip rules and ip tables).

## Routes <a name="link_2"></a>

Routes are managed by the ip route (iproute2) and route tools. The difference is ip route is current (iproute2) and route (iproute) was deprecated quite some time ago. In spite of this, the latter is still useful for some tasks (particularly read-only lookups), and continues to be relevant in the greater Linux community. Linux routing table entries may be edited via various means, including the route and ip route commands, subject to certain limitations. The ip route command is strongly preferred.

The use of route should be restricted to read-only operations. Its scope is limited to the main route table, making it nearly useless for complex routing configurations. It cannot be used to view or manipulate the other two built-in routing tables: local and default, though they may be viewed with ip route. Both command-line tools are limited to displaying the contents of one routing table at a time, even though iproute2 is capable of handling up to 256 independent routing tables, which are managed by the Master Routing Table. But, before diving into the Master Routing Table and routes, I'll segue into a brief discussion of the 2nd member of the RPDB triad: Routing Rules.

### Routing Rules <a name="link_3"></a>

The RPDB's routing rules are stored in a separate database capable of holding up to 32,768 unique rules that operate in conjunction with the routing tables referenced by the MRT, and their routes. Together, these three components (routes, routing tables, and rules) create a complex, intertwined web of packet routing that is much more robust than virtually any other packet routing design.

Routing rules are the real workhorse and key to the task of manipulating routing outcomes successfully. The numbering and ordering of tables in the Master Routing Table are irrelevant, for they do not control order-of-execution. That privilege belongs to the routing rules, which control what happens when.

Each routing table is self-contained in the context of route evaluation. Rules cannot contain routes, and routes cannot contain rules. You may liken it to a checks-and-balances form of government, where the routes, routing tables, and routing rules are three independent branches that must all work together in order to achieve anything. Routing rules are useless without routes to govern, so for the moment, we will set aside the role of ip rules and come back to it in a later discussion after thoroughly vetting a discussion of routes.

### The Master Routing Table <a name="link_4"></a>

The Master Routing Table (MRT) was introduced when the RPDB concept was launched with iproute2. It is an indirect index of all routing tables on a device and replaced the former single fixed routing table system (iproute) that is customary in traditional routing systems. The beauty of the RPDB system is its modular design that compartmentalizes routing logic tasks into logical groups.

The Master Routing Table is a file. It contains an ordered list of up to 256 integer and name associations. Each line in the file is a combination numeric and named value pair indexed to a specific router table. This is part of Linux' Routing Policy DataBase (RPDB) system. As mentioned previously, the order in which these tables are processed is dependent on the RPDB's routing rules.

The Master Routing Table is always the same filename, and is always found in the same location:

```
/etc/iproute2/rt_tables
```

The file is a simple affair. Take a look at yours.

```
~# cat /etc/iproute2/rt_tables
```

You'll see a list of the routing table numbers and names that looks something like this:

```
#
# reserved values
#
255local
254main
253default
0  unspec
#
# local
#
#1inr.ruhep
```

The master routing table contains the list of all the routing tables on your server. The following tables are included in the table list by default on an unmodified system:

```
local   	Local and broadcast addresses; do not modify or remove
main    	Operated on by route and ip route processes; default when no policy specified
default 	Reserved for post-processing rules
unspec  	Failsafe; do not modify or remove
ruhep 	    Legacy reference; theoretically unnecessary
```

Note the entry, "#1 table inr.ruhep" in the routing table is commented out. This is legacy code and may be ignored or deleted.

The master routing table allows you to utilize the RPDB to its full capacity by associating rules with independent routing tables. However, many people don't realize it exists, because Linux' network routing system runs out-of-the-box with no modifications. How? By default, all network traffic is passed through. If you don't have a need to control, filter, or redirect any network traffic passing through it then you really don't have any reason to modify your server's routing table(s) at all.

## Default (Built-in) Routing Tables <a name="link_5"></a>

There are four built-in route tables in Ubuntu: default, local, main, and unspec. These routes are all special, though how they are named is a bit confusing.
The default table is empty. Contrary to the logic of its name, the default table is not used. You may choose to remove it, though leaving it does no harm.
The local table handles TCP/IP traffic internal to the server (e.g. between internal ports), and includes the loopback adapter and broadcast traffic.
The main table is the primary routing table or what I would call the true 'default' table. Any route or ip route command where the table is not specified will action the main table by default.
The unspec table name is shorthand for "unspecified." It is a set of instructions for the kernel to follow when all other routing paths fail.
Now, try this command for each of the three standard router tables (main, local, and unspec):

```
~# ip route show table {table name}
```

Such as

```
~# ip route show table local
```

Contrary to what one might expect, the number of each table is irrelevant. Their order in the rt_tables file doesn't matter. What is significant are the table names. Each table must have a unique name/number reference within the table file. This file is simply an index. The tables are called by name via rules.

This is one of the few components of packet filtering that does not require restarting the server for changes to take effect. The routing table index can be modified at any time and the changes will take effect immediately. There is no cached version of this file. It is read every time a table is called by a rule.

If the order doesn't matter, why have an ordered list? First, legacy: this format was created a long time ago, and it's essentially just been stuck in Linux since the kernel 2.1/2.2 era when the RPDB concept was created. I suspect the original thought was 256 tables should be sufficient for any need, and I tend to agree that is still true today. Second, it places a soft limit on the amount memory required of table numbers. Each routing table may contain an unlimited number of routes.

## Examining Existing Routes <a name="link_6"></a>

The next step is to figure out how your RPDB is currently branching network traffic. Remember, this process is a combination of routing tables indexed in the master routing table and rules in the routing rules database. Once you understand how to discover your existing network routes, you'll be able to use these techniques to verify route changes in the future.

You may use several different tools in Ubuntu server to identify routes and hosts on your network (LAN), their outbound interface, and the order in which your server prioritizes its network routes. Examine your current routing structure with the ip command set. Run this command and examine the output:

```
~# ip route list
```

On a fresh server, your output should look similar to this:

```
default via 192.168.10.10 dev eth0
192.168.10.0/24 dev eth0  proto kernel  scope link  src 192.168.10.11
```

Or you could use this command:

```
~# ip route show table main
```

And view the same result, which will look something like this:

```
default via 192.168.10.10 dev eth0
192.168.10.0/24 dev eth0  proto kernel  scope link  src 192.168.10.11
```

Why is the output the same?

The default table in ip route is the 'main' table. The first command presumes the default routing table, because a table is not specified. "Default" in the context of the command refers to the routing table called main.

What does this output mean?

The default route is used when a more specific route cannot be found (thus the term 'default'). This is a little different from the question of which routing table is being displayed. You may now begin to see why Linux routing can be so confusing! When viewing the table output, as in the two lines above, the word, "default" means, "If no other route matches the destination IP address more specifically, select this route."

When you're talking about a default routing table, in Linux that normally means the main table. When you're talking about a default selector in a routing rule, to iproute2 that means the route to be used when a more specific route is not identified. Linux prioritizes network traffic route selection based on a longest match model. If a longer route cannot be identified, the kernel will use the route identified as the default route.

Notice in the example above the physical interface is also specified (eth0). A fresh RPDB in Ubuntu is configured such that the default state is to allow all traffic through the server's primary interface to your WAN. In this case the default path is pointing to the upstream router or gateway at 192.168.10.10 on the eth0 interface. This only pertains to outgoing traffic. Remember, default means "use this route if no other route better matches the destination address."

The second line shows a route to a network 192.168.10.0/24 via the eth0 interface. The "scope link" indicates this route is directly linked to the server. In other words, it's a LAN. The "src" is the IPv4 source address assigned to packets leaving this server and proceeding along this route (source NAT). Put another way, this line tells your server there is a local network with a route of 192.168.10.0/24, and when directing outgoing traffic to that network the current server will identify itself with IP address 192.168.10.11.

Though it doesn't provide a wealth of information, this output example identifies the server's connections to the network at a high level. Taken together, those two lines indicate the following facts:

```
    There is a network route 192.168.10.0 - 192.168.10.255 that must be a LAN because this server's source IP address on that route is set to 192.168.10.11;
    Network packets not destined for the LAN will be routed to 192.168.10.10 on the same interface (eth0) and will not have their source IP address modified by the routing rules;
    There must be an upstream gateway or router at 192.168.10.10

```

## IP Route Syntax <a name="link_7"></a>

This is a good opportunity to explain what some of the words mean that you'll see in the ip route list command output.

The following are the relevant Route Types:

```
broadcast 	Packets are sent as link broadcast messages
blackhole 	Packets are discarded and dropped silently
local 	Packets are delivered to the loopback device (local to the server)
prohibit 	Packets are rejected; error returned, "Communication is administratively prohibited"
throw 	Table lookup terminated; packet is dropped; error message returned, "net unreachable"
unicast 	Path to a destination address (this is what most routes are)
unreachable 	Packet is discarded and ICMP error message returned, "host unreachable"
```

These are the most relevant Control Values:

```
dev [name] 	Name of network device to route the packet through (e.g. eth0)
scope [value] 	Scope of area where valid { host|link|global }
proto 	Which process created the route (i.e., is it temporary or permanent)?
```

Scope Values. "Scope" describes where the address is valid.

```
global 	Valid everywhere (globally); default scope if none specified
link Local 	valid only on this device
host 	Only valid inside the current host (server)
```

Proto Values. Also known as "RTPROTO" or "route protocol." It identifies the process that created the associated route.

```
boot 	Added after boot; temporary
static 	Override added by sysadmin
kernel 	Added by kernel (this is normally what you want to see)
```

As you can see, one can group several of these into a category of "drop the packet" (namely blackhole, prohibit, throw, and unreachable). Dropping and rejecting packets may also be accomplished via iptables. The unicast (forward packet to address such-and-such), local (send to localhost), and broadcast actions instruct the kernel where to send the current packet.

## Adding New Routes <a name="link_8"></a>

So, you've decided you want to add a new route. Perhaps you want to setup a VPN tunnel or add a new network interface to your server and you need to tell it how to use the new interface. Adding a new route boils down to instructing your server how to direct traffic from or to a specific IP address or range of addresses. You either want to create a route the server doesn't understand or see right now, or add a new one that changes how your server currently directs traffic.

Regardless of why you want to add a new route, the process is the same. Just remember routes affect both inbound and outbound network traffic.

There are three options when adding a new route:

```
    Add a route to the default routing table (main)
    Add a route to another existing table
    Create a new route table and add at least one new rules that points to it
```

To add a new route, the ip route command argument structure is:

```
ip route add [type] [prefix] via [next hop] dev [interface name] table [table name/ID] src [source IP]
```

Prefix means the destination IP address, including netmask (if present). If type is omitted, unicast is presumed. Nearly all routes are unicast. For other types, refer to the charts above for information. Next hop is the gateway or upstream router the packet will be sent to.

If prefix is set to default it is the same as assigning an IPv4 address of 0/0 or 0.0.0.0/0 or 0.0.0.0/0.0.0.0.

The formatting boils down to the identification of the destination IP address or range, whether the route is direct or via a gateway, network device, and it may contain other values depending on whether or not the route points to a gateway, host, or a group of IP addresses (e.g. a LAN branch). The preceding sections (especially Examining Existing Routes) have more detailed explanations on the syntax.

Here's an example of how to add a new route to a route table called custom. The new route directs all traffic not routed by a more specific route to a gateway router at 192.168.1.100 via the eth1 network interface.

```
ip route add default via 192.168.1.100 dev eth1 table custom
```

If you translated this to English, it would read something like this,

"Add a new route to the table named custom that by default routes all traffic to a router at ipv4 address over device eth1."

You can verify the results of your handiwork with this command:

```
ip route show table custom
```

Even though your new routes are now created, they won't be honored by the server until the ip rule and route caches are flushed.

```
ip route flush cache
```

**All RPDB rules are loaded into the kernel’s memory when the server starts up. If you make changes to ip rules or ip routes and wish to utilize them prior to the next system reboot, you must flush their cache. This forces the kernel to reload the respective databases.**

## Main Routing Table Best Practices <a name="link_9"></a>

Here are some brief concepts for you to keep in mind when adding new routing tables to your master routing table file.

```
    Ensure table name and number are both unique!
    Do not modify default values in the file
    New table references should be numbered between 100 and 200
    Remember the "default" table is actually named main
```

Adding New Routes to the Default (main) Routing Table (main)

To simply create a new route in the default routing table, you just need to insert a new route in the main table. This is accomplished via ip route.

First, take a look at the current state of your main routing table. Remember, your table labeled main is the actual default routing table.

```
ip route show
```

or

```
ip route show table main
```

or

```
route -n
```

If you ever see a route with a non-zero metric value, it is a priority value. Metric is an arbitrary 32-bit number that delineates route preferences. Smaller values denote higher priority. Zero is the highest priority metric. 65535 is the lowest.

Now, follow the instructions below to create new routes in the main table. To add a new route to the default main table, simply omit the table <table ID> portion of each command line.

## Adding New Routes to Existing Routing Tables <a name="link_10"></a>

Adding a new route to an existing table that is not the main table is a simple process. Routing tables have a very basic command structure. The possible routing types are described above in the routing type chart shown above under IP Route Syntax.

For the purpose of this discussion I'm going to focus only on the unicast route type. This narrows down the route configurations to the most common scenarios when the server is not a router. Thus, the command format to add a new route becomes:

```
ip route add {[destination ip/mask] [default]} {via [ip/mask]} {dev} [device] {table} [table ID] src [source ip]

```

## Route Priority Processing <a name="link_11"></a>

How does netfilter determine which route to choose from a routing table? What happens if a packet matches more than one route in the table?

Complex routing tables in large networks can contain hundreds of route entries. When the RPDB is ready to scan a route table and attempt to match a packet to one of the routes in that table, how does it decide which route to apply?

Recall that at this juncture, the RPDB has been directed to the current table by a rule. Routes are compared with the current packet based on the route's prefix and ToS value (if any). The prefix is a pair of values equal to the destination IP address and its netmask. The RPDB compares the current packet to each route in the table. The most specific match will be chosen, in this order:

```
    Destination IP address of the packet matches the prefix, up to the length of the prefix
    ToS bits of packet and route match
    The route's ToS=0 (regardless of packet ToS value)
```

If more than one route matches the packet, the list is pruned in the following order until only a single route remains:

```
    Longest matching (most specific) destination IP address including netmask
    If a single route ToS and the packet ToS bits match, use that route
    Routes where ToS=0
    If no ToS=0 routes exist, fail on error (unreachable)
    If multiple ToS=0 routes still exist, select route with best preference value
    As a last resort, select the first route in chronological order
```

## IP Route Command Examples <a name="link_12"></a>

Here are some examples demonstrating how to structure the command line of common scenarios.

### Point Destination to Gateway Router <a name="link_13"></a>

These instructions direct the packet with indicated destination IP address to the indicated gateway router. Destination IP address may be single address or sub-net. CIDR (netmask) is optional.

```
ip route add [destination address/mask] via [gateway IP]
ip route add n.n.n.n/n.n.n.n via n.n.n.n/n.n.n.n
ip route add n.n.n.n/nn via n.n.n.n/nn
```

### Set Default Route to Gateway Router <a name="link_14"></a>

These instructions assign the default route to the indicated gateway router or next hop.

```
ip route add default via [gateway IP]
ip route add default via [next hop router IP]
ip route add default via n.n.n.n/n.n.n.n
ip route add default via n.n.n.n/nn

```

### Point Destination to Next Hop <a name="link_15"></a>

Destination IP address may be single address or sub-net; CIDR (netmask) optional. These instructions direct the packet with indicated destination IP address to the indicated router that is the next hop.

```
ip route add [destination address/mask] via [next hop IP]
ip route add n.n.n.n/n.n.n.n via n.n.n.n/n.n.n.n
ip route add n.n.n.n/nn via n.n.n.n/nn
```

### Assign Route to an Interface <a name="link_16"></a>

Add a new route tied to a specific interface.

```
ip route add [destination address/mask] dev [interface name]
ip route add default dev [interface name]
ip route add n.n.n.n dev [interface name]
ip route add n.n.n.n/nn dev [interface name]
ip route add n.n.n.n/n.n.n.n dev [interface name]
```

### Set Default Route to Specific Interface <a name="link_17"></a>

Change the device associated with the default route.

```
ip route add default dev [interface name]
```

### Policy Routing (Routing Tables) <a name="link_18"></a>

When applied to the RPDB policy routing model, the syntax is the same with the exception of the table specification. Simply append "table table ID" to the end of the command line. Table ID may be either the name or number of the table in the rt_tables file. Here are a few syntax examples:

```
ip route add default via [next hop] table [table ID]
ip route add default dev [interface name] table [table ID]
```

Set default route in table vpn as tun0 interface:

```
ip route add default dev tun0 table vpn
```

Set default route in table test to the gateway router (default) at IPv4 address 192.168.1.1:

```
ip route add default via 192.168.1.1 table test
```

### Automatic Fallback/Down Detection and Redirection <a name="link_19"></a>

This scenario involves two gateways and how to establish one of them as a priority path while using the other as a fallback. An example would be if your endpoint was attached to two independent internet service providers on the same network interface. How does new outgoing traffic get routed over one versus the other? There are multiple ways to decide. One method involves the use of UP and DOWN route commands in your server's network configuration.

Here is an example of setting up your router table using that method and branches network traffic to one of two new router tables if the destination port matches.

Create a new table in /etc/ip route2/rt_tables
Name the new tables vpn1 and vpn2.

```
    echo 1 vpn1 >> /etc/ip route2/rt_tables
    echo 2 vpn2 >> /etc/ip route2/rt_tables
```

Create new routes that point to the new tables.
For the table vpn1:

```
    ip route add default dev tun0 table vpn1
```

For the table vpn2:

```
    ip route add default dev tun1 table vpn2
```

Create filter rules. Add rules to the mangle table (iptables) and the set-mark action to map specific port destinations to a particular routing table. The example below branches traffic for destination ports 22 or 80. Notice a different mark value is used depending on which table the traffic should be redirected to.

```
    iptables -A PREROUTING -t mangle -i eth0 -p tcp --dport 22 -j MARK --set-mark 1
    iptables -A PREROUTING -t mangle -i eth0 -p tcp --dport 80 -j MARK --set-mark 2
```

Add new ip rules to funnel marked traffic to the new route tables.

```
    ip rule add from all fwmark 1 table vpn1
    ip rule add from all fwmark 2 table vpn2
```

## Deleting Routes <a name="link_20"></a>

Deleting routes is the reverse of creating them. You must provide sufficiently specific information that the ip route command is able to isolate a single matching rule for deletion.

```
ip route delete {full route statement you wish to delete}
```

The full route instruction may be required, particularly if your table contains many routes.
Don't forget to flush.

```
ip route flush cache
```

## Creating Additional Routing Tables <a name="link_21"></a>

New routing tables in the RPDB are created by simply adding a line to the file rt_tables
All that is required is an index value and table name. Each table must have a unique index value and unique name. Beyond that, the chronological order in the table doesn't matter. See The Master Routing Table for more information.

Adding a new route table is straightforward, but do you truly need to? If you're just adding a few new routes, it may make more sense to simply use the existing main table. Ask yourself: should I be adding a new routing table, or simply adding a new route? If you just want to add a new route, the main routing table can be utilized. However, if you are considering marking packets (fwmark) or creating a conditional branch such as a split VPN, a separate table can be very useful.

When you create a new routing table, you must also create a minimum of one corresponding rule that points to it, and you need to design the routes in the table to handle any possible outcomes. Three steps are required:

```
    Add new entry to master routing table
    Populate new routing table
    Create at least one rule that points to the new table
```

Best Practices When Adding New Routing Tables

Here are some best practices to consider when creating new routing tables. Remember, you will be modifying the master routing table. If you decide to make your changes persistent, make sure they are working properly first or you may make your server inaccessible if something goes wrong.

```
    Ensure the table name and number are both unique!
    Do not modify default values in the file
    New table references should be numbered between 100 and 200 (this allows you the ability to adjust route priorities in the future)
    Use only lowercase characters for your table name
    Do not use consecutive table numbers or bunch them together; leave some room between them to make future updates easier to implement
```

**Sometimes, creating your own routing tables is a good idea. The main table is unique and has special features. Care needs to be taken not to disrupt it. An advantage to creating your own routing tables is you're much less likely to accidentally create a problem you can't easily fix. Regardless,
always test your routes thoroughly before making them persistent.**

## How To Create a New Routing Table <a name="link_22"></a>

Adding a new routing table to a Linux server is a 3-step process.
**Step 1**. Manually edit the master routing table

You have two possible methods of completing this step.
**1a. Method #1**. Open the master routing table file for editing.

```
nano /etc/iproute2/rt_tables
```

Here's how your new table might look:

```
#
# reserved values
#
255     local
254     main
253     default
#
# vpn table
#
200     stealth
#0       unspec
```

Choose an available value for your new table. It must be between 1 and 252 and not in use by any other table. Next, choose an alphanumeric name with no spaces. As an example, let's use 200 for the table number and "stealth" as its name.

The order of your tables in the master routing table doesn't matter; rules control the flow. These entries in the master routing table just tell the kernel where to find the route information.

**Do not allow any empty lines in the master routing table file.**

Remember, the order in which the indexes (table numbers) are presented in the master routing table doesn't matter; though the corresponding table numbers do. Route tables are processed in chronological order, beginning with number 0.
**1b. Method #2**. Use the command line to inject a new line at the end of the master routing table.

```
echo 100 custom >> /etc/iproute2/rt_tables
```

This command will place the new table entry at the end of the file with the name, "custom" and an index or table ID of 100. The order of the router table entries in the file is irrelevant. What is important is the routing table instructions are evaluated in order of the index of the routing tables. Table number zero (0) has the higest priority. Its routes are evaluated first, before all others.

**Avoid duplicate table names or index numbers. Table numbers 0, 253, 254, and 255 are reserved. Do not use them.**

**Step 2**. Populate your new table with one or more routes.

Now, we still have a problem, which is the fact the custom router table you just created is empty. Take a look at the syntax of your existing tables. Routing tables have a very basic command structure.
Here's an outline of how the routes are structured in a table (routing syntax):

```
[destination ip] | {via [ipv4]} | dev {device} | {proto [kernel or static]} | {scope [scope type]} | {src [ipv4]}
```

The formatting primarily boils down to the identification of the destination IP address or range, whether the route is direct or via a gateway, and the network device the packet will be sent out on. Recall these are outgoing routes only. Each route may contain other values depending on whether or not the route points to a gateway, host, or a group of IP addresses (e.g. a LAN branch). The preceding sections (especially Examining Existing Routes) have more detailed explanations on the syntax.

Here's an example of how to add a new route to your route table. The table will have just one route, which directs all traffic to a gateway router at 192.168.1.100 via the eth1 network interface.

```
ip route add default via 192.168.1.100 dev eth1 table custom
```

If you translated this to English, it would read something like this,
"Add a new route to the table named custom that routes all traffic to a gateway at ipv4 address 192.168.1.100 over device eth1."
You can verify the results of your handiwork with this command:

```
ip route show table custom
```

**Step 3**. Create at least one rule that points to your new table.

Routing rules are stored in the RPDB and created via the ip rule command.

This is arguably the most important part of this process. Even though this particular discussion is regarding routes, rules have a great impact on which routes a packet is capable of traversing. And therefore, you need to be cognizant of how new rules you create will behave in the context of other routing rules and other routing tables in the RPDB. Remember, the kernel won't pay any attention to your fancy new route table and its routes unless you have rules instructing it to do so.

Details of routing rules (ip rules) are discussed in their own section, but for the moment you should be clear on the most important factors when creating a new routing rule:

```
    Rules are processed in priority order with 0 (zero) as the highest priority
    Longest matching rule wins a tie
    If more than one rule is matching and lengths are identical, the higher priority rule wins
```
