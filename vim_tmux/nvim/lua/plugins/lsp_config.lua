-- https://www.getman.io/posts/programming-go-in-neovim/
-- https://gist.github.com/sergii4/afd763bb378aec45aba17c20b3cf2115#file-lsp_config-lua
local nvim_lsp = require('lspconfig')

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

local capabilities = vim.lsp.protocol.make_client_capabilities()
capabilities.textDocument.completion.completionItem.snippetSupport = true

local on_attach = function(client, bufnr)
    local function buf_set_keymap(...)
        vim.api.nvim_buf_set_keymap(bufnr, ...)
    end
    local function buf_set_option(...)
        vim.api.nvim_buf_set_option(bufnr, ...)
    end

    buf_set_option('omnifunc', 'v:lua.vim.lsp.omnifunc')

    -- Mappings.
    local opts = {noremap = true, silent = true}
    buf_set_keymap('n', 'gD', '<Cmd>lua vim.lsp.buf.declaration()<CR>', opts)
    buf_set_keymap('n', 'gd', '<Cmd>lua vim.lsp.buf.definition()<CR>', opts)
    buf_set_keymap('n', 'ga', '<Cmd>lua vim.lsp.buf.code_action()<CR>', opts)
    buf_set_keymap('n', 'K', '<Cmd>lua vim.lsp.buf.hover()<CR>', opts)
    buf_set_keymap('n', 'gi', '<cmd>lua vim.lsp.buf.implementation()<CR>', opts)
    buf_set_keymap('n', '<C-k>', '<cmd>lua vim.lsp.buf.signature_help()<CR>',
                   opts)
    buf_set_keymap('n', '<space>wa',
                   '<cmd>lua vim.lsp.buf.add_workspace_folder()<CR>', opts)
    buf_set_keymap('n', '<space>wr',
                   '<cmd>lua vim.lsp.buf.remove_workspace_folder()<CR>', opts)
    buf_set_keymap('n', '<space>wl',
                   '<cmd>lua print(vim.inspect(vim.lsp.buf.list_workspace_folders()))<CR>',
                   opts)
    buf_set_keymap('n', '<space>D',
                   '<cmd>lua vim.lsp.buf.type_definition()<CR>', opts)
    buf_set_keymap('n', '<space>rn', '<cmd>lua vim.lsp.buf.rename()<CR>', opts)
    buf_set_keymap('n', 'gr', '<cmd>lua vim.lsp.buf.references()<CR>', opts)
    buf_set_keymap('n', '<space>n', '<cmd>lua vim.diagnostic.open_float()<CR>',
                   opts)
    buf_set_keymap('n', '[d', '<cmd>lua vim.diagnostic.goto_prev()<CR>', opts)
    buf_set_keymap('n', ']d', '<cmd>lua vim.diagnostic.goto_next()<CR>', opts)
    buf_set_keymap('n', '<space>q', '<cmd>lua vim.diagnostic.setloclist()<CR>', -- setloclist setqflist
                   opts)

    -- Set some keybinds conditional on server capabilities
    -- :lua =vim.lsp.get_active_clients()[1].server_capabilities
    if client.server_capabilities.documentFormattingProvider then
        buf_set_keymap("n", "gff", "<cmd>lua vim.lsp.buf.format()<CR>", opts)
    elseif client.server_capabilities.rangeFormatting then
        buf_set_keymap("n", "gfr",
                       "<cmd>lua vim.lsp.buf.range_formatting()<CR>", opts)
    end

    -- Set autocommands conditional on server_capabilities
    -- https://github.com/neovim/neovim/issues/14090#issuecomment-1113956767
    -- if client.server_capabilities.documentHighlightProvider then
    --     vim.api.nvim_exec([[
    --   hi LspReferenceRead cterm=bold ctermbg=DarkMagenta guibg=LightYellow
    --   hi LspReferenceText cterm=bold ctermbg=DarkMagenta guibg=LightYellow
    --   hi LspReferenceWrite cterm=bold ctermbg=DarkMagenta guibg=LightYellow
    --   augroup lsp_document_highlight
    --     autocmd! * <buffer>
    --     autocmd CursorHold <buffer> lua vim.lsp.buf.document_highlight()
    --     autocmd CursorMoved <buffer> lua vim.lsp.buf.clear_references()
    --   augroup END
    -- ]], false)
    -- end

    -- https://smarttech101.com/nvim-lsp-configure-language-servers-shortcuts-highlights/
    if client.server_capabilities.documentHighlightProvider then
        vim.cmd [[
      hi! LspReferenceRead cterm=bold ctermbg=235 guibg=LightYellow
      hi! LspReferenceText cterm=bold ctermbg=235 guibg=LightYellow
      hi! LspReferenceWrite cterm=bold ctermbg=235 guibg=LightYellow
    ]]
        vim.api.nvim_create_augroup('lsp_document_highlight', {})
        vim.api.nvim_create_autocmd({'CursorHold', 'CursorHoldI'}, {
            group = 'lsp_document_highlight',
            buffer = 0,
            callback = vim.lsp.buf.document_highlight
        })
        vim.api.nvim_create_autocmd('CursorMoved', {
            group = 'lsp_document_highlight',
            buffer = 0,
            callback = vim.lsp.buf.clear_references
        })
    end
end

nvim_lsp.gopls.setup {
    cmd = {'gopls'},
    -- for postfix snippets and analyzers
    capabilities = capabilities,
    settings = {
        gopls = {
            experimentalPostfixCompletions = true,
            analyses = {unusedparams = true, shadow = true},
            staticcheck = true
        }
    },
    on_attach = on_attach
}

function goimports(timeoutms)
    local context = {source = {organizeImports = true}}
    vim.validate {context = {context, "t", true}}

    local params = vim.lsp.util.make_range_params()
    params.context = context

    -- See the implementation of the textDocument/codeAction callback
    -- (lua/vim/lsp/handler.lua) for how to do this properly.
    local result = vim.lsp.buf_request_sync(0, "textDocument/codeAction",
                                            params, timeout_ms)
    if not result or next(result) == nil then return end
    local actions = result[1].result
    if not actions then return end
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

-- vim.lsp.set_log_level("debug")
