set nocompatible              " be iMproved, required
set number
filetype off                  " required
set laststatus=2
set noshowmode
set cmdheight=1
set updatetime=50
set showcmd
set pastetoggle=<F2>
" set colorcolumn=80
" set the runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()
Plugin 'VundleVim/Vundle.vim'
Plugin 'tpope/vim-fugitive'
Plugin 'git://git.wincent.com/command-t.git'
Plugin 'rstacruz/sparkup', {'rtp': 'vim/'}
Plugin 'flazz/vim-colorschemes'
Plugin 'tpope/vim-surround'
Plugin 'itchyny/lightline.vim'
Plugin 'ryanoasis/vim-devicons'
Plugin 'dracula/vim', {'name':'dracula'}
Plugin 'chriskempson/base16-vim'

call vundle#end()            " required
filetype plugin indent on    " required
set tabstop=4 
set shiftwidth=4
set smarttab
set expandtab 
set softtabstop=4 
set autoindent
let python_highlight_all = 1
set t_Co=256

autocmd BufWritePre *.py normal m`:%s/\s\+$//e ``
autocmd BufRead *.py set smartindent cinwords=if,elif,else,for,while,try,except,finally,def,class

syntax on 
set termencoding=utf-8 
set novisualbell 
set t_vb= 
set backspace=indent,eol,start whichwrap+=<,>,[,]
set showtabline=1

set wrap
set linebreak

set nobackup
set noswapfile
set encoding=utf-8 
set fileencodings=utf8,cp1251

set clipboard=unnamed
set ruler

set hidden
nnoremap <C-N> :bnext<CR>
nnoremap <C-P> :bprev<CR>

set visualbell t_vb=

if has("gui_macvim")
  " Press Ctrl-Tab to switch between open tabs (like browser tabs) to 
  " the right side. Ctrl-Shift-Tab goes the other way.
  noremap <C-Tab> :tabnext<CR>
  noremap <C-S-Tab> :tabprev<CR>

 
  noremap <D-1> :tabn 1<CR>
  noremap <D-2> :tabn 2<CR>
  noremap <D-3> :tabn 3<CR>
  noremap <D-4> :tabn 4<CR>
  noremap <D-5> :tabn 5<CR>
  noremap <D-6> :tabn 6<CR>
  noremap <D-7> :tabn 7<CR>
  noremap <D-8> :tabn 8<CR>
  noremap <D-9> :tabn 9<CR>
  noremap <D-0> :tablast<CR>
endif

set guifont=Monaco:h18
colorscheme OceanicNext

let g:lightline = {
      \ 'colorscheme': 'wombat',
      \ 'active': {
      \   'left': [ [ 'mode', 'paste' ],
      \             [ 'gitbranch', 'readonly', 'filename', 'modified' ] ]
      \ },
      \ 'component_function': {
     \   'gitbranch': 'FugitiveHead',
     \   'filename': 'LightlineFilename',
      \ },
      \ }


function! LightlineFilename()
      return &filetype ==# 'vimfiler' ? vimfiler#get_status_string() :
              \ &filetype ==# 'unite' ? unite#get_status_string() :
              \ &filetype ==# 'vimshell' ? vimshell#get_status_string() :
              \ expand('%:t') !=# '' ? expand('%:t') : '[No Name]'
  endfunction

  let g:unite_force_overwrite_statusline = 0
  let g:vimfiler_force_overwrite_statusline = 0
  let g:vimshell_force_overwrite_statusline = 0

imap [ []<LEFT>
imap ( ()<LEFT>
imap { {}<LEFT>
" :inoremap " ""<LEFT>
" :inoremap ' ''<LEFT>
