-- Figure 21.3. Accounts using a dual representation
local balance = {}
Account = {}

function Account:withdraw(v)
    balance[self] = balance[self] - v
end

function Account:deposit(v)
    balance[self] = balance[self] + v
end

function Account:balance()
    return balance[self]
end

function Account:new(o)
    o = o or {}
    -- create table if user does not provide one
    setmetatable(o, self)
    self.__index = self
    balance[o] = 0
    -- initial balance
    return o
end
-- We use this class just like any other one:
a = Account:new{}
a:deposit(100.00)
print(a:balance())
--[[
However, we cannot tamper with an account balance. By keeping the table balance private to the mod-
ule, this implementation ensures its safety.
Inheritance works without modifications. This approach has a cost quite similar to the standard one, both
in terms of time and of memory. New objects need one new table and one new entry in each private table
being used. The access balance[self] can be slightly slower than self.balance, because the
latter uses a local variable while the first uses an external variable. Usually this difference is negligible.
As we will see later, it also demands some extra work from the garbage collector.
--]]
