https://neovim.io/doc/user/diagnostic.html#vim.diagnostic

lua vim.print(vim.inspect(vim.diagnostic.get(0, { severity = vim.diagnostic.severity.WARN })))
lua vim.print(vim.inspect(vim.diagnostic.get(0 ))) - все предупреждения

можно увидеть источник - source = "flake8"
{
    bufnr = 1,                                                                                                                                                                                                            
    col = 0,                                                                                                          
    lnum = 2,                                                                                                     
    message = "Import statements are in the wrong order. 'import os' should be before 'import sys'",                                                                                                                               
    namespace = 23,                                                                                                                                                                                                                 
    row = "3",                                                                                                                                                                                                                     
    severity = 2,                                                                                                                                                                                                                   
    source = "flake8"                                                                                                                                                                                                               
  } 

vim.diagnostic.severity.ERROR
vim.diagnostic.severity.WARN
vim.diagnostic.severity.INFO
vim.diagnostic.severity.HINT

lua vim.print(vim.inspect(vim.diagnostic.get(0, { severity = { vim.diagnostic.severity.WARN, vim.diagnostic.severity.INFO} })))


lua vim.print(vim.inspect(vim.diagnostic.GetOpts(23, 2, vim.diagnostic.severity.WARN)))
A table with the following keys:
Fields:
{namespace} (integer[]|integer) Limit diagnostics to one or more namespaces.
{lnum} (integer) Limit diagnostics to those spanning the specified line number.
{severity} (vim.diagnostic.SeverityFilter) See diagnostic-severity. 

lua vim.print(vim.inspect(vim.diagnostic.get_namespaces())) все namespace
lua vim.print(vim.inspect(vim.diagnostic.get_namespace(23))) информация по конкретному namespace 

lua vim.print(vim.inspect(vim.diagnostic))

## vim.diagnostic.GetOpts
    A table with the following keys:
    Fields:
    {namespace} (integer[]|integer) Limit diagnostics to one or more namespaces.
    {lnum} (integer) Limit diagnostics to those spanning the specified line number.
    {severity} (vim.diagnostic.SeverityFilter) See diagnostic-severity. 

## vim.diagnostic.count
Parameters:
{bufnr} (integer?) Buffer number to get diagnostics from. Use 0 for current buffer or nil for all buffers.
{opts} (vim.diagnostic.GetOpts?) See vim.diagnostic.GetOpts. 
lua vim.print(vim.diagnostic.count())
lua vim.print(vim.diagnostic.count(1))
lua vim.print(vim.diagnostic.count(1, {namespace=23, severity=vim.diagnostic.severity.INFO}))
lua vim.print(vim.diagnostic.count(1, {namespace=23, severity=vim.diagnostic.severity.WARN}))
Return:
        (table) Table with actually present severity values as keys (see
        diagnostic-severity) and integer counts as values.
{
    [3] = 2  - означает что есть 2 предупреждения с номером 3(vim.diagnostic.severity.INFO)
}


## vim.diagnostic.get_next()

    Get the next diagnostic closest to the cursor position.
Parameters:
{opts} (vim.diagnostic.JumpOpts?) See vim.diagnostic.JumpOpts.
Return:
        (vim.Diagnostic?) Next diagnostic. See vim.Diagnostic.


lua vim.print(vim.diagnostic.JumpOpts)

при наведении на предупреждение - отобразит текст в плавающем окне, чтобы можно было прочесть длиные предупреждения
https://neovim.io/doc/user/diagnostic.html#vim.diagnostic.Opts.Float - параметры для open_float
lua vim.diagnostic.open_float(0, {scope="line"})

