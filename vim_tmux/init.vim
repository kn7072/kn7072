set number
set tabstop=4
set expandtab
set encoding=UTF-8
set noswapfile
set mouse=a

inoremap jk <esc>

syntax on
let g:mapleader=','
set hlsearch
set incsearch

" Toggle relative line number
nmap <C-L><C-L> :set invrelativenumber<CR>

call plug#begin()

Plug 'scrooloose/nerdtree', { 'on':  'NERDTreeToggle' }
Plug 'chun-yang/auto-pairs'
Plug 'tpope/vim-fugitive'
Plug 'ctrlpvim/ctrlp.vim'
Plug 'easymotion/vim-easymotion'
Plug 'mileszs/ack.vim'

" undo
Plug 'mbbill/undotree'

" color schemas
Plug 'morhetz/gruvbox'  " colorscheme gruvbox
Plug 'mhartington/oceanic-next'  " colorscheme oceanicnext
Plug 'kaicataldo/material.vim', { 'branch': 'main' }
Plug 'ayu-theme/ayu-vim'
Plug 'vim-airline/vim-airline'

" Debugging
Plug 'puremourning/vimspector'

" Иконки к файлам - под разные расширения
" Plug 'ryanoasis/vim-devicons'

" pgsql
Plug 'lifepillar/pgsql.vim'

call plug#end()

" Дерево изменений файла
noremap <leader>u :UndotreeToggle<CR>

let g:vimspector_enable_mappings = 'HUMAN'

nnoremap <Leader>dd :call vimspector#Launch()<CR>
nnoremap <Leader>de :call vimspector#Reset()<CR>
nnoremap <Leader>dc :call vimspector#Continue()<CR>

nnoremap <Leader>dt :call vimspector#ToggleBreakpoint()<CR>
nnoremap <Leader>dT :call vimspector#ClearBreakpoints()<CR>

nmap <Leader>dk <Plug>VimspectorRestart
nmap <Leader>dh <Plug>VimspectorStepOut
nmap <Leader>dl <Plug>VimspectorStepInto
nmap <Leader>dj <Plug>VimspectorStepOver

" цветовая схема
set background=dark
colorscheme gruvbox

" Go to tab by number
noremap <leader>1 1gt
noremap <leader>2 2gt
noremap <leader>3 3gt
noremap <leader>4 4gt
noremap <leader>5 5gt
noremap <leader>6 6gt
noremap <leader>7 7gt
noremap <leader>8 8gt
noremap <leader>9 9gt
noremap <leader>0 :tablast<cr>

"mappings
map <c-n> :NERDTreeToggle<cr>
map <leader> <plug>(easymotion-prefix)

" Move to word
map  <Leader>w <Plug>(easymotion-bd-w)
nmap <Leader>w <Plug>(easymotion-overwin-w)

" Move to line
map <Leader>L <Plug>(easymotion-bd-jk)
nmap <Leader>L <Plug>(easymotion-overwin-line)

" <Leader>f{char} to move to {char}
map  <Leader>f <Plug>(easymotion-bd-f)
nmap <Leader>f <Plug>(easymotion-overwin-f)

" s{char}{char} to move to {char}{char}
nmap s <Plug>(easymotion-overwin-f2)

" ctrl - a
map <c-a> <esc>ggvg<cr>

" PG_SQL
let g:sql_type_default = 'pgsql'

