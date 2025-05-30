# Lua annotations

LuaCATS (Lua Comment And Type System) provides a structured way to annotate Lua code with type information and documentation, similar to how TypeScript or JSDoc works for JavaScript. Below is a comprehensive cheatsheet that covers the key annotations and their usage in LuaCATS.

## [](https://www.barbarianmeetscoding.com/notes/lua/annotations/#basic-syntax)Basic Syntax

LuaCATS annotations are prefixed with `---` similar to a lua comment but with one extra dash:

```lua
-- This is a lua comment
---This is an annotation
```

You can take advantage of markdown syntax inside an annotation to provide formatting. For [a full of supported markdown syntax refer to the documentation](https://luals.github.io/wiki/annotations/#annotation-formatting).

## [](https://www.barbarianmeetscoding.com/notes/lua/annotations/#type-annotations)Type Annotations

- **@type**: Specifies the type of a variable or a return type.
    
    ```lua
    -- @type string
    local name = "John"
    
    -- @type number
    local age = 25
    ```
    
- **@param**: Specifies the type and name of a function parameter.
    
    ```lua
    -- @param name string
    -- @param age number
    function greet(name, age)
      print("Hello " .. name .. ", you are " .. age .. " years old.")
    end
    ```
    
- **@return**: Specifies the return type of a function.
    
    ```lua
    -- @return number
    function add(a, b)
      return a + b
    end
    ```
    
- **@field**: Annotates fields in a table.
    
    ```lua
    -- @field name string
    -- @field age number
    local person = {
      name = "Alice",
      age = 30
    }
    ```
    

## [](https://www.barbarianmeetscoding.com/notes/lua/annotations/#composite-types)Composite Types

- **@type Array**: Represents an array of a specific type.
    
    ```lua
    -- @type number[]
    local numbers = {1, 2, 3, 4, 5}
    ```
    
- **@type Table**: Represents a table with specific key-value types.
    
    ```lua
    -- @type table<string, number>
    local ages = {Alice = 30, Bob = 25}
    ```
    
- **@type Union**: Represents a union of multiple types.
    
    ```lua
    -- @type string|number
    local id = "12345"
    ```
    
- **@type Function**: Represents a function type.
    
    ```lua
    -- @type fun(a: number, b: number): number
    local function add(a, b)
      return a + b
    end
    ```
    

## [](https://www.barbarianmeetscoding.com/notes/lua/annotations/#object-oriented-annotations)Object-Oriented Annotations

- **@class**: Defines a class-like structure.
    
    ```lua
    -- @class Person
    -- @field name string
    -- @field age number
    local Person = {}
    ```
    
- **@constructor**: Marks a function as a constructor.
    
    ```lua
    -- @constructor
    -- @param name string
    -- @param age number
    function Person.new(name, age)
      local self = setmetatable({}, Person)
      self.name = name
      self.age = age
      return self
    end
    ```
    
- **@method**: Annotates a method in a class.
    
    ```lua
    -- @method greet
    -- @return string
    function Person:greet()
      return "Hello, my name is " .. self.name
    end
    ```
    

## [](https://www.barbarianmeetscoding.com/notes/lua/annotations/#advanced-annotations)Advanced Annotations

- **@alias**: Defines an alias for a type.
    
    ```lua
    -- @alias Name string
    -- @alias Age number
    -- @type table<Name, Age>
    local people = {John = 25, Jane = 22}
    ```
    
- **@vararg**: Specifies that a function takes a variable number of arguments.
    
    ```lua
    -- @vararg number
    function sum(...)
      local total = 0
      for _, v in ipairs({...}) do
        total = total + v
      end
      return total
    end
    ```
    
- **@deprecated**: Marks a function or variable as deprecated.
    
    ```lua
    -- @deprecated
    -- This function is deprecated, use `newFunction` instead.
    function oldFunction()
      -- ...
    end
    ```
    
- **@see**: Provides a reference to related documentation or functions.
    
    ```lua
    -- @see newFunction
    function oldFunction()
      -- ...
    end
    ```
    

## [](https://www.barbarianmeetscoding.com/notes/lua/annotations/#miscellaneous-annotations)Miscellaneous Annotations

- **@generic**: Defines a generic type.
    
    ```lua
    -- @generic T
    -- @param x T
    -- @return T
    function identity(x)
      return x
    end
    ```
    
- **@overload**: Specifies an overload for a function.
    
    ```lua
    -- @overload fun(a: number, b: number): number
    -- @overload fun(a: string, b: string): string
    function concat(a, b)
      return a .. b
    end
    ```
    
- **@tuple**: Represents a tuple type.
    
    ```lua
    -- @type fun(): (string, number)
    function getNameAndAge()
      return "Alice", 30
    end
    ```
    
- **@nodiscard**: Indicates that the result of a function should not be discarded.
    
    ```lua
    -- @nodiscard
    -- This function’s result should not be ignored.
    function importantResult()
      return 42
    end
    ```
    

---

This cheatsheet covers the most common annotations used in LuaCATS, but there may be more specific annotations or usage patterns depending on your project’s needs or the specific LuaCATS implementation you are working with.

## [](https://www.barbarianmeetscoding.com/notes/lua/annotations/#referring-to-symbols)Referring to symbols

You can refer to other symbols in markdown descriptions using markdown links. Hovering (`:h hover`) the described value will show a hyperlink that, when followed (`K`), will take you to where the symbol is defined:

```lua
---@alias MyCustomType integer

---Calculate a value using [my custom type](lua://MyCustomType)
function calculate(x) end
```