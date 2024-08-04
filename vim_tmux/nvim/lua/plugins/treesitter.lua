require'nvim-treesitter.configs'.setup {
    ensure_installed = {
        "typescript", "lua", "go", "javascript", "python", "bash", "sql",
        "markdown_inline", "c"
    },
    sync_install = false,
    auto_install = true,
    highlight = {
        enable = true,
        -- disable = {"sql"}
        disable = function(lang, buf)
            local max_filesize = 1000 * 1024 -- 1000 KB
            local ok, stats = pcall(vim.loop.fs_stat,
                                    vim.api.nvim_buf_get_name(buf))
            if ok and stats and stats.size > max_filesize then
                return true
            end
        end
    }
}
