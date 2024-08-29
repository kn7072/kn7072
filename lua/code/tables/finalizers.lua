--[[
Another tricky point about finalizers is resurrection. When a finalizer is called, it gets the object being
finalized as a parameter. So, the object becomes alive again, at least during the finalization. I call this a
transient resurrection. While the finalizer runs, nothing stops it from storing the object in a global variable,
for instance, so that it remains accessible after the finalizer returns. I call this a permanent resurrection.
Resurrection must be transitive. Consider the following piece of code:
--]] --
A = {x = "this is A"}
B = {f = A}
setmetatable(B, {
    __gc = function(o)
        print(string.format("del %s", o.f.x))
    end
})
A = nil

collectgarbage() -- > this is A
print(B.f.x)
for k, v in pairs(B) do
    print(k, v)
end

print("end")
