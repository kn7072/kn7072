[source](https://dev.to/ajinkya_singh_2c02bd40423/understanding-container-magic-the-overlay-filesystem-story-37dh)

- [ 🎬 Act 1: The Party Problem](#link_1)
  - [ The Expensive Approach ❌](#link_2)
  - [ The Smart Approach ✅](#link_3)
- [ 🏗️ Act 2: Understanding the Architecture](#link_4)
  - [ The Three-Layer Cake 🎂](#link_5)
    - [ 🎯 The Lower Layer (The Foundation)](#link_6)
    - [ ✍️ The Upper Layer (Your Workspace)](#link_7)
    - [ 👀 The Merged Layer (The Magic View)](#link_8)
- [ 🎪 Act 3: The Copy-on-Write Magic Show](#link_9)
  - [ Scenario: The Recipe Book 📖](#link_10)
  - [ Real Container Example](#link_11)
- [ 🎯 Act 4: The Real-World Impact](#link_12)
  - [ Before Overlay FS: The Dark Ages 😱](#link_13)
  - [ After Overlay FS: The Renaissance ✨](#link_14)
- [ 🛠️ Act 5: Hands-On Workshop](#link_15)
  - [ Workshop Setup: Three Coffee Shops ☕](#link_16)
    - [ Step 1: Create the Directory Structure](#link_17)
    - [ Step 2: Mount Downtown Shop (First Container)](#link_18)
    - [ Step 3: Make Shop-Specific Changes](#link_19)
    - [ Step 4: Create Another Shop (Second Container)](#link_20)
  - [ 🎊 What We Achieved:](#link_21)
- [ 🎭 Act 6: The Delete Mystery](#link_22)
- [ 🚀 Act 7: Real Container Architecture](#link_23)
  - [ The Dockerfile Connection](#link_24)

# Understanding Container Magic: The Overlay Filesystem Story

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

_How modern containers achieve incredible efficiency and isolation_

---

## 🎬 Act 1: The Party Problem <a name="link_1"></a>

Imagine you're organizing a massive tech conference with three separate tracks happening simultaneously:

**🎨 The Design Track** - UI/UX designers discussing Figma and Sketch

**💻 The DevOps Track** - Engineers exploring Kubernetes and CI/CD

**🤖 The AI Track** - Researchers presenting machine learning models

Each track needs:

- A presentation room (isolated space)
- Audio/visual equipment (shared resources)
- Custom materials (track-specific content)
- Whiteboards for notes (temporary changes)

### The Expensive Approach ❌ <a name="link_2"></a>

You could buy **three complete sets** of everything:

- 3 projectors @ $2,000 each = $6,000
- 3 sound systems @ $1,500 each = $4,500
- 3 furniture sets @ $3,000 each = $9,000

**Total: $19,500** 😱

### The Smart Approach ✅ <a name="link_3"></a>

What if you could:

- **Share** the expensive equipment (projectors, furniture)
- Give each track **private notebooks** for their own notes
- Let them **customize** only what they need

**Total: $6,500 + 3 notebooks**

_This is exactly what overlay filesystems do for containers!_

---

## 🏗️ Act 2: Understanding the Architecture <a name="link_4"></a>

### The Three-Layer Cake 🎂 <a name="link_5"></a>

Think of the overlay filesystem as a delicious three-layer cake:

```
┌──────────────────────────────────────┐
│     🍰 MERGED LAYER (What You See)   │ ← The complete cake you eat
│     Combines everything below        │
├──────────────────────────────────────┤
│     ✏️  UPPER LAYER (Your Changes)   │ ← Your frosting and decorations
│     Read/Write - Personal Edits      │
├──────────────────────────────────────┤
│     📦 LOWER LAYER (Base Recipe)     │ ← The original cake (untouched)
│     Read-Only - Shared Foundation    │
└──────────────────────────────────────┘
```

#### 🎯 The Lower Layer (The Foundation) <a name="link_6"></a>

- **Read-only** - Like a published cookbook
- Contains your base operating system (Ubuntu, Alpine Linux)
- Shared across ALL containers
- Never gets modified

#### ✍️ The Upper Layer (Your Workspace) <a name="link_7"></a>

- **Read/write** - Your personal notepad
- Stores all YOUR changes
- Unique to each container
- Where creativity happens!

#### 👀 The Merged Layer (The Magic View) <a name="link_8"></a>

- What users actually see and interact with
- Automatically combines Lower + Upper
- Feels like one complete filesystem

---

## 🎪 Act 3: The Copy-on-Write Magic Show <a name="link_9"></a>

Let me show you the most clever trick in the container world: **Copy-on-Write (COW)**

### Scenario: The Recipe Book 📖 <a name="link_10"></a>

Imagine you have a **master recipe book** (lower layer) with 100 recipes.

**Day 1**: You read "Chocolate Cake" → _No copying needed!_

You're just reading from the shared book. Fast and efficient!

**Day 2**: You want to modify "Chocolate Cake" → _NOW the magic happens!_

```
STEP 1: System spots you editing
   ↓
STEP 2: "Hold on! Let me copy this page to YOUR notebook!"
   ↓
STEP 3: Copy "Chocolate Cake" to upper layer
   ↓
STEP 4: You modify YOUR copy
   ↓
STEP 5: Original recipe stays pristine ✨
```

**The Result:**

- Master book: Still has original "Chocolate Cake" ✅
- Your notebook: Has your modified "Spicy Chocolate Cake" ✅
- Everyone else: Still sees the original recipe ✅

### Real Container Example <a name="link_11"></a>

```
# Container starts with nginx.conf from base image
$ cat /etc/nginx/nginx.conf
→ Reading from LOWER layer (shared base image)

# You edit the config file
$ echo "worker_processes 4;" >> /etc/nginx/nginx.conf
→ System COPIES file to UPPER layer
→ Your edit goes into YOUR copy
→ Base image remains unchanged!

# Your change is private to YOUR container
→ 1000 other nginx containers still see the original
```

---

## 🎯 Act 4: The Real-World Impact <a name="link_12"></a>

### Before Overlay FS: The Dark Ages 😱 <a name="link_13"></a>

Launching 100 web applications:

```
App 1:  Ubuntu (500MB) + Node.js (100MB) = 600MB
App 2:  Ubuntu (500MB) + Node.js (100MB) = 600MB
App 3:  Ubuntu (500MB) + Node.js (100MB) = 600MB
...
App 100: Ubuntu (500MB) + Node.js (100MB) = 600MB

TOTAL: 60,000 MB (60 GB!) 💀
```

### After Overlay FS: The Renaissance ✨ <a name="link_14"></a>

```
Shared Ubuntu:     500MB (one time!)
Shared Node.js:    100MB (one time!)
App 1 changes:     2MB
App 2 changes:     3MB
App 3 changes:     1MB
...
App 100 changes:   2MB

TOTAL: 600MB + 200MB changes = 800MB 🎉

SAVED: 59.2 GB (98.7% reduction!)
```

---

## 🛠️ Act 5: Hands-On Workshop <a name="link_15"></a>

Let's build our own overlay filesystem step-by-step!

### Workshop Setup: Three Coffee Shops ☕ <a name="link_16"></a>

You're running three coffee shops, each needs menus and custom recipes.

#### Step 1: Create the Directory Structure <a name="link_17"></a>

```
# Our shared base (the franchise template)
mkdir -p coffee-franchise/{base,shop-downtown,shop-uptown,shop-campus}
mkdir -p coffee-franchise/work-{downtown,uptown,campus}
mkdir -p coffee-franchise/merged-{downtown,uptown,campus}

cd coffee-franchise

# Create shared base menu (lower layer)
echo "1. Espresso - $3" > base/menu.txt
echo "2. Latte - $4" >> base/menu.txt
echo "3. Cappuccino - $4.50" >> base/menu.txt
echo "Standard Coffee Brewing Guide" > base/brewing.txt
```

#### Step 2: Mount Downtown Shop (First Container) <a name="link_18"></a>

```
# Create the overlay filesystem
sudo mount -t overlay overlay \
  -o lowerdir=base,upperdir=shop-downtown,workdir=work-downtown \
  merged-downtown

# Check what's visible
ls merged-downtown/
# Output: menu.txt  brewing.txt (from base!)
```

#### Step 3: Make Shop-Specific Changes <a name="link_19"></a>

```
# Downtown caters to business people - add premium options
echo "4. Cold Brew - $5" >> merged-downtown/menu.txt
echo "Downtown Specialty: Extra Strong!" > merged-downtown/special.txt

# Check what happened:
ls base/
# Output: menu.txt  brewing.txt (unchanged!)

ls shop-downtown/
# Output: menu.txt  special.txt (YOUR changes only!)
```

#### Step 4: Create Another Shop (Second Container) <a name="link_20"></a>

```
# Mount campus shop
sudo mount -t overlay overlay \
  -o lowerdir=base,upperdir=shop-uptown,workdir=work-uptown \
  merged-uptown

# Campus caters to students - add budget options
echo "4. Small Coffee - $2" >> merged-uptown/menu.txt
echo "Campus Special: Student Discount 20%!" > merged-uptown/special.txt

# Each shop sees different menus!
cat merged-downtown/special.txt
# Output: Downtown Specialty: Extra Strong!

cat merged-uptown/special.txt
# Output: Campus Special: Student Discount 20%!
```

### 🎊 What We Achieved: <a name="link_21"></a>

✅ **One base menu** shared across all shops

✅ **Custom modifications** per shop

✅ **Complete isolation** - changes don't affect others

✅ **Massive space savings** - one copy of common files

---

## 🎭 Act 6: The Delete Mystery <a name="link_22"></a>

What happens when you delete a file from the lower layer?

```
# Try to delete the base menu from downtown
rm merged-downtown/menu.txt

# The file disappears from downtown view... but wait!
ls merged-downtown/
# Output: brewing.txt  special.txt (menu.txt is gone!)

# Check the other shop
ls merged-uptown/
# Output: menu.txt  brewing.txt  special.txt (still there!)

# The secret: a WHITEOUT file
ls -la shop-downtown/
# Output: c--------- 1 root root 0, 0 menu.txt (special marker!)
```

**The Magic:**

Instead of deleting from base (impossible - it's read-only!), the system creates a special "whiteout" marker that hides the file _only in your view_.

---

## 🚀 Act 7: Real Container Architecture <a name="link_23"></a>

Here's how Docker/Kubernetes actually use this:

```
┌──────────────────────────────────────────┐
│   YOUR RUNNING CONTAINER (Merged)        │
│   What you see when you 'docker exec'    │
├──────────────────────────────────────────┤
│   CONTAINER LAYER (Upper) ✏️             │
│   - Your app logs                        │
│   - Temp files                           │
│   - Runtime changes                      │
├──────────────────────────────────────────┤
│   APP LAYER (Lower 3) 📱                 │
│   - Your application code                │
│   - App dependencies                     │
├──────────────────────────────────────────┤
│   RUNTIME LAYER (Lower 2) ⚙️             │
│   - Python/Node.js/Java                  │
│   - Libraries                            │
├──────────────────────────────────────────┤
│   BASE OS LAYER (Lower 1) 🏗️             │
│   - Ubuntu/Alpine Linux                  │
│   - Core utilities                       │
└──────────────────────────────────────────┘
     ↑
     └─ All "Lower" layers are SHARED!
```

### The Dockerfile Connection <a name="link_24"></a>

```
FROM ubuntu:20.04           # ← Lower Layer 1 (shared!)
RUN apt-get install python3  # ← Lower Layer 2 (shared!)
COPY app.py /app/           # ← Lower Layer 3 (shared!)
CMD ["python3", "app.py"]    # ← Upper Layer (YOUR changes!)
```

Each line creates a layer. When you run 1000 containers from this image:

- **Ubuntu layer**: Stored ONCE
- **Python layer**: Stored ONCE
- **App layer**: Stored ONCE
- **Runtime changes**: 1000 unique upper layers (small!)
