local lsp_common = require("plugins.lsp_common")

local capabilities = vim.lsp.protocol.make_client_capabilities()
capabilities = require('cmp_nvim_lsp').default_capabilities(capabilities)
-- Sntup language servers.
local lspconfig = require('lspconfig')
lspconfig.pyright.setup {
    capabilities = capabilities,
    on_attach = lsp_common.on_attach
}
lspconfig.ts_ls.setup {}
lspconfig.prismals.setup {}
lspconfig.cssls.setup {capabilities = capabilities}

-- https://clangd.llvm.org/installation.html
lspconfig.clangd.setup {
    capabilities = capabilities,
    on_attach = lsp_common.on_attach
}
-- lspconfig.ccls.setup {
--     init_options = {
--         compilationDatabaseDirectory = "build",
--         index = {threads = 0},
--         clang = {excludeArgs = {"-frounding-math"}}
--     }
-- }

-- https://github.com/neovim/nvim-lspconfig/blob/master/doc/server_configurations.md#lua_ls
-- lspconfig.lua_ls.setup {}
lspconfig.lua_ls.setup {
    on_init = function(client)
        local file = assert(io.open("tmpfile_new", "w"))
        file:write("CLIENT\n" .. vim.inspect(client) .. "\n")
        file:write("CLIENT_lua\n" .. vim.inspect(client.config.settings.Lua) ..
                       "\n")
        file:write("CLIENT_CONFIG_lua\n" .. vim.inspect(client.config) .. "\n")
        local workspace_folders = client.workspace_folders
        local path = workspace_folders and workspace_folders[1].name or "_"
        local run_files = vim.api.nvim_get_runtime_file('', true)
        table.insert(run_files, "${3rd}/luassert/library")

        file:flush()

        -- local path = client.workspace_folders[1].name
        if not vim.loop.fs_stat(path .. '/.luarc.json') and
            not vim.loop.fs_stat(path .. '/.luarc.jsonc') then
            client.config.settings = vim.tbl_deep_extend('force', client.config
                                                             .settings, {
                Lua = {
                    runtime = {
                        -- Tell the language server which version of Lua you're using
                        -- (most likely LuaJIT in the case of Neovim)
                        version = 'LuaJIT'
                    },
                    -- Make the server aware of Neovim runtime files
                    workspace = {
                        checkThirdParty = false,
                        library = run_files -- {
                        -- vim.env.VIMRUNTIME
                        -- "${3rd}/luv/library"
                        -- "${3rd}/busted/library",
                        -- }
                        -- or pull in all of 'runtimepath'. NOTE: this is a lot slower
                        -- library = vim.api.nvim_get_runtime_file("", true)
                    },
                    diagnostics = {
                        -- Get the language server to recognize the `vim` global
                        -- Now, you don't get error/warning "Undefined global `vim`".
                        globals = {'vim'}
                    }
                }
            })

            client.notify("workspace/didChangeConfiguration",
                          {settings = client.config.settings})

            file:write("CLIENT_lua_finish\n" ..
                           vim.inspect(client.config.settings) .. "\n")

        end
        file:close()
        -- return true
    end
}

lspconfig.rust_analyzer.setup {
    settings = {
        ['rust-analyzer'] = {
            diagnostics = {enable = true, experimental = {enable = true}}
        }
    }
}
