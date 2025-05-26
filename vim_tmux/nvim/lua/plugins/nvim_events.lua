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

-- api.nvim_create_autocmd({"FocusLost", "FocusGained"}, {
--     group = group,
--     callback = function(ev)
--         local is_caps_on = is_capslock()
--         if ev.event == "FocusGained" then
--             hide:stop()
--             print(string.format("FocusGained index %d, capslock_is_on %d",
--                                 index, is_caps_on))
--             index = index + 1
--         else
--             hide:start(5000, 0, function()
--                 print("FocusLost")
--                 api.nvim_input("<esc>")
--             end)
--         end
--     end
-- })

local function time_background()
    local timer = vim.loop.new_timer()
    timer:start(0, 600, vim.schedule_wrap(function()
        local hour = tonumber(os.date('%H'))
        local bg = (hour > 6 and hour < 18) and 'dark' or 'light'
        if vim.o.bg ~= bg then
            vim.o.bg = bg
        end
    end))
end

local function change_fold_column()
    local bg_capslock = "#d72323"
    local bg_capslock_trim = string.gsub(bg_capslock, '#', '')
    local bg_capslock_int = tonumber(bg_capslock_trim, 16)
    local capslock_hl = {
        ctermbg = 70,
        bg = bg_capslock,
        -- fg = "#11cbd7",
        bold = true
    }
    local default_hl = {
        ctermbg = 70,
        bg = "#5a524c",
        -- fg = "#11cbd7",
        bold = true
    }
    local timer = vim.loop.new_timer()
    timer:start(0, 1000, vim.schedule_wrap(function()
        local is_caps_on = is_capslock()
        local cur_hl = api.nvim_get_hl(0, {name = 'FoldColumn'})
        -- print(string.format("capslock %s ", is_caps_on))
        if is_caps_on == 1 then
            -- capslock on
            if cur_hl.bg ~= bg_capslock_int then
                -- если цветовая схема не соответствует подсветки для capslock - включаем ее
                api.nvim_set_hl(0, "FoldColumn", capslock_hl)
            end
        else
            -- capslock off
            if cur_hl.bg == bg_capslock_int then
                -- выключаем подсветку для capslock
                -- print("caps off")
                api.nvim_set_hl(0, "FoldColumn", default_hl)
            end
        end

    end))
end

vim.api.nvim_create_autocmd("FileType", {
    pattern = "qf",
    callback = function()
        vim.keymap.set("n", "<Up>", "<Up><CR><C-w>p", {
            buffer = true,
            remap = false,
            desc = "Navigate up quickfix"
        })
        vim.keymap.set("n", "<Down>", "<Down><CR><C-w>p",
                       {remap = false, desc = "Navigate down quickfix"})
    end
})

-- FoldColumn     xxx ctermfg=239 guifg=#5a524c                
-- time_background()
-- change_fold_column()
