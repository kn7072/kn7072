## Search and replace in multiple buffers

Often [search and replace](https://vim.fandom.com/wiki/Search_and_replace "Search and replace") is needed in multiple files. This tip uses the procedures from [run a command in multiple buffers](https://vim.fandom.com/wiki/Run_a_command_in_multiple_buffers "Run a command in multiple buffers") to show how a substitute may be executed multiple times using `:argdo` (all files in argument list), or `:bufdo` (all buffers), or `:tabdo` (all tabs), `:windo` (all windows in the current tab), or `:cdo` (all files listed in the quickfix list).

## Contents
1 All buffers
2 All windows
3 All files in a tree
4 Replacing current word
5 Comments

## All buffers

The following performs a search and replace in all buffers (all those listed with the `:ls` command):

:bufdo %s/pattern/replace/ge | update

|           |             |
| --------- | ----------- |
| `bufdo`   | Apply the following commands to all buffers.                                                                                                                                                                                                                                                                                                 |
| `%s`      | Search and replace all lines in the buffer.                                                                                                                                                                                                                                                                                                  |
| `pattern` | Search ![](data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs=)[![](data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs=)pattern![](data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs=)](https://vim.fandom.com/wiki/Search_patterns "Search patterns")![](data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs=). |
| `replace` | Replacement text.                                                                                                                                                                                                                                                                                                                            |
| `g`       | Change all occurrences in each line (global).                                                                                                                                                                                                                                                                                                |
| `e`       | No error if the pattern is not found.                                                                                                                                                                                                                                                                                                        |
| `\|`      | Separator between commands.                                                                                                                                                                                                                                                                                                                  |
| `update`  | Save (write file only if changes were made).                                                                                                                                                                                                                                                                                                 |
The command above uses `:update` to save each buffer, if it was changed. That is necessary because, by default, Vim will not switch away from a buffer if it has been changed.

One alternative is to set the `'autowriteall'` option so changed buffers are automatically saved when required:

:set autowriteall
:bufdo %s/pattern/replace/ge

Another alternative is to set the `'hidden'` option so buffers do not need to be saved, then use `:wa` to save all changes (only changed buffers are written):

:set hidden
:bufdo %s/pattern/replace/ge
:wa

If you don't wish to save the results of your replacement, but want to review each changed buffer first, you can force the bufdo to continue without saving files with `bufdo!`:

:bufdo! %s/pattern/replace/ge

## All windows

If you are not dealing with a lot of files, it can be useful to display each wanted file in its own window, then operate on each window. For example, after opening multiple files with a shell command like `gvim *.c`, you could choose which files you wanted to operate on like this:

|   |   |
|---|---|
|`:sball`|Split screen to show all buffers (one window per buffer).|
|...|Move to a window you do _not_ want to change.|
|`<C-w>c`|Close the window (press Ctrl-W then `c`).|
|`<C-w>T<C-PageUp>`|Or, move the window to a new tab page, then switch back to the original tab.|
|...|Repeat until only buffers you want to change are displayed in the current tab page.|
|`:windo %s/pattern/replace/ge`|Search and replace in all visible windows.|
|`:wa`|Save all changes.|
## All files in a tree

Suppose all *.cpp and *.h files in the current directory need to be changed (not subdirectories). One approach is to use the argument list (arglist):

|   |   |
|---|---|
|`:arg *.cpp`|All *.cpp files in current directory.|
|`:argadd *.h`|And all *.h files.|
|`:arg`|_Optional_: Display the current arglist.|
|`:argdo %s/pattern/replace/ge \| update`|Search and replace in all files in arglist.|

A similar procedure can perform the same operation on all wanted files in the current directory, and in all subdirectories (or in any specified tree of directories):

|   |   |
|---|---|
|`:arg **/*.cpp`|All *.cpp files in and below current directory.|
|`:argadd **/*.h`|And all *.h files.|
|`...`|As above, use `:arg` to list files, or `:argdo` to change.|

In the above, a forward slash was used in `**/*.cpp`. That works on all systems (Unix and Windows). If wanted, a backslash can be used on Windows systems.

## Replacing current word

A common requirement is to replace the word under the cursor in a number of files. Rather than automating the process, it is best to use Vim's procedures. For example:

|                                   |                                             |
| --------------------------------- | ------------------------------------------- |
| `:arg *.cpp`                      | All *.cpp files in directory.               |
| `:argadd *.h`                     | And all *.h files.                          |
| `...`                             | Move cursor to word that is to be replaced. |
| `*`                               | Search for that exact word.                 |
| `:argdo %s//replace/ge \| update` | Search and replace in all files in arglist. |

In the above substitute command:

- The search pattern is empty, so the last search is used.
    
- Type your replacement text instead of `replace`. If the text is similar to the current word press Ctrl-R then Ctrl-W to insert that word into the command line, then change it.
    

Alternatively, you might try the following user command or mapping.
```bash
" Search for current word and replace with given text for files in arglist.
function! Replace(bang, replace)
  let flag = 'ge'
  if !a:bang
    let flag .= 'c'
  endif
  let search = '\<' . escape(expand('<cword>'), '/\.*$^~[') . '\>'
  let replace = escape(a:replace, '/\&~')
  execute 'argdo %s/' . search . '/' . replace . '/' . flag
endfunction
command! -nargs=1 -bang Replace :call Replace(<bang>0, <q-args>)
nnoremap <Leader>r :call Replace(0, input('Replace '.expand('<cword>').' with: '))<CR>
```
For example:

|      |      |
| ---- | ---- |
|`:arg *.c`| All *.c files in current directory.|
|`:set hidden`| Allow switching away from a changed buffer without saving.|
|`:set autowriteall`| Or, use this for automatic saving (instead of `:set hidden`).|
|`...`| Move cursor to word that is to be replaced.|
|`:Replace whatever`| Search and replace in all files in arglist; confirm each change.|
|`:Replace! whatever`| Same, but do not confirm each change.|
|`:wa`| Write all changed files (not needed if used `:set autowriteall`).|


Instead of the `:Replace` command, you could use the mapping. Move the cursor to the word that is to be replaced and press `\r` (backslash, assuming the default Leader key, then `r`).

In the function, any special characters in the search word are escaped for generality, although that is unlikely to be needed since a word will not contain special characters. If the cursor is on the word `old_text`, the search pattern will be `\<old_text\>` so that only instances of the whole word are found.
