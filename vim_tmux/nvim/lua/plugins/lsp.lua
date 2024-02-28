local capabilities = vim.lsp.protocol.make_client_capabilities()
capabilities = require('cmp_nvim_lsp').default_capabilities(capabilities)
-- Sntup language servers.
local lspconfig = require('lspconfig')
lspconfig.pyright.setup {}
lspconfig.tsserver.setup {}
lspconfig.prismals.setup {}
lspconfig.cssls.setup {capabilities = capabilities}

-- https://clangd.llvm.org/installation.html
lspconfig.clangd.setup {}
-- lspconfig.ccls.setup {
--     init_options = {
--         compilationDatabaseDirectory = "build",
--         index = {threads = 0},
--         clang = {excludeArgs = {"-frounding-math"}}
--     }
-- }

-- lspconfig.golangci_lint_ls.setup {filetypes = {'go', 'gomod'}}

-- lspconfig.lua_ls.setup {
--     settings = {
--         Lua = {
--             runtime = {
--                 -- Tell the language server which version of Lua you're using (most likely LuaJIT in the case of Neovim)
--                 version = 'LuaJIT'
--             },
--             diagnostics = {
--                 -- Get the language server to recognize the `vim` global
--                 globals = {'vim'}
--             },
--             workspace = {
--                 -- Make the server aware of Neovim runtime files
--                 library = vim.api.nvim_get_runtime_file("", true)
--             },
--             -- Do not send telemetry data containing a randomized but unique identifier
--             telemetry = {enable = false}
--         }
--     }
-- }
-- https://github.com/neovim/nvim-lspconfig/blob/master/doc/server_configurations.md#lua_ls
-- lspconfig.lua_ls.setup {}
lspconfig.lua_ls.setup {
    on_init = function(client)
        local path = client.workspace_folders[1].name
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
                        library = {
                            vim.env.VIMRUNTIME
                            -- "${3rd}/luv/library"
                            -- "${3rd}/busted/library",
                        }
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
        end
        return true
    end
}

util = require "lspconfig/util"

-- lspconfig.gopls.setup {
--     cmd = {"gopls", "serve"},
--     filetypes = {"go", "gomod"},
--     root_dir = util.root_pattern("go.work", "go.mod", ".git"),
--     settings = {gopls = {analyses = {unusedparams = true}, staticcheck = true}}
-- }

lspconfig.rust_analyzer.setup {
    settings = {
        ['rust-analyzer'] = {
            diagnostics = {enable = true, experimental = {enable = true}}
        }
    }
}
