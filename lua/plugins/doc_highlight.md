###nvim-treesitter

https://github.com/nvim-treesitter/nvim-treesitter

To customize the syntax highlighting of a capture, simply define or link a highlight group of the same name:

-- Highlight the @foo.bar capture group with the "Identifier" highlight group
vim.api.nvim_set_hl(0, "@foo.bar", { link = "Identifier" })

For a language-specific highlight, append the name of the language:

-- Highlight @foo.bar as "Identifier" only in Lua files
vim.api.nvim_set_hl(0, "@foo.bar.lua", { link = "Identifier" })

https://neovim.io/doc/user/api.html#nvim_set_hl()


See :h treesitter-highlight-groups for details.

  *treesitter-highlight-groups*
The capture names, with `@` included, are directly usable as highlight groups.
For many commonly used captures, the corresponding highlight groups are linked
to Nvim's standard |highlight-groups| by default but can be overridden in
colorschemes.

A fallback system is implemented, so that more specific groups fallback to
more generic ones. For instance, in a language that has separate doc comments,
`@comment.doc` could be used. If this group is not defined, the highlighting
for an ordinary `@comment` is used. This way, existing color schemes already
work out of the box, but it is possible to add more specific variants for
queries that make them available.

As an additional rule, capture highlights can always be specialized by
language, by appending the language name after an additional dot. For
instance, to highlight comments differently per language: >vim

    hi @comment.c guifg=Blue
    hi @comment.lua guifg=DarkBlue
    hi link @comment.doc.java String
<
The following captures are linked by default to standard |group-name|s:
 
    @text.literal      Comment
    @text.reference    Identifier
    @text.title        Title
    @text.uri          Underlined
    @text.underline    Underlined
    @text.todo         Todo

    @comment           Comment
    @punctuation       Delimiter

    @constant          Constant
    @constant.builtin  Special
    @constant.macro    Define
    @define            Define
    @macro             Macro
    @string            String
    @string.escape     SpecialChar
    @string.special    SpecialChar
    @character         Character
    @character.special SpecialChar
    @number            Number
    @boolean           Boolean
    @float             Float

    @function          Function
    @function.builtin  Special
    @function.macro    Macro
    @parameter         Identifier
    @method            Function
    @field             Identifier
    @property          Identifier
    @constructor       Special

    @conditional       Conditional
    @repeat            Repeat
    @label             Label
    @operator          Operator
    @keyword           Keyword
    @exception         Exception

    @variable          Identifier
    @type              Type
    @type.definition   Typedef
    @storageclass      StorageClass
    @structure         Structure
    @namespace         Identifier
    @include           Include
    @preproc           PreProc
    @debug             Debug
    @tag               Tag


###nvim_set_hl
:highlight посмотреть все стили
:highlight Identifier посмотреть группу Identifier

nvim_set_hl({ns_id}, {name}, {val})
Sets a highlight group.
Note:
Unlike the :highlight command which can update a highlight group, this function completely replaces the definition. For example: nvim_set_hl(0, 'Visual', {}) will clear the highlight group 'Visual'.
The fg and bg keys also accept the string values "fg" or "bg" which act as aliases to the corresponding foreground and background values of the Normal group. If the Normal group has not been defined, using these values results in an error.
If link is used in combination with other attributes; only the link will take effect (see :hi-link).
Parameters:
{ns_id} Namespace id for this highlight nvim_create_namespace(). Use 0 to set a highlight group globally :highlight. Highlights from non-global namespaces are not active by default, use nvim_set_hl_ns() or nvim_win_set_hl_ns() to activate them.
{name} Highlight group name, e.g. "ErrorMsg"
{val} Highlight definition map, accepts the following keys:
fg: color name or "#RRGGBB", see note.
bg: color name or "#RRGGBB", see note.
sp: color name or "#RRGGBB"
blend: integer between 0 and 100
bold: boolean
standout: boolean
underline: boolean
undercurl: boolean
underdouble: boolean
underdotted: boolean
underdashed: boolean
strikethrough: boolean
italic: boolean
reverse: boolean
nocombine: boolean
link: name of another highlight group to link to, see :hi-link.
default: Don't override existing definition :hi-default
ctermfg: Sets foreground of cterm color ctermfg
ctermbg: Sets background of cterm color ctermbg
cterm: cterm attribute map, like highlight-args. If not set, cterm attributes will match those from the attribute map documented above.
force: if true force update the highlight group when it exists.


======================================================
diff
:help hl-DiffAdd

The colors are controlled by these four highlight groups (:help hl-DiffAdd):

DiffAdd     diff mode: Added line
DiffChange  diff mode: Changed line
DiffDelete  diff mode: Deleted line
DiffText    diff mode: Changed text within a changed line

These are typically defined by a color scheme, but you can customize them in your ~/.vimrc (after the :colorscheme command) if you like you scheme overall, just not its diff highlighting. Just redefine using :highlight. Here are my personal customizations (for GVIM; for the terminal you need the appropriate ctermfg/bg=... attributes instead / in addition):

hi DiffAdd      gui=none    guifg=NONE          guibg=#bada9f
hi DiffChange   gui=none    guifg=NONE          guibg=#e5d5ac
hi DiffDelete   gui=bold    guifg=#ff8080       guibg=#ffb0b0
hi DiffText     gui=none    guifg=NONE          guibg=#8cbee2

If you're switching colorschemes on the fly, you need to re-invoke those :hi commands via :autocmd ColorScheme * hi ...



