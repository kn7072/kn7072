local foo

do
    local _ENV = _ENV
    function foo()
        print(X)
    end
end

X = 13
_ENV = nil
foo()
local x = ""
