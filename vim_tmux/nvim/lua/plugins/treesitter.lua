require'nvim-treesitter.configs'.setup {
    ensure_installed = {
        "typescript", "lua", "go", "javascript", "python", "bash", "sql",
        "markdown_inline"
    },

    sync_install = false,
    auto_install = true,
    highlight = {enable = true}
}
