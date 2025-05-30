# What are Type Annotations?

Type annotations are a feature of Luau that allow you to define constraints to the variables in your code. They provide contextual clues to how your code is intended to be used, and blueprints for how to structure data. When these constraints are violated, warnings will be emitted by Luau’s analyzer suggesting that you fix them.

To make the most effective use of type annotations, **it’s highly recommended** that you add this comment to the top of your script:

```lua
--!strict
```

It ensures variables will always try to give you a properly inferred type instead of falling back to the default “`any`” type.

# [](https://devforum.roblox.com/t/type-annotations-a-guide-to-writing-luau-code-that-is-actually-good/2843221#basic-usage-3)Basic Usage

When you mouse over a variable, a tooltip should appear that describes what the variable’s type is.

```lua
local value = 0 -- Should report as [number]
local part = Instance.new("Part") -- Should report as [Part]
```

You can explicitly define the type of a variable by writing them as such:

```lua
local value: number = 0
local part: Part = Instance.new("Part")
```

When annotations are explicitly defined, they will emit warnings if you attempt to assign values to them which don’t match their defined types:

```lua
value = 5 -- good!
value = "lol" -- bad!

part = workspace -- bad!
part = Instance.new("SpawnLocation") -- good!
```

---

## [](https://devforum.roblox.com/t/type-annotations-a-guide-to-writing-luau-code-that-is-actually-good/2843221#null-types-and-refinement-4)Null Types and Refinement

Type names can be suffixed with a question mark (`?`) to mark them as potentially `nil`. For example, `Instance:FindFirstChild` returns a type of `Instance?` to indicate that it may not have found a child with the specified name.

```lua
-- `inst` has the inferred type: [Instance?]
local inst = workspace:FindFirstChild("Instance") 
```

Attempting to index the fields of a nullable type will produce a warning. You must conditionally evaluate the variable’s existence. The nice thing is that Luau will automatically refine the type on the spot when this evaluation happens.

**Consider the following example:**

```lua
local maybe: number? = nil -- (Imagine this is assigned a value somewhere)
```

There are several ways to refine the nullability of this type:

### [](https://devforum.roblox.com/t/type-annotations-a-guide-to-writing-luau-code-that-is-actually-good/2843221#option-1-inline-refinement-5)Option 1: Inline refinement

```lua
-- `maybePlus1` is evaluated as [number?]
local maybePlus1 = (maybe and maybe + 1) -- `maybe` refines to [number] past `and`
```

### [](https://devforum.roblox.com/t/type-annotations-a-guide-to-writing-luau-code-that-is-actually-good/2843221#option-2-if-statement-refinement-6)Option 2: If statement refinement

```lua
if maybePlus1 then
    -- `maybePlus1` refines to: [number] in this body.
    print("maybePlus1 is defined!", maybePlus1)
else
    -- `maybePlus1` is now refined to: [nil]
    print("maybePlus1 is nil!")
end
```

### [](https://devforum.roblox.com/t/type-annotations-a-guide-to-writing-luau-code-that-is-actually-good/2843221#option-3-return-or-breakcontinue-refinement-7)Option 3: Return (or break/continue) refinement

```lua
if not maybePlus1 then
    return
end

-- `maybePlus1` is now refined to: [number]
print("the maybePlus1 is real!!!", maybePlus1)
```

### [](https://devforum.roblox.com/t/type-annotations-a-guide-to-writing-luau-code-that-is-actually-good/2843221#option-4-assertion-refinement-8)Option 4: Assertion refinement

```lua
assert(maybePlus1, "maybePlus1 is not defined!") -- Will error if maybePlus1 is nil!

-- maybePlus1 is now refined to: [number]
print("maybePlus2:", maybePlus1 + 1)
```

---

## [](https://devforum.roblox.com/t/type-annotations-a-guide-to-writing-luau-code-that-is-actually-good/2843221#built-in-types-9)Built-in Types

Luau has 10 built-in type names defined:

- `nil`
- `string`
- `number`
- `thread`
- `boolean`
- `vector`
- `buffer`
- `any`
- `never`
- `unknown`

There are types for `function` and `table` as well, but they have a different structure which will be described later.

**The last 3 types:** `any`, `never`, and `unknown`, are special in that they don’t represent specific primitive types in Luau’s VM. They instead represent certain sets of all types in Luau:

### [](https://devforum.roblox.com/t/type-annotations-a-guide-to-writing-luau-code-that-is-actually-good/2843221#any-10)any

`any` can store any type of value, effectively muting the type annotation system. You shouldn’t use this unless you have no choice.

```lua
local value: any = 0
value = "lol" -- valid!
value = nil -- valid!
value = 2 -- valid!
```

### [](https://devforum.roblox.com/t/type-annotations-a-guide-to-writing-luau-code-that-is-actually-good/2843221#unknown-11)unknown

`unknown` **must** have it’s type evaluated through the `type`/`typeof` functions in order to be stored or used as any other variable type besides `unknown`. However, it can still be assigned to any value directly:

```lua
local value: unknown
value = "lol" -- valid!
value = nil -- valid!
value = 2 -- valid!

if type(value) == "number" then
    -- `value` is [number] in here
elseif type(value) == "string" then
    -- `value` is [string] in here
else
    -- `value` is [unknown] in here
end
```

### [](https://devforum.roblox.com/t/type-annotations-a-guide-to-writing-luau-code-that-is-actually-good/2843221#never-12)never

`never` cannot be refined into any type. It’s usually not defined directly, instead appearing when attempting to do a type refinement deemed impossible:

```lua
local value: unknown = true

if type(value) == "buffer" and type(value) == "boolean" then
    -- `value is now [never] because it cannot
    -- be a buffer and a boolean at the same time!
    print("This message will never print!", value)
end
```

## [](https://devforum.roblox.com/t/type-annotations-a-guide-to-writing-luau-code-that-is-actually-good/2843221#concrete-types-13)Concrete Types

Roblox’s Luau environment defines “_concrete_” types for each defined engine type in the [API Reference](https://create.roblox.com/docs/en-us/reference/engine).

Concrete types are statically defined and can extend from one another, but they **cannot be defined by Luau code** directly. They are declared by the Luau vendor (i.e. Roblox) at runtime.

Concrete types can be refined from `any`/`unknown` through the use of Luau’s `typeof` function:

```lua
local object: unknown

if typeof(object) == "Instance" then
    -- `object` is now refined to [Instance]
    print("object is an Instance:", object.Name)
else
    -- `object` is still [unknown]
    print("object type is not an Instance:", object)
end
```

All of Roblox’s top-level concrete types are listed in the [datatypes](https://create.roblox.com/docs/en-us/reference/engine/datatypes) documentation.

### [](https://devforum.roblox.com/t/type-annotations-a-guide-to-writing-luau-code-that-is-actually-good/2843221#refining-concrete-types-via-magic-functions-14)Refining Concrete Types via “Magic Functions”

Consider the following:

```lua
local part = Instance.new("Part")
print(typeof(part)) -- prints "Instance"
```

Why does this print _Instance_ instead of _Part_? Well, it turns out the `typeof` function will only describe **top-level concrete types**!

For concrete types that are _extensions_ of top-level concrete types, you’ll need to use certain _magic functions_ in Luau to refine these extended types. (_“Magic”_ in this case being a hack on the C++ end, but it works™)

An example of this is the `Object:IsA` function, which provides a mechanism for downcasting to inherited classes in the refined scope:

```lua
 -- `object` starts as [Instance?]
local object = workspace:FindFirstChild("Terrain")

if object then
    -- `object` is now refined to [Instance]
    print(object.Name)

    if object:IsA("BasePart") then
        -- `object` is now refined to [BasePart]
        print(object.Size)

        if object:IsA("Terrain") then
            -- `object` is now refined to [Terrain]
            print(object:CountCells())
        end

        -- `object` is once again [BasePart]
        print(object.Position)
    end

    -- `object` is once again [Instance]
    print(object.Parent)
end

-- `object` is once again [Instance?]
print(object ~= nil)
```

---

## [](https://devforum.roblox.com/t/type-annotations-a-guide-to-writing-luau-code-that-is-actually-good/2843221#function-types-15)Function Types

### [](https://devforum.roblox.com/t/type-annotations-a-guide-to-writing-luau-code-that-is-actually-good/2843221#arguments-16)Arguments

When declaring functions, you can annotate their arguments with types to make them more explicitly defined:

```lua
local function addNumbers(a: number, b: number)
    return a + b
end

addNumbers(5, 2) -- valid!
addNumbers(1) -- needs two arguments!
addNumbers("a", "b") -- argument types are wrong!
```

### [](https://devforum.roblox.com/t/type-annotations-a-guide-to-writing-luau-code-that-is-actually-good/2843221#return-types-17)Return Types

You can explicitly annotate a function’s return type:

```lua
local function toVector2(vec3: Vector3): Vector2
    return Vector2.new(vec3.X, vec3.Y)
end

local a: Vector2 = toVector2(Vector3.one) -- valid!
local b: number = toVector2(Vector3.one) -- wrong type for b!
local c = toVector2("lol") -- wrong argument type for vec3!
```

This is helpful when authoring a function knowing what it will return in advance. Luau will make sure to enforce that you’ve returned the correct type:

```lua
-- "not implemented yet!"
local function getNumber(object: Instance, name: string): number
    -- A warning will appear reporting that the 
    -- function doesn't always return a `number`
end
```

### [](https://devforum.roblox.com/t/type-annotations-a-guide-to-writing-luau-code-that-is-actually-good/2843221#tuples-18)Tuples

If you have a function that returns multiple values, you can wrap their return types in parentheses comma-separated as such:

```lua
local function getCFrameAndSize(part: BasePart?): (CFrame?, Vector3?)
    if part then
        return part.CFrame, part.Size
    end

    return -- explicit return is required
end
```

If your function doesn’t return anything, you can leave the contents of the parentheses empty:

```lua
local function reportIfPartFound(message: string): ()
    if workspace:FindFirstChildOfClass("Part") then
        print(message)
    end
end
```

### [](https://devforum.roblox.com/t/type-annotations-a-guide-to-writing-luau-code-that-is-actually-good/2843221#variadics-19)Variadics

You can typecheck variadic functions by annotating the `...` argument of the function:

```lua
local function debugPrint(...: unknown)
    if DEBUG then
        print(...)
    end
end
```

Functions that return a variable amount of some type can annotated as `...T`

```lua
local function gimmeSomeNumbers(): ...number
    if os.clock() % 2 > 1 then
        return 1, 2, 3
    else
        return 4, 5, 6, 7
    end
end
```

## [](https://devforum.roblox.com/t/type-annotations-a-guide-to-writing-luau-code-that-is-actually-good/2843221#function-type-annotating-20)Function Type Annotating

A function variable is type annotated by wrapping the typenames of the function’s arguments and return types in parenthesis, separated by an arrow `->`.

One basic example to start with is a function that takes no arguments and returns nothing. It would use the following type name: `() -> ()`

```lua
local noArgsOrReturn: () -> () = function()
	print("This function takes no arguments and returns nothing")
end

-- valid!
noArgsOrReturn = function()
	print("We can reassign the variable since we know its type!")
end

-- bad assignment: cannot convert a function with 1 arg into a function with no args.
noArgsOrReturn = function(arg: any)
	print(arg, "????")
end

-- ok, but invalid in practice. see below.
noArgsOrReturn = function()
	return "lol"
end

-- attempts to assign a variable to the "return" of this function
-- will warn that it's not supposed to return anything.
local value = noArgsOrReturn()

-- attempting to call it with arguments will also report
-- that it's not supposed to take arguments.
noArgsOrReturn("lol")
```

### [](https://devforum.roblox.com/t/type-annotations-a-guide-to-writing-luau-code-that-is-actually-good/2843221#annotating-arguments-and-returns-21)Annotating Arguments and Returns

Function arguments and return types are defined in a similar way to how they are directly declared. They also may be optionally given argument names to help contextualize their use:

```lua
local coolFunction: (part: BasePart) -> (CFrame, Vector3) = function (part)
    -- `part` is inferred as [BasePart]
    return part.CFrame, part.Size
end
```

### [](https://devforum.roblox.com/t/type-annotations-a-guide-to-writing-luau-code-that-is-actually-good/2843221#nullable-functions-22)Nullable Functions

If you want to define a function as nullable, you can put a question mark next to the return type:

```lua
local maybeFunc: (Instance, string) -> ()?

if maybeFunc then
    -- `maybeFunc` is now [(Instance, string) -> ()]
    maybeFunc()
end
```

**HOWEVER**, there are a few places where you need to be careful with how you define them.

For example: `(Instance, string) -> Part?` is not a nullable function type, it’s a function that returns a nullable `Part`. You can fix this by putting parenthesis in the right place:

`((Instance, string) -> Part)?`

### [](https://devforum.roblox.com/t/type-annotations-a-guide-to-writing-luau-code-that-is-actually-good/2843221#tupled-arguments-and-returns-23)Tupled Arguments and Returns

Functions that take variadic arguments are written as `...T`, and are not allowed to have a named argument:

```lua
local goodFunc: (format: string, ...any) -> ()? -- valid!
local badFunc: (format: string, args: ...any) -> ()? -- syntax error!
```

### [](https://devforum.roblox.com/t/type-annotations-a-guide-to-writing-luau-code-that-is-actually-good/2843221#functions-as-arguments-24)Functions as Arguments

You can define the type of a function argument as a function type annotation:

```lua
local function awaitChild(object: Instance, name: string, andThen: (child: Instance) -> ())
    task.spawn(function()
        local child = object:WaitForChild(name)
        andThen(child)
    end)
end
```

---

## [](https://devforum.roblox.com/t/type-annotations-a-guide-to-writing-luau-code-that-is-actually-good/2843221#arrays-25)Arrays

Arrays in Luau’s type checker are defined by wrapping a type name in curly braces `{}`. For example, the return type of `Instance:GetChildren()` is defined as `{ Instance }`

```lua
local objects = workspace:GetChildren() -- objects has type: [{Instance}]

for i, child in objects do
    -- child is [Instance]
    print(child.Name)
end
```

You can define what kind of values an array expects by annotating their type:

```lua
local t: {number} = {}
table.insert(t, 5) -- good!
table.insert(t, "lol") -- invalid!
```

## [](https://devforum.roblox.com/t/type-annotations-a-guide-to-writing-luau-code-that-is-actually-good/2843221#dictionaries-26)Dictionaries

Dictionary types are a bit more in-depth. There are two ways you can define dictionary fields, both of which can be used at the same time.

### [](https://devforum.roblox.com/t/type-annotations-a-guide-to-writing-luau-code-that-is-actually-good/2843221#indexer-type-27)Indexer Type

Array types in Luau are actually just a shorthand for a `number` dictionary indexer. In practice this means `{T}` is a shorthand for `{ [number]: T }` which is how dictionary indexers are defined:

```lua
local t = {} :: {
    [number]: number
}

table.insert(t, 5) -- good!
table.insert(t, "lol") -- invalid!

t[1] = 2 -- good!
t.lol = 3 -- invalid!
t[Vector3.zero] = 4 -- invalid!
```

(Note: The typecast operator `::` will be explained more later, it’s being used here to make the table declaration look a little cleaner)

You can define the indexer to be any type! For example, here’s a way to map `Player` objects to their positions:

```lua
--!strict
local Players = game:GetService("Players")

local positionMap = {} :: {
    [Player]: Vector3?
}

local function onPlayerRemoving(player: Player)
    -- This assignment is valid because we're removing
    -- the player from the dictionary index.
    positionMap[player] = nil
end

local function updatePositions()
    for i, player in Players:GetPlayers() do
        -- Character is a reference, so its type is [Model?]
        local character = player.Character

        if character then
            local cf = character:GetPivot()
            positionMap[player] = cf.Position
        end
    end
end

Players.PlayerRemoving:Connect(onPlayerRemoving)
```

### [](https://devforum.roblox.com/t/type-annotations-a-guide-to-writing-luau-code-that-is-actually-good/2843221#explicit-fields-type-declarations-28)Explicit Fields & Type Declarations

Type declarations are a core feature of Luau that I’ve refrained from talking about so far because their best use case is with dictionaries. You can use them to create concisely shaped structures for your tables!

```lua
type SimpleType = {
    Number: number,
    String: string,
    Function: (...any) -> (...any),
}

local value: SimpleType = {
    Number = 0,
    String = "lol",
    Function = print,
}
```

Dictionaries are types in the same way that functions and other primitives are types.  
If you want to declare a table that starts nil but will exist later, you can do that!

```lua
--!strict

local pendingData = nil :: {
    Player: Player,
    UserId: number,
    Coins: number,
}? -- Question mark is important!

local Players = game:GetService("Players")
local player = assert(Players.LocalPlayer)

local userId = player.UserId
local coins = math.random(1, 1000)

pendingData = {
    Player = player,
    UserId = userId,
    Coins = coins,
}
```

Here are a few real use-cases:

```lua
-- This is an entry in the array returned by `HumanoidDescription:GetAccessories`
type AccessoryInfo = {
    AccessoryType: Enum.AccessoryType,
    AssetId: number,
    IsLayered: boolean,
    Order: number?,
    Puffiness: number?,
}

-- With this, we can iterate over the contents of the table with a type annotation!
local accessories: { AccessoryInfo } = hDesc:GetAccessories(true)

for i, info in accessories do
    -- Inferred type of `info` is [AccessoryInfo]
    print("Got accessory with type", info.AccessoryType, "and AssetId", info.AssetId)

    if info.IsLayered then
        print("\tAccessory is layered! Order is:", assert(info.Order))
    end
end
```

## [](https://devforum.roblox.com/t/type-annotations-a-guide-to-writing-luau-code-that-is-actually-good/2843221#using-the-typeof-function-in-type-declarations-29)Using the `typeof` function in type declarations

In Roblox, `Instances` have parent->child relations bound to the `DataModel`, relative to the `script` and `game` variables. If you get a reference to an `Instance`, you can directly access the children and parent of that instance through auto-complete.

Lets say you have a template object that has some children in it, and you want to clone this template object and use it as a type so the cloned children can be accessed later. This is where Luau’s `typeof` function comes in handy.

```lua
local template = script.Template
type Template = typeof(template)

local function createTemplate(): Template
    return template:Clone()
end
```

This type can be used in dictionaries, arrays, functions, pretty much any context you would normally expect a Luau type to work against.

**The only caveat** is that, at least in the present moment, the `Parent` property may emit warnings disagreeing with where you parent the object to because it expects the parent to be the same class as its source parent.

If this ever happens, you may have to typecast the new parent to `any` to work around it:

```lua
local new = createTemplate()
new.Parent = workspace :: any
```

## [](https://devforum.roblox.com/t/type-annotations-a-guide-to-writing-luau-code-that-is-actually-good/2843221#prototype-based-classes-30)Prototype-based Classes

Metatables can facilitate artificial object-oriented classes, and they are supported in Luau’s type annotations! The syntax for it is a little strange, but the benefits of it outweigh the quirkiness by a long shot.

Here’s a simple `Person` ModuleScript example to start with:

```lua
--!strict

local Person = {}
Person.__index = Person

export type Class = typeof(setmetatable({} :: {
    FirstName: string,
    LastName: string,
}, Person))

function Person.new(firstName: string, lastName: string): Class
    return setmetatable({
        FirstName = firstName,
        LastName = lastName,
    }, Person)
end

function Person.GetFullName(self: Class): string
    return `{self.FirstName} {self.LastName}`
end

return Person
```

What exactly did we just do here? Don’t worry, I’ll run through it step by step.  
(Note: These descriptions cite [Roblox’s Lua Style guide](https://roblox.github.io/lua-style-guide/#prototype-based-classes), which didn’t overcomplicate the description as much as I previously did.)

### [](https://devforum.roblox.com/t/type-annotations-a-guide-to-writing-luau-code-that-is-actually-good/2843221#self-referencing-metatable-31)Self-referencing Metatable

```lua
local Person = {}
Person.__index = Person
```

This is a neat trick that allows the module definition itself to be the metatable of the created `Person` instances.

### [](https://devforum.roblox.com/t/type-annotations-a-guide-to-writing-luau-code-that-is-actually-good/2843221#declaring-the-shape-of-our-class-32)Declaring the “Shape” of our Class.

```lua
export type Class = typeof(setmetatable({} :: {
    FirstName: string,
    LastName: string,
}, Person))
```

This syntax creates a type definition that matches metatable-backed instances of our module. It defines the shape of the instance and what fields either can, or need to be defined in its data.

The first argument to `setmetatable` molds the type of the instance, and the second argument binds the `Person` module as the instance’s metatable. This is all wrapped in `typeof()`, which (in the context of type annotations) extracts the evaluated type of what was passed into it.

### [](https://devforum.roblox.com/t/type-annotations-a-guide-to-writing-luau-code-that-is-actually-good/2843221#putting-it-into-practice-33)Putting it into practice

With all of that out of the way, now you can require this `Person` module from another script, import its `Class` type, and use it in both functions and dictionary types as we see fit!

Here’s a super lazy example of a `School` using the `Person` type we created:

```lua
--!strict
local Person = require(script.Parent.Person)
type Person = Person.Class

type School = {
    Name: string,
    Principal: Person,
    
    Teachers: { Person },
    Students: { Person },
}

local function addTeacher(school: School, student: Person)
    table.insert(school.Teachers, student)
end

local function addStudent(school: School, student: Person)
    table.insert(school.Students, student)
end

local coolSchool: School = {
    Name = "Hella Cool School",
    Principal = Person.new("John", "Doe"),

    Teachers = {},
    Students = {},    
}

local janeDoe = Person.new("Jane", "Doe")
addStudent(coolSchool, janeDoe)

local coolTeacher = Person.new("Cool", "Teacher")
addTeacher(coolSchool, coolTeacher)

----------------------------------------------------------------------------

local function printSchoolInfo(school: School)
    print("School Name:", school.Name)
    print("Principal:", school.Principal:GetFullName())

    print("Teachers:")
    for i, teacher in school.Teachers do
        print(`\t{teacher:GetFullName()}`)
    end

    print("Students:")
    for i, student in school.Students do
        print(`\t{student:GetFullName()}`)
    end
end

printSchoolInfo(coolSchool)

----------------------------------------------------------------------------
```

## [](https://devforum.roblox.com/t/type-annotations-a-guide-to-writing-luau-code-that-is-actually-good/2843221#typecasting-34)Typecasting

So what was the deal with that `::` operator earlier? This is a feature of Luau called typecasting, which allows you to override what the automatically inferred type of a value is.

Typecasts are allowed if the provided type can be converted into the target type. There are a few rules and points to be made of this:

- All types can be casted into `any`/`unknown`/`never`. Likewise, `any`/`unknown`/`never` can be casted into any type.
    - Do this with caution understanding what you’re trying to do, because this effectively bypasses Luau’s type contracting and puts the responsibility onto you and whoever may maintain your code in the future to ensure it complies.
- Untyped empty tables can be casted into any _indexer table_.
    - As soon as Luau gets a contextual clue to what the type is, the type will become inferred and cannot be inferred as another type.
- Concrete types can be casted up into their base classes (i.e. `BasePart` → `PVInstance` → `Instance`), but not the other way around.

### [](https://devforum.roblox.com/t/type-annotations-a-guide-to-writing-luau-code-that-is-actually-good/2843221#use-cases-35)Use Cases

#### [](https://devforum.roblox.com/t/type-annotations-a-guide-to-writing-luau-code-that-is-actually-good/2843221#inline-typing-36)Inline Typing

Consider the following untyped definition:

```lua
local data = {
    Kills = {},
    Deaths = {},
}
```

If we want to convert this to type annotations, we _could_ declare the type explicitly like this:

```lua
type PlayersData = {
    Kills: {
        [Player]: number
    },
    Deaths: {
        [Player]: number
    },
}

local data: PlayersData = {
    Kills = {},
    Deaths = {},
}
```

This is fine, but we might only use this `PlayersData` type annotation once for the `data` variable, so we could just inline the type instead of defining a type alias for it:

```lua
local data: {
    Kills: {
        [Player]: number
    },
    Deaths: {
        [Player]: number
    },
} = {
    Kills = {},
    Deaths = {},
}
```

As you can see though… this looks a little bit rough. It’s not very hygenic to have a multi-line type inline like this.

This is where typecasting empty tables comes in handy:

```lua
local data = {
    Kills = {} :: {
        [Player]: number
    },

    Deaths = {} :: {
        [Player]: number
    },
}
```

Now we effectively have the same type behavior, but in a more compact and readable structure on-site!

### [](https://devforum.roblox.com/t/type-annotations-a-guide-to-writing-luau-code-that-is-actually-good/2843221#unsafe-dynamic-access-37)Unsafe Dynamic Access

At the moment, Luau warns when trying to perform dynamic table indexing on concrete types. If you absolutely know what you’re doing is fine, you can use a cast to `any` to get around this.

For example:

```lua
local bodyColors = Instance.new("BodyColors")

for i, bodyPart in Enum.BodyPart:GetEnumItems() do
    (bodyColors :: any)[`{bodyPart.Name}Color3`] = Color3.new(1, 0, 0)
end
```

# [](https://devforum.roblox.com/t/type-annotations-a-guide-to-writing-luau-code-that-is-actually-good/2843221#thats-all-smallfor-nowsmall-folks-38)That’s all (for now) folks!

This isn’t every aspect of Luau, but it’s a lot of the core stuff I desperately felt was in need of a full proper best-practices tutorial. I’ll definitely update this more in the future if people would like to see more areas covered (such as generics and type unioning).

Feel free to check out Roblox’s official typechecking documentation as well for coverage of additional things I may not have covered here yet: [Type checking - Luau](https://luau-lang.org/typecheck)

If it’s any help, I also have a few open source projects and modules that are fully `--!strict`