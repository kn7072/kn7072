## documentation
https://neovim.io/doc/user/api.html#nvim_create_user_command()

### nvim_create_user_command
nvim_create_user_command({name}, {command}, {opts}) Creates a global user-commands command.
For Lua usage see lua-guide-commands-create.
Example:

:call nvim_create_user_command('SayHello', 'echo "Hello world!"', {'bang': v:true})
:SayHello
Hello world!

Parameters:
{name} Name of the new user command. Must begin with an uppercase letter.
{command} Replacement command to execute when this user command is executed. When called from Lua, the command can also be a Lua function. The function is called with a single table argument that contains the following keys:
name: (string) Command name
args: (string) The args passed to the command, if any <args>
fargs: (table) The args split by unescaped whitespace (when more than one argument is allowed), if any <f-args>
nargs: (string) Number of arguments :command-nargs
bang: (boolean) "true" if the command was executed with a ! modifier <bang>
line1: (number) The starting line of the command range <line1>
line2: (number) The final line of the command range <line2>
range: (number) The number of items in the command range: 0, 1, or 2 <range>
count: (number) Any count supplied <count>
reg: (string) The optional register, if specified <reg>
mods: (string) Command modifiers, if any <mods>
smods: (table) Command modifiers in a structured format. Has the same structure as the "mods" key of nvim_parse_cmd().
{opts} Optional command-attributes.
Set boolean attributes such as :command-bang or :command-bar to true (but not :command-buffer, use nvim_buf_create_user_command() instead).
"complete" :command-complete also accepts a Lua function which works like :command-completion-customlist.
Other parameters:
desc: (string) Used for listing the command when a Lua function is used for {command}.
force: (boolean, default true) Override any previous definition.
preview: (function) Preview callback for 'inccommand' :command-preview

https://dev.to/vonheikemen/everything-you-need-to-know-to-configure-neovim-using-lua-3h58
https://stackoverflow.com/questions/76095689/passing-arguments-to-vim-api-nvim-create-user-command-in-order-to-execute-a-bash

:command SayHello  информация о команде

https://github.com/nanotee/nvim-lua-guide?tab=readme-ov-file
The -complete attribute can take a Lua function in addition to the attributes listed in :help :command-complete.

vim.api.nvim_create_user_command('Upper', function() end, {
    nargs = 1,
    complete = function(ArgLead, CmdLine, CursorPos)
        -- return completion candidates as a list-like table
        return { 'foo', 'bar', 'baz' }
    end,
})

:lua vim.cmd("Upper2 foo")

vim.api.nvim_create_user_command(
    'Upper',
    function(opts)
        print(string.upper(opts.args))
    end,
    { nargs = 1 }
)

:lua vim.cmd('Upper hello world')
:lua print(vim.cmd("Flake8 test_s.py"))
:lua vim.cmd.Flake8("test_s.py")

## creare command for comments
https://slar.se/comment-and-uncomment-code-in-neovim.html
local non_c_line_comments_by_filetype = {
    lua = "--",
    python = "#",
    sql = "--",
}

local function comment_out(opts)
    local line_comment = non_c_line_comments_by_filetype[vim.bo.filetype] or "//"
    local start = math.min(opts.line1, opts.line2)
    local finish = math.max(opts.line1, opts.line2)

    vim.api.nvim_command(start .. "," .. finish .. "s:^:" .. line_comment .. ":")
    vim.api.nvim_command("noh")
end

local function uncomment(opts)
    local line_comment = non_c_line_comments_by_filetype[vim.bo.filetype] or "//"
    local start = math.min(opts.line1, opts.line2)
    local finish = math.max(opts.line1, opts.line2)

    pcall(vim.api.nvim_command, start .. "," .. finish .. "s:^\\(\\s\\{-\\}\\)" .. line_comment .. ":\\1:")
    vim.api.nvim_command("noh")
end

vim.api.nvim_create_user_command("CommentOut", comment_out, { range = true })
vim.keymap.set("v", "<leader>co", ":CommentOut<CR>")
vim.keymap.set("n", "<leader>co", ":CommentOut<CR>")

vim.api.nvim_create_user_command("Uncomment", uncomment, { range = true })
vim.keymap.set("v", "<leader>uc", ":Uncomment<CR>")
vim.keymap.set("n", "<leader>uc", ":Uncomment<CR>")

