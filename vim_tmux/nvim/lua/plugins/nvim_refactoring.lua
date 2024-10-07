local err, ref_obj = pcall(require, "refactoring")
if not err then
    error(string.format("error %s", err))
end

ref_obj.setup({
    prompt_func_return_type = {
        go = true,
        java = false,

        cpp = false,
        c = true,
        h = true,
        hpp = false,
        cxx = false
    },
    prompt_func_param_type = {
        go = true,
        java = false,

        cpp = false,
        c = true,
        h = true,
        hpp = false,
        cxx = false
    },
    printf_statements = {},
    print_var_statements = {},
    show_success_message = false -- shows a message with information about the refactor on success
    -- i.e. [Refactor] Inlined 3 variable occurrences
})

-- load refactoring Telescope extension
-- require("telescope").load_extension("refactoring")

vim.keymap.set({"n", "x"}, "<leader>rr", function()
    require('refactoring').select_refactor()
    -- require('telescope').extensions.refactoring.refactors()
end)
