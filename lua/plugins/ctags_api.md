## articales
https://habr.com/ru/articles/468265/
асинхронный вызов
Давайте в качестве нашего подопечного возьмём плагин AsyncRun. Он умеет запускать асинхронно терминальные программы как в Vim 8, так и в NeoVim (ну и всех их разновидностях).

...
Plug 'skywind3000/asyncrun.vim'
...

nnoremap <F3> :AsyncRun ctags -R<CR>

## Api vim
### gettagstack
https://neovim.io/doc/user/builtin.html#gettagstack()
lua print(vim.inspect(vim.fn.gettagstack(0)));

### taglist
https://neovim.io/doc/user/builtin.html#taglist()
lua print(vim.inspect(vim.fn.taglist("^CALLOC")));

### settagstack
Write to the tag stack just like :tag but with a user-defined
jumper#jump_to_tag function:

" Store where we're jumping from before we jump.
let tag = expand('<cword>')
let pos = [bufnr()] + getcurpos()[1:]
let item = {'bufnr': pos[0], 'from': pos, 'tagname': tag}
if jumper#jump_to_tag(tag)
        " Jump was successful, write previous location to tag stack.
        let winid = win_getid()
        let stack = gettagstack(winid)
        let stack['items'] = [item]
        call settagstack(winid, stack, 't')
endif


https://neovim.io/doc/user/builtin.html#settagstack()
settagstack({nr}, {dict} [, {action}])
		Modify the tag stack of the window {nr} using {dict}.
		{nr} can be the window number or the window-ID.
		For a list of supported items in {dict}, refer to
		gettagstack(). "curidx" takes effect before changing the tag
		stack.
							E962  

		How the tag stack is modified depends on the {action} argument:
If {action} is not present or is set to 'r', then the tag stack is replaced.
If {action} is set to 'a', then new entries from {dict} are pushed (added) onto the tag stack.
If {action} is set to 't', then all the entries from the current entry in the tag stack or "curidx" in {dict} are removed and then new entries are pushed to the stack.
		The current index is set to one after the length of the tag
		stack after the modification.
		Returns zero for success, -1 for failure.
		Examples (for more examples see tagstack-examples):
		    Empty the tag stack of window 3:

call settagstack(3, {'items' : []})
Save and restore the tag stack:

let stack = gettagstack(1003)
" do something else
call settagstack(1003, stack)
unlet stack

Parameters:
{nr} (integer)
{dict} (any)
{action} (string?)
Return:
                  (any)

Set current index of the tag stack to 4:
call settagstack(1005, {'curidx' : 4})

Push a new item onto the tag stack:

let pos = [bufnr('myfile.txt'), 10, 1, 0]
let newtag = [{'tagname' : 'mytag', 'from' : pos}]
call settagstack(2, {'items' : newtag}, 'a')

### tagfiles
https://neovim.io/doc/user/builtin.html#tagfiles() узнать пути для поиска тегов

lua print(vim.inspect(vim.fn.tagfiles()));

:set tags? или так
## priority of tags

:h :tag (https://neovim.io/doc/user/tagsrch.html#tag-%21)
When there are multiple matches for a tag, this priority is used:
1. "FSC"  A full matching static tag for the current file.
2. "F C"  A full matching global tag for the current file.
3. "F  "  A full matching global tag for another file.
4. "FS "  A full matching static tag for another file.
5. " SC"  An ignore-case matching static tag for the current file.
6. "  C"  An ignore-case matching global tag for the current file.
7. "   "  An ignore-case matching global tag for another file.
8. " S "  An ignore-case matching static tag for another file.

Note that when the current file changes, the priority list is mostly not
changed, to avoid confusion when using ":tnext".  It is changed when using
":tag {name}".

:ta /^get
:tag /^CALLOC

:tag main
<	jumps to the tag "main" that has the highest priority. >

:tag /^get
<	jumps to the tag that starts with "get" and has the highest priority. >

:tag /norm
<	lists all the tags that contain "norm", including "id_norm".

Following vim commands can be used to navigate through relevant functions

    :ts – shows the list.
    :tn – goes to the next tag in that list.
    :tp – goes to the previous tag in that list.
    :tf – goes to the function which is in the first of the list.
    :tl – goes to the function which is in the last of the list.

## short_cut
https://stackoverflow.com/questions/563616/vim-and-ctags-tips-and-tricks

Ctrl+] - go to definition
Ctrl+T - Jump back from the definition.
Ctrl+W Ctrl+] - Open the definition in a horizontal split

Add these lines in vimrc
map <C-\> :tab split<CR>:exec("tag ".expand("<cword>"))<CR>
map <A-]> :vsp <CR>:exec("tag ".expand("<cword>"))<CR>

Ctrl+\ - Open the definition in a new tab
Alt+] - Open the definition in a vertical split

After the tags are generated. You can use the following keys to tag into and tag out of functions:

Ctrl+Left MouseClick - Go to definition
Ctrl+Right MouseClick - Jump back from definition

