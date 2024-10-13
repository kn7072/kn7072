local M = {}

M.on_attach = function(client, bufnr)
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
      hi! LspReferenceRead cterm=bold ctermbg=235 guibg=#e5c07b guifg=#000087 gui=bold
      hi! LspReferenceText cterm=bold ctermbg=235 guibg=#e5c07b guifg=#000087 gui=bold
      hi! LspReferenceWrite cterm=bold ctermbg=235 guibg=#e5c07b guifg=#000087 gui=bold
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

return M
