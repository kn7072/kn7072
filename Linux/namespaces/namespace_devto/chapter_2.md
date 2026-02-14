[source](https://dev.to/ajinkya_singh_2c02bd40423/understanding-linux-namespaces-a-guide-to-process-isolation-4gbg)

- [ The Secret Ingredient in Modern Cloud Computing](#link_1)
- [ 📚 Previous Post Recap](#link_2)
- [ What Are Namespaces?](#link_3)
- [ Why Process Isolation Matters](#link_4)
- [ Types of Namespaces](#link_5)
- [ How PID Namespaces Work](#link_6)
  - [ The Parent-Child Hierarchy](#link_7)
- [ Creating a New PID Namespace](#link_8)
  - [ The Importance of --mount-proc](#link_9)
- [ Practical Example: Isolating Applications](#link_10)
  - [ Test Scripts](#link_11)
  - [ Scenario 1: No Isolation (Default)](#link_12)
  - [ Scenario 2: Partial Isolation](#link_13)
  - [ Scenario 3: Complete Isolation](#link_14)
- [ Understanding Process ID Mapping](#link_15)
- [ Verifying Namespace Isolation](#link_16)
  - [ Check Current Namespace](#link_17)
  - [ Test Process Visibility](#link_18)
  - [ Verify Communication Blocking](#link_19)
- [ Essential Commands Reference](#link_20)
- [ Key Takeaways](#link_21)

# Understanding Linux Namespaces: A Guide to Process Isolation

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

---

## The Secret Ingredient in Modern Cloud Computing <a name="link_1"></a>

Have you ever wondered how Docker runs thousands of applications on a single server without them interfering with each other? The answer lies in a powerful Linux kernel feature called **namespaces**. Let's dive into this fascinating technology that powers the modern cloud infrastructure.

---

## 📚 Previous Post Recap <a name="link_2"></a>

In my [previous article](https://dev.to/ajinkya_singh_2c02bd40423/understanding-linux-kernel-namespaces-the-magic-behind-containers-919), we explored the fundamentals of Linux kernel namespaces - what they are, why they matter, and how they form the foundation of containerization. We covered the seven types of namespaces and their role in isolating different system resources.

Now, we're taking it a step further with hands-on examples and practical demonstrations. If you haven't read the previous post, I recommend checking it out for a solid foundation!

---

## What Are Namespaces? <a name="link_3"></a>

Linux namespaces are a kernel feature that creates isolated environments for processes. They partition system resources so that different groups of processes operate independently, each believing they have exclusive access to their own instance of global resources.

**Core principle:** When you think namespaces, think isolation.

## Why Process Isolation Matters <a name="link_4"></a>

In Linux systems, process isolation prevents unwanted interactions between different applications or users. The fundamental rule is simple: **visibility equals communication**. If one process cannot see another, they cannot interfere with each other.

Imagine running multiple applications on a server—a web service, a database, and a background job processor. Without isolation, these processes could potentially conflict, consume each other's resources, or create security vulnerabilities.

## Types of Namespaces <a name="link_5"></a>

Linux provides seven types of namespaces, each isolating different system resources:

1. **PID Namespace** - Isolates process IDs
2. **Mount Namespace** - Isolates filesystem mount points
3. **Network Namespace** - Isolates network interfaces and routing tables
4. **UTS Namespace** - Isolates hostname and domain name
5. **IPC Namespace** - Isolates inter-process communication resources
6. **User Namespace** - Isolates user and group IDs
7. **Cgroup Namespace** - Isolates cgroup hierarchies

## How PID Namespaces Work <a name="link_6"></a>

The PID (Process ID) namespace is one of the most fundamental isolation mechanisms. It creates separate process ID spaces where processes in different namespaces can have the same PID without conflict.

### The Parent-Child Hierarchy <a name="link_7"></a>

Namespaces follow a hierarchical structure:

- **Parent namespace** can see all processes in child namespaces
- **Child namespaces** cannot see processes in the parent or sibling namespaces
- Each child namespace maintains its own isolated view of the system

This asymmetric visibility is crucial for system administration—the root namespace can monitor all processes while keeping workloads isolated from each other.

## Creating a New PID Namespace <a name="link_8"></a>

To create a new PID namespace, use the `unshare` command:

```
sudo unshare -p -f --mount-proc /bin/bash
```

Breaking down the flags:

- `-p` creates a new PID namespace
- `-f` forks a new process to become PID 1 in the new namespace
- `--mount-proc` mounts a new /proc filesystem
- `/bin/bash` launches a bash shell in the isolated environment

### The Importance of --mount-proc <a name="link_9"></a>

The `--mount-proc` flag is critical. Without it, the new namespace would inherit the parent's `/proc` filesystem, defeating the purpose of isolation. The `/proc` filesystem exposes kernel information about running processes, so mounting a fresh instance ensures processes only see others in their namespace.

## Practical Example: Isolating Applications <a name="link_10"></a>

Let's create some simple scripts to demonstrate namespace isolation in action.

### Test Scripts <a name="link_11"></a>

First, create a simple web server simulator:

```
#!/bin/bash
# webserver.sh

echo "🌐 Web Server Starting..."
echo "Process: webserver | PID: $$"

while true; do
    echo "[$(date +%T)] Serving requests..."

    # Check if database is visible
    if pgrep -f "database.sh" > /dev/null; then
        echo "  ✓ Database connection available"
    else
        echo "  ✗ Database not found (isolated!)"
    fi

    sleep 3
done
```

Create a database simulator:

```
#!/bin/bash
# database.sh

echo "💾 Database Starting..."
echo "Process: database | PID: $$"

while true; do
    echo "[$(date +%T)] Processing queries..."

    # Check if webserver is visible
    if pgrep -f "webserver.sh" > /dev/null; then
        echo "  ✓ Webserver connection detected"
    else
        echo "  ✗ Webserver not found (isolated!)"
    fi

    sleep 3
done
```

Create a cache service:

```
#!/bin/bash
# cache.sh

echo "⚡ Cache Service Starting..."
echo "Process: cache | PID: $$"

while true; do
    echo "[$(date +%T)] Caching data..."

    # Count visible services
    count=$(pgrep -f ".sh$" | wc -l)
    echo "  Visible processes: $count"

    sleep 3
done
```

Make them executable:

```
chmod +x webserver.sh database.sh cache.sh
```

### Scenario 1: No Isolation (Default) <a name="link_12"></a>

Run all services in the same namespace:

```
# Terminal 1
./webserver.sh &

# Terminal 2
./database.sh &

# Terminal 3
./cache.sh &

# Check what each can see
ps aux | grep ".sh$"
```

**Result:** All services can see each other - no isolation!

### Scenario 2: Partial Isolation <a name="link_13"></a>

```
# Terminal 1 (Parent namespace)
./database.sh &
./cache.sh &

# Terminal 2 (Child namespace)
sudo unshare -p -f --mount-proc /bin/bash
./webserver.sh
```

**Result:**

- Webserver cannot see database or cache
- Database and cache can still see the webserver (parent sees all)

### Scenario 3: Complete Isolation <a name="link_14"></a>

```
# Terminal 1 (Namespace A)
sudo unshare -p -f --mount-proc /bin/bash
./webserver.sh

# Terminal 2 (Namespace B)
sudo unshare -p -f --mount-proc /bin/bash
./database.sh

# Terminal 3 (Namespace C)
sudo unshare -p -f --mount-proc /bin/bash
./cache.sh
```

**Result:** All three services run in complete isolation—none can see or interact with the others!

## Understanding Process ID Mapping <a name="link_15"></a>

An interesting aspect of namespaces is how process IDs differ between parent and child views:

| Process   | PID in Child Namespace | PID in Parent Namespace |
| --------- | ---------------------- | ----------------------- |
| webserver | 1                      | 52341                   |
| worker    | 15                     | 52358                   |
| cache     | 23                     | 52367                   |

The parent namespace assigns unique PIDs to distinguish between processes across multiple child namespaces that might use the same local PIDs.

## Verifying Namespace Isolation <a name="link_16"></a>

### Check Current Namespace <a name="link_17"></a>

```
# View your current PID namespace
lsns -t pid

# Check a specific process's namespace
readlink /proc/[PID]/ns/pid
```

### Test Process Visibility <a name="link_18"></a>

```
# In parent namespace
ps aux | grep webserver
# Shows: webserver with PID 42156

# In child namespace
ps aux | grep webserver
# Shows: webserver with PID 1 (or not at all if in different namespace)
```

### Verify Communication Blocking <a name="link_19"></a>

```
# Attempt to find processes from another namespace
pgrep database
# Returns nothing if isolated properly
```

## Essential Commands Reference <a name="link_20"></a>

```
# List all PID namespaces
lsns -t pid

# List all namespace types
lsns -t all

# Check process namespace
readlink /proc/[PID]/ns/pid

# Create new PID namespace
sudo unshare -p -f --mount-proc /bin/bash

# List processes in current namespace
ps aux

# Find process by name
pgrep [process_name]
```

## Key Takeaways <a name="link_21"></a>

1. **Namespaces enable isolation** - They're the core technology behind containerization
2. **Parent-child hierarchy** - Parents can monitor children, but children remain isolated from each other
3. **Multiple namespace types** - Different resources require different namespace types
4. **The /proc filesystem matters** - Always remount it for true PID isolation
5. **Building block for containers** - Understanding namespaces illuminates how Docker and Kubernetes work under the hood

**Stay tuned, and happy coding!** 🚀
