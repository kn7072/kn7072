local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
if not vim.loop.fs_stat(lazypath) then
    vim.fn.system({
        "git", "clone", "--filter=blob:none",
        "https://github.com/folke/lazy.nvim.git", "--branch=stable", -- latest stable release
        lazypath
    })
end
vim.opt.rtp:prepend(lazypath)

require("lazy").setup({
    {'phaazon/hop.nvim'}, {
        'nvim-neo-tree/neo-tree.nvim',
        branch = 'v2.x',
        dependencies = {
            "nvim-lua/plenary.nvim", "nvim-tree/nvim-web-devicons",
            "MunifTanjim/nui.nvim", "s1n7ax/nvim-window-picker"
        }
    }, {'nvim-treesitter/nvim-treesitter'}, {'neovim/nvim-lspconfig'},
    {"williamboman/mason.nvim", build = ":MasonUpdate"},
    {'joshdick/onedark.vim'}, {'hrsh7th/cmp-nvim-lsp'}, {'hrsh7th/cmp-buffer'},
    {'hrsh7th/cmp-path'}, {'hrsh7th/cmp-cmdline'}, {'hrsh7th/nvim-cmp'}, {
        'nvim-telescope/telescope.nvim',
        tag = '0.1.1',
        dependencies = {'nvim-lua/plenary.nvim'}
    }, {'jose-elias-alvarez/null-ls.nvim'},
    {'akinsho/toggleterm.nvim', version = "*", config = true},
    {"akinsho/bufferline.nvim", dependencies = {'nvim-tree/nvim-web-devicons'}},
    {
        'glepnir/dashboard-nvim',
        event = 'VimEnter',
        dependencies = {{'nvim-tree/nvim-web-devicons'}}
    }, {'lewis6991/gitsigns.nvim'}, {
        'linrongbin16/lsp-progress.nvim',
        event = {'VimEnter'},
        dependencies = {'nvim-tree/nvim-web-devicons'},
        config = function() require('lsp-progress').setup() end
    }, {
        'nvim-lualine/lualine.nvim',
        dependencies = {
            'nvim-tree/nvim-web-devicons', 'linrongbin16/lsp-progress.nvim'
        }
    }, {"folke/which-key.nvim"}, {'windwp/nvim-autopairs'},
    {'terrortylor/nvim-comment'}, {'mfussenegger/nvim-dap'},
    {'nvim-tree/nvim-web-devicons'}, {'ryanoasis/vim-devicons'},
    {'rcarriga/nvim-dap-ui'}, {'leoluz/nvim-dap-go'},
    {'puremourning/vimspector'}, {'jay-babu/mason-nvim-dap.nvim'},
    {'hrsh7th/vim-vsnip'}, {'hrsh7th/vim-vsnip-integ'},
    {'slembcke/debugger.lua'}, {'jbyuki/one-small-step-for-vimkind'},
    {'example-plugin', dir = "~/example-plugin"},
    {'nvim-whid', dir = "~/.local/share/nvim/nvim-whid"}

})