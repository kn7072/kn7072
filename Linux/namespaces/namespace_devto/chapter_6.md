[source](https://dev.to/ajinkya_singh_2c02bd40423/container-networking-demystified-a-deep-dive-into-linux-network-namespaces-3gll)

- [ Understanding How Docker and Kubernetes Actually Work Under the Hood](#link_1)
- [ The Apartment Building Analogy](#link_2)
- [ Part 1: Creating Your First Network Namespace](#link_3)
  - [ Exploring Network Isolation](#link_4)
  - [ Bringing the Namespace to Life](#link_5)
- [ Part 2: Connecting Namespaces with Virtual Cables](#link_6)
  - [ Creating a Point-to-Point Connection](#link_7)
  - [ Running Real Services](#link_8)
- [ Part 3: Scaling with Linux Bridges](#link_9)
  - [ Creating a Bridge Network](#link_10)
  - [ Testing Full Mesh Connectivity](#link_11)
- [ Part 4: Internet Connectivity with NAT](#link_12)
  - [ The NAT Configuration](#link_13)
  - [ Understanding NAT Packet Flow](#link_14)
- [ Part 5: Exposing Services with Port Forwarding](#link_15)
  - [ Basic Port Forwarding](#link_16)
  - [ Multiple Services](#link_17)
- [ Part 6: Network Security and Isolation](#link_18)
  - [ Creating Security Zones](#link_19)
  - [ Creating a Secure Database Network](#link_20)
- [ Critical Concept: Why Bridges Matter](#link_21)
  - [ Direct veth vs Bridge](#link_22)
- [ Practical Exercise: Three-Tier Application](#link_23)
- [ Cleanup Script](#link_24)
- [ Key Takeaways](#link_25)

# Linux Container Networking Demystified: A Deep Dive into Linux Network Namespaces

[Conti - Lets's make Container Runtime (8 Part Series)](https://dev.to/ajinkya_singh_2c02bd40423/series/33653)

> **🚀 I'm Building My Own Container Runtime!**
>
> This is part of a complete series where I'm building [**Conti**](https://github.com/a-ZINC/Conti) - a container runtime from scratch. Check it out on GitHub!
>
> **About This Series:**
>
> - I'm sharing everything I learn while building my own container runtime
> - Most concepts come from videos, documentation, and LLM-assisted learning (for educational purposes)
> - Focus: Understanding through practice - raw Linux commands and practical implementation
> - **Important**: When building your own container, DON'T copy code from sources - it kills the fun! Write it yourself, break things, debug, and learn.
>
> **Why Build Your Own?**
>
> - Deep understanding of how containers really work
> - Master low-level Linux concepts
> - Learn by doing, not just reading
> - It's incredibly fun when things finally click!

## Understanding How Docker and Kubernetes Actually Work Under the Hood <a name="link_1"></a>

Have you ever wondered how Docker containers remain isolated yet can communicate with each other and the internet? The answer lies in a powerful Linux kernel feature called **network namespaces**. In this comprehensive guide, we'll unravel the mysteries of container networking by building our own container network from scratch.

---

## The Apartment Building Analogy <a name="link_2"></a>

Think of your Linux host as an apartment building, and network namespaces as individual apartments within that building:

- **Complete Isolation**: Each apartment (namespace) has its own utilities, locks, and living space
- **The Landlord's View**: The building manager (host) can access all apartments
- **Controlled Connectivity**: Apartments can be connected through hallways and shared spaces when needed

This is exactly how containers work—each one gets its own isolated network stack, completely separate from the host and other containers.

---

## Part 1: Creating Your First Network Namespace <a name="link_3"></a>

Let's start by creating an isolated network environment. First, verify you have the required tools:

```
# Check for required utilities
ip --version
iptables --version

# Install if missing (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install -y iproute2 iptables bridge-utils
```

### Exploring Network Isolation <a name="link_4"></a>

```
# View your host's network interfaces
echo "=== Host Network Interfaces ==="
ip link show
# You'll see: lo, eth0, possibly docker0, etc.

# Create your first network namespace
sudo ip netns add production

# List all namespaces
sudo ip netns list

# Check what's inside the namespace
echo "=== Inside the Namespace ==="
sudo ip netns exec production ip link show
# You'll only see 'lo' (loopback) - and it's DOWN!
```

**Key Insight**: The namespace is completely isolated. It has no access to your host's network interfaces, routing tables, or firewall rules.

### Bringing the Namespace to Life <a name="link_5"></a>

```
# Enable the loopback interface
sudo ip netns exec production ip link set lo up

# Test localhost connectivity
sudo ip netns exec production ping -c 2 127.0.0.1
# Success! The namespace can talk to itself

# But try to reach the internet
sudo ip netns exec production ping -c 2 8.8.8.8
# Fails - it's completely isolated
```

---

## Part 2: Connecting Namespaces with Virtual Cables <a name="link_6"></a>

To connect namespaces, we use **veth pairs** (virtual ethernet pairs). Think of them as virtual network cables with two ends.

### Creating a Point-to-Point Connection <a name="link_7"></a>

```
# Create two namespaces
sudo ip netns add frontend
sudo ip netns add backend

# Create a virtual ethernet cable
sudo ip link add veth-front type veth peer name veth-back

# Check the cable ends (both currently on host)
ip link show | grep veth

# Connect each end to a namespace
sudo ip link set veth-front netns frontend
sudo ip link set veth-back netns backend

# The interfaces disappear from host - they're now in namespaces!
ip link show | grep veth  # No results

# Configure the frontend end
sudo ip netns exec frontend ip addr add 10.0.1.10/24 dev veth-front
sudo ip netns exec frontend ip link set veth-front up
sudo ip netns exec frontend ip link set lo up

# Configure the backend end
sudo ip netns exec backend ip addr add 10.0.1.20/24 dev veth-back
sudo ip netns exec backend ip link set veth-back up
sudo ip netns exec backend ip link set lo up

# Test the connection
sudo ip netns exec frontend ping -c 3 10.0.1.20
# Success! They can communicate
```

### Running Real Services <a name="link_8"></a>

```
# Start a web server in the backend namespace
sudo ip netns exec backend python3 -c "
import http.server
import socketserver

with open('/tmp/index.html', 'w') as f:
    f.write('<h1>Hello from Backend!</h1>')

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory='/tmp', **kwargs)

with socketserver.TCPServer(('10.0.1.20', 8080), Handler) as httpd:
    print('Backend serving on 10.0.1.20:8080')
    httpd.serve_forever()
" &

# Access from frontend
sudo ip netns exec frontend curl http://10.0.1.20:8080
# Output: <h1>Hello from Backend!</h1>
```

---

## Part 3: Scaling with Linux Bridges <a name="link_9"></a>

Direct veth connections only work for pairs of namespaces. For multiple containers, we need a **bridge**—essentially a virtual network switch.

### Creating a Bridge Network <a name="link_10"></a>

```
# Create a bridge (virtual switch)
sudo ip link add cloud-bridge type bridge
sudo ip link set cloud-bridge up
sudo ip addr add 172.20.0.1/24 dev cloud-bridge

# Create three application namespaces
for i in 1 2 3; do
    sudo ip netns add app$i

    # Create veth pair
    sudo ip link add veth$i type veth peer name eth$i

    # Attach one end to bridge
    sudo ip link set veth$i master cloud-bridge
    sudo ip link set veth$i up

    # Move other end to namespace
    sudo ip link set eth$i netns app$i

    # Configure namespace interface
    sudo ip netns exec app$i ip addr add 172.20.0.$((i+10))/24 dev eth$i
    sudo ip netns exec app$i ip link set eth$i up
    sudo ip netns exec app$i ip link set lo up

    echo "Configured app$i with IP 172.20.0.$((i+10))"
done
```

### Testing Full Mesh Connectivity <a name="link_11"></a>

```
# Test communication between all applications
echo "=== App1 → App2 ==="
sudo ip netns exec app1 ping -c 2 172.20.0.12

echo "=== App2 → App3 ==="
sudo ip netns exec app2 ping -c 2 172.20.0.13

echo "=== App3 → App1 ==="
sudo ip netns exec app3 ping -c 2 172.20.0.11

# All applications can reach each other through the bridge!
```

---

## Part 4: Internet Connectivity with NAT <a name="link_12"></a>

Now for the crucial part—giving our namespaces access to the external world. This requires three components:

1. **Default Route**: Tell namespace where to send external traffic
2. **IP Forwarding**: Allow host to forward packets
3. **NAT (Network Address Translation)**: Replace private IPs with host's public IP

### The NAT Configuration <a name="link_13"></a>

```
# Add default route in namespace
sudo ip netns exec app1 ip route add default via 172.20.0.1

# Enable IP forwarding on host
sudo sysctl -w net.ipv4.ip_forward=1

# Add NAT rule for masquerading
sudo iptables -t nat -A POSTROUTING -s 172.20.0.0/24 -j MASQUERADE

# Test internet access
sudo ip netns exec app1 ping -c 3 8.8.8.8
# Success! The namespace can reach the internet

# Verify NAT is working
sudo ip netns exec app1 curl -s http://api.ipify.org
# Shows your host's public IP - NAT in action!
```

### Understanding NAT Packet Flow <a name="link_14"></a>

Here's what happens when a namespace accesses the internet:

```
1. Namespace sends packet:
   Source: 172.20.0.11 (private)
   Destination: 8.8.8.8

2. Host receives packet on bridge:
   Routing table: "Forward to eth0"

3. NAT happens in POSTROUTING:
   BEFORE: src=172.20.0.11
   AFTER:  src=<host's public IP>

4. Packet leaves via eth0:
   Now has valid public source IP
   Internet routers accept it

5. Reply returns:
   Connection tracking remembers translation
   Destination NAT: dst=<host IP> → dst=172.20.0.11
   Packet forwarded back to namespace
```

---

## Part 5: Exposing Services with Port Forwarding <a name="link_15"></a>

To make services in namespaces accessible from the outside world, we use port forwarding.

### Basic Port Forwarding <a name="link_16"></a>

```
# Start a web service in app1
sudo ip netns exec app1 python3 -c "
import http.server
import socketserver

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory='/tmp', **kwargs)

with socketserver.TCPServer(('172.20.0.11', 80), Handler) as httpd:
    httpd.serve_forever()
" &

# Forward host port 8080 to namespace port 80
sudo iptables -t nat -A PREROUTING -p tcp --dport 8080 \
    -j DNAT --to-destination 172.20.0.11:80

# Allow the forwarded traffic
sudo iptables -A FORWARD -p tcp -d 172.20.0.11 --dport 80 -j ACCEPT

# Test from host
curl http://localhost:8080
# Works! External clients can access via <host-ip>:8080
```

### Multiple Services <a name="link_17"></a>

```
# Run different services in each namespace
# App1: Port 8081 → 80
# App2: Port 8082 → 80
# App3: Port 3000 → 3000

sudo iptables -t nat -A PREROUTING -p tcp --dport 8081 \
    -j DNAT --to-destination 172.20.0.11:80

sudo iptables -t nat -A PREROUTING -p tcp --dport 8082 \
    -j DNAT --to-destination 172.20.0.12:80

sudo iptables -t nat -A PREROUTING -p tcp --dport 3000 \
    -j DNAT --to-destination 172.20.0.13:3000
```

---

## Part 6: Network Security and Isolation <a name="link_18"></a>

### Creating Security Zones <a name="link_19"></a>

```
# Block communication between specific namespaces
sudo iptables -I FORWARD -s 172.20.0.11 -d 172.20.0.12 -j DROP
sudo iptables -I FORWARD -s 172.20.0.12 -d 172.20.0.11 -j DROP

# Test isolation
sudo ip netns exec app1 ping -c 2 -W 1 172.20.0.12
# Fails - communication blocked

# But app1 can still reach app3
sudo ip netns exec app1 ping -c 2 172.20.0.13
# Works!
```

### Creating a Secure Database Network <a name="link_20"></a>

```
# Create isolated database network
sudo ip link add secure-bridge type bridge
sudo ip addr add 10.10.0.1/24 dev secure-bridge
sudo ip link set secure-bridge up

# Create database namespace
sudo ip netns add database

# Connect to secure bridge
sudo ip link add veth-db type veth peer name eth-db
sudo ip link set veth-db master secure-bridge
sudo ip link set veth-db up
sudo ip link set eth-db netns database
sudo ip netns exec database ip addr add 10.10.0.2/24 dev eth-db
sudo ip netns exec database ip link set eth-db up
sudo ip netns exec database ip link set lo up

# Allow only app1 to access database on port 3306
sudo iptables -A FORWARD -s 172.20.0.11 -d 10.10.0.2 \
    -p tcp --dport 3306 -j ACCEPT
sudo iptables -A FORWARD -d 10.10.0.2 -j DROP

# Database remains isolated from internet (no default route)
# Only app1 can access it on port 3306
```

---

## Critical Concept: Why Bridges Matter <a name="link_21"></a>

### Direct veth vs Bridge <a name="link_22"></a>

**Without Bridge** (Point-to-Point):

- Host has one end of veth pair
- Container has other end
- They can only talk to each other
- Adding more containers requires more veth pairs
- No automatic forwarding between containers

**With Bridge** (Network Switch):

- Bridge acts as virtual switch
- All containers connect to bridge via veth pairs
- Host connects to bridge with single interface
- Bridge handles MAC learning and forwarding automatically
- Scales to unlimited containers

This is why Docker creates the `docker0` bridge—it's the virtual switch connecting all containers!

---

## Practical Exercise: Three-Tier Application <a name="link_23"></a>

Let's build a complete three-tier application network:

```
#!/bin/bash

# Frontend network (DMZ)
sudo ip link add frontend-bridge type bridge
sudo ip addr add 192.168.10.1/24 dev frontend-bridge
sudo ip link set frontend-bridge up

# Backend network (Application tier)
sudo ip link add backend-bridge type bridge
sudo ip addr add 192.168.20.1/24 dev backend-bridge
sudo ip link set backend-bridge up

# Database network (Data tier)
sudo ip link add database-bridge type bridge
sudo ip addr add 192.168.30.1/24 dev database-bridge
sudo ip link set database-bridge up

# Create and connect frontend
sudo ip netns add web-server
sudo ip link add veth-web type veth peer name eth-web
sudo ip link set veth-web master frontend-bridge
sudo ip link set veth-web up
sudo ip link set eth-web netns web-server
sudo ip netns exec web-server ip addr add 192.168.10.10/24 dev eth-web
sudo ip netns exec web-server ip link set eth-web up
sudo ip netns exec web-server ip link set lo up
sudo ip netns exec web-server ip route add default via 192.168.10.1

# Create and connect backend
sudo ip netns add api-server
sudo ip link add veth-api type veth peer name eth-api
sudo ip link set veth-api master backend-bridge
sudo ip link set veth-api up
sudo ip link set eth-api netns api-server
sudo ip netns exec api-server ip addr add 192.168.20.10/24 dev eth-api
sudo ip netns exec api-server ip link set eth-api up
sudo ip netns exec api-server ip link set lo up

# Create and connect database
sudo ip netns add db-server
sudo ip link add veth-db type veth peer name eth-db
sudo ip link set veth-db master database-bridge
sudo ip link set veth-db up
sudo ip link set eth-db netns db-server
sudo ip netns exec db-server ip addr add 192.168.30.10/24 dev eth-db
sudo ip netns exec db-server ip link set eth-db up
sudo ip netns exec db-server ip link set lo up

# Enable routing between tiers
sudo sysctl -w net.ipv4.ip_forward=1

# Frontend can reach backend
sudo iptables -A FORWARD -s 192.168.10.0/24 -d 192.168.20.0/24 -j ACCEPT
sudo iptables -A FORWARD -s 192.168.20.0/24 -d 192.168.10.0/24 -j ACCEPT

# Backend can reach database
sudo iptables -A FORWARD -s 192.168.20.0/24 -d 192.168.30.0/24 -j ACCEPT
sudo iptables -A FORWARD -s 192.168.30.0/24 -d 192.168.20.0/24 -j ACCEPT

# Frontend CANNOT reach database directly
sudo iptables -A FORWARD -s 192.168.10.0/24 -d 192.168.30.0/24 -j DROP

# Only frontend has internet access
sudo iptables -t nat -A POSTROUTING -s 192.168.10.0/24 -j MASQUERADE

# Expose web server to outside world
sudo iptables -t nat -A PREROUTING -p tcp --dport 80 \
    -j DNAT --to-destination 192.168.10.10:80

echo "Three-tier network created successfully!"
```

---

## Cleanup Script <a name="link_24"></a>

```
#!/bin/bash
# cleanup.sh - Remove all test namespaces and bridges

echo "=== Cleaning up namespaces ==="
for ns in $(sudo ip netns list | cut -d' ' -f1); do
    echo "Deleting namespace: $ns"
    sudo ip netns delete $ns
done

echo "=== Cleaning up bridges ==="
for bridge in cloud-bridge frontend-bridge backend-bridge database-bridge secure-bridge; do
    if ip link show $bridge &>/dev/null; then
        echo "Deleting bridge: $bridge"
        sudo ip link delete $bridge
    fi
done

echo "=== Cleaning up iptables rules ==="
sudo iptables -t nat -F
sudo iptables -F FORWARD

echo "=== Cleanup complete! ==="
```

---

## Key Takeaways <a name="link_25"></a>

1. **Network Namespaces** provide complete network isolation—the foundation of container networking
2. **veth Pairs** act as virtual ethernet cables connecting namespaces together
3. **Linux Bridges** work like virtual network switches, enabling scalable multi-container networks
4. **NAT** allows private container IPs to access the internet by masquerading behind the host's public IP
5. **Port Forwarding** exposes containerized services to external networks
6. **iptables** provides powerful firewall capabilities for network security and isolation
7. **This is Docker**: Every concept we explored is exactly how Docker, Kubernetes, and other container platforms work under the hood
