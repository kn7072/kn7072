function traceback()
    for level = 1, math.huge do
        local info = debug.getinfo(level, "Sl")
        if not info then break end
        if info.what == "C" then
            -- is a C function?
            print(string.format("%d\tC function", level))
        else
            -- a Lua function
            print(string.format("%d\t[%s]:%d", level, info.short_src,
                                info.currentline))
        end
    end
end

function myfunction(a, b)
    print(debug.traceback("Stack trace"))
    local get_info = debug.getinfo(2, "LS")
    if not get_info then return end
    for i, v in ipairs(get_info.activelines) do print(i, v) end

    print("source")
    print(get_info.source)
    print("Stack trace end")

    traceback()

    return 10
end

myfunction()
print(debug.getinfo(1))
print("finish")

local info_func = debug.getinfo(myfunction)
print(info_func.nparams)
print(info_func.nups)
print(info_func.linedefined)
print(info_func.lastlinedefined)
