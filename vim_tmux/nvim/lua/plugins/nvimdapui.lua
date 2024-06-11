local dap_ok, dap = pcall(require, "dap")
local dap_ui_ok, dapui = pcall(require, "dapui")

if not (dap_ok and dap_ui_ok) then
    require("notify")("nvim-dap or dap-ui not installed!", "warning") -- nvim-notify is a separate plugin, I recommend it too!
    return
end

dap.listeners.after.event_initialized["dapui_config"] =
    function() dapui.open() end
dap.listeners.before.event_terminated["dapui_config"] =
    function() dapui.close() end
dap.listeners.before.event_exited["dapui_config"] = function() dapui.close() end

-- dapui.setup()
dapui.setup({
    icons = {expanded = "▾", collapsed = "▸"},
    mappings = {
        open = "o",
        remove = "d",
        edit = "e",
        repl = "r",
        toggle = "t",
        expand = {"<CR>", "<2-LeftMouse>"}
    },
    expand_lines = vim.fn.has("nvim-0.7"),
    layouts = {
        {
            elements = {
                {id = "scopes", size = 0.6}, {id = "watches", size = 0.3},
                {id = "stacks", size = 0.3}
            },
            size = 0.3,
            position = "left"
        }, {
            elements = {
                {id = "repl", size = 0.4}, {id = "breakpoints", size = 0.3},
                {id = "console", size = 0.3}
            },
            size = 0.2,
            position = "bottom"
        }
    },
    floating = {
        max_height = nil,
        max_width = nil,
        border = "single",
        mappings = {close = {"q", "<Esc>"}}
    },
    windows = {indent = 1},
    render = {max_type_length = nil}
})

-- vim.fn.sign_define('DapBreakpoint',
--                    {text = '🟥', texthl = '', linehl = '', numhl = ''})
-- vim.fn.sign_define('DapStopped',
--                    {text = '▶️', texthl = '', linehl = '', numhl = ''})
--
local dap_breakpoint_color = {
    breakpoint = {ctermbg = 0, fg = '#993939', bg = '#31353f'},
    logpoing = {ctermbg = 0, fg = '#61afef', bg = '#31353f'},
    stopped = {ctermbg = 0, fg = '#98c379', bg = '#31353f'}
}

vim.api.nvim_set_hl(0, 'DapBreakpoint', dap_breakpoint_color.breakpoint)
vim.api.nvim_set_hl(0, 'DapLogPoint', dap_breakpoint_color.logpoing)
vim.api.nvim_set_hl(0, 'DapStopped', dap_breakpoint_color.stopped)

local dap_breakpoint = {
    error = {
        text = "",
        texthl = "DapBreakpoint",
        linehl = "DapBreakpoint",
        numhl = "DapBreakpoint"
    },
    condition = {
        text = 'ﳁ',
        texthl = 'DapBreakpoint',
        linehl = 'DapBreakpoint',
        numhl = 'DapBreakpoint'
    },
    rejected = {
        text = "",
        texthl = "DapBreakpint",
        linehl = "DapBreakpoint",
        numhl = "DapBreakpoint"
    },
    logpoint = {
        text = '',
        texthl = 'DapLogPoint',
        linehl = 'DapLogPoint',
        numhl = 'DapLogPoint'
    },
    stopped = {
        text = '',
        texthl = 'DapStopped',
        linehl = 'DapStopped',
        numhl = 'DapStopped'
    }
}

vim.fn.sign_define('DapBreakpoint', dap_breakpoint.error)
vim.fn.sign_define('DapBreakpointCondition', dap_breakpoint.condition)
vim.fn.sign_define('DapBreakpointRejected', dap_breakpoint.rejected)
vim.fn.sign_define('DapLogPoint', dap_breakpoint.logpoint)
vim.fn.sign_define('DapStopped', dap_breakpoint.stopped)

vim.keymap.set('n', '<Leader>dc', dap.continue)
vim.keymap.set('n', '<Leader>dn', dap.step_over)
vim.keymap.set('n', '<Leader>di', dap.step_into)
vim.keymap.set('n', '<Leader>do', dap.step_out)
vim.keymap.set('n', '<leader>db', dap.toggle_breakpoint)

vim.keymap.set('n', '<Leader>dB', function() dap.set_breakpoint() end)
vim.keymap.set('n', '<Leader>dbc', function()
    dap.set_breakpoint(vim.fn.input('condition: '), nil, nil)
end)
vim.keymap.set("n", "<Leader>dC", function()
    dap.clear_breakpoints()
    require("notify")("Breakpoints cleared", "warn")
end)

vim.keymap.set({'n', 'v'}, '<Leader>dh',
               function() require('dap.ui.widgets').hover() end)
vim.keymap.set({'n', 'v'}, '<Leader>dp',
               function() require('dap.ui.widgets').preview() end)
-- vim.keymap.set('n', '<Leader>df', function()
--     local widgets = require('dap.ui.widgets')
--     widgets.centered_float(widgets.frames)
-- end)
-- vim.keymap.set('n', '<Leader>ds', function()
--     local widgets = require('dap.ui.widgets')
--     widgets.centered_float(widgets.scopes)
-- end)
-- Close debugger and clear breakpoints
vim.keymap.set("n", "<leader>de", function()
    dap.clear_breakpoints()
    dapui.toggle({})
    dap.terminate()
    vim.api.nvim_feedkeys(vim.api.nvim_replace_termcodes("<C-w>=", false, true,
                                                         true), "n", false)
    require("notify")("Debugger session ended", "warn")
end)
