require('dap-go').setup {
    -- Additional dap configurations can be added.
    -- dap_configurations accepts a list of tables where each entry
    -- represents a dap configuration. For more details do:
    -- :help dap-configuration
    dap_configurations = {
        {type = "go", name = "Debug 1", request = "launch", program = "${file}"},
        {
            type = "go",
            name = "Debug test 1",
            request = "launch",
            mode = "test", -- Mode is important
            program = "${file}"
        }
    },
    -- delve configurations
    delve = {
        -- the path to the executable dlv which will be used for debugging.
        -- by default, this is the "dlv" executable on your PATH.
        path = "dlv",
        -- time to wait for delve to initialize the debug session.
        -- defaul:t to 20 seconds
        -- initialize_timeout_sec = 20,
        -- a string that defines the port to start delve debugger.
        -- default to string "${port}" which instructs nvim-dap
        -- to start the process in a random available port
        port = "${port}",
        -- additional args to pass to dlv
        args = {}
    }
}

require('dap').set_log_level('TRACE')
-- require('dap-go').setup({})
--
-- local dap = require("dap")
--
-- dap.adapters.delve = {
--     type = 'server',
--     port = '${port}',
--     executable = {
--         command = 'dlv',
--         args = {'dap', '-l', '127.0.0.1:${port}', ' -log'} --  --log-output=dap'
--     }
-- }
--
-- dap.configurations.go = {
--     {type = "delve", name = "Debug", request = "launch", program = "${file}"},
--     {
--         type = "delve",
--         name = "Debug test", -- configuration for debugging test files
--         request = "launch",
--         mode = "test",
--         program = "${file}"
--     }, -- works with go.mod packages and sub packages 
--     {
--         type = "delve",
--         name = "Debug test (go.mod)",
--         request = "launch",
--         mode = "test",
--         program = "./${relativeFileDirname}"
--     }
-- }
-- require('dap-go').setup()
-- local dap = require("dap")
-- require('dap').set_log_level('INFO') -- Helps when configuring DAP, see logs with :DapShowLog
--
-- -- dap.adapters.go = function(callback, config)
-- --     -- Wait for delve to start
-- --     vim.defer_fn(function()
-- --         callback({type = "server", host = "127.0.0.1", port = "38697"})
-- --     end, 100)
-- -- end
--
-- dap.adapters.go = {
--     type = "server",
--     port = "${port}",
--     executable = {
--         command = vim.fn.stdpath("data") .. '/mason/bin/dlv',
--         args = {"dap", "-l", "127.0.0.1:${port}"}
--     }
-- }
--
-- dap.configurations.go = {
--     {type = "go", name = "Debug", request = "launch", program = "${file}"}
-- }
--
-- require('dap-go').setup()
-- local dap = require("dap")
-- dap.adapters.delve = {type = "server", host = "127.0.0.1", port = 38697}

-- local dap_ok, dap = pcall(require, "dap")
-- if not (dap_ok) then
--     print("nvim-dap not installed!")
--     return
-- end
--
--
-- dap.configurations = {
--     go = {
--         {
--             type = "go", -- Which adapter to use
--             name = "Debug", -- Human readable name
--             request = "launch", -- Whether to "launch" or "attach" to program
--             program = "${file}" -- The buffer you are focused on when running nvim-dap
--         }
--     }
-- }
--
-- dap.adapters.go = {
--     type = "server",
--     port = "${port}",
--     executable = {
--         command = vim.fn.stdpath("data") .. '/mason/bin/dlv',
--         args = {"dap", "-l", "127.0.0.1:${port}"}
--     }
-- }
