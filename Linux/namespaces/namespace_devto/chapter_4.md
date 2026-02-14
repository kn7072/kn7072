[source](https://dev.to/ajinkya_singh_2c02bd40423/mount-namespace-practice-guide-4c84)

- [ 🎯 Overview](#link_1)
- [ 🔍 What is Pivot Root?](#link_2)
  - [ How It Works](#link_3)
  - [ Key Requirements](#link_4)
- [ 📋 Quick Setup Exercise](#link_5)
  - [ Scenario](#link_6)
- [ 🚀 Practice Steps](#link_7)
  - [ Initial Setup](#link_8)
  - [ Create First Namespace (Bookstore)](#link_9)
  - [ Create Second Namespace (Cafe)](#link_10)
  - [ 4. Test Isolation](#link_11)
- [ Key Commands](#link_12)
- [ Quick Verification](#link_13)

# Linux Mount Namespace Practice Guide

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

## 🎯 Overview <a name="link_1"></a>

Practice creating isolated filesystem views using mount namespaces with a simple bookstore/cafe scenario.

---

## 🔍 What is Pivot Root? <a name="link_2"></a>

**Pivot root** changes the root filesystem (`/`) for a process and its children, providing complete filesystem isolation.

### How It Works <a name="link_3"></a>

```
BEFORE PIVOT ROOT:
┌─────────────────────────┐
│  System Root (/)        │
│  ├── home/              │
│  ├── var/               │
│  ├── bookstore/         │ ← Target directory
│  │   ├── books/         │
│  │   ├── checkout/      │
│  │   └── old_root/      │ (empty)
│  └── cafe/              │
└─────────────────────────┘

AFTER PIVOT ROOT (from bookstore):
┌─────────────────────────┐
│  New Root (/)           │
│  ├── books/             │ ← Bookstore content
│  ├── checkout/          │
│  └── old_root/          │ ← Old system root moved here
│      ├── home/          │
│      ├── var/           │
│      └── cafe/          │
└─────────────────────────┘
```

### Key Requirements <a name="link_4"></a>

✓ Target directory **must be a mount point**

✓ Needs a directory to move old root (e.g., `old_root/`)

✓ Must be run in a **mount namespace** (or as init process)

---

## 📋 Quick Setup Exercise <a name="link_5"></a>

### Scenario <a name="link_6"></a>

Create two isolated environments:

- **Bookstore** zone with its own resources
- **Cafe** zone with its own resources

---

## 🚀 Practice Steps <a name="link_7"></a>

### Initial Setup <a name="link_8"></a>

```
# Create directory structures
mkdir -p bookstore/{books,checkout,lounge,old_root}
mkdir -p cafe/{menu,kitchen,seating,old_root}

# Add sample files
echo "Fiction novels" > bookstore/books/inventory.txt
echo "Coffee menu" > cafe/menu/drinks.txt
```

### Create First Namespace (Bookstore) <a name="link_9"></a>

```
# Open terminal 1
sudo unshare -m -p --mount-proc /bin/bash

# Make it a mount point
sudo mount --bind bookstore bookstore

# Change root
cd bookstore
sudo pivot_root . old_root

# Verify isolation
ls /  # Should only show: books, checkout, lounge, old_root
```

### Create Second Namespace (Cafe) <a name="link_10"></a>

```
# Open terminal 2
sudo unshare -m -p --mount-proc /bin/bash

# Make it a mount point
sudo mount --bind cafe cafe

# Change root
cd cafe
sudo pivot_root . old_root

# Verify isolation
ls /  # Should only show: menu, kitchen, seating, old_root
```

### 4. Test Isolation <a name="link_11"></a>

```
# In bookstore namespace
cd /
cat books/inventory.txt  # ✓ Works
cat menu/drinks.txt      # ✗ Doesn't exist

# In cafe namespace
cd /
cat menu/drinks.txt      # ✓ Works
cat books/inventory.txt  # ✗ Doesn't exist
```

---

## Key Commands <a name="link_12"></a>

| Command                                | Purpose                      |
| -------------------------------------- | ---------------------------- |
| `unshare -m -p --mount-proc /bin/bash` | Create isolated namespace    |
| `mount --bind dir dir`                 | Make directory a mount point |
| `pivot_root . old_root`                | Change root directory        |
| `lsns -t mnt`                          | List mount namespaces        |

---

## Quick Verification <a name="link_13"></a>

```
# Check you're in a namespace
lsns -t mnt -t pid

# Verify mount point
df -a | grep bookstore

# Check current root
pwd  # Should show /
```
