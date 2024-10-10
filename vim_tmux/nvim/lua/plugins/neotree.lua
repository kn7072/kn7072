vim.cmd([[ let g:neo_tree_remove_legacy_commands = 1 ]])

local sign = function(opts)
    vim.fn.sign_define(opts.name,
                       {texthl = opts.name, text = opts.text, numhl = ''})
end

-- If you want icons for diagnostic errors, you'll need to define them somewhere:
sign({name = 'DiagnosticSignError', text = ""})
sign({name = 'DiagnosticSignWarn', text = ""})
sign({name = 'DiagnosticSignHint', text = ""})
sign({name = 'DiagnosticSignInfo', text = ""})

-- NOTE: this is changed from v1.x, which used the old style of highlight groups
-- in the form "LspDiagnosticsSignWarning"

--[[
https://dev.to/vonheikemen/neovim-lsp-setup-nvim-lspconfig-nvim-cmp-4k8e?ysclid=m20o8b9s47591338765
{
  virtual_text = true,
  signs = true,
  update_in_insert = false,
  underline = true,
  severity_sort = false,
  float = true,
}

    virtual_text: Show diagnostic message using virtual text.

    signs: Show a sign next to the line with a diagnostic.

    update_in_insert: Update diagnostics while editing in insert mode.

    underline: Use an underline to show a diagnostic location.

    severity_sort: Order diagnostics by severity.

    float: Show diagnostic messages in floating windows.

Each one of these option can be either a boolean or a lua table. You can find more details about them in the documentation:

:help vim.diagnostic.config().

I prefer less distracting diagnostics. This is the setup I use.


vim.diagnostic.config({
  virtual_text = false,
  severity_sort = true,
  float = {
    border = 'rounded',
    source = 'always',
  },
})

--]]

require("neo-tree").setup({})
