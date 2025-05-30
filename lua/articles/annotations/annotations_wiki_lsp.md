> ⚠️ **Warning**
>
> This wiki has been replaced by the wiki on [our website](https://luals.github.io/wiki/annotations). This wiki will be removed in the future.

# Annotations
The language server does its best to infer types through contextual analysis, however, sometimes manual documentation is necessary to improve completion and signature information.

Annotations are prefixed with `---`, like a Lua comment with one extra dash. To learn more, check out [Formatting Annotations](https://github.com/LuaLS/lua-language-server/wiki/Formatting-Annotations).

![](https://user-images.githubusercontent.com/1073877/111884243-a337c780-89c0-11eb-856e-b6c3b1042810.gif)

> **Note**
> The annotations used by the server are based off of [EmmyLua annotations](https://emmylua.github.io/annotation.html) but a [rename is in progress](https://github.com/LuaLS/lua-language-server/discussions/1587).

> ⚠️ Warning: The annotations used by the server are [no longer cross-compatible](https://github.com/LuaLS/lua-language-server/issues/980) with [EmmyLua annotations](https://emmylua.github.io/annotation.html) since `v3.0.0`.

The annotations are also described in `script.lua` which can be found in multiple languages in [`locale/`](https://github.com/LuaLS/lua-language-server/blob/master/locale). Corrections and translations can be provided in these `script.lua` files and submitted through a [pull request](https://github.com/LuaLS/lua-language-server/pulls).


## Tips
- If you type `---` one line above a function, you will receive a suggested snippet that includes `@param` and `@return` annotations for each parameter and return value found in the function. ![](https://user-images.githubusercontent.com/61925890/183302905-32daa693-1da6-4d62-a10c-40f018b1eb5b.png)


## Documenting Types
Properly documenting types with the language server is very important and where a lot of the features and advantages are. Below is a list of all recognized Lua types (regardless of [version in use](https://github.com/LuaLS/lua-language-server/wiki/Settings#runtimeversion)):

- `nil`
- `any`
- `boolean`
- `string`
- `number`
- `integer`
- `function`
- `table`
- `thread`
- `userdata`
- `lightuserdata`

You can also simulate [classes](https://github.com/LuaLS/lua-language-server/wiki/Annotations#class) and [fields](https://github.com/LuaLS/lua-language-server/wiki/Annotations#field) and even [create your own types](https://github.com/LuaLS/lua-language-server/wiki/Annotations#alias).

Adding a question mark `?` after a type like `boolean?` or `number?` is the same as saying `boolean|nil` or `number|nil`. This can be used to specify that something is either a specified type **or** nil. This can be very useful for function returns where a value **or** nil can be returned.

Below is a list of how you can document more advanced types:

|      Type       |               Document As                |
| :-------------: | :--------------------------------------: |
|   Union Type    |            `TYPE_1 \| TYPE_2`            |
|      Array      |              `VALUE_TYPE[]`              |
|   Dictionary    |        `{ [string]: VALUE_TYPE }`        |
| Key-Value Table |      `table<KEY_TYPE, VALUE_TYPE>`       |
|  Table Literal  | `{ key1: VALUE_TYPE, key2: VALUE_TYPE }` |
|    Function     |     `fun(PARAM: TYPE): RETURN_TYPE`      |

Unions may need to be placed in parentheses in certain situations, such as when defining an array that contains multiple value types:
```lua
---@type (string | integer)[]
local myArray = {}
```


## Understanding This Page
To get an understanding of how to use the annotations described on this page, you'll need to know how to read the `Syntax` sections of each annotation.

|           Symbol           |               Meaning                |
| :------------------------: | :----------------------------------: |
|       `<value_name>`       |  A required value that you provide   |
|       `[value_name]`       |    Everything inside is optional     |
|     `[value_name...]`      |       This value is repeatable       |
| `value_name \| value_name` | The left **or** right side are valid |

Any other symbols are syntactically required and should be copied verbatim.

If this is confusing, take a look at a couple examples under an annotation and it should make more sense.

## Annotations List
Below is a list of all annotations recognized by the language server:


### `@alias`
An alias can be useful when re-using a type. It can also be used to provide an enum. If you are looking for an enum and already have the values defined in a Lua table, take a look at [`@enum`](https://github.com/LuaLS/lua-language-server/wiki/Annotations#enum).

**Syntax**

`---@alias <name> <type>`

or

```lua
---@alias <name>
---| '<value>' [# description]
```

> **Note**
> The above pipe character (`|`) on the left is necessary for each line and does not signify an "or".

**Examples**
<details>
<summary>Simple Alias</summary>

```lua
---@alias userID integer The ID of a user
```
</details>

<details>
<summary>Custom Type</summary>

```lua
---@alias modes "r" | "w"
```

</details>

<details>
<summary>Custom Type with Descriptions</summary>

```lua
---@alias side
---| '"left"' # The left side of the device
---| '"right"' # The right side of the device
---| '"top"' # The top side of the device
---| '"bottom"' # The bottom side of the device
---| '"front"' # The front side of the device
---| '"back"' # The back side of the device

---@param side side
local function checkSide(side) end
```

</details>

<details>
<summary>Literal Custom Type</summary>

```lua
local A = "Hello"
local B = "World"

---@alias myLiteralAlias `A` | `B`

---@param x myLiteralAlias
function foo(x) end
```

</details>

<details>
<summary>Literal Custom Type with Descriptions</summary>

```lua
local A = "Hello"
local B = "World"

---@alias myLiteralAliases
---|`A` # Will offer completion for A, which has a value of "Hello"
---|`B` # Will offer completion for B, which has a value of "World"

---@param x myLiteralAliases
function foo(x) end
```

</details>

![alias](https://user-images.githubusercontent.com/61925890/181307619-fce11318-7b2a-490c-8c03-e935438e3b1a.png)

<br>

### `@as`
Force a type onto an expression.

> ⚠️ Warning: This annotation cannot be added using `---@as <type>` - it must be done like `--[[@as <type>]]`.

> **Note**
> When marking an expression as an array, such as `string[]`, you must use `--[=[@as string[]]=]` due to the extra square brackets causing parsing issues.

**Syntax**

`--[[@as <type>]]`

> **Note**
> The square brackets in the above syntax definition do not refer to it being optional. Those square brackets must be used verbatim.

**Examples**
<details>
<summary>Override Type</summary>

```lua
---@param key string Must be a string
local function doSomething(key) end

local x = nil

doSomething(x --[[@as string]])
```

</details>

![as](https://user-images.githubusercontent.com/61925890/181307718-cb0e7fa1-6cf1-48be-a97f-46a1a99d8997.png)

<br>

### `@async`
Mark a function as being asynchronous. When [`hint.await`](https://github.com/LuaLS/lua-language-server/wiki/Settings#hintawait) is `true`, functions marked with `@async` will have an `await` hint displayed next to them. Used by diagnostics from the [`await` group](https://github.com/LuaLS/lua-language-server/wiki/Diagnostics#await).

**Syntax**

`---@async`

**Examples**
<details>
<summary>Asynchronous Declaration</summary>

```lua
---@async
---Perform an asynchronous HTTP GET request
function http.get(url) end
```

</details>

![async](https://user-images.githubusercontent.com/61925890/181307740-22ad1d85-f132-492a-a2c9-c7969cc53637.png)

<br>

### `@cast`
Cast a variable to a different type or types

**Syntax**

`---@cast <value_name> [+|-]<type|?>[, [+|-]<type|?>...]`

**Examples**
<details>
<summary>Simple Cast</summary>

```lua
---@type integer
local x

---@cast x string
print(x) --> x: string
```

</details>

<details>
<summary>Add Type</summary>

```lua
---@type integer
local x

---@cast x +boolean
print(x) --> x: integer | boolean
```

</details>

<details>
<summary>Remove Type</summary>

```lua
---@type integer|string
local x

---@cast x -integer
print(x) --> x: string
```

</details>

<details>
<summary>Cast multiple types</summary>

```lua
---@type string
local x --> x: string

---@cast x +boolean, +number
print(x) --> x:string | boolean | number
```

</details>

<details>
<summary>Cast unknown</summary>

```lua
---@type string
local x

---@cast x +?
print(x) --> x:string?
```

</details>

<br>

### `@class`
Define a class. Can be used with [`@field`](https://github.com/LuaLS/lua-language-server/wiki/Annotations#field) to define a table structure. Once a class is defined, it can be used as a type for [parameters](https://github.com/LuaLS/lua-language-server/wiki/Annotations#param), [returns](https://github.com/LuaLS/lua-language-server/wiki/Annotations#return), and more. A class can also inherit from a parent class.

**Syntax**

`---@class <name>[: <parent>]`

**Examples**
<details>
<summary>Define a Class</summary>

```lua
---@class Car
local Car = {}
```

</details>

<details>
<summary>Class Inheritance</summary>

```lua
---@class Vehicle
local Vehicle = {}

---@class Plane: Vehicle
local Plane = {}
```

</details>

<br>

### `@deprecated`
Mark a function as deprecated. This will trigger the [`deprecated` diagnostic](https://github.com/LuaLS/lua-language-server/wiki/Diagnostics#deprecated), displaying it as ~~struck through~~.

**Syntax**

`---@deprecated`

**Examples**
<details>
<summary>Mark function as deprecated</summary>

```lua
---@deprecated
function outdated() end
```

</details>

<br>

### `@diagnostic`
Toggle [diagnostics](https://github.com/LuaLS/lua-language-server/wiki/Diagnostics) for the next line, current line, or whole file.

**Syntax**
<code>---@diagnostic &lt;state&gt;:&lt;<a href="https://github.com/LuaLS/lua-language-server/wiki/Diagnostics">diagnostic</a>&gt;</code>

`state` options:
- `disable-next-line` (Disable diagnostic on the following line)
- `disable-line` (Disable diagnostic on this line)
- `disable` (Disable diagnostic in this file)
- `enable` (Enable diagnostic in this file)

**Examples**
<details>
<summary>Disable diagnostic on next line</summary>

```lua
---@diagnostic disable-next-line: unused-local
```
![](https://user-images.githubusercontent.com/1073877/112364413-c4f1c100-8cd6-11eb-88a0-e45a56953e76.gif)

</details>

<details>
<summary>Enable spell checking in this file</summary>

```lua
---@diagnostic enable:spell-check
```

</details>

<br>

### `@enum`
Mark a Lua table as an enum, giving it similar functionality to [`@alias`](https://github.com/LuaLS/lua-language-server/wiki/Annotations#alias), only the table is still usable at runtime.

[View Original Request](https://github.com/LuaLS/lua-language-server/issues/1255)

**Syntax**

`---@enum <name>`

**Examples**
<details>
<summary>Define table as enum</summary>

```lua
---@enum colors
local COLORS = {
	black = 0,
	red = 2,
	green = 4,
	yellow = 8,
	blue = 16,
	white = 32
}

---@param color colors
local function setColor(color) end

setColor(COLORS.green)
```

![enum](https://user-images.githubusercontent.com/61925890/181307783-532fdd86-6004-4483-9d81-2c822c01fa51.png)

</details>

<br>

### `@field`
Define a field within a table. Should be immediately following a [`@class`](https://github.com/LuaLS/lua-language-server/wiki/Annotations#class). As of `v3.6.0`, you can mark a field as `private`, `protected`, `public`, or `package`.

**Syntax**

> **Note**
> `\[` and `\]` below mean literal `[` and `]`

<br>

`---@field [scope] <name> <type> [description]`
<br>
`---@field [scope] \[<type>\] <type> [description]`

**Examples**
<details>
<summary>Simple documentation of class</summary>

```lua
---@class Person
---@field height number The height of this person in cm
---@field weight number The weight of this person in kg
---@field firstName string The first name of this person
---@field lastName string The last name of this person
---@field age integer The age of this person

---@param person Person
local function hire(person) end
```

</details>

![field](https://user-images.githubusercontent.com/61925890/181307814-81f14004-db8a-4f17-af40-03dd27673648.gif)

<details>
<summary>Mark field as private</summary>

```lua
---@class Animal
---@field private legs integer
---@field eyes integer

---@class Dog:Animal
local myDog = {}

---Child class Dog CANNOT use private field legs
function myDog:legCount()
	return self.legs
end
```

</details>

<details>
<summary>Mark field as protected</summary>

```lua
---@class Animal
---@field protected legs integer
---@field eyes integer

---@class Dog:Animal
local myDog = {}

---Child class Dog can use protected field legs
function myDog:legCount()
	return self.legs
end
```

</details>

<details>
<summary>Typed field</summary>

> **Note**
> Named fields must be declared before typed field if type is string

```lua
---@class Numbers
---@field named string
---@field [string] integer
local Numbers = {}
```

</details>

<br>

### `@generic`
Generics allow code to be reused and serve as a sort of "placeholder" for a type. Surrounding the generic in backticks (`` ` ``) will capture the value and use it for the type. [Generics are still WIP](https://github.com/LuaLS/lua-language-server/issues/1861).

**Syntax**

`---@generic <name> [:parent_type] [, <name> [:parent_type]]`

**Examples**
<details>
<summary>Generic Function</summary>

```lua
---@generic T : integer
---@param p1 T
---@return T, T[]
function Generic(p1) end

-- v1: string
-- v2: string[]
local v1, v2 = Generic("String")

-- v3: integer
-- v4: integer[]
local v3, v4 = Generic(10)
```

</details>

<details>
<summary>Capture with Backticks</summary>

```lua
---@class Vehicle
local Vehicle = {}
function Vehicle:drive() end

---@generic T
---@param class `T` # the type is captured using `T`
---@return T       # generic type is returned
local function new(class) end

-- obj: Vehicle
local obj = new("Vehicle")
```

</details>

<details>
<summary>How the Table Class is Implemented</summary>

```lua
---@class table<K, V>: { [K]: V }
```

</details>

<details>
<summary>Array Class Using Generics</summary>

```lua
---@class Array<T>: { [integer]: T }

---@type Array<string>
local arr = {}

-- Warns that I am assigning a boolean to a string
arr[1] = false

arr[3] = "Correct"
```

See [#734](https://github.com/LuaLS/lua-language-server/issues/734#issuecomment-1436317116)

</details>

<details>
<summary>Dictionary class using generics</summary>

```lua
---@class Dictionary<T>: { [string]: T }

---@type Dictionary<boolean>
local dict = {}

-- no warning despite assigning a string
dict["foo"] = "bar?"

dict["correct"] = true
```

See [#734](https://github.com/LuaLS/lua-language-server/issues/734#issuecomment-1436317116)

</details>

<br>

### `@meta`
Marks a file as "meta", meaning it is used for definitions and not for its functional Lua code. Used internally by the language server for defining the built-in Lua libraries. If you are [writing your own definition files](https://github.com/LuaLS/lua-language-server/wiki/Libraries#custom), you will probably want to include this annotation in them. If you specify a name, it will only be able to be required by the given name. Giving the name `_` will make it unable to be required. Files with the `@meta` tag in them behave a little different:

- Completion will not display context in a meta file
- Hovering a `require` of a meta file will show `[meta]` instead of its absolute path
- `Find Reference` ignores meta files

**Syntax**

`---@meta [name]`

**Examples**
<details>
<summary>Mark Meta File</summary>

```lua
---@meta
```

</details>

<br>

### `@module`
Simulates `require`-ing a file.

**Syntax**

`---@module '<module_name>'`

**Examples**
<details>
<summary>"Require" a File</summary>

```lua
---@module 'http'

--The above provides the same as
require 'http'
--within the language server
```

</details>

<details>
<summary>"Require" a File and Assign to a Variable</summary>

```lua
---@module 'http'
local http

--The above provides the same as
local http = require 'http'
--within the language server
```

</details>

<br>

### `@nodiscard`
Mark a function as having return values that **cannot** be ignored/discarded. This can help users understand how to use the function as if they do not capture the returns, a warning will be raised.

**Syntax**

`---@nodiscard`

**Examples**
<details>
<summary>Prevent Ignoring a Function's Returns</summary>

```lua
---@return string username
---@nodiscard
function getUsername() end
```

</details>

<br>

### `@operator`
Provides type declarations for an [operator metamethod](http://lua-users.org/wiki/MetatableEvents).

[View Original Request](https://github.com/LuaLS/lua-language-server/issues/599)

**Syntax**

`---@operator <operation>[(input_type)]:<resulting_type>`

> ℹ️ Note: This syntax differs slightly from the `fun()` syntax used for defining functions. Notice that the parentheses are **optional** here, so `@operator call:integer` is valid.

**Examples**
<details>
<summary>Declare <code>__add</code> Metamethod</summary>

```lua
---@class Vector
---@operator add(Vector): Vector

---@type Vector
local v1
---@type Vector
local v2

--> v3: Vector
local v3 = v1 + v2
```

</details>

<details>
<summary>Declare Unary Minus Metamethod</summary>

```lua
---@class Passcode
---@operation unm:integer

---@type Passcode
local pA

local pB = -pA
--> integer
```

</details>

<details>
<summary>Declare <code>__call</code> Metamethod</summary>

> ℹ️ Note: it is recommended to instead use [@overload](#overload) to specify the call signature for a class.

```lua
---@class URL
---@operator call:string
local URL = {}
```

</details>

<br>

### `@overload`
Define an additional signature for a function. This does not allow descriptions to be provided for the new signature being defined - if you want descriptions, you are better off writing out an entire `function` with the same name but different [`@param`](https://github.com/LuaLS/lua-language-server/wiki/Annotations#param) and [`@return`](https://github.com/LuaLS/lua-language-server/wiki/Annotations#return) annotations.

**Syntax**

`---@overload fun([param: type[, param: type...]]): [return_value[, return_value]]`

**Examples**
<details>
<summary>Define Function Overload</summary>

```lua
---@param objectID integer The id of the object to remove
---@param whenOutOfView boolean Only remove the object when it is not visible
---@return boolean success If the object was successfully removed
---@overload fun(objectID: integer): boolean
local function removeObject(objectID, whenOutOfView) end
```

</details>

<details>
<summary>Define Class Call Signature</summary>

```lua
---@overload fun(a: string): boolean
local foo = setmetatable({}, {
	__call = function(a)
		print(a)
        return true
	end,
})

local bool = foo("myString")
```

</details>

<br>

### `@package`
Mark a function as private to the file it is defined in. A packaged function cannot be accessed from another file.

**Syntax**

`---@package`

**Examples**
<details>
<summary>Mark a function as package-private</summary>

```lua
---@class Animal
---@field private eyes integer
local Animal = {}

---@package
---This cannot be accessed in another file
function Animal:eyesCount()
    return self.eyes
end
```

</details>

<br>

### `@param`
Define a parameter for a function. This tells the language server what types are expected and can help enforce types and provide completion. Putting a question mark (`?`) after the parameter name will mark it as optional, meaning `nil` is an accepted type. The `type` provided can be an [`@alias`](https://github.com/LuaLS/lua-language-server/wiki/Annotations#alias), [`@enum`](https://github.com/LuaLS/lua-language-server/wiki/Annotations#enum), or [`@class`](https://github.com/LuaLS/lua-language-server/wiki/Annotations#class) as well.

**Syntax**

`---@param <name[?]> <type[|type...]> [description]`

**Examples**
<details>
<summary>Simple Function Parameter</summary>

```lua
---@param username string The name to set for this user
function setUsername(username) end
```

</details>

<details>
<summary>Parameter Union Type</summary>

```lua
---@param setting string The name of the setting
---@param value string|number|boolean The value of the setting
local function settings.set(setting, value) end
```

</details>

<details>
<summary>Optional Parameter</summary>

```lua
---@param role string The name of the role
---@param isActive? boolean If the role is currently active
---@return Role
function Role.new(role, isActive) end
```

</details>

<details>
<summary>Variable Number of Parameters</summary>

```lua
---@param index integer
---@param ... string Tags to add to this entry
local function addTags(index, ...) end
```
</details>

<details>
<summary>Generic Function Parameter</summary>

```lua
---@class Box

---@generic T
---@param objectID integer The ID of the object to set the type of
---@param type `T` The type of object to set
---@return `T` object The object as a Lua object
local function setObjectType(objectID, type) end

--> boxObject: Box
local boxObject = setObjectType(1, "Box")
```

See [`@generic`](https://github.com/LuaLS/lua-language-server/wiki/Annotations#generic) for more info.

</details>

<details>
<summary>Custom Type Parameter</summary>

```lua
---@param mode string
---|"'immediate'"  # comment 1
---|"'async'" # comment 2
function bar(mode) end
```

</details>

<details>
<summary>Literal Custom Type Parameter</summary>

```lua
local A = 0
local B = 1

---@param active integer
---| `A` # Has a value of 0
---| `B` # Has a value of 1
function set(active) end
```
Looking to do this with a table? You probably want to use [`@enum`](https://github.com/LuaLS/lua-language-server/wiki/Annotations#enum)

</details>

<br>

### `@private`
Mark a function as private to a [`@class`](https://github.com/LuaLS/lua-language-server/wiki/Annotations#class). Private functions can be accessed only from within their class and are **not** accessable from child classes.

**Syntax**

`---@private`

**Examples**
<details>
<summary>Mark a function as private</summary>

```lua
---@class Animal
---@field private eyes integer
local Animal = {}

---@private
function Animal:eyesCount()
    return self.eyes
end

---@class Dog:Animal
local myDog = {}

---NOT PERMITTED!
myDog:eyesCount();
```

</details>

<br>

### `@protected`
Mark a function as protected within a [`@class`](https://github.com/LuaLS/lua-language-server/wiki/Annotations#class). Protected functions can be accessed only from within their class or from child classes.

**Syntax**

`---@protected`

**Examples**
<details>
<summary>Mark a function as protected</summary>

```lua
---@class Animal
---@field private eyes integer
local Animal = {}

---@protected
function Animal:eyesCount()
    return self.eyes
end

---@class Dog:Animal
local myDog = {}

---Permitted because function is protected, not private.
myDog:eyesCount();
```

</details>

<br>

### `@return`
Define a `return` value for a function. This tells the language server what types are expected and can help enforce types and provide completion.

**Syntax**

`---@return <type> [<name> [comment] | [name] #<comment>]`

**Examples**
<details>
<summary>Simple Function Return</summary>

```lua
---@return boolean
local function isEnabled() end
```

</details>

<details>
<summary>Named Function Return</summary>

```lua
---@return boolean enabled
local function isEnabled() end
```

</details>

<details>
<summary>Named, Described Function Return</summary>

```lua
---@return boolean enabled If the item is enabled
local function isEnabled() end
```

</details>

<details>
<summary>Described Function Return</summary>

```lua
---@return boolean # If the item is enabled
local function isEnabled() end
```

</details>

<details>
<summary>Optional Function Return</summary>

```lua
---@return boolean|nil error
local function makeRequest() end
```

</details>

<details>
<summary>Variable Function Returns</summary>

```lua
---@return integer count Number of nicknames found
---@return string ...
local function getNicknames() end
```

</details>

<br>

### `@see`
Currently has no function other than allowing you to add a basic comment. This is not shown when hovering and has no additional functionality [yet](https://github.com/LuaLS/lua-language-server/issues/1344).

**Syntax**

`---@see`

**Examples**
<details>
<summary>Basic Usage</summary>

```lua
---@see http.get
function request(url) end
```

</details>

<br>

### `@source`
Provide a reference to some source code which lives in another file. When
searching for the defintion of an item, its `@source` will be used.

**Syntax**

`@source <path>`

**Examples**
<details>
<summary>Link to file using absolute path</summary>

```lua
---@source C:/Users/me/Documents/program/myFile.c
local a
```

</details>

<details>
<summary>Link to file using URI</summary>

```lua
---@source file:///C:/Users/me/Documents/program/myFile.c:10
local b
```

</details>

<details>
<summary>Link to file using relative path</summary>

```lua
---@source local/file.c
local c
```

</details>

<details>
<summary>Link to line and character in file</summary>

```lua
---@source local/file.c:10:8
local d
```

</details>

<br>

### `@type`
Mark a variable as being of a certain type. Union types are separated with a pipe character `|`. The `type` provided can be an [`@alias`](https://github.com/LuaLS/lua-language-server/wiki/Annotations#alias), [`@enum`](https://github.com/LuaLS/lua-language-server/wiki/Annotations#enum), or [`@class`](https://github.com/LuaLS/lua-language-server/wiki/Annotations#class) as well. Please note that you cannot add a field to a class using `@type`, [you must instead use `@class`](https://github.com/LuaLS/lua-language-server/issues/1971#issuecomment-1458119701).

**Syntax**

`---@type <type>`

**Examples**
<details>
<summary>Basic Type Definition</summary>

```lua
---@type boolean
local x
```

</details>

<details>
<summary>Union Type Definition</summary>

```lua
---@type boolean|number
local x
```

</details>

<details>
<summary>Array Type Definition</summary>

```lua
---@type string[]
local names
```

</details>

<details>
<summary>Dictionary Type Definition</summary>

```lua
---@type { [string]: boolean }
local statuses
```

</details>

<details>
<summary>Table Type Definition</summary>

```lua
---@type table<userID, Player>
local players
```

</details>

<details>
<summary>Union Type Definition</summary>

```lua
---@type boolean|number|"yes"|"no"
local x
```

</details>

<details>
<summary>Function Type Definition</summary>

```lua
---@type fun(name: string, value: any): boolean
local x
```

</details>

<br>

### `@vararg`
<blockquote>
	<br>
	<div align="center">
		🚮 <b>DEPRECATED</b> 🚮
	</div>
	<br>
	<div align="center">
		This annotation has been deprecated and is purely for legacy support for EmmyLua annotations.
		<br>
		<br>
		You should instead use <a>@param</a> for documenting parameters, variable or not.
	</div>
	<br>
</blockquote>

Mark a `function` as having variable arguments. For variable returns, see [`@return`](https://github.com/LuaLS/lua-language-server/wiki/Annotations#return).

**Syntax**

`---@vararg <type>`

**Examples**
<details>
<summary>Basic Variable Function Arguments</summary>

```lua
---@vararg string
function concat(...) end
```

</details>

<br>

### `@version`
Mark the required Lua version for a `function` or [`@class`](https://github.com/LuaLS/lua-language-server/wiki/Annotations#class).


**Syntax**

`---@version [<|>]<version> [, [<|>]version...]`

Possible `version` values:
- `5.1`
- `5.2`
- `5.3`
- `5.4`
- `JIT`

**Examples**
<details>
<summary>Declare Function Version</summary>

```lua
---@version >5.2, JIT
function hello() end
```

</details>

<details>
<summary>Declare Class Version</summary>

```lua
---@version 5.4
---@class Entry
```

See [`@class`](https://github.com/LuaLS/lua-language-server/wiki/Annotations#class) for more info

</details>


## Links

Found an issue? [Report it on the issue tracker](https://github.com/LuaLS/lua-language-server/issues?q=label%3AEmmyLua).

Unit tests for the annotations can be found in [`test/definition/luadoc.lua`](https://github.com/LuaLS/lua-language-server/blob/master/test/definition/luadoc.lua).
