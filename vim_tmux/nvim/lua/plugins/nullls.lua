local null_ls = require("null-ls")
local augroup = vim.api.nvim_create_augroup("LspFormatting", {})

null_ls.setup({
    sources = {
        null_ls.builtins.formatting.eslint_d.with({
            filetypes = {
                "typescript", "javascript", "typescriptreact", "javascriptreact"
            }
        }), null_ls.builtins.formatting.lua_format,
        null_ls.builtins.diagnostics.eslint_d,
        -- null_ls.builtins.formatting.stylua,
        -- null_ls.builtins.diagnostics.ltrs,
        -- null_ls.builtins.formatting.rustfmt,
        null_ls.builtins.formatting.clang_format.with({
            -- extra_args = {"--style=Google"}
            extra_args = {
                -- https://clang.llvm.org/docs/ClangFormatStyleOptions.html
                string.format("--style=file:%s", vim.fn.stdpath("config") ..
                                  "/plugin_configs/.clang-format")
            }
        }), null_ls.builtins.formatting.black.with({filetypes = {"python"}}),
        null_ls.builtins.formatting.isort.with({
            filetypes = {"python"},
            extra_args = {
                string.format("--settings-path=%s", vim.fn.stdpath("config") ..
                                  "/plugin_configs/.isort.cfg")
            }
        }), null_ls.builtins.diagnostics.flake8.with({
            extra_args = {
                "--config",
                vim.fn.stdpath("config") .. "/plugin_configs/.flake8"

                -- string.format("--config %s", vim.fn.stdpath("config") ..
                -- "/plugin_configs/.flake8")
                -- "--format '%(path)s::%(row)d,%(col)d::%(code)s::%(text)s'"
            }
            -- extra_args = {"--max-line-length=88", "--max-complexity=8"}
        }), null_ls.builtins.diagnostics.shellcheck,
        null_ls.builtins.formatting.prettierd.with({
            filetypes = {
                "css", "scss", "less", "html", "json", "jsonc", "yaml",
                "markdown", "markdown.mdx", "graphql", "handlebars"
            }
        })
    },
    on_attach = function(client, bufnr)
        if client.supports_method("textDocument/formatting") then
            vim.api.nvim_clear_autocmds({group = augroup, buffer = bufnr})
            vim.api.nvim_create_autocmd("BufWritePre", {
                group = augroup,
                buffer = bufnr,
                callback = function()
                    vim.lsp.buf.format({
                        bufnr = bufnr,
                        filter = function(client)
                            return client.name == "null-ls"
                        end
                    })
                    -- vim.lsp.buf.formatting_sync()
                end
            })
        end
    end
})
