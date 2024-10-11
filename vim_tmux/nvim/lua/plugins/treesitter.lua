require'nvim-treesitter.configs'.setup({
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
        end,
        additional_vim_regex_highlighting = false

    },
    incremental_selection = {
        -- https://www.josean.com/posts/nvim-treesitter-and-textobjects
        -- Incremental selection based on the named nodes from the grammar.
        enable = true,
        keymaps = {
            init_selection = "<C-space>",
            node_incremental = "<C-space>",
            scope_incremental = false,
            node_decremental = "<bs>"
        }
    }
})
-- https://github.com/nvim-treesitter/nvim-treesitter
-- vim.wo.foldmethod = 'expr'
-- vim.wo.foldexpr = 'v:lua.vim.treesitter.foldexpr()'
--
-- vim.opt.fillchars:append({fold = ' '})
--
-- function myfoldtext()
--     local line = vim.fn.getline(vim.v.foldstart)
--     return string.format("%s %s ( lines: %s )", '+--', line,
--                          (vim.v.foldend - vim.v.foldstart + 1))
-- end
--
-- vim.opt.foldtext = 'v:lua.myfoldtext()'

-- не работает
-- vim.api.nvim_create_autocmd({"FileType"}, {
--     callback = function()
--         if require("nvim-treesitter.parsers").has_parser() then
--             vim.opt.foldmethod = "expr"
--             vim.opt.foldexpr = "nvim_treesitter#foldexpr()"
--         else
--             vim.opt.foldmethod = "syntax"
--         end
--     end
-- })
-- vim.cmd([[
--   set nofoldenable
--   set foldmethod=expr
--   set foldexpr=nvim_treesitter#foldexpr()
-- ]])
