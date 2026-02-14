[source](https://dev.to/ajinkya_singh_2c02bd40423/understanding-linux-cgroups-2kf1)

- [ What are Cgroups?](#link_1)
  - [ The Core Formula](#link_2)
  - [ Why Do We Need Cgroups?](#link_3)
- [ Real-World Analogy](#link_4)
  - [ Without Cgroups (No Rules)](#link_5)
  - [ With Cgroups (Managed Parking)](#link_6)
- [ How Cgroups Work](#link_7)
  - [ Step-by-Step Process](#link_8)
  - [ Cgroup Hierarchy](#link_9)
- [ Resource Types](#link_10)
  - [ 1. Memory Control](#link_11)
  - [ 2. CPU Control](#link_12)
  - [ 3. Network Control](#link_13)
  - [ 4. Disk I/O Control](#link_14)
- [ Memory Management](#link_15)
  - [ Creating a Memory Control Group](#link_16)
    - [ Step 1: Create the Control Group](#link_17)
    - [ Step 2: Set Memory Limit](#link_18)
    - [ Step 3: Run Your Application](#link_19)
  - [ What Happens When Memory Limit Is Exceeded?](#link_20)
  - [ Monitoring Memory Usage](#link_21)
- [ CPU Control](#link_22)
  - [ Method 1: Hard Limits (CFS Quota)](#link_23)
    - [ The Formula](#link_24)
    - [ Example: Limit to 35% CPU](#link_25)
    - [ Common CPU Percentages](#link_26)
  - [ Method 2: Soft Limits (CPU Shares)](#link_27)
    - [ Key Concept](#link_28)
    - [ The Formula](#link_29)
    - [ Example: Three Applications Sharing CPU](#link_30)
  - [ Hard Limits vs Soft Limits](#link_31)
    - [ Visualization](#link_32)
- [ Practical Examples](#link_33)
  - [ Example 1: Development Environment](#link_34)
  - [ Example 2: Machine Learning Training](#link_35)
  - [ Example 3: CI/CD Pipeline](#link_36)
  - [ Example 4: Multi-Tenant Web Hosting](#link_37)

# 🎮 Understanding Linux Cgroups

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

## What are Cgroups? <a name="link_1"></a>

**Control Groups (Cgroups)** are a Linux kernel feature that allows you to allocate, limit, and monitor system resources for processes and groups of processes.

### The Core Formula <a name="link_2"></a>

```
Cgroups = Resource Control + Resource Isolation + Resource Accounting
```

### Why Do We Need Cgroups? <a name="link_3"></a>

Imagine you're running a web server that hosts multiple applications:

- **E-commerce Store**: Needs 8GB RAM, 40% CPU
- **Analytics Dashboard**: Needs 4GB RAM, 30% CPU
- **Email Service**: Needs 2GB RAM, 20% CPU

Without cgroups, these applications could:

- ❌ Steal resources from each other
- ❌ Cause system crashes
- ❌ Create unpredictable performance

With cgroups, you can:

- ✅ Guarantee each application gets its resources
- ✅ Prevent any single app from hogging the system
- ✅ Maintain stable, predictable performance

---

## Real-World Analogy <a name="link_4"></a>

Think of a **shopping mall** with limited parking spaces:

### Without Cgroups (No Rules) <a name="link_5"></a>

- Early shoppers take all parking spaces
- Late arrivals have nowhere to park
- Chaos and complaints

### With Cgroups (Managed Parking) <a name="link_6"></a>

- **Restaurant customers**: 40 spaces reserved
- **Movie theater guests**: 30 spaces reserved
- **Retail shoppers**: 30 spaces reserved

Each group is guaranteed their allocation, and no group can exceed their limit.

---

## How Cgroups Work <a name="link_7"></a>

### Step-by-Step Process <a name="link_8"></a>

```
1. Define Resource Groups
   └─> Create named groups for each resource type

2. Set Resource Limits
   └─> Assign specific limits to each group

3. Launch Applications
   └─> Start apps within their assigned groups

4. Kernel Enforces Limits
   └─> Automatic enforcement, no manual intervention needed
```

### Cgroup Hierarchy <a name="link_9"></a>

All cgroups live in the filesystem at `/sys/fs/cgroup/`:

```
/sys/fs/cgroup/
├── memory/          # RAM control
├── cpu/             # CPU time control
├── cpuset/          # CPU core assignment
├── blkio/           # Disk I/O control
├── net_cls/         # Network control
└── devices/         # Device access control
```

---

## Resource Types <a name="link_10"></a>

### 1. Memory Control <a name="link_11"></a>

- Maximum RAM allocation
- Swap space limits
- Out-of-memory (OOM) handling
- Memory usage tracking

### 2. CPU Control <a name="link_12"></a>

- CPU percentage allocation
- CPU core assignment (pinning)
- Scheduling priorities
- Multi-core management

### 3. Network Control <a name="link_13"></a>

- Bandwidth limitations
- Priority queuing
- Traffic shaping
- Network class assignments

### 4. Disk I/O Control <a name="link_14"></a>

- Read/write speed limits
- IOPS (operations per second)
- Device-specific quotas
- Priority levels

---

## Memory Management <a name="link_15"></a>

### Creating a Memory Control Group <a name="link_16"></a>

**Scenario**: You want to run a data processing script that shouldn't use more than 20MB of RAM.

#### Step 1: Create the Control Group <a name="link_17"></a>

```
# Create a new control group called 'data_processor'
cgcreate -g memory:data_processor
```

#### Step 2: Set Memory Limit <a name="link_18"></a>

```
# Set memory limit to 20MB (20 × 1024 × 1024 = 20,971,520 bytes)
cgset -r memory.limit_in_bytes=20971520 data_processor

# Also limit swap to prevent workarounds
cgset -r memory.memsw.limit_in_bytes=20971520 data_processor
```

#### Step 3: Run Your Application <a name="link_19"></a>

```
# Execute the script within the control group
cgexec -g memory:data_processor python3 process_data.py
```

### What Happens When Memory Limit Is Exceeded? <a name="link_20"></a>

```
Application starts
    ↓
Allocates memory
    ↓
Reaches 20MB limit
    ↓
Tries to allocate more
    ↓
┌─────────────────┐
│ Kernel detects  │
│   violation     │
└────────┬────────┘
         ↓
┌─────────────────┐
│  OOM Killer     │
│  Activated      │
└────────┬────────┘
         ↓
   Process killed
```

### Monitoring Memory Usage <a name="link_21"></a>

```
# Check current memory usage
cat /sys/fs/cgroup/memory/data_processor/memory.usage_in_bytes

# Check if OOM killer was triggered
cat /sys/fs/cgroup/memory/data_processor/memory.oom_control
```

---

## CPU Control <a name="link_22"></a>

There are **two methods** to control CPU usage:

### Method 1: Hard Limits (CFS Quota) <a name="link_23"></a>

Use this when you need **absolute limits** that are always enforced.

#### The Formula <a name="link_24"></a>

```
CPU Limit % = (cfs_quota_us / cfs_period_us) × 100
```

Where:

- `cfs_period_us`: Time window (default: 100,000 μs = 100ms)
- `cfs_quota_us`: CPU time allowed in that window

#### Example: Limit to 35% CPU <a name="link_25"></a>

```
# Step 1: Create control group
cgcreate -g cpu:video_encoder

# Step 2: Set 35% limit
# 35% of 100,000 = 35,000 microseconds
cgset -r cpu.cfs_quota_us=35000 video_encoder

# Step 3: Run application
cgexec -g cpu:video_encoder ffmpeg -i input.mp4 output.mp4
```

#### Common CPU Percentages <a name="link_26"></a>

| Desired CPU | cfs_quota_us | Calculation      |
| ----------- | ------------ | ---------------- |
| 10%         | 10,000       | 10,000 / 100,000 |
| 25%         | 25,000       | 25,000 / 100,000 |
| 50%         | 50,000       | 50,000 / 100,000 |
| 75%         | 75,000       | 75,000 / 100,000 |

### Method 2: Soft Limits (CPU Shares) <a name="link_27"></a>

Use this when you want **proportional sharing** during resource contention.

#### Key Concept <a name="link_28"></a>

- Maximum value: **1024** (represents 100%)
- Only enforced when multiple processes compete for CPU
- If CPU is idle, processes can use more than their share

#### The Formula <a name="link_29"></a>

```
Process CPU % = (process_shares / total_shares) × 100
```

#### Example: Three Applications Sharing CPU <a name="link_30"></a>

**Scenario**: You have three services running:

- **Web Server**: Should get 50% during contention
- **Background Jobs**: Should get 30% during contention
- **Monitoring**: Should get 20% during contention

```
# Create control groups
cgcreate -g cpu:web_server
cgcreate -g cpu:background_jobs
cgcreate -g cpu:monitoring

# Set CPU shares
cgset -r cpu.shares=512 web_server      # 512/1024 = 50%
cgset -r cpu.shares=307 background_jobs # 307/1024 ≈ 30%
cgset -r cpu.shares=205 monitoring      # 205/1024 ≈ 20%

# Launch applications
cgexec -g cpu:web_server nginx
cgexec -g cpu:background_jobs python worker.py
cgexec -g cpu:monitoring ./monitor.sh
```

### Hard Limits vs Soft Limits <a name="link_31"></a>

| Aspect          | Hard Limits (Quota)     | Soft Limits (Shares)   |
| --------------- | ----------------------- | ---------------------- |
| **Type**        | Absolute ceiling        | Relative distribution  |
| **Enforcement** | Always active           | Only during contention |
| **Idle CPU**    | Wasted if limit reached | Fully utilized         |
| **Use Case**    | Strict isolation        | Flexible sharing       |
| **Analogy**     | Speed limiter in car    | Highway lanes          |

#### Visualization <a name="link_32"></a>

**Hard Limit (30% quota)**:

```
CPU Available: 100%
Process usage: 30% ████████
Unused:        70% (wasted even if CPU is idle)
```

**Soft Limit (30% shares, no contention)**:

```
CPU Available: 100%
Process usage: 100% ████████████████████████████████
(Can use full CPU when alone)
```

**Soft Limit (30% shares, with contention)**:

```
CPU Available: 100%
Process 1:     30% ████████
Process 2:     40% ███████████
Process 3:     30% ████████
(Shares enforced when competing)
```

---

## Practical Examples <a name="link_33"></a>

### Example 1: Development Environment <a name="link_34"></a>

**Scenario**: You're running Docker containers for development:

- **Database**: 2GB RAM, 40% CPU
- **API Server**: 1GB RAM, 30% CPU
- **Redis Cache**: 512MB RAM, 20% CPU

```
# Database container
cgcreate -g memory,cpu:dev_database
cgset -r memory.limit_in_bytes=2147483648 dev_database
cgset -r cpu.cfs_quota_us=40000 dev_database

# API Server container
cgcreate -g memory,cpu:dev_api
cgset -r memory.limit_in_bytes=1073741824 dev_api
cgset -r cpu.cfs_quota_us=30000 dev_api

# Redis Cache container
cgcreate -g memory,cpu:dev_redis
cgset -r memory.limit_in_bytes=536870912 dev_redis
cgset -r cpu.cfs_quota_us=20000 dev_redis
```

### Example 2: Machine Learning Training <a name="link_35"></a>

**Scenario**: Training ML model that needs lots of resources but shouldn't crash the system.

```
# Create control group with generous limits
cgcreate -g memory,cpu:ml_training
cgset -r memory.limit_in_bytes=16106127360 ml_training  # 15GB
cgset -r cpu.cfs_quota_us=300000 ml_training  # 300% (3 full cores)

# Run training script
cgexec -g memory,cpu:ml_training python train_model.py
```

### Example 3: CI/CD Pipeline <a name="link_36"></a>

**Scenario**: Running automated tests that shouldn't hog server resources.

```
# Create control group for CI jobs
cgcreate -g memory,cpu:ci_runner
cgset -r memory.limit_in_bytes=4294967296 ci_runner  # 4GB
cgset -r cpu.shares=256 ci_runner  # Low priority (25% share)

# Run tests
cgexec -g memory,cpu:ci_runner npm test
```

### Example 4: Multi-Tenant Web Hosting <a name="link_37"></a>

**Scenario**: Hosting multiple customer websites on one server.

```
# Customer A - Premium tier
cgcreate -g memory,cpu:customer_a
cgset -r memory.limit_in_bytes=8589934592 customer_a  # 8GB
cgset -r cpu.shares=768 customer_a  # 75% share

# Customer B - Standard tier
cgcreate -g memory,cpu:customer_b
cgset -r memory.limit_in_bytes=4294967296 customer_b  # 4GB
cgset -r cpu.shares=256 customer_b  # 25% share
```
