local obj_a = {a = 1}
local obj_b = {b = 2}
local obj_c = {c = 3}

setmetatable(obj_c, {
    __index = function(_, k)
        return obj_b[k]
    end

})
setmetatable(obj_b, {
    __index = function(_, k)
        return obj_a[k]
    end
})

print(obj_c.a) -- 1

function obj_a:fun_a()
    print("fun_a")
end

function obj_c:fun_c()
    print(self.a)
end

print(obj_c:fun_c()) -- 1
obj_c:fun_a()
