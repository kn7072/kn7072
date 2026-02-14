[source](https://dev.to/ajinkya_singh_2c02bd40423/mount-namespaces-and-nsenter-deep-dive-39o7)

- [ Understanding Mount Namespaces](#link_1)
  - [ The Isolation Problem](#link_2)
  - [ With Mount Namespace Isolation](#link_3)
- [ Understanding Mount Points](#link_4)
  - [ What is Mounting?](#link_5)
  - [ Storage Device to Unified View](#link_6)
- [ Types of Mounts](#link_7)
  - [ 1. Device Mount](#link_8)
  - [ 2. Bind Mount](#link_9)
- [ Creating Mount Namespaces](#link_10)
  - [ Basic Mount Namespace](#link_11)
  - [ Why This Matters for Containers](#link_12)
- [ Managing Namespaces with nsenter](#link_13)
  - [ What is nsenter?](#link_14)
  - [ Command Structure](#link_15)
- [ Practical nsenter Examples](#link_16)
  - [ Example 1: Viewing Container Processes](#link_17)
  - [ Example 2: Inspecting Container Filesystem](#link_18)
  - [ Example 3: Full Container Debug Session](#link_19)
  - [ Example 4: Resource Monitoring](#link_20)
- [ Complete Isolation Example](#link_21)
  - [ Entering This Container from Outside](#link_22)
- [ Key Concepts Recap](#link_23)
  - [ Mount Points](#link_24)
  - [ Mount Namespaces](#link_25)
  - [ nsenter](#link_26)
- [ Quick Reference Commands](#link_27)
- [ Why This Matters for Conti](#link_28)

# Linux Mount Namespaces and nsenter: Deep Dive

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

## Understanding Mount Namespaces <a name="link_1"></a>

We've already covered what namespaces are. Now let's dive deep into **mount namespaces** - one of the most critical components for container filesystem isolation.

Mount namespaces control which files and directories are visible to processes. They allow each containerized application to have its own view of the filesystem, preventing interference between applications.

### The Isolation Problem <a name="link_2"></a>

Without mount namespaces, all applications share the same filesystem view:

```
WITHOUT ISOLATION
─────────────────
📁 /
├── 📁 bin/
├── 📁 etc/
├── 📁 var/
└── 📁 sensitive-data/
    ├── webapp-secrets/      ← App A can see this
    ├── database-config/     ← App B can see this
    └── api-keys/            ← Everyone can see this

⚠️ Security Risk: All apps see all files
```

### With Mount Namespace Isolation <a name="link_3"></a>

```
┌──────────────────────┐     ┌──────────────────────┐
│  WebApp Namespace    │     │  Database Namespace  │
│                      │     │                      │
│  📁 /                │     │  📁 /                │
│  ├── bin/            │     │  ├── bin/            │
│  ├── lib/            │     │  ├── lib/            │
│  └── data/           │     │  └── data/           │
│      └── webapp/     │     │      └── db/         │
│                      │     │                      │
│  ✅ Isolated view    │     │  ✅ Isolated view    │
└──────────────────────┘     └──────────────────────┘
```

## Understanding Mount Points <a name="link_4"></a>

Before we go further, let's understand what "mounting" means.

### What is Mounting? <a name="link_5"></a>

Mounting is the process of making a filesystem accessible at a specific point in the directory tree. Think of your Linux system as a tree that can have different "branches" (filesystems) plugged in at various points.

### Storage Device to Unified View <a name="link_6"></a>

```
STORAGE DEVICE
──────────────
┌────────┐ ┌────────┐ ┌────────┐
│ Part 1 │ │ Part 2 │ │ Part 3 │
│ (sda1) │ │ (sda2) │ │ (sda3) │
│  ext4  │ │  swap  │ │ btrfs  │
└────────┘ └────────┘ └────────┘
    ↓          ↓          ↓
  [root]    [swap]     [home]

         Kernel Magic ✨
              ↓

UNIFIED FILE SYSTEM
──────────────────
📁 / (from sda1)
├── 📁 bin/
├── 📁 etc/
├── 📁 home/ (mounted from sda3)
├── 📁 var/
└── 📁 usr/
```

The kernel stitches together multiple physical storage devices into one seamless directory tree.

## Types of Mounts <a name="link_7"></a>

### 1. Device Mount <a name="link_8"></a>

Mounting a physical device or partition:

```
# Mount a USB drive
mount /dev/sdb1 /mnt/usb

# Mount a disk partition
mount /dev/sda3 /home
```

### 2. Bind Mount <a name="link_9"></a>

Mounting an existing directory to another location - making the same content appear in two places:

```
# Make /source/project appear at /workspace/active
mount --bind /source/project /workspace/active
```

**Bind Mount Visual:**

```
BEFORE BIND MOUNT:
──────────────────
/project/           /workspace/
├── src/            ├── temp/
├── docs/           └── logs/
└── README

AFTER: mount --bind /project /workspace/active
────────────────────────────────────────────
/project/           /workspace/
├── src/            ├── temp/
├── docs/           ├── logs/
└── README          └── active/  ← Now shows
                        ├── src/     project
                        ├── docs/    content
                        └── README
```

## Creating Mount Namespaces <a name="link_10"></a>

### Basic Mount Namespace <a name="link_11"></a>

```
# Create new mount namespace
sudo unshare --mount /bin/bash

# Now you're in an isolated mount namespace
# Any mounts you create are invisible outside
mkdir /tmp/isolated
mount --bind /home/user/data /tmp/isolated

# Exit the namespace
exit

# Check from parent - /tmp/isolated won't show the mount
ls /tmp/isolated  # Empty or doesn't exist
```

### Why This Matters for Containers <a name="link_12"></a>

When a container starts, it needs its own filesystem view:

- Container shouldn't see host mounts
- Host shouldn't be affected by container mounts
- Each container has its own `/tmp`, `/var`, etc.

## Managing Namespaces with nsenter <a name="link_13"></a>

Now that we understand mount namespaces, how do we interact with processes running inside them? Enter `nsenter`.

### What is nsenter? <a name="link_14"></a>

`nsenter` (namespace enter) allows you to enter the namespaces of an existing process. It's essential for debugging containers and understanding what's happening inside isolated environments.

### Command Structure <a name="link_15"></a>

```
nsenter --target <PID> [OPTIONS] <command>

# Common options:
--pid      # Enter PID namespace
--mount    # Enter mount namespace
--uts      # Enter UTS namespace
--net      # Enter network namespace
--all      # Enter all namespaces
```

## Practical nsenter Examples <a name="link_16"></a>

### Example 1: Viewing Container Processes <a name="link_17"></a>

```
# Find the container's main process
ps aux | grep myapp
# Output: 4500 root /usr/bin/myapp

# Enter its PID namespace and list processes
sudo nsenter --target 4500 --pid ps aux

# You'll see only processes inside that namespace
# PID 1 will be the container's init process
```

### Example 2: Inspecting Container Filesystem <a name="link_18"></a>

```
# Enter mount namespace to see what's mounted
sudo nsenter --target 4500 --mount df -h

# Or get a shell inside
sudo nsenter --target 4500 --mount /bin/bash
ls /  # You see the container's root filesystem
```

### Example 3: Full Container Debug Session <a name="link_19"></a>

```
# Enter ALL namespaces of process 4500
sudo nsenter --target 4500 --all /bin/bash

# Now you're fully inside the container
hostname        # Container's hostname
ps aux          # Container's processes
ip addr         # Container's network interfaces
mount           # Container's mounts
cat /etc/hosts  # Container's host file

# Exit to return to host
exit
```

### Example 4: Resource Monitoring <a name="link_20"></a>

```
# Monitor CPU/memory from inside container
sudo nsenter --target 4500 --pid top

# Check disk usage
sudo nsenter --target 4500 --mount du -sh /var/log

# Network connections
sudo nsenter --target 4500 --net netstat -tuln
```

## Complete Isolation Example <a name="link_21"></a>

Let's create a container-like environment using multiple namespaces:

```
# Create PID, Mount, and UTS namespaces
sudo unshare --pid --mount --uts --fork /bin/bash

# At this point you're in isolated namespaces

# Set custom hostname (UTS namespace in action)
hostname my-container
hostname  # Shows: my-container

# Create isolated mount point
mkdir -p /tmp/container-root/{bin,lib,usr,var,tmp}

# Bind mount necessary directories
mount --bind /bin /tmp/container-root/bin
mount --bind /lib /tmp/container-root/lib

# Change root to our isolated filesystem
chroot /tmp/container-root

# Now you have:
# ✅ Isolated PID namespace
# ✅ Isolated mount namespace
# ✅ Custom hostname
# ✅ Restricted filesystem view
```

### Entering This Container from Outside <a name="link_22"></a>

```
# In another terminal, find the container process
ps aux | grep "my-container"
# Let's say PID is 6000

# Enter all its namespaces
sudo nsenter --target 6000 --all /bin/bash

# You're now inside the container
# Same view as if you were inside originally
```

## Key Concepts Recap <a name="link_23"></a>

### Mount Points <a name="link_24"></a>

- **Mount Point**: Directory where a filesystem is attached
- **Bind Mount**: Making existing directory appear elsewhere
- **Root Filesystem**: Primary filesystem containing system files

### Mount Namespaces <a name="link_25"></a>

- Provide filesystem isolation
- Allow processes to have different views of directory tree
- Essential for container security

### nsenter <a name="link_26"></a>

- Enters namespaces of running processes
- Critical for debugging containers
- Can enter specific or all namespaces
- Must target a running process PID

## Quick Reference Commands <a name="link_27"></a>

```
# CREATE MOUNT NAMESPACES
unshare --mount /bin/bash                    # New mount namespace
unshare --mount --pid --fork /bin/bash       # Mount + PID namespaces

# MOUNT OPERATIONS
mount /dev/sdb1 /mnt/usb                     # Device mount
mount --bind /source /target                 # Bind mount
umount /mnt/usb                              # Unmount

# NSENTER - ENTER NAMESPACES
nsenter --target <PID> --mount /bin/bash     # Enter mount namespace
nsenter --target <PID> --pid ps aux          # Run command in PID namespace
nsenter --target <PID> --all /bin/bash       # Enter all namespaces

# VIEW NAMESPACE INFO
lsns                                         # List all namespaces
ls -l /proc/<PID>/ns/                        # View process namespaces
readlink /proc/<PID>/ns/mnt                  # Get mount namespace ID
findmnt                                      # Show mount tree
```

## Why This Matters for Conti <a name="link_28"></a>

When building your container runtime, mount namespaces and `nsenter` are crucial:

1. **Isolation**: Each container needs its own filesystem view
2. **Security**: Prevent containers from accessing host files
3. **Debugging**: Use nsenter to troubleshoot running containers
4. **Resource Management**: Monitor container filesystem usage
5. **Root Filesystem**: Create minimal root filesystems for containers

---
