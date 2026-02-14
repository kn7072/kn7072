[source](https://dev.to/ajinkya_singh_2c02bd40423/mount-namespace-practice-guide-4c84)

- [ Network Namespaces](#link_1)
  - [ What are Network Namespaces?](#link_2)
  - [ Three Key Network Resources](#link_3)
  - [ Visual Architecture](#link_4)
  - [ Practical Commands](#link_5)
  - [ Use Cases for Network Namespaces](#link_6)
- [ UTS Namespaces](#link_7)
  - [ What are UTS Namespaces?](#link_8)
  - [ Visual Concept](#link_9)
  - [ Practical Implementation](#link_10)
  - [ Benefits of UTS Namespaces](#link_11)
- [ IPC Namespaces](#link_12)
  - [ What are IPC Namespaces?](#link_13)
  - [ IPC Resources Isolation](#link_14)
  - [ Practical Commands](#link_15)
- [ Commands Reference](#link_16)
  - [ Essential Commands Summary](#link_17)
  - [ Common Namespace Creation Patterns](#link_18)
- [ Summary](#link_19)
  - [ Key Takeaways](#link_20)
  - [ Namespace Interaction Diagram](#link_21)
  - [ Real-World Applications](#link_22)

# Linux Namespaces: Network, UTS, and IPC

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

## Network Namespaces <a name="link_1"></a>

### What are Network Namespaces? <a name="link_2"></a>

Network namespaces provide isolation of network resources, giving each application its own networking stack.

### Three Key Network Resources <a name="link_3"></a>

**1. Network Devices**

- Ethernet interfaces (eth0, eth1)
- Loopback device (lo)
- Virtual interfaces

**2. IP Tables (Firewall Rules)**

- Packet filtering rules
- NAT rules
- Security policies

**3. Routing Tables**

- Route decisions
- Gateway configurations
- Network paths

### Visual Architecture <a name="link_4"></a>

```
┌──────────────────────────────────────────────────┐
│ Host System                                      │
├──────────────────────────────────────────────────┤
│                                                  │
│ ┌─────────────────────┐ ┌─────────────────────┐  │
│ │ Default Namespace   │ │ App Namespace       │  │
│ ├─────────────────────┤ ├─────────────────────┤  │
│ │ Devices:            │ │ Devices:            │  │
│ │ • lo (127.0.0.1)    │ │ • lo (isolated)     │  │
│ │ • eth0              │ │                     │  │
│ │ • docker0           │ │                     │  │
│ ├─────────────────────┤ ├─────────────────────┤  │
│ │ IPTables:           │ │ IPTables:           │  │
│ │ • Complex rules     │ │ • Default/empty     │  │
│ │ • Firewall config   │ │ • Customizable      │  │
│ ├─────────────────────┤ ├─────────────────────┤  │
│ │ Routing:            │ │ Routing:            │  │
│ │ • Internet routes   │ │ • Empty initially   │  │
│ │ • Local routes      │ │ • Isolated          │  │
│ └─────────────────────┘ └─────────────────────┘  │
│                                                  │
└──────────────────────────────────────────────────┘
```

### Practical Commands <a name="link_5"></a>

**View Network Resources on Host:**

```
# List network devices
ip link list

# View IP tables rules (requires sudo)
sudo iptables --list

# Show routing table
ip route
```

**Create Network Namespace:**

```
# Create isolated namespace with network isolation
sudo unshare --pid --net --fork --mount-proc /bin/bash

# Inside namespace, check resources:
ip link list        # Only loopback device
iptables --list     # Different rules
ip route            # Empty routing table
```

### Use Cases for Network Namespaces <a name="link_6"></a>

1. **Security Isolation:** Prevent applications from accessing the internet
2. **Network Testing:** Simulate different network conditions
3. **Container Networking:** Foundation for Docker/Kubernetes networking
4. **Multi-tenancy:** Separate network resources for different applications

---

## UTS Namespaces <a name="link_7"></a>

### What are UTS Namespaces? <a name="link_8"></a>

UTS (UNIX Time-Sharing) namespaces provide isolation of hostname and domain name.

### Visual Concept <a name="link_9"></a>

```
┌──────────────────────────────────────────────┐
│ Host: "production-server"                    │
├──────────────────────────────────────────────┤
│                                              │
│ ┌────────────────┐ ┌────────────────┐        │
│ │ Web App 1      │ │ Web App 2      │        │
│ │                │ │                │        │
│ │ Hostname:      │ │ Hostname:      │        │
│ │ "webapp-01"    │ │ "webapp-02"    │        │
│ │                │ │                │        │
│ │ UTS Namespace  │ │ UTS Namespace  │        │
│ └────────────────┘ └────────────────┘        │
│                                              │
└──────────────────────────────────────────────┘
```

### Practical Implementation <a name="link_10"></a>

```
# Create namespace with UTS isolation
sudo unshare --uts --pid --fork --mount-proc /bin/bash

# Change hostname in namespace
hostname webapp-01

# Reload bash to see change
exec bash

# Verify hostname
hostname
# Output: webapp-01
```

### Benefits of UTS Namespaces <a name="link_11"></a>

- **Application Identity:** Each container can have its own hostname
- **Configuration Isolation:** Applications can use hostname-based configs
- **Testing:** Simulate different server environments

---

## IPC Namespaces <a name="link_12"></a>

### What are IPC Namespaces? <a name="link_13"></a>

IPC (Inter-Process Communication) namespaces provide isolation of:

- System V IPC objects: Message queues, semaphores, shared memory
- POSIX message queues

### IPC Resources Isolation <a name="link_14"></a>

```
┌───────────────────────────────────────────────┐
│ Host System                                   │
├───────────────────────────────────────────────┤
│                                               │
│ ┌─────────────────┐ ┌─────────────────┐       │
│ │ Namespace 1     │ │ Namespace 2     │       │
│ ├─────────────────┤ ├─────────────────┤       │
│ │ Message Queue:  │ │ Message Queue:  │       │
│ │ Key: 0x12345    │ │ Key: 0x67890    │       │
│ │                 │ │                 │       │
│ │ Processes can   │ │ Processes can   │       │
│ │ only see their  │ │ only see their  │       │
│ │ own queue       │ │ own queue       │       │
│ └─────────────────┘ └─────────────────┘       │
│        ↑                    ↑                 │
│        └────────┬───────────┘                 │
│            Isolated IPC                       │
└───────────────────────────────────────────────┘
```

### Practical Commands <a name="link_15"></a>

```
# Create namespace with IPC isolation
sudo unshare --ipc --pid --fork --mount-proc /bin/bash

# Create a message queue
ipcmk -Q

# View message queues
ipcs -q

# The queue is only visible in this namespace
```

---

## Commands Reference <a name="link_16"></a>

### Essential Commands Summary <a name="link_17"></a>

| Command    | Purpose                    | Example                              |
| ---------- | -------------------------- | ------------------------------------ |
| `unshare`  | Create new namespaces      | `sudo unshare --net --pid /bin/bash` |
| `ip link`  | View network devices       | `ip link list`                       |
| `ip route` | View routing table         | `ip route show`                      |
| `iptables` | View/modify firewall rules | `sudo iptables -L`                   |
| `hostname` | View/set hostname          | `hostname NewName`                   |
| `ipcmk`    | Create IPC resources       | `ipcmk -Q`                           |
| `ipcs`     | View IPC resources         | `ipcs -q`                            |

### Common Namespace Creation Patterns <a name="link_18"></a>

```
# Complete isolation (all namespaces)
sudo unshare --uts --ipc --pid --net --fork --mount-proc /bin/bash

# Network testing environment
sudo unshare --net --fork /bin/bash

# Application container simulation
sudo unshare --pid --net --uts --ipc --fork --mount-proc /bin/bash
```

---

## Summary <a name="link_19"></a>

### Key Takeaways <a name="link_20"></a>

**1. Network Namespaces provide:**

- Isolated network devices
- Separate IP tables (firewall rules)
- Independent routing tables
- Foundation for container networking

**2. UTS Namespaces enable:**

- Hostname isolation
- Domain name isolation
- Per-container identity

**3. IPC Namespaces offer:**

- Message queue isolation
- Semaphore isolation
- Shared memory isolation
- Secure inter-process communication

### Namespace Interaction Diagram <a name="link_21"></a>

```
┌─────────────────────────────────────────────────┐
│ Linux Kernel                                    │
├─────────────────────────────────────────────────┤
│                                                 │
│ ┌───────────────────────────────────────────┐   │
│ │ Containerized Application                 │   │
│ ├───────────────────────────────────────────┤   │
│ │                                           │   │
│ │ ┌─────────┐ ┌─────────┐ ┌─────────┐       │   │
│ │ │   PID   │ │   NET   │ │   UTS   │       │   │
│ │ │Namespace│ │Namespace│ │Namespace│       │   │
│ │ └─────────┘ └─────────┘ └─────────┘       │   │
│ │                                           │   │
│ │ ┌─────────┐ ┌─────────┐ ┌─────────┐       │   │
│ │ │   IPC   │ │  Mount  │ │  User   │       │   │
│ │ │Namespace│ │Namespace│ │Namespace│       │   │
│ │ └─────────┘ └─────────┘ └─────────┘       │   │
│ │                                           │   │
│ │      Complete Resource Isolation          │   │
│ └───────────────────────────────────────────┘   │
│                                                 │
└─────────────────────────────────────────────────┘
```

### Real-World Applications <a name="link_22"></a>

- **Docker:** Uses all namespace types for container isolation
- **Kubernetes:** Builds on namespaces for pod isolation
- **systemd:** Uses namespaces for service isolation

---
