local lsp_common = require("plugins.lsp_common")

local capabilities = vim.lsp.protocol.make_client_capabilities()
capabilities = require('cmp_nvim_lsp').default_capabilities(capabilities)

-- Sntup language servers.
-- https://github.com/microsoft/pyright/blob/main/docs/settings.md
local lspconfig = require('lspconfig')
lspconfig.pyright.setup {
    capabilities = capabilities,
    on_attach = lsp_common.on_attach,
    single_file_support = true,
    settings = {
        --     -- pyright = {
        --     --     disableLanguageServices = false,
        --     --     disableOrganizeImports = false
        --     -- },
        python = {
            -- pythonPath = "/home/stepan/.cache/pypoetry/virtualenvs/telegrambot-XV0byvRV-py3.12/bin/python",
            analysis = {
                autoImportCompletions = true,
                autoSearchPaths = true,
                diagnosticMode = "openFilesOnly", -- openFilesOnly, workspace
                typeCheckingMode = "basic", -- off, basic, strict
                useLibraryCodeForTypes = true
            }
        }
    }
}

lspconfig.ts_ls.setup {}
lspconfig.prismals.setup {}
lspconfig.cssls.setup {capabilities = capabilities}

-- https://clangd.llvm.org/installation.html
lspconfig.clangd.setup {
    capabilities = capabilities,
    on_attach = lsp_common.on_attach,
    cmd = {"clangd", "--offset-encoding=utf-16"}
}
-- lspconfig.ccls.setup {
--     init_options = {
--         compilationDatabaseDirectory = "build",
--         index = {threads = 0},
--         clang = {excludeArgs = {"-frounding-math"}}
--     }
-- }

-- https://github.com/neovim/nvim-lspconfig/blob/master/doc/server_configurations.md#lua_ls
-- https://luals.github.io/wiki/formatter/
lspconfig.lua_ls.setup {
    capabilities = capabilities,
    on_attach = lsp_common.on_attach,
    -- enabled = false,
    single_file_support = true,
    settings = {
        Lua = {
            runtime = {
                -- Tell the language server which version of Lua you're using
                -- (most likely LuaJIT in the case of Neovim)
                version = 'LuaJIT'
            },

            workspace = {checkThirdParty = false},
            completion = {
                enable = true,
                workspaceWord = true,
                callSnippet = "Both"
            },
            misc = {
                parameters = {
                    -- "--log-level=trace",
                }
            },
            hint = {
                enable = true,
                setType = false,
                paramType = true,
                paramName = "All",
                semicolon = "All",
                arrayIndex = "Disable"
            },
            doc = {privateName = {"^_"}},
            type = {castNumberToInteger = true},
            diagnostics = {
                enable = true,
                disable = {"incomplete-signature-doc", "trailing-space"},
                -- enable = false,
                groupSeverity = {strong = "Warning", strict = "Warning"},
                groupFileStatus = {
                    ["ambiguity"] = "Opened",
                    ["await"] = "Opened",
                    ["codestyle"] = "None",
                    ["duplicate"] = "Opened",
                    ["global"] = "Opened",
                    ["luadoc"] = "Opened",
                    ["redefined"] = "Opened",
                    ["strict"] = "Opened",
                    ["strong"] = "Opened",
                    ["type-check"] = "Opened",
                    ["unbalanced"] = "Opened",
                    ["unused"] = "Opened"
                },
                unusedLocalExclude = {"_*"},
                globals = {'vim'}

            },
            format = {
                enable = false,
                defaultConfig = {
                    indent_style = "space",
                    indent_size = "4",
                    continuation_indent_size = "4"
                }
            }
        }
    }

}
-- lspconfig.lua_ls.setup {
--     on_init = function(client)
--         -- local file = assert(io.open("tmpfile_new", "w"))
--         -- file:write("CLIENT\n" .. vim.inspect(client) .. "\n")
--         -- file:write("CLIENT_lua\n" .. vim.inspect(client.config.settings.Lua) ..
--         --                "\n")
--         -- file:write("CLIENT_CONFIG_lua\n" .. vim.inspect(client.config) .. "\n")
--         local workspace_folders = client.workspace_folders
--         local path = workspace_folders and workspace_folders[1].name or "_"
--         local run_files = vim.api.nvim_get_runtime_file('', true)
--         table.insert(run_files, "${3rd}/luassert/library")
--
--         -- file:flush()
--
--         -- local path = client.workspace_folders[1].name
--         if not vim.loop.fs_stat(path .. '/.luarc.json') and
--             not vim.loop.fs_stat(path .. '/.luarc.jsonc') then
--             client.config.settings = vim.tbl_deep_extend('force', client.config
--                                                              .settings, {
--                 Lua = {
--                     runtime = {
--                         -- Tell the language server which version of Lua you're using
--                         -- (most likely LuaJIT in the case of Neovim)
--                         version = 'LuaJIT'
--                     },
--                     -- Make the server aware of Neovim runtime files
--                     workspace = {
--                         checkThirdParty = false,
--                         library = run_files -- {
--                         -- vim.env.VIMRUNTIME
--                         -- "${3rd}/luv/library"
--                         -- "${3rd}/busted/library",
--                         -- }
--                         -- or pull in all of 'runtimepath'. NOTE: this is a lot slower
--                         -- library = vim.api.nvim_get_runtime_file("", true)
--                     },
--                     diagnostics = {
--                         -- Get the language server to recognize the `vim` global
--                         -- Now, you don't get error/warning "Undefined global `vim`".
--                         globals = {'vim'}
--                     }
--                 }
--             })
--
--             client.notify("workspace/didChangeConfiguration",
--                           {settings = client.config.settings})
--
--             -- file:write("CLIENT_lua_finish\n" ..
--             --                vim.inspect(client.config.settings) .. "\n")
--
--         end
--         -- file:close()
--         -- return true
--     end
-- }

lspconfig.rust_analyzer.setup {
    settings = {
        ['rust-analyzer'] = {
            diagnostics = {enable = true, experimental = {enable = true}}
        }
    }
}
