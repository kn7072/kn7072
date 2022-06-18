set number
set tabstop=4
set shiftwidth=4
set expandtab
set smarttab
set encoding=UTF-8
set noswapfile
set mouse=a
" Подсвечивать строку на которой находится курсор
set cursorline
" Показывать колонну на 80 символе строк (по счёту)
set colorcolumn=80
" «Умный» поиск:
" - при вводе только маленьких (строчных) букв
"   ищет регистро-независимо
" - а если введена хотя бы одна большая (заглавная/прописная)
"   буква, то будет искать регистро-зависимо
set ignorecase
set smartcase
" Перенос длинных строк с разбиением по пробелам, а не по символам
" (слова переносятся целиком, soft wrap)
set wrap
set linebreak


inoremap jk <esc>

syntax on
let g:mapleader=','
set hlsearch
set incsearch

" Орфография
set spell spelllang=ru,en_us

" Автообновление, при изменении файла извне
set updatetime=2000
set autoread
autocmd FocusGained,BufEnter,CursorHold,CursorHoldI * checktime

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

" python
Plug 'Vimjas/vim-python-pep8-indent'
Plug 'dense-analysis/ale'
Plug 'neoclide/coc.nvim', {'branch': 'release'}
" Plug 'neoclide/coc-python'

" Debugging
Plug 'puremourning/vimspector'

" Иконки к файлам - под разные расширения
" Plug 'ryanoasis/vim-devicons'

" pgsql
Plug 'lifepillar/pgsql.vim'

" json
Plug 'kevinoid/vim-jsonc'
autocmd FileType json syntax match Comment +\/\/.\+$+

" Maximizes and restores the current window in Vim.
Plug 'szw/vim-maximizer'

" окружает слово в кавычки
Plug 'tpope/vim-surround'

" fzf - Нечёткий поиск (fuzzy finding) части имени файла
Plug 'junegunn/fzf', { 'do': { -> fzf#install() } }
Plug 'junegunn/fzf.vim'

call plug#end()

" Дерево изменений файла
noremap <leader>u :UndotreeToggle<CR>


fun GotoWindow(id)
        call win_gotoid(a:id)
        " MaximizerToggle
endfun        

" Debugger remaps
" https://www.youtube.com/watch?v=AnTX2mtOl9Q
nnoremap <Leader>m :MaximizerToggle!<CR>
nnoremap <Leader>ds :call GotoWindow(g:vimspector_session_windows.stack_trace)<CR>
" nnoremap <Leader>dtx :call win_gotoid( g:vimspector_session_windows.terminal )<CR>

nnoremap <Leader>dd :call vimspector#Launch()<CR>
nnoremap <Leader>de :call vimspector#Reset()<CR>
nnoremap <Leader>dc :call vimspector#Continue()<CR>

nnoremap <Leader>dt :call vimspector#ToggleBreakpoint()<CR>
nnoremap <Leader>dT :call vimspector#ClearBreakpoints()<CR>

nmap <Leader>dk <Plug>VimspectorRestart
nmap <Leader>dh <Plug>VimspectorStepOut
nmap <Leader>dl <Plug>VimspectorStepInto
nmap <Leader>dj <Plug>VimspectorStepOver

" убирает подсветку поиска
nnoremap <Leader><space> :nohlsearch<CR>

" Копирование от текущего символа до конца строки
" в режиме NORMAL при нажатии Shift+Y
" (Как Shift+D, только не удаляет скопированные символы)
nnoremap Y y$

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

" Линтер
let g:ale_linters = {'python': 'all'}
let g:ale_fixers = {'python': ['isort', 'yapf', 'remove_trailing_lines', 'trim_whitespace']}

let g:ale_lsp_suggestions = 1
let g:ale_fix_on_save = 1
let g:ale_go_gofmt_options = '-s'
let g:ale_go_gometalinter_options = '— enable=gosimple — enable=staticcheck'
let g:ale_completion_enabled = 1
let g:ale_echo_msg_error_str = 'E'
let g:ale_echo_msg_warning_str = 'W'
let g:ale_echo_msg_format = '[%linter%] [%severity%] %code: %%s'





