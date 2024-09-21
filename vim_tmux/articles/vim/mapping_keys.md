This is the first part of a three part tutorial on mapping keys in Vim. You can read the other two parts of this tutorial from the following pages:

- [Mapping keys in Vim - Tutorial (Part 2)](https://vim.fandom.com/wiki/Mapping_keys_in_Vim_-_Tutorial_(Part_2) "Mapping keys in Vim - Tutorial (Part 2)")
- [Mapping keys in Vim - Tutorial (Part 3)](https://vim.fandom.com/wiki/Mapping_keys_in_Vim_-_Tutorial_(Part_3) "Mapping keys in Vim - Tutorial (Part 3)")

  

## Contents

- [1 Introduction](https://vim.fandom.com/wiki/Mapping_keys_in_Vim_-_Tutorial_(Part_1)#Introduction)
- [2 Creating keymaps](https://vim.fandom.com/wiki/Mapping_keys_in_Vim_-_Tutorial_(Part_1)#Creating_keymaps)
- [3 Storing the key maps](https://vim.fandom.com/wiki/Mapping_keys_in_Vim_-_Tutorial_(Part_1)#Storing_the_key_maps)
- [4 Listing key maps](https://vim.fandom.com/wiki/Mapping_keys_in_Vim_-_Tutorial_(Part_1)#Listing_key_maps)
- [5 Removing a keymap](https://vim.fandom.com/wiki/Mapping_keys_in_Vim_-_Tutorial_(Part_1)#Removing_a_keymap)
- [6 Mode-specific maps](https://vim.fandom.com/wiki/Mapping_keys_in_Vim_-_Tutorial_(Part_1)#Mode-specific_maps)
    - [6.1 Normal mode maps](https://vim.fandom.com/wiki/Mapping_keys_in_Vim_-_Tutorial_(Part_1)#Normal_mode_maps)
    - [6.2 Insert mode maps](https://vim.fandom.com/wiki/Mapping_keys_in_Vim_-_Tutorial_(Part_1)#Insert_mode_maps)
    - [6.3 Visual mode maps](https://vim.fandom.com/wiki/Mapping_keys_in_Vim_-_Tutorial_(Part_1)#Visual_mode_maps)
    - [6.4 Command-line mode maps](https://vim.fandom.com/wiki/Mapping_keys_in_Vim_-_Tutorial_(Part_1)#Command-line_mode_maps)
    - [6.5 Operator pending mode maps](https://vim.fandom.com/wiki/Mapping_keys_in_Vim_-_Tutorial_(Part_1)#Operator_pending_mode_maps)
- [7 Mapping mouse events](https://vim.fandom.com/wiki/Mapping_keys_in_Vim_-_Tutorial_(Part_1)#Mapping_mouse_events)
- [8 Nested (recursive) maps](https://vim.fandom.com/wiki/Mapping_keys_in_Vim_-_Tutorial_(Part_1)#Nested_(recursive)_maps)
- [9 Comments](https://vim.fandom.com/wiki/Mapping_keys_in_Vim_-_Tutorial_(Part_1)#Comments)

## Introduction[](https://vim.fandom.com/wiki/Mapping_keys_in_Vim_-_Tutorial_(Part_1)?veaction=edit&section=1 "Edit section: Introduction")

Key mapping refers to creating a shortcut for repeating a sequence of keys or commands. You can map keys to execute frequently used key sequences or to invoke an Ex command or to invoke a Vim function or to invoke external commands. Using key maps you can define your own Vim commands.

Vim supports several editing modes - normal, insert, replace, visual, select, command-line and operator-pending. You can map a key to work in all or some of these modes.

The general syntax of a map command is:

{cmd} {attr} {lhs} {rhs}

where
{cmd}  is one of ':map', ':map!', ':nmap', ':vmap', ':imap',
       ':cmap', ':smap', ':xmap', ':omap', ':lmap', etc.
{attr} is optional and one or more of the following: <buffer>, <silent>,
       <expr> <script>, <unique> and <special>.
       More than one attribute can be specified to a map.
{lhs}  left hand side, is a sequence of one or more keys that you will use
       in your new shortcut.
{rhs}  right hand side, is the sequence of keys that the {lhs} shortcut keys
       will execute when entered.

Examples:

map <F2> :echo 'Current time is ' . strftime('%c')<CR>
map! <F3> <C-R>=strftime('%c')<CR>
nnoremap <silent> <F2> :lchdir %:p:h<CR>:pwd<CR>

The first step in creating a map is to decide the sequence of keys the mapping will run. When you invoke a map, Vim will execute the sequence of keys as though you entered it from the keyboard. You can test the keys for your mapping by manually entering the key sequence and verifying that it performs the desired operation.

The second step is to decide the editing mode (insert mode, visual mode, command-line mode, normal mode, etc.) in which the map should work. Instead of creating a map that works in all the modes, it is better to define the map that works only in selected modes.

The third step is to find an unused key sequence that can be used to invoke the map. You can invoke a map using either a single key or a sequence of keys. [:help map-which-keys](http://vimdoc.sourceforge.net/cgi-bin/help?tag=map-which-keys)

The above steps are explained in more detail in the following sections.

  

## Creating keymaps[](https://vim.fandom.com/wiki/Mapping_keys_in_Vim_-_Tutorial_(Part_1)?veaction=edit&section=2 "Edit section: Creating keymaps")

To map a sequence of keys to execute another sequence of keys, use the ':map' command.

For example, the following command maps the <F2> key to display the current date and time.

:map <F2> :echo 'Current time is ' . strftime('%c')<CR>

The following command maps the <F3> key to insert the current date and time in the current buffer:

:map! <F3> <C-R>=strftime('%c')<CR>

The ':map' command creates a key map that works in normal, visual, select and operator pending modes. The ':map!' command creates a key map that works in insert and command-line mode.

A better alternative than using the 'map' and 'map!' commands is to use mode-specific map commands which are described in later sections.

## Storing the key maps[](https://vim.fandom.com/wiki/Mapping_keys_in_Vim_-_Tutorial_(Part_1)?veaction=edit&section=3 "Edit section: Storing the key maps")

If you want to map a key for only one Vim session temporarily, then you don't need to save the map command in a file. When you quit that Vim instance, the temporary map definition will be lost.

If you want to restore the key maps across Vim instances, you need to save the map definition command in a file.

One place to store the map commands is the $HOME/.vimrc or $HOME/_vimrc or $VIM/_vimrc file. If you have filetype specific key maps, then you can store them in the filetype specific plugin files. The key maps defined by Vim plugins are stored in the plugin or script file itself.

When adding the map commands to a file, there is no need to prefix the commands with the ':' character.

  

## Listing key maps[](https://vim.fandom.com/wiki/Mapping_keys_in_Vim_-_Tutorial_(Part_1)?veaction=edit&section=4 "Edit section: Listing key maps")

You can display a list of existing key maps using the following commands without any arguments:

:map
:map!

The first command displays the maps that work in normal, visual and select and operator pending mode. The second command displays the maps that work in insert and command-line mode.

To display the mode specific maps, prefix the ':map' command with the letter representing the mode.

:nmap - Display normal mode maps
:imap - Display insert mode maps
:vmap - Display visual and select mode maps
:smap - Display select mode maps
:xmap - Display visual mode maps
:cmap - Display command-line mode maps
:omap - Display operator pending mode maps

Example:

:nmap
n  <C-W>*      * <C-W><C-S>*
n  <C-W>#      * <C-W><C-S>#
n  <F2>        * :lchdir %:p:h<CR>:pwd<CR>

In the output of the above commands, the first column indicates the mode in which the map works. You can interpret the first column character using the following table:

n  Normal mode map. Defined using ':nmap' or ':nnoremap'.
i  Insert mode map. Defined using ':imap' or ':inoremap'.
v  Visual and select mode map. Defined using ':vmap' or ':vnoremap'.
x  Visual mode map. Defined using ':xmap' or ':xnoremap'.
s  Select mode map. Defined using ':smap' or ':snoremap'.
c  Command-line mode map. Defined using ':cmap' or ':cnoremap'.
o  Operator pending mode map. Defined using ':omap' or ':onoremap'.

<Space>  Normal, Visual and operator pending mode map. Defined using
         ':map' or ':noremap'.
!  Insert and command-line mode map. Defined using 'map!' or
   'noremap!'.

The following characters may be displayed before the {rhs} of the map:

*  The {rhs} of the map is not re-mappable. Defined using the
   ':noremap' or ':nnoremap' or ':inoremap', etc. commands.
&  Only script local mappings are re-mappable in the {rhs} of the
   map. The map command has the <script> attribute.
@  A buffer local map command with the <buffer> attribute.

To display all the key maps that start with a particular key sequence, enter the key sequence in the above commands. For example, the following command displays all the normal mode maps that start with 'g'.

:nmap g

To display all the buffer-local maps for the current buffer, use the following commands:

:map <buffer>
:map! <buffer>

Typically the output of the above commands will span several pages. You can use the following set of commands to redirect the output to the vim_maps.txt file:

:redir! > vim_maps.txt
:map
:map!
:redir END

## Removing a keymap[](https://vim.fandom.com/wiki/Mapping_keys_in_Vim_-_Tutorial_(Part_1)?veaction=edit&section=5 "Edit section: Removing a keymap")

To permanently remove a map, you first need to locate the place where it is defined by using the ':verbose map {lhs}' command (replace {lhs} with the mapped key sequence). If the map is defined in the .vimrc or _vimrc file or in one of the files in the vimfiles or .vim directory, then you can edit the file to remove the map.

Another approach is to use the ':unmap' and ':unmap!' commands to remove the map. For example, to remove the map for the <F8> key, you can use the following commands:

:unmap <F8>
:unmap! <F8>

Note that after a key is unmapped using the ':unmap' command, it can be mapped again later. Also you cannot unmap a key used by one of the Vim internal commands. Instead you have to map it to <Nop> to disable its functionality. If you are trying to disable a key map defined by a plugin, make sure the unmap command is executed after the key map is defined by the plugin. To do this in .vimrc, use autocmd:

autocmd VimEnter * unmap! <F8>

Filetype plugins can be a little tricky, because they can redefine mappings any time you open a file of a certain type. You can just use a different autocmd event for this, e.g.:

autocmd FileType python unmap! <F8>

Or, you can place the unmap command in the appropriate after directory. [:help after-directory](http://vimdoc.sourceforge.net/cgi-bin/help?tag=after-directory).

You can remove a mode-specific map by using the mode specific unmap command. The mode-specific unmap commands are listed below:

nunmap - Unmap a normal mode map
vunmap - Unmap a visual and select mode map
xunmap - Unmap a visual mode map
sunmap - Unmap a select mode map
iunmap - Unmap an insert and replace mode map
cunmap - Unmap a command-line mode map
ounmap - Unmap an operator pending mode map

Note that in the above unmap commands, if a space character is present at the end of the unmapped key sequence, then the command will fail. For example, the following unmap command will fail (replace <Space> with a space character):

:nnoremap <F2> :ls<CR>
:nunmap <F2><Space>

To map a key in only a selected set of modes, you can use the ':map' and ':map!' commands and then unmap them using the mode specific unmap commands in a few modes. For example, to map a key in normal and visual mode but not in operator-pending mode, you can use the following commands:

:map <F6> ....
:ounmap <F6>

To clear all the mappings for a particular mode, you can use the ':mapclear' command. The mode-specific map clear commands are listed below:

mapclear  - Clear all normal, visual, select and operating pending
            mode maps
mapclear! - Clear all insert and command-line mode maps
nmapclear - Clear all normal mode maps
vmapclear - Clear all visual and select mode maps
xmapclear - Clear all visual mode maps
smapclear - Clear all select mode maps
imapclear - Clear all insert mode maps
cmapclear - Clear all command-line mode maps
omapclear - Clear all operating pending mode maps

## Mode-specific maps[](https://vim.fandom.com/wiki/Mapping_keys_in_Vim_-_Tutorial_(Part_1)?veaction=edit&section=6 "Edit section: Mode-specific maps")

Vim supports creating keymaps that work only in specific editing modes. You can create keymaps that work only in normal, insert, visual, select, command and operator pending modes. The following table lists the various map commands and their corresponding editing mode:

Commands                        Mode
--------                        ----
nmap, nnoremap, nunmap          Normal mode
imap, inoremap, iunmap          Insert and Replace mode
vmap, vnoremap, vunmap          Visual and Select mode
xmap, xnoremap, xunmap          Visual mode
smap, snoremap, sunmap          Select mode
cmap, cnoremap, cunmap          Command-line mode
omap, onoremap, ounmap          Operator pending mode

Note that the language specific mappings defined using the ':lmap' and ':lnoremap' commands are not discussed here. For more information about this refer to the Vim help.

### Normal mode maps[](https://vim.fandom.com/wiki/Mapping_keys_in_Vim_-_Tutorial_(Part_1)?veaction=edit&section=7 "Edit section: Normal mode maps")

To map keys that work only in the normal mode, use the ':nmap' or ':nnoremap' command. The 'n' in ':nmap' and ':nnoremap' denotes normal mode.

For example, the following command maps the <F5> key to search for the keyword under the cursor in the current directory using the 'grep' command:

:nnoremap <F5> :grep <C-R><C-W> *<CR>

Examples:

The following commands map the 'j' key to execute 'gj' and the 'k' key to execute 'gk'. These are useful for moving between long wrapped lines.

:nnoremap k gk
:nnoremap j gj

The following command maps ',b' to display the buffer list and invoke the ':buffer' command. You can enter the desired buffer number and hit <Enter> to edit the buffer.

:nnoremap ,b :ls<CR>:buffer<Space>

In the above command, you can enter <Space> at the end of the map command either literally or by pressing the space bar.

To display the currently defined normal mode maps, use the ':nmap' command without any argument:

:nmap

To remove a keymap from normal mode, use the ':nunmap' command. For example, the following command removes the map for the <F9> key from normal mode:

:nunmap <F9>

If you invoke an Ex command from a map, you have to add a <CR> or <Enter> or <Return> at the end of the Ex command to execute the command. Otherwise the command will not be executed. For example:

:nnoremap <F3> :ls

With the above map, if you use <F3> in normal mode, you will be left in the ':' command-line after the text 'ls'. To execute the command, you have to use <CR> at the end of the command:

:nnoremap <F3> :ls<CR>

Now, when you press <F3>, the 'ls' Ex command will be executed.

From a normal mode map, you can get the keyword under the cursor using the expand('<cword>') function or using the <C-R><C-W> command. For example, the following two map commands provide the same functionality:

:nnoremap ,s :exe 'grep ' . expand('<cword>') . ' *'<CR>
:nnoremap ,s :grep <C-R><C-W> *<CR>

### Insert mode maps[](https://vim.fandom.com/wiki/Mapping_keys_in_Vim_-_Tutorial_(Part_1)?veaction=edit&section=8 "Edit section: Insert mode maps")

To map keys that work only in the insert and replace modes, use the 'imap' or 'inoremap' command.

Example: The following command maps <F2> to insert the directory name of the current buffer:

:inoremap <F2> <C-R>=expand('%:p:h')<CR>

To display the currently defined insert mode maps, use the 'imap' command without any argument:

:imap

To remove a keymap from insert mode, use the ':iunmap' command. For example, the following command removes the insert mode map for <F2>.

:iunmap <F2>

As printable keys insert a character in the current buffer in insert mode, you should use non-printable keys to create insert mode maps. Some examples for non-printable keys include the function keys <F2>, keys prefixed with the Ctrl or Alt key.

Alternatively, you can map keys that you're just not likely to need to insert, such as two capital letters in a row. This can be an attractive option for [quick insert-mode access to common normal-mode commands](https://vim.fandom.com/wiki/Quick_command_in_insert_mode "Quick command in insert mode").

To execute Vim normal mode commands from an insert mode map, you have to go from insert mode to normal mode. But after executing the map, you may want to restore the mode back to insert mode. To do this, you can use the <CTRL-O> insert-mode key which temporarily goes to normal-mode for one normal mode command and then comes back to insert mode. For example, to call the Vim function MyVimFunc() from insert mode, you can use the following map command:

:inoremap <F5> <C-O>:call MyVimFunc()<CR>

One caveat with using the <C-O> command is that if the cursor is after the last character in a line in insert mode, then <C-O> moves the cursor one character to the left after executing the map. If you don't want this, then you can use the <C-\><C-O> command, which doesn't move the cursor. But now the cursor may be placed on a character beyond the end of a line. The above map command is modified to use the <C-\><C-O> key:

:inoremap <F5> <C-\><C-O>:call MyVimFunc()<CR>

Both the <C-O> and <C-\><C-O> commands create a new undo point, i.e. you can undo the text inserted before and after typing these commands separately.

Another alternative for going from insert mode to normal mode is to use the <Esc> key. But it is preferable to use the <C-O> or <C-\><C-O> command for this.

If you press <Esc> in normal mode to make sure you are in normal mode, then you will hear the error beep sound. Instead, you can use the CTRL-\ CTRL-N command to go to normal mode. If you are already in normal mode, this command will not result in the error bell. This command can be used from a map to go to normal mode.

After executing the normal mode commands from an insert mode map, if the cursor position was moved by the map and no new text was inserted by the commands invoked, then you can use the gi command to restart the insert mode from the previous position where the insert mode was last stopped.

You can insert the result of a Vim expression in insert mode using the <C-R>= command. For example, the following command creates an insert mode map command that inserts the current directory:

:inoremap <F2> <C-R>=expand('%:p:h')<CR>

If you don't want to insert anything then you can return an empty string from the expression. For example, you can invoke a function from the insert mode map to perform some operation but return an empty string from the function.

The <C-R>= command doesn't create a new undo point. You can also call Vim functions using the <C-R>= command:

:inoremap <F2> <C-R>=MyVimFunc()<CR>

If the return value of MyVimFunc() is to be ignored and not entered after its call, a ternary operator trick may be used:

:inoremap <F2> <C-R>=MyVimFunc()?'':''<CR>

This will return an empty string, independent of what MyVimFunc() returns.

When Vim parses a string in a map command, the \<...> sequence of characters is replaced by the corresponding control character. For example, let us say in insert mode you want the down arrow key to execute <C-N> when the insert complete popup menu is displayed. Otherwise, you want the down arrow key to move the cursor one line down. You can try the following command (which doesn't work):

:inoremap <Down> <C-R>=pumvisible() ? '\<C-N>' : '\<Down>'<CR>

When parsing the above command, Vim replaces <C-N> and <Down> with the corresponding control characters. When you press the down arrow in insert mode, as there are control characters in the expression now, the command will fail.

To fix this, you should escape the '<' character, so that Vim will not replace '\<C-N>' with the control character when parsing the command. The following command works:

:inoremap <Down> <C-R>=pumvisible() ? '\<lt>C-N>' : '\<lt>Down>'<CR>

With the above command, Vim will use the control character only when the map is invoked and not when the above command is parsed.

To insert a template you should use a Vim abbreviation instead of a insert mode map. For more information about abbreviations refer to the Vim help.

Note that if the 'paste' option is set, then insert mode maps are disabled.

### Visual mode maps[](https://vim.fandom.com/wiki/Mapping_keys_in_Vim_-_Tutorial_(Part_1)?veaction=edit&section=9 "Edit section: Visual mode maps")

To map keys that work only in visual mode, use the ':vmap' or ':vnoremap' commands. These maps are invoked when you press the mapped keys after visually selecting a range of characters.

For example, the following command maps the g/ key sequence to search for the visually selected sequence of characters:

:vnoremap g/ y/<C-R>"<CR>

Another visual mode map example to add single quotes around a selected block of text:

:vnoremap qq <Esc>`>a'<Esc>`<i'<Esc>

To display all the currently defined visual mode maps, use the ':vmap' command without any arguments:

:vmap

To remove a visual mode map, use the ":vunmap" command. For example, the following command removes the visual mode map for g/:

:vunmap g/

From a visual mode map, you can either perform a text editing operation on the selected characters or add/remove characters at the beginning and/or end of the selected region or pass the selected text to some other internal/external command.

The '< Vim mark represents the first _line_ of a visual region and the '> mark represents the last _line_ of the visual region. The similar `< mark represents the beginning _character position_ of the visual region and the `> mark represents the ending _character position_ of the visual region. You can use these marks in your map to perform operation at the beginning and end of the visual region. If the map is invoked from visual mode, then these marks will refer to the beginning and end of the previous selection and not to the current selected region.

If you want to use the visually selected text in your map, then you can yank the text and then use it in your map. You can either yank the text to a register or use the unnamed (") register. For example, the following command maps the g/ key sequence to search for the visually selected text:

:vnoremap g/ y/<C-R>"<CR>

Another approach is to use the above described marks and get the text in the region from the buffer using the getline() function.

To execute an Ex command from a visual mode map, you have to first enter the command-line mode using the ':' character. After visually selecting a sequence of characters, when you press ':' to execute a Vim Ex command, Vim automatically inserts the visual block begin ('<') and end ('>') marks. If you invoke an Ex command with this range, then the command is executed for every line in this range. This may be undesirable. For example, if you invoke a Vim function, then the function will be executed separately for each line in the range (unless the function is defined with the '-range' attribute). To remove the visual block start and end marks, use the <C-U> command, which removes all the characters between the start of the line and the current cursor position, at the beginning of your map. For example,

:vnoremap <F2> :<C-U>call MyVimFunc()<CR>

When you enter a mapped key sequence in character-wise or line-wise or block-wise visual mode, the same visual map is invoked. You can use the visualmode() function in your map to differentiate between these modes. For example, the following code maps the <F5> keys in visual mode to invoke the MyFunc() function. The MyFunc() function uses the visualmode() function to distinguish between the visual modes.

vnoremap <silent> <F5> :<C-U>call MyFunc()<CR>
function! MyFunc()
    let m = visualmode()
    if m ==# 'v'
        echo 'character-wise visual'
    elseif m == 'V'
        echo 'line-wise visual'
    elseif m == "\<C-V>"
        echo 'block-wise visual'
    endif
endfunction

Note that we use ==# for the initial comparison instead of ==. This is because ==# will always make a case-sensitive comparison, whereas == will consider 'v' and 'V' to be the same if the ignorecase option has been set.

When you enter the command mode using ':' in visual mode, the visual mode is stopped. If you want to re-enter the visual mode from a function invoked from a map, you can use the gv command:

vnoremap <silent> <F5> :<C-U>call MyFunc()<CR>
function! MyFunc()
    normal! gv
endfunction

The maps created with the ":vmap" and ":vnoremap" commands work in both Visual mode and Select mode. When a map is invoked in select mode, Vim temporarily switches to visual mode before executing the map and at the end of the map, switches back to select mode. So the map behaves the same in visual and select mode.

To create a map that works only in Visual mode and not in Select mode use the ":xmap" and ":xnoremap" commands. All the other descriptions for the ":vmap" and ":vnoremap" commands also apply to the ":xmap" and ":xnoremap" commands.

To create a map that works only in Select mode and not in Visual mode use the ":smap" and ":snoremap" commands.

### Command-line mode maps[](https://vim.fandom.com/wiki/Mapping_keys_in_Vim_-_Tutorial_(Part_1)?veaction=edit&section=10 "Edit section: Command-line mode maps")

To map keys to work only in the command-line mode, use the "cmap" or ":cnoremap" commands.

The command-line mode map works in the following command prompts:

:    Ex command prompt
/    Forward search prompt
?    Backward search prompt
>    Debug prompt
@    input() prompt
-    :insert and :append prompts.

You can distinguish between the above prompts using the getcmdtype() function in your map. Example:

:cnoremap <F8> <C-R>=MyFunc()<CR>
function! MyFunc()
    let cmdtype = getcmdtype()
    if cmdtype == ':'
        " Perform Ex command map action
    elseif cmdtype == '/' || cmdtype == '?'
        " Perform search prompt map action
    elseif cmdtype == '@'
        " Perform input() prompt map action
    else
        " Perform other command-line prompt action
    endif
endfunction

To invoke functions from a command-line map, you have to use the '<C-R>=' command or the 'CTRL-\ e' command. An example map that shows this is below:

:cnoremap <C-F6> <C-R>=Somefunc()<CR>
:cnoremap <C-F6> <C-\>eSomefunc()<CR>

The <C-R>= command inserts the value returned by the invoked function at the current location in the command-line. The <C-\>e command replaces the entire command-line with the value returned by the invoked function.

The <C-R>= and <C-\>e commands cannot be used in the prompt for getting an expression (represented by =). For example, to insert the value of the Vim variable 'abc' in the command line, you can use <C-R>=abc<CR> command. In the prompt where you enter the variable name, you cannot again use <C-R>= and <C-\>e. To do this use the <expr> attribute to the map command as explained below.

Another way to invoke a function from a command-line mode map is to use the <expr> attribute as shown below:

:cnoremap <expr> <C-F6> Cmdfunc()

Using the above map, the value returned by Cmdfunc() is inserted at the current location in the command-line.

In the function invoked by the <C-R>= and <C-\>e commands and <expr> attribute, you can use the getcmdpos() function to get the current position of the cursor in the command. You can use the setcmdpos() function to change the location of the cursor in the command-line. You can use the getcmdline() function to get the current command-line.

It is preferable to use a non-printable control character for invoking a command-line mode map. Otherwise, the map may interfere with the printable characters used in the Vim Ex commands.

Note that if the 'paste' option is set, then command-line mode maps are disabled.

### Operator pending mode maps[](https://vim.fandom.com/wiki/Mapping_keys_in_Vim_-_Tutorial_(Part_1)?veaction=edit&section=11 "Edit section: Operator pending mode maps")

You can create maps that work only when waiting for a motion command from an operator command. For example, the yank command 'y' yanks the text that is selected by the motion that follows the command. To yank the current line and the two following lines of text, you can use the command 'y2j'. After pressing 'y', Vim waits for you to enter the motion command. The operator pending maps can be used here. The operator pending mode maps can be used to define your own text objects.

Operator pending commands are defined using the ":omap" and ":onoremap" commands.

For example, the following command creates an operator pending map for <F6> to select the current inner block defined by "{" and "}".

:onoremap <F6> iB

You can now yank an inner block using the y<F6> command, delete an inner block using the d<F6> command, etc.

To change the starting location of the operator from a operator-pending mode map, you can start visual mode and select the desired range of characters. One disadvantage in starting visual mode is that the previous visual region will be lost.

## Mapping mouse events[](https://vim.fandom.com/wiki/Mapping_keys_in_Vim_-_Tutorial_(Part_1)?veaction=edit&section=12 "Edit section: Mapping mouse events")

You can map mouse events similar to mapping keys to perform some action. The following mouse events can be mapped:

<LeftMouse>     - Left mouse button press
<RightMouse>    - Right mouse button press
<MiddleMouse>   - Middle mouse button press
<LeftRelease>   - Left mouse button release
<RightRelease>  - Right mouse button release
<MiddleRelease> - Middle mouse button release
<LeftDrag>      - Mouse drag while Left mouse button is pressed
<RightDrag>     - Mouse drag while Right mouse button is pressed
<MiddleDrag>    - Mouse drag while Middle mouse button is pressed
<2-LeftMouse>   - Left mouse button double-click
<2-RightMouse>  - Right mouse button double-click
<3-LeftMouse>   - Left mouse button triple-click
<3-RightMouse>  - Right mouse button triple-click
<4-LeftMouse>   - Left mouse button quadruple-click
<4-RightMouse>  - Right mouse button quadruple-click
<X1Mouse>       - X1 button press
<X2Mouse>       - X2 button press
<X1Release>     - X1 button release
<X2Release>     - X2 button release
<X1Drag>        - Mouse drag while X1 button is pressed
<X2Drag>        - Mouse drag while X2 button is pressed

Few examples for mapping the above mouse events is given below.

To jump to the tag under the cursor when the tag is double clicked, you can use the following map:

:nnoremap <2-LeftMouse> :exe "tag ". expand("<cword>")<CR>

The above map uses the expand() function to get the keyword under the cursor and then invokes the "tag" command with the current keyword. The "execute" command is used to concatenate the tag command and the output of the expand() function.

To map the X1 and X2 buttons to go forward and backward in the jump list, you can use the following map:

:nnoremap <X1Mouse> <C-O>
:nnoremap <X2Mouse> <C-I>

The above maps use the <C-O> and <C-I> normal mode commands to walk the jump list.

When you paste text using the middle mouse button, the text is pasted at the current cursor position. To paste at the position of the middle mouse button click, you can use the following map:

:nnoremap <MiddleMouse> <LeftMouse><MiddleMouse>

The above map first moves the cursor to the point where the click is made and then invokes the <MiddleMouse> functionality.

If you create a map for one of these mouse events, it overrides the internal default handling of that event by Vim. To pass the event to Vim, so that the default handling is also done, you can use "nnoremap" and specify the event in the {rhs} of the map. For example,

:nnoremap <LeftRelease> <LeftRelease>:call MyFunc()<CR>

With the above map, when the Left mouse button is pressed, the cursor is moved to that location and then the function MyFunc() is called.

You can disable a mouse event, by mapping it to <Nop> If you have a scrollwheel and often accidentally paste text when scrolling text, you can use the following mappings to disable the pasting with the middle mouse button:

:nnoremap <MiddleMouse> <Nop>
:inoremap <MiddleMouse> <Nop>

  

## Nested (recursive) maps[](https://vim.fandom.com/wiki/Mapping_keys_in_Vim_-_Tutorial_(Part_1)?veaction=edit&section=13 "Edit section: Nested (recursive) maps")

When executing a mapped key sequence, if the {lhs} is not a prefix of the {rhs}, then Vim scans and recursively replaces any mapped keys in the {rhs} of the map. This allows you to define nested and recursive mappings. For example, consider the following set of commands:

:map <F2>  :echo 'Current time = ' . strftime('%c')<CR>
:map <F3> <F2>

When you press <F3>, Vim executes the mapped key sequence for <F2> and displays the current time.

Note that Vim recursively checks for mappings on the {rhs} of a map when executing the map and not when defining the map. In the above example, if you redefine the map for <F2> later, then <F3> will execute the new map for <F2>.

If you include the {lhs} of a map in the {rhs}, then you will create an infinitely recursive key map. For example, the following insert mode map command creates an infinitely recursive map:

:imap ab xyzab

With the above map, when you enter "ab" in insert mode, it is replaced with "xyz" followed by "ab" which is replaced by "xyz" and so on. You can interrupt the recursive map by pressing CTRL-C.

Vim will recursively replace the mapped key sequence in the {rhs} of a map till it encounters an error. This can be used to create a recursive map that stops on error. For example, the following command creates a map for \s to replace "emacs" with "vi" in all the files in the argument list:

:nmap \s  :%s/emacs/vi/g \| update \| n<CR>\s

The "\s" at the end of the {rhs} in the map creates a recursive map. The recursive map will stop when it reaches the last file in the argument list as the "n" command will fail.

If the {rhs} of a map begins with the {lhs}, then it is not recursively replaced. For example, the following command will not create a recursive map for x:

:nmap x xyz

If you want to invoke other maps from your map, then define your maps using the ":map", ":map!", ":nmap", ":imap", ":vmap", ":cmap", ":xmap", ":smap" and ":omap" commands.

To prevent Vim from recursively replacing the mapped keys in the {rhs} of map, you can set the 'noremap' option. But instead of setting this option, it is preferable to use the 'noremap' command.

You can use the 'noremap' command to execute the {rhs} of a map literally without any map substitutions. For example, consider the following command which visually selects the current paragraph:

:map <F2> vip

If a map is defined for any character sequence in the {rhs}, then the above command will break. For example, consider the following map command which maps 'vi' to invoke 'gg':

:map vi gg

When you invoke <F2>, "vi" in the {rhs} will be replaced with "gg" resulting in an unexpected result. To prevent this from happening, you can use the following map command:

:noremap <F2> vip

Vim has the "noremap" version of the map command for all the mode specific map commands. You can use "nnoremap", "inoremap", "cnoremap", "vnoremap", "snoremap", "xnoremap" and "onoremap". In most of the map commands, it is better to use the "noremap" version of the command to prevent unexpected behavior.

When a key sequence which is mapped using "noremap" is entered at the end of an abbreviation, the abbreviation will not be expanded. For example, the following command creates an insert mode abbreviation for "vi":

:iabbr vi Vi Improved

In insert mode, when you enter "vi" followed by a space or Enter or some other control character, it is replaced with "Vi Improved". If you have the following map command for the <Enter> key:

:inoremap <Enter> <Enter><C-G>u

Now, if you press <Enter> after entering "vi", it will not be expanded to "Vi Improved". You can expand the abbreviation by pressing <Space> or by entering Ctrl-].

To read the second part of this tutorial, visit the [Mapping keys in Vim - Tutorial (Part_2)](https://vim.fandom.com/wiki/Mapping_keys_in_Vim_-_Tutorial_(Part_2) "Mapping keys in Vim - Tutorial (Part 2)") page.

## Comments[](https://vim.fandom.com/wiki/Mapping_keys_in_Vim_-_Tutorial_(Part_1)?veaction=edit&section=14 "Edit section: Comments")

It would be nice to have links to the official documentation (see [Template:Help](https://vim.fandom.com/wiki/Template:Help "Template:Help")).

Long ago we used !map - but I forget how it worked!

Regarding [#Operator pending mode maps](https://vim.fandom.com/wiki/Mapping_keys_in_Vim_-_Tutorial_(Part_1)#Operator_pending_mode_maps), it is actually possible to define custom text object selection o-mappings that change the starting location of the cursor. We must first move the cursor to the start of the selection, then go to visual mode, and finally move the cursor to the end of the selection. See for instance:

- [Indent text object](https://vim.fandom.com/wiki/Indent_text_object "Indent text object")
- [Creating new text objects](https://vim.fandom.com/wiki/Creating_new_text_objects "Creating new text objects")
- the thread about [Text object selection for function parameters](http://groups.google.com/group/vim_use/browse_frm/thread/94a43931e9e999c3/5b7fd13c4a2c8cae) on Vim mailing list.
- In the mouse section, it would be nice to mention if mouse scroll wheel events can be mapped

Very useful, thanks!


# Mapping keys in Vim - Tutorial (Part 2)
## Finding unused keys

_Further information: [Unused keys](https://vim.fandom.com/wiki/Unused_keys "Unused keys")_

In your private maps you should use key sequences that are not used by Vim and by other Vim plugins. [:help map-which-keys](http://vimdoc.sourceforge.net/cgi-bin/help?tag=map-which-keys)

Many of the key sequences that you can enter from the keyboard are used by Vim to implement the various internal commands. If you use a key sequence in your map that is already used by Vim, then you will not be able to use the functionality provided by Vim for that key sequence. To get a list of the key sequences used by Vim, read the following help topic:

:help index.txt

If you don't use some Vim functionality invoked by a particular key sequence or you have an alternate key sequence to use that functionality then you can use that key sequence in your maps.

Some of the key sequences may be used by the existing Vim scripts and plugins. To display the list of keys that are currently mapped, use the following commands:

:map
:map!

To determine the script or plugin that defines a map for a key sequence, use the following command.

:verbose map <key>

In the above command, replace <key> with the desired key sequence. For example, to list all the locations where maps beginning with "," are defined, use the following command:

:verbose map ,

Try to use an unused key sequence in your maps. Typically, the <F2>, <F3>, ... etc function keys are unused. The function keys in combination with Control, Alt and Shift can also be used. But some of the key combinations may not work in all the terminal emulators. Most of the key combinations should work in GUI Vim.

You can also prefix the desired key sequence with a backslash (\) or comma (,) or underscore (_), etc. and use that in your maps.

Note that you cannot map the Shift or Alt or Ctrl keys alone as they are key modifiers. You have to combine these key modifiers with other keys to create a map.

You should not use a frequently used Vim key sequence at the start of your maps. For example, you should not start your normal mode map key sequence with "j" or "k" or "l" or "h". These keys are used for moving the cursor in normal mode. If you use any of these keys at the beginning of your maps, then you will observe a delay when you enter a single "j" or "k" or "l" or "h".

## Key notation

When defining a map command, you can enter printable characters like 'a', 'V', etc. literally. You can enter non-printable control characters (like Ctrl-G, Alt-U, Ctrl-Shift-F2, F2, etc.) in several different ways.

You can enter a non-printable control character in a map command by preceding it with CTRL-V. For example, to map the Ctrl-K key to display the buffer list, you can use the following map command:

:map <press Ctrl-V><press Ctrl-K> :ls<press Ctrl-V><press Enter>

The Ctrl-V key sequence is used to escape the following control character.

The following table shows the mapping between some of the keys on the keyboard and the equivalent Ctrl-key combination:

Ctrl-I      Tab
Ctrl-[      Esc
Ctrl-M      Enter
Ctrl-H      Backspace

If you use one of the Ctrl-key combination in the above table in a map, the map also applies to the corresponding key. Both the keys produce the same key scan code. For example, if you create a map for CTRL-I, then you can invoke the map by pressing Ctrl-I or the Tab key.

On Unix like systems, the Ctrl-S and Ctrl-Q keys may be used for terminal flow control. If you map these keys in Vim, then when you invoke them, Vim will not receive these key sequences. To use these keys in Vim, you have to change the flow control characters used by the terminal using the 'stty start' and stty stop' commands to some other character or disable the terminal flow control using the following command:

$ stty -ixon

Similarly, Ctrl-Z is used to suspend Vim on Unix-like systems. To use Ctrl-Z in your maps, you can change the suspend character using the 'stty susp' command.

On MS-Windows, if the mswin.vim file is used, then CTRL-V is mapped to paste text from the clipboard. In this case, you can use CTRL-Q or CTRL+SHIFT+V instead of CTRL-V to escape control characters.

To create a map for the Ctrl-v key, you have to enter it four times:

:imap ^V^V^V^V EscapeCharacter

In the above command to enter a single ^V, you have to press Ctrl and v. When Vim parses the above command, it replaces the ^V^V^V^V sequence with ^V^V (two Ctrl-V characters). When the map is invoked, Vim replaces the two Ctrl-V characters with a single Ctrl-V character.

The Ctrl-J character represents the linefeed and is internally used by Vim to represent the Nul character. You cannot create a map for Ctrl-J by using the following command:

"The following command doesn't work
:imap <press Ctrl-V><press Ctrl-j> Newlinecharacter

You can also enter a control character by pressing Ctrl-V followed by the decimal or octal or hexadecimal value of the character. For example, to enter CTRL-P, you can press Ctrl-V followed by 016 (decimal) or x10 (hexadecimal) or o020.

Instead of entering the control characters directly in a map command as described above, it is preferable to use symbolic key notation for the control characters for readability. Vim supports representing control characters using symbolic notation like <F1>, <C-W>, <C-S-F1>, etc.

To determine the special key code representation that can be used in a map command, in insert mode, press the <CTRL-K> key followed by the key.

A key with the Ctrl key modifier is represented using the <C-key> notation. For example Ctrl-R is represented using <C-R>. A key with the Shift key modifier is represented using the <S-key> notation. For example Shift-F2 is represented using <S-F2>. A key with the Alt key modifier is represented using <A-key> or <M-key> notation. You can combine one or more key modifiers. For example, to represent Ctrl+Shift+F3 you can use <C-S-F3>. Super is represented <D-key> in MacVim and <T-key> in gtk2 gvim. In gvim it doesn't work with all the keys.

The Vim key notation for other special characters is listed below:

<BS>           Backspace
<Tab>          Tab
<CR>           Enter
<Enter>        Enter
<Return>       Enter
<Esc>          Escape
<Space>        Space
<Up>           Up arrow
<Down>         Down arrow
<Left>         Left arrow
<Right>        Right arrow
<F1> - <F12>   Function keys 1 to 12
#1, #2..#9,#0  Function keys F1 to F9, F10
<Insert>       Insert
<Del>          Delete
<Home>         Home
<End>          End
<PageUp>       Page-Up
<PageDown>     Page-Down
<bar>          the '|' character, which otherwise needs to be escaped '\|'

Note that Vim understands only those keys that are supplied by the operating system to Vim. If a particular key sequence is handled by a window manager or is intercepted by the operating system, then Vim will not see that key sequence. Then, you can not use that key sequence in Vim.

To determine whether Vim receives a key sequence, in insert mode press <CTRL-V> followed by the key sequence. If you see some characters in the buffer, then Vim is receiving the entered key sequence.

If the escape sequence received by Vim is not a standard sequence, you can set the sequence to the desired key. For example, let us say <PageUp> is generating a non-standard key sequence in your system. Then you can use the following command:

:set <PageUp>=<type Ctrl-V><type PageUp>

In the above command, the first <PageUp> is inserted literally (8 characters). The argument after = is entered by pressing Ctrl-V followed by the <PageUp> key.

You can also specify a character by its numeric value in a map. A character is represented by <Char-xxx>, where xxx is the value of the character in decimal or octal or hexadecimal.

For example, the key CTRL-P has a value of 16 (decimal). This is represented by <Char-16> (in decimal), <Char-020> (in octal) and <Char-0x10> (in hexadecimal). You can create a map for <CTRL-P> using any one of the following commands:

:nnoremap <C-P> {
:nnoremap <Char-16> {
:nnoremap <Char-020> {
:nnoremap <Char-0x10> {

You can also use the termcap entry for a key in the map. The termcap entries are represented using the format <t_xx> where 'xx' is replaced with the key. You can get a list of termcap keys using the ":set termcap" command. For example, to map F8 you can use <t_F8>:

:nnoremap <t_F8> :make<CR>

But it is preferable to use key notations instead of terminal codes for special keys.

## Supplying a count to a map

To repeat a normal mode Vim command, you can specify a count before the command. For example, to move the cursor 3 lines up, you can use the '3k' command. If you specify a count before a mapped key sequence, the map may not be repated by the specified count.

When a count is entered before invoking a map, the count will be prepended to the key sequence executed for the map. For example, assume you have mapped <F7> to move the cursor by 5 characters to the right:

:nnoremap <F7> 5l

If you invoke the above map with a count of 2 using 2<F7>, the cursor will not be moved 10 characters to the right. Instead, the cursor will be moved 25 characters to the right. This is because the count 2 is prepended to the 5 in the map resulting in 25.

To allow repeating a map by a specified count, you have to define your map using either the '=' expression register, the execute command, or a Vim function.

The '=' expression register allows you to specify an expression for the register contents. To use the expression register in your map, you have to combine that with the '@' operator. The '@' operator executes the contents of a register. If a count is specified before the '@' operator, then it executes the contents of a register by the specified count.

For example, change the above map command to:

:nnoremap <F7> @='5l'<CR>

Now, if you use 2<F7>, the cursor will be moved 10 characters to the right.

Some things to note about using the '=' register in your map. After specifying an expression, you have to use <CR> to end the command-line. If you want to use the escape character in the expression, you have to escape it using CTRL-V. For example, if you want to define a map to add the '#' character at the beginning of the current line, exit the insert mode and move the cursor one line down, you can use the following command:

:nnoremap <F4> @='I#<C-V><Esc>j'<CR>

Now if you press 3<F4>, the 3 lines starting from the current line are prefixed with the '#' character.

In the above map, if you specify a key sequence after the contents of the expression register, then those keys will not be executed by the '@' operator. So the specified count doesn't apply to those keys. For example, in the above map, if you move the 'j' out of the contents of the expression register:

:nnoremap <F4> @='I#<C-V><Esc>'<CR>j

Now, if you execute '3<F4>', three '#' characters will be added to the beginning of the current line and the cursor is moved to the following line.

Another approach, which is useful when mapping to Ex commands, is to build a command string with the concatenate operator '.' and execute this with the 'execute' command. Example:

:nnoremap g<C-T> :<C-U>exe v:count1 . "tag"<CR>

This will map 'g<C-T>' to ':tag' and '5g<C-T>' to ':5tag'.

The v:count1 variable returns 1 if a count is not specified to the last normal mode command. The v:count variable returns 0 if a count is not specified to the last normal mode command/map. In the above map, <C-U> is used to erase the text on the command-line before invoking the function.

A third approach to allow repeating a map is to use a Vim function to define the map. A Vim function can be defined to accept a count and repeat a operation that many number of times. You can use the "range" attribute to define a function that accepts a count.

If you supply a count to a function that doesn't accept a range, then you will get the 'Invalid range' error message. Example:

function! Myfunc()
  " Function that doesn't accept a range
endfunction
:nnoremap _w :call Myfunc()<CR>

If you specify a count to the _w command, then you will see the 'Invalid range' error message.

If you want your map to accept a range, then you have to specify the range attribute when defining the function as shown below:

function! Myfunc() range
  echo 'range = ' . a:firstline . ',' . a:lastline
endfunction
:nnoremap _w :call Myfunc()<CR>

Now you can pass a count to the _w map. The a:firstline and a:lastline variables in the function refer to the starting line number and ending line number of the range supplied to the function. The default is the current line number.

You can also use the internal v:count and v:count1 Vim variables in your function to get the count specified to the last normal mode command or map. Example:

:nnoremap <C-W> :<C-U>call Myfunc()<CR>
function! Myfunc()
  let c = v:count
  " Do something count number of times
endfunction

## Using multiple Ex commands in a map

You can specify multiple Ex commands separated by "|" (bar) in the Ex command line (":"). The "|" is used as the command separator. For example,

:set invignorecase | set ignorecase?

If you specify "|" in the {rhs} of a map, then Vim will treat it as a command separator and only the first command will be part of the map and the subsequent commands will be executed when defining the map. For example,

:nnoremap <F9> :set invignorecase | set ignorecase?<CR>

In the above command, "set ignorecase?" will not be part of the map for <F9>.

You have to escape the "|" by using backslash (\) or by using the <Bar> symbolic notation or by using CTRL-V. The following commands will work:

:nnoremap <F9> :set invignorecase \| set ignorecase?<CR>

:nnoremap <F9> :set invignorecase <Bar> set ignorecase?<CR>
:nnoremap <F9> :set invignorecase <press Ctrl-V>| set ignorecase?<CR>

Some Ex commands use the command that follows them (separated by |) as part of the command itself. For example, the ":global" (or ":g") command repeats the command that follows it for every matched pattern. In the following command,

:g/foo/s/abc/xyz/g | echo 'Completed substitution'

The ":echo" command is repeated for every 'foo' found in the current buffer. To execute the ":echo" command only once after the ":g" command completes, you have to use the ":exe" command.

:exe 'g/foo/s/abc/xyz/ge' | echo 'Completed substitution'

If your map uses one of these commands like ":g" then you have to use ":exe" in your map command.

Another way to invoke multiple Ex commands from a map is to invoke them separately as shown below:

:nnoremap <F9> :set invignorecase<CR>:set ignorecase?<CR>

Ex commands invoked from a map are not added to the command history. You can't recall the individual commands invoked by a map from the command-line.

## Using space characters in a map

If you want to use a space character in the {lhs} of a map command, then you have to use <Space> or escape the space character with CTRL-V (need to use two CTRL-Vs). Example:

nnoremap q<Space> M

The above command creates a normal mode map for the key sequence "q" followed by the space character to move the cursor to the middle of the page.

If you want to use the space character at the beginning of the {rhs} of a map command, then use <Space>. In other places in the {rhs}, you can use the space character by pressing the space bar. Example:

inoremap <C-F4> <Space><Space><Space>

The above command creates an insert mode map for the key sequence CTRL-F4 to enter three space characters.

Note that if you inadvertently use a space character at the end of the {rhs} in a map command, then the map may behave differently. For example, the following command maps the backspace character in normal mode to behave like the 'X' command and delete the character before the cursor:

nnoremap <BS> X

If there is a space character after "X" in the above command, then the map will delete the character before the cursor but leave the cursor at the current location instead of moving it back by one position. You can locate these kinds of errors, by looking at the output of the ":map" command. In the ":map" output, the space character at the end of the {rhs} in a map will be shown as "<Space>".

## Disabling key and mouse events

You can disable key and mouse events by mapping them to the special string "<Nop>". For example, to disable the <F4> key in normal mode, you can use the following command:

:nmap <F4> <Nop>

You can use the mode specific map command to disable a key in a particular mode.

The <Nop> sequence has a special meaning only if it appears by itself in the {rhs} of a map. You cannot use <Nop> with other keys in the {rhs} of a map. For example, the following command will not disable the <F1> key:

:inoremap <F1> <Nop><Nop>

You can disable mouse buttons and mouse events by mapping them to <Nop>. For example to disable the <MiddleMouse> button, you can use the following command:

:imap <MiddleMouse> <Nop>

## Error in mapped key sequences

When executing the key sequences in a key map, if Vim encounters an error, then the map will be aborted and the remaining key sequences will not be executed. You will not see any error message indicating that this has happened. If you have the 'errorbells' or 'visualbell' option set, then you will see the screen flash or hear the audio beep.

For example, consider the following key map that maps <F5> to toggle the case of the first letter of the current word.

nmap <F5> wb~

In most cases the above map will work as desired. But when the cursor is at the last word in the last line of a file, the above map will not work. In the last word of a file, the "w" command will fail and will not move the cursor to the next word. So the remaining part of the map will not be executed.

One way to workaround this problem is to split the command into two parts and execute them using the ":exec" command:

nmap <F5> :exec 'normal w'<Bar>exec 'normal b~'<CR>

## Maps and 'cpoptions' option

The 'cpoptions' Vim option contains many flags that control the compatibility level of Vim with the Vi behavior. To get the current value of the 'cpoptions' option, use the following command:

:set cpoptions?

When Vim is running in Vi-compatible mode, all the possible flags are set in the 'cpoptions' option.

The flags in the 'cpoptions' Vim option affect map definitions and their usage. These flags are described below.

If the flag 'b' is present in 'cpoptions', then a "|" character in a map command is treated as the end of the map command. This means that you cannot use backslash (\) to escape the "|" character in map command definitions.

Example:

:nnoremap <F5> :set invhlsearch \| set hlsearch?<CR>

If the 'b' flag is present in 'cpoptions', then the above map command definition will fail. All the characters after the backslash will not be part of the map.

If the flag 'B' is present in 'cpoptions', then the backslash character is not treated as a special character in map commands. For example, let us say you want to create an insert-mode map for the <F6> key to insert the text "Press <Home> to go to first character". For this, you can try using the following command:

imap <F6> Press <Home> to go to first character

When you press <F6> in the insert mode, the <Home> in the above map will cause Vim to move the cursor to the first character in the line and insert the reminder of the text there. To literally enter the text "<Home>", you need to escape it:

imap <F6> Press \<Home> to go to first character

If the flag 'B' is not present in 'cpoptions', then the above map command will insert the correct text. If the flag 'B' is present, then the backslash character is not treated as a special character and the above map will not insert the correct text. To treat <Home> literally independent of the 'cpoptions' setting, you can use the following command:

imap <F6> Press <lt>Home> to go to first character

In the above command, the notation <lt> is used for "<" in "<Home>".

If the flag 'K' is present in 'cpoptions', then you can cancel the invocation of a map in the middle of the key sequence by pressing <Esc>. For example, let us say you have the following map command:

:nnoremap <F3><F3> :ls<CR>

If the flag 'K' is present, then after entering the first <F3>, you can cancel the map by pressing <Esc>. If the flag 'K' is not present, then if you don't press any key after the first <F3>, Vim will wait for 'timeoutlen' milliseconds before cancelling the map (assuming the 'timeout' option is set).

If the flag 'k' is present in 'cpoptions', then raw key codes are not recognized in map commands. You can enter raw key code in a map command by pressing Ctrl-V followed by a control key. For example, consider the following map command:

nnoremap <press Ctrl-V><press Up arrow> gk

The above command maps the raw key code for the up arrow key to invoke the gk command. If the 'k' flag is not present in 'cpoptions', then the above command will properly work. If the 'k' flag is present in 'cpoptions', then the above map command will not work.

If the flag '<' is present in 'cpoptions', then special keys codes like <Tab>, <C-K>, <F1>, etc. are not recognized in maps. For example, consider the following maps:

:nnoremap <M-Right> <C-W>l
:nnoremap <M-Left> <C-W>h

If the '<' flag is present in 'cpoptions', then the above map commands will not work as the special key codes <M-Right>, <M-Left> and <C-W> will not be recognized.

## Maps and 'paste' option

While pasting text into a Vim buffer, to disable automatic indentation and interpreting mapped key sequences in the inserted text, you can set the 'paste' option. When the 'paste' option is set, mapped key sequences are ignored. By default, the 'paste' option is disabled. If your mapped keys are not working in a buffer, check whether the 'paste' option is set.

## Map attributes

You can modify the behavior of a key map by specifying several attributes in the map command. The supported attributes are <buffer>, <silent>, <special>, <script>, <expr>, and <unique>. You can specify one or more of these attributes in a map command immediately after the map command name.

### Buffer-local maps

When you create a map, the mapped key can be used in all the Vim buffers. To create a map that is applicable only to specific buffers, use the <buffer> attribute to the map command. For example,

:setlocal makeprg=gcc\ -o\ %<
:nnoremap <buffer> <F3> :make<CR>

The above command creates a map to compile the file opened in the current buffer. You can add the above set of commands to a filetype plugin. For example, you can add it to file `~/.vim/after/ftplugin/c.vim` (Unix) or `$HOME/vimfiles/after/ftplugin/c.vim` (Windows)—create any missing directories or files. Now, you can compile a C file in the current buffer, by pressing the <F3> key. When you open a Java file, this command will not be available.

When a buffer is deleted, the buffer local mappings for that buffer are removed. When a buffer is unloaded or hidden, you will not lose the mappings.

When you remove a buffer local map, you have to specify the <buffer> attribute to the ":unmap" or ":mapclear" command. Without the <buffer> attribute you cannot remove the map.

To display all the buffer-local mappings for the current buffer, use the following commands:

:map <buffer>
:map! <buffer>

To display the mode specific buffer-local maps, use the map command for that mode in the above command.

### Silent maps

When a map is invoked, the sequence of keys executed is displayed on the screen. If an Ex command is invoked by the map, then you can see the Ex command at the Vim status line. To silently execute a map, use the <silent> attribute for the map. For example,

:nnoremap <silent> <F2> :lchdir %:p:h<CR>:pwd<CR>

The above command maps the <F2> key to change to the directory of the current file and then display the current directory. When you invoke the above command, due to the <silent> attribute, you will not see the commands that are executed.

If the commands invoked by the map display a message, then those messages will be visible even though <silent> attribute is specified for the map command. For example, in the above command, the current directory displayed by the ":pwd" command will be visible.

### Expression maps

For simple maps, the action to be carried out for a key sequence can be defined without using a Vim function. But for complex maps, it is simpler to use a Vim function to implement the action for the map.

You can use the <expr> attribute to a map command to invoke a Vim function and use the returned value as the key sequence to execute.

For example, the following code creates a normal mode map to change to the directory of the current buffer.

function! ChangeToLocalDir()
  lchdir %:p:h
  return ''
endfunction
nnoremap <expr> _c ChangeToLocalDir()

In this example, the function returns an empty string so the map takes no action other than executing the function.

The <expr> attribute can be used with all the mode specific map commands.

### Special characters in maps

To use non-printable characters using the <> notation like <F5> in a map command, the '<' flag should not be present in the 'cpoptions' option. For example, the following map command will not work:

:set cpo+=<
:inoremap <F7> <C-X><C-N>

In insert mode, if you press <F7>, instead of executing the map, the characters <F7> will be inserted. To prevent this, you can use the <special> map attribute:

:inoremap <special> <F7> <C-X><C-N>

With the <special> map attribute, independent of the 'cpoptions' option setting, Vim will correctly process the <> key codes in the {rhs} of a map command.

[Mapping keys in Vim - Tutorial (Part 3)](https://vim.fandom.com/wiki/Mapping_keys_in_Vim_-_Tutorial_(Part_3) "Mapping keys in Vim - Tutorial (Part 3)")
										  
## Using maps in Vim plugins and scripts

A Vim plugin or script can define new key maps to let the user invoke the commands and functions provided by the plugin. A Vim plugin can also invoke key maps defined by other Vim plugins.

A plugin can choose to map any available key. But to avoid surprising (annoying) the user, it is better not to use the keys that already have pre-defined functionality in Vim.

In a Vim plugin, the ":normal" command is used to execute normal mode commands. For example, the "gqip" normal mode command is used to format a paragraph. To invoke this command from a Vim plugin, the following line can be used:

normal gqip

If any of the keys in "gqip" is mapped, then the mapped key sequence will be executed. This may change the expected behavior of the "gqip" command. To avoid this, add the "!" suffix to the "normal" command:

normal! gqip

With the "!" suffix, the "normal" command executes the built-in functionality provided by Vim for the specified sequence of keys.

To invoke a script local function, defined with the "s:" prefix, from a map, you have to prefix the function name with <SID>. You cannot use the "s:" prefix for the script-local function, as the map will be invoked from outside of the script context.

:inoremap <expr> <C-U> <SID>InsertFunc()

A plugin may map one or more keys to easily invoke the functionality provided by the plugin. In the plugin functions used by these types of maps, it is advisable not to alter user Vim option settings, register contents and marks. Otherwise, the user will be surprised to see that some options are changed after invoking a plugin provided map.

### Map leader

If the key maps provided by all the Vim plugins start with a same key, then it is easier for a user to distinguish between their own key maps and the ones provided by plugins. To facilitate this, Vim provides a special keyword that can be used in a map command.

If the {lhs} key sequence of a map command starts with the string "<Leader>", then Vim replaces it with the key set in the 'mapleader' variable. The default setting for the 'mapleader' variable is backslash ('\'). Note that 'mapleader' is a Vim variable and not a Vim option. The value of this variable can be changed using the 'let' command. For example, to set it to '_' (underscore), you can use the following command in your vimrc file:

let mapleader = "_"

Vim replaces <Leader> with the 'mapleader' value only when defining the map and not when the map is invoked. This means that after several map commands are defined if the 'mapleader' variable is changed, it will not affect the previously defined maps.

For example, consider the following map command defined by a plugin:

nnoremap <Leader>f :call <SID>JumpToFile()<CR>

When defining the above command, Vim replaces <Leader> with the value of the 'mapleader' variable. If the user didn't set the 'mapleader' variable then the above map can be invoked by entering \f. If the user sets the 'mapleader' to a comma (','), then it can be invoked using ,f.

The <Leader> prefix should be used for global mappings (applicable to all buffers) defined by a plugin. For buffer-local mappings, the <LocalLeader> prefix should be used. Vim will replace this with the value set in the 'maplocalleader' variable. The default value for this variable is backslash ('\'). The <LocalLeader> is generally used in mappings defined by a Vim filetype plugin.

The 'mapleader' and 'maplocalleader' variables allow the user to choose different keys as starting keys for global mappings and buffer-local mappings defined by Vim plugins.

### Script maps

If you want to use recursive maps in your map command, but want to use only those keys mapped in your script or plugin, then you can use the <script> attribute in the map definition. For example, consider the following two map commands in a script file:

noremap <SID>(FindTopic) /Topic<CR>
nmap <script> ,dt <SID>(FindTopic)dd

Within the second map command, only the '<SID>(FindTopic)' part is remapped. Without '<script>', 'dd' could be remapped too if someone defined a mapping for it.

If you use the <script> attribute with a ":noremap" command, then the <script> attribute overrides the ":noremap" command. The {rhs} of the map is still scanned for script-local key mappings. But the maps defined outside of the script are not used.

### Unique maps

If you want to make sure that the mapped key is unique and doesn't interfere with other existing mappings, use the <unique> map attribute. This attribute is particularly useful with the maps defined by a Vim plugin. A map definition with the <unique> attribute will fail if the specified key is already mapped.

:nnoremap <unique> \s :set invhlsearch<CR>

The above command will fail, if the user already has a mapping for the "\s" key sequence.

### Use of <Plug>

If you are developing a Vim plugin or script and you want to provide the user with the flexibility of assigning their own key map to invoke a function provided by your script, then you can prefix the map with <Plug>.

For example, let us say a plugin has a function s:VimScriptFn() and the user has to create a map to assign a key to invoke this function. The plugin can provide the following map to simplify this:

noremap <unique> <Plug>ScriptFunc :call <SID>VimScriptFn()<CR>

Note that in the above map command, instead of the typical key sequence for the {lhs} of the map, the <Plug>ScriptFunc text is used. The <Plug> generates a unique key sequence that a user cannot enter from a keyboard. The above map is visible outside of the script where it is defined.

With the above command, the user can assign _p to invoke the script function as shown below:

:nmap _p <Plug>ScriptFunc

### Map related functions

Vim provides built-in functions to check whether a key sequence is mapped or not and to get the mapped key sequence.

### maparg()

To get the {rhs} of a map command from a script or plugin, use the maparg() function. For example, consider the following commands:

:nnoremap <C-F2> 2<C-G>
:let x = maparg("<C-F2>", "n")
:echo x

The variable 'x' will be set to the mapped key sequence "2<C-G>".

The first argument to the maparg() function specifies the key sequence and the second argument specifies the editing mode. The maparg() function checks whether the specified key sequence is mapped in the specified mode and returns the {rhs} of the map if it is defined. If the mode is not specified, then the maparg() function checks for the map in the normal, visual and operator pending modes.

The maparg() function can be used to chain map commands. For example, let us say you want to define a map for <Tab>. But at the same time you don't want to lose the existing map (if any) for <Tab>. Then you can do the following:

:exe 'nnoremap <Tab> ==' . maparg('<Tab>', 'n')

The above command maps <Tab> to invoke the == command and then invoke the existing map for <Tab> in normal mode.

### mapcheck()

To check whether a map is defined for a key sequence, you can use the mapcheck() function. Example:

:echo mapcheck(';g', 'n')

### mode()

In a map command, you can use the mode() Vim function to get the current editing mode. But this function returns 'n' (normal) or 'c (command-line) in most cases. So this function cannot be used reliably from a map command to get the current mode. Instead, you should pass the current mode as an argument to the called function. For example, if you want to use a Vim function Somefunc() in several mode-specific map commands and want to distinguish between the modes in the function, then you can do the following:

:nnoremap _g :call Somefunc('n')<CR>
:inoremap _g <C-O>:call Somefunc('i')<CR>
:vnoremap _g :<C-U>call Somefunc('v')<CR>

### hasmapto()

To check whether a map is defined for a particular key sequence, you can use the hasmapto() function. Note that this function checks for the key sequence in the {rhs} of a map. Example:

if !hasmapto(":grep")
    " Define a mapping to invoke the :grep command
endif

The hasmapto() function checks for the specified key sequence anywhere in the {rhs} of a map (not necessarily at the beginning of the map).

The hasmapto() function also accepts an optional {mode} argument which allows you to check whether a map definition exists in a particular mode.

if !hasmapto(":grep", 'n')
    " Define a normal mode map to invoke :grep
endif

## Comments

Great series, thanks! One question: Suppose I have a plugin that remaps <C-\> and another plugin that calls <C-\><C-o> to execute a normal mode command in an insert mode mapping. The latter plugin assumes that <C-\> has not been remapped. Is there a way to change the second plugin so that it works even if <C-\> is remapped?

noremap, nnoremap...

[79.184.175.155](https://vim.fandom.com/wiki/Special:Contributions/79.184.175.155 "Special:Contributions/79.184.175.155") 13:21, March 12, 2012 (UTC)

The feedkeys() function could be given a mention? The flags 'nt' seem to me a nice sane way to remap keys when swapping them, that (hopefully) won't cause too many unwanted side-effects.