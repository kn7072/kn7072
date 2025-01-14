local dap = require("dap")
-- dap.adapters.gdb = {type = "executable", command = "gdb", args = {"-i", "dap"}}

-- dap.configurations.c = {
--     {
--         name = "Launch",
--         type = "gdb",
--         request = "launch",
--         program = function()
--             return vim.fn.input('Path to executable: ', vim.fn.getcwd() .. '/',
--                                 'file')
--         end,
--         cwd = "${workspaceFolder}"
--     }
-- }

-- https://blog.cryptomilk.org/2024/01/02/neovim-dap-and-gdb-14-1/
-- https://sourceware.org/gdb/current/onlinedocs/gdb.html/Interpreters.html
-- https://sourceware.org/gdb/current/onlinedocs/gdb.html/Debugger-Adapter-Protocol.html
--
vim.env.CPATH = string.format("%s:%s", "./..", vim.env.CPATH)

dap.adapters.gdb = {
    id = 'gdb',
    type = 'executable',
    command = 'gdb',
    args = {
        '--quiet', '--interpreter=dap'
        -- '-x', '/home/stepan/GIT/kn7072/C/code/CPrimerPlus6E/Ch03/my_break'
    }
}

dap.configurations.c = {
    {
        name = 'Run executable (GDB)',
        type = 'gdb',
        request = 'launch',
        -- This requires special handling of 'run_last', see
        -- https://github.com/mfussenegger/nvim-dap/issues/1025#issuecomment-1695852355
        program = function()
            local path = vim.fn.input({
                prompt = 'Path to executable: ',
                default = vim.fn.getcwd() .. '/',
                completion = 'file'
            })

            return (path and path ~= '') and path or dap.ABORT
        end
    }, {
        name = 'Run executable with arguments (GDB)',
        type = 'gdb',
        request = 'launch',
        -- This requires special handling of 'run_last', see
        -- https://github.com/mfussenegger/nvim-dap/issues/1025#issuecomment-1695852355
        program = function()
            local path = vim.fn.input({
                prompt = 'Path to executable: ',
                default = vim.fn.getcwd() .. '/',
                completion = 'file'
            })

            return (path and path ~= '') and path or dap.ABORT
        end,
        args = function()
            local delimiter = vim.fn.input({
                prompt = 'Delimiter:(default spece)',
                default = " "
            })
            local args_str = vim.fn.input({prompt = 'Arguments: '})
            return vim.split(args_str, string.format("%s+", delimiter))
        end
    }, {
        name = 'Attach to process (GDB)',
        type = 'gdb',
        request = 'attach',
        processId = require('dap.utils').pick_process
    }
}
