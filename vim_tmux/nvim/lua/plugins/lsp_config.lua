local lsp_common = require("plugins.lsp_common")

-- https://www.getman.io/posts/programming-go-in-neovim/
-- https://gist.github.com/sergii4/afd763bb378aec45aba17c20b3cf2115#file-lsp_config-lua
local nvim_lsp = require('lspconfig')

local capabilities = vim.lsp.protocol.make_client_capabilities()
capabilities.textDocument.completion.completionItem.snippetSupport = true
-- vim.api.nvim_create_autocmd("BufEnter",
--                             {callback = function() print("hello nvim") end})

vim.api.nvim_create_autocmd("BufWritePre", {
    callback = function()
        vim.lsp.buf.format()
        goimports(1000)
        -- print("buf_write_pre")
    end,
    pattern = {"*.go"}
})

function goimports(timeoutms)
    local context = {source = {organizeImports = true}}
    vim.validate {context = {context, "t", true}}

    local params = vim.lsp.util.make_range_params()
    params.context = context

    -- See the implementation of the textDocument/codeAction callback
    -- (lua/vim/lsp/handler.lua) for how to do this properly.
    local result = vim.lsp.buf_request_sync(0, "textDocument/codeAction",
                                            params, timeoutms)
    if not result or next(result) == nil then
        return
    end
    local actions = result[1].result
    if not actions then
        return
    end
    local action = actions[1]

    -- textDocument/codeAction can return either Command[] or CodeAction[]. If it
    -- is a CodeAction, it can have either an edit, a command or both. Edits
    -- should be executed first.
    if action.edit or type(action.command) == "table" then
        if action.edit then
            vim.lsp.util.apply_workspace_edit(action.edit)
        end
        if type(action.command) == "table" then
            vim.lsp.buf.execute_command(action.command)
        end
    else
        vim.lsp.buf.execute_command(action)
    end
end

nvim_lsp.gopls.setup {
    cmd = {'gopls'},
    -- for postfix snippets and analyzers
    capabilities = capabilities,
    settings = {
        -- https://github.com/golang/tools/blob/master/gopls/doc/settings.md
        -- https://github.com/golang/tools/blob/master/gopls/doc/analyzers.md
        -- https://github.com/golang/tools/blob/master/gopls/doc/settings.md
        -- https://github.com/golang/tools/blob/master/gopls/doc/inlayHints.md
        gopls = {
            experimentalPostfixCompletions = true,
            gofumpt = true,
            codelenses = {
                gc_details = true,
                generate = true,
                regenerate_cgo = true,
                run_govulncheck = true,
                test = true,
                tidy = true,
                upgrade_dependency = true,
                vendor = true
            },

            analyses = {
                fieldalignment = true,
                nilness = true,
                unusedparams = true,
                unusedwrite = true,
                useany = true,
                shadow = true
                -- simplifyslice = true
            },
            hints = {
                assignVariableTypes = true,
                compositeLiteralFields = true,
                compositeLiteralTypes = true,
                constantValues = true,
                functionTypeParameters = true,
                parameterNames = true,
                rangeVariableTypes = true
            },
            usePlaceholders = true,
            completeUnimported = true,
            staticcheck = true,
            directoryFilters = {
                "-.git", "-.vscode", "-.idea", "-.vscode-test", "-node_modules"
            },
            semanticTokens = true

        }
    },
    on_attach = lsp_common.on_attach
}

-- vim.lsp.set_log_level("debug")
