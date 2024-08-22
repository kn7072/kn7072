Account = {
    balance = 0,
    xxx = function(self) print("self.balance = %s", self.balance) end
}

function Account:new(o)
    o = o or {}
    self.__index = self
    setmetatable(o, self)
    return o
end

b = Account:new()
print(string.format("%s", b.balance))
b:xxx()
print("=========")
b.balance = 50
b:xxx()
