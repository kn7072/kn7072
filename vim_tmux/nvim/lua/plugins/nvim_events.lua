local api = vim.api
local uv = vim.uv or vim.loop

local group = vim.api.nvim_create_augroup("my_events", {clear = true})
local hide = uv.new_timer()
local index = 0

local function is_capslock()
    local cmd = "xset q 2> /dev/null | grep 'LED' | awk '{print $NF}'"
    -- 00000000 capslock turns off
    -- 00000001 capslock turns on
    local output = tonumber(vim.trim(vim.fn.system(cmd)))
    -- print(output)
    return output
end

api.nvim_create_autocmd({"FocusLost", "FocusGained"}, {
    group = group,
    callback = function(ev)
        local is_caps_on = is_capslock()
        if ev.event == "FocusGained" then
            hide:stop()
            print(string.format("FocusGained index %d, capslock_is_on %d",
                                index, is_caps_on))
            index = index + 1
        else
            hide:start(5000, 0, function()
                print("FocusLost")
                api.nvim_input("<esc>")
            end)
        end
    end
})
