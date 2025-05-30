local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
local path_to_my_plugin = vim.fn.stdpath('config') .. "/my_plugins/"

if not vim.loop.fs_stat(lazypath) then
    vim.fn.system({
        "git", "clone", "--filter=blob:none",
        "https://github.com/folke/lazy.nvim.git", "--branch=stable", -- latest stable release
        lazypath
    })
end
vim.opt.rtp:prepend(lazypath)

require("lazy").setup({
    {"phaazon/hop.nvim"}, {
        "nvim-neo-tree/neo-tree.nvim",
        branch = "v2.x",
        dependencies = {
            "nvim-lua/plenary.nvim", "nvim-tree/nvim-web-devicons",
            "MunifTanjim/nui.nvim", "s1n7ax/nvim-window-picker"
        }
    }, {"nvim-treesitter/nvim-treesitter"}, {"neovim/nvim-lspconfig"},
    {"williamboman/mason.nvim", build = ":MasonUpdate"},
    {"joshdick/onedark.vim"}, {"rebelot/kanagawa.nvim"},
    {'sainnhe/gruvbox-material', lazy = false, priority = 1000},
    {"hrsh7th/cmp-nvim-lsp"}, {"hrsh7th/cmp-buffer"}, {"hrsh7th/cmp-path"},
    {"hrsh7th/cmp-cmdline"}, {"hrsh7th/nvim-cmp"},
    {"hrsh7th/cmp-nvim-lsp-signature-help"}, {
        "nvim-telescope/telescope.nvim",
        tag = "0.1.8",
        -- branch = '0.1.x'
        dependencies = {
            {"nvim-lua/plenary.nvim"},
            {"nvim-telescope/telescope-live-grep-args.nvim"}
        }
    }, -- {"jose-elias-alvarez/null-ls.nvim"},
    {"nvimtools/none-ls.nvim"}, -- замена "jose-elias-alvarez/null-ls.nvim" НО не работает если просто заменить,
    {"akinsho/toggleterm.nvim", version = "*", config = true},
    {"akinsho/bufferline.nvim", dependencies = {"nvim-tree/nvim-web-devicons"}},
    {
        "glepnir/dashboard-nvim",
        event = "VimEnter",
        dependencies = {{"nvim-tree/nvim-web-devicons"}}
    }, {"lewis6991/gitsigns.nvim"}, {
        "linrongbin16/lsp-progress.nvim",
        event = {"VimEnter"},
        dependencies = {"nvim-tree/nvim-web-devicons"},
        config = function()
            require("lsp-progress").setup()
        end
    }, {
        "nvim-lualine/lualine.nvim",
        dependencies = {
            "nvim-tree/nvim-web-devicons", "linrongbin16/lsp-progress.nvim"
        }
    }, {"folke/which-key.nvim"}, {"windwp/nvim-autopairs"},
    {"terrortylor/nvim-comment"}, {"mfussenegger/nvim-dap"},
    {"nvim-tree/nvim-web-devicons"}, {"ryanoasis/vim-devicons"}, {
        "rcarriga/nvim-dap-ui",
        dependencies = {"mfussenegger/nvim-dap", "nvim-neotest/nvim-nio"}
    }, {"leoluz/nvim-dap-go"}, {"jay-babu/mason-nvim-dap.nvim"},
    --    {'hrsh7th/vim-vsnip'}, {'hrsh7th/vim-vsnip-integ'},
    -- {'slembcke/debugger.lua'},
    {"jbyuki/one-small-step-for-vimkind"}, {"rcarriga/nvim-notify"},
    {"yorickpeterse/nvim-window", config = true},
    -- {dir = "~/git_repos/kn7072/lua/plugins/switch_buffer"},
    -- {dir = "~/git_repos/kn7072/lua/plugins/surround"},
    {dir = path_to_my_plugin .. "switch_buffer"},
    {dir = path_to_my_plugin .. "surround"},
    {dir = "~/git_repos/kn7072/lua/plugins/study"}, {
        "L3MON4D3/LuaSnip",
        build = "make install_jsregexp",
        dependencies = {"rafamadriz/friendly-snippets"}
    }, {"rafamadriz/friendly-snippets"}, {"saadparwaiz1/cmp_luasnip"},
    {"mbbill/undotree"}, {
        "ThePrimeagen/refactoring.nvim",
        dependencies = {
            "nvim-lua/plenary.nvim", "nvim-treesitter/nvim-treesitter"
        }
    }, {"kevinhwang91/nvim-ufo", dependencies = {"kevinhwang91/promise-async"}},
    {"mmarchini/bpftrace.vim"}, -- {'window', dir = "~/.local/share/nvim/windows"},
    -- {'name_space', dir = "~/git_repos/kn7072/lua/plugins/name_space"}
    -- {'debugger_my', dir = "~/LUA/repo/debugger_my"}
    {
        "Wansmer/langmapper.nvim",
        lazy = false,
        priority = 1, -- High priority is needed if you will use `autoremap()`
        config = function()
            require("langmapper").setup({ --[[ your config ]] })
        end
    }, {"chentoast/marks.nvim", event = "VeryLazy", opts = {}}, {
        'iamcco/markdown-preview.nvim',
        cmd = {
            'MarkdownPreviewToggle', 'MarkdownPreview', 'MarkdownPreviewStop'
        },
        ft = {'markdown'},
        build = function()
            vim.fn['mkdp#util#install']()
        end
    }, {
        "lervag/vimtex",
        lazy = false, -- we don't want to lazy load VimTeX
        -- tag = "v2.15", -- uncomment to pin to a specific release
        init = function()
            -- VimTeX configuration goes here, e.g.
            -- vim.g.vimtex_view_method = "okular"
            vim.g.vimtex_view_general_viewer = 'okular'
            vim.g.vimtex_view_general_options =
                "--unique file:@pdf#src:@line@tex"

        end
    }
})
