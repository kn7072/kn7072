-- https://github.com/mfussenegger/nvim-dap/wiki/Debug-Adapter-installation
local dap = require('dap')

local pythonPath = function()
    -- debugpy supports launching an application with a different interpreter then the one used to launch debugpy itself.
    -- The code below looks for a `venv` or `.venv` folder in the current directly and uses the python within.
    -- You could adapt this - to for example use the `VIRTUAL_ENV` environment variable.
    local cwd = vim.fn.getcwd()
    if vim.fn.executable(cwd .. '/venv/bin/python') == 1 then
        return cwd .. '/venv/bin/python'
    elseif vim.fn.executable(cwd .. '/.venv/bin/python') == 1 then
        return cwd .. '/.venv/bin/python'
    else
        -- return '/usr/bin/python3'
        return "python3"
        -- '/home/stepan/.cache/pypoetry/virtualenvs/telegrambot-XV0byvRV-py3.12/bin/python'
    end
end

dap.adapters.python = function(cb, config)
    if config.request == 'attach' then
        ---@diagnostic disable-next-line: undefined-field
        local port = (config.connect or config).port
        ---@diagnostic disable-next-line: undefined-field
        local host = (config.connect or config).host or '127.0.0.1'
        cb({
            type = 'server',
            port = assert(port,
                          '`connect.port` is required for a python `attach` configuration'),
            host = host,
            options = {source_filetype = 'python'}
        })
    else
        cb({
            type = 'executable',
            -- command = '/home/stepan/.cache/pypoetry/virtualenvs/telegrambot-XV0byvRV-py3.12/bin/python', -- 'path/to/virtualenvs/debugpy/bin/python',
            -- command = '/usr/bin/python3',
            command = 'python3',
            args = {'-m', 'debugpy.adapter'},
            options = {source_filetype = 'python'}
        })
    end
end

dap.configurations.python = {
    {
        -- The first three options are required by nvim-dap
        type = 'python', -- the type here established the link to the adapter definition: `dap.adapters.python`
        request = 'launch',
        name = "Launch file",
        console = 'integratedTerminal',
        justMyCode = false,
        -- Options below are for debugpy, see https://github.com/microsoft/debugpy/wiki/Debug-configuration-settings for supported options
        program = "${file}", -- This configuration will launch the current file if used.
        pythonPath = pythonPath()
    }, -- {
    --         type = 'python',
    --         request = 'launch',
    --         name = 'DAP Django',
    --         program = vim.loop.cwd() .. '/manage.py',
    --         args = {'runserver', '--noreload'},
    --         justMyCode = true,
    --         django = true,
    --         console = "integratedTerminal",
    --     },
    {
        type = 'python',
        request = 'attach',
        name = 'Attach remote',
        connect = function()
            return {host = '127.0.0.1', port = 5678}
        end
    }, {
        type = 'python',
        request = 'launch',
        name = 'Launch file with arguments',
        program = '${file}',
        args = function()
            local args_string = vim.fn.input('Arguments: ')
            return vim.split(args_string, " +")
        end,
        console = "integratedTerminal",
        pythonPath = pythonPath()
    }
}
