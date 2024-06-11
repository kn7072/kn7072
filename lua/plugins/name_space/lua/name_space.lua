local api = vim.api
local fn = vim.fn

local M = {}
local ns = vim.api.nvim_create_namespace("my_namespace")

vim.diagnostic.config({
    ["my/notify"] = {log_level = vim.log.levels.INFO},
    virtual_text = {prefix = "xxxxxx"}
})

vim.diagnostic.handlers["my/notify"] = {
    show = function(namespace, bufnr, diagnostics, opts)
        -- In our example, the opts table has a "log_level" option
        local level = opts["my/notify"].log_level
        local name = vim.diagnostic.get_namespace(namespace).name
        local msg = string.format("%d diagnostics in buffer %d from %s",
                                  #diagnostics, bufnr, name)
        vim.notify(msg, level)
    end
}

function M.setup()
    local pos = api.nvim_win_get_cursor(0)
    local ns = api.nvim_create_namespace('my-plugin')
    -- Create new extmark at line 1, column 1.
    local m1 = api.nvim_buf_set_extmark(0, ns, 0, 0, {})
    -- Create new extmark at line 3, column 1.
    local m2 = api.nvim_buf_set_extmark(0, ns, 14, 9, {})
    -- Get extmarks only from line 3.
    local ms = api.nvim_buf_get_extmarks(0, ns, {2, 0}, {2, 0}, {})
    -- Get all marks in this buffer + namespace.
    local all = api.nvim_buf_get_extmarks(0, ns, 0, -1, {})
    vim.print(ms)
end

function M.diag()
    local ns = api.nvim_create_namespace('my_ns')
    local diag_config = vim.diagnostic.config()
    -- vim.notify
    local s = "WARNING filename:27:3: Variable 'foo' does not exist"
    local pattern = "^(%w+) %w+:(%d+):(%d+): (.+)$"
    local groups = {"severity", "lnum", "col", "message"}
    local res = vim.diagnostic.match(s, pattern, groups,
                                     {WARNING = vim.diagnostic.WARN})
    print(res.message)

    -- vim.diagnostic.show(ns, 0, {lnum = 2, col = 4, message = "my_message"}, {})
    vim.notify(vim.diagnostic.count(0), vim.log.levels.INFO)
end

function M.diag_2()
    -- Create a custom namespace. This will aggregate signs from all other
    -- namespaces and only show the one with the highest severity on a
    -- given line

    -- Get a reference to the original signs handler
    local orig_signs_handler = vim.diagnostic.handlers.signs
    -- Override the built-in signs handler
    vim.diagnostic.handlers.signs = {
        show = function(_, bufnr, _, opts)
            -- Get all diagnostics from the whole buffer rather than just the
            -- diagnostics passed to the handler
            local diagnostics = vim.diagnostic.get(bufnr)
            -- Find the "worst" diagnostic per line
            local max_severity_per_line = {}
            for _, d in pairs(diagnostics) do
                local m = max_severity_per_line[d.lnum]
                if not m or d.severity < m.severity then
                    max_severity_per_line[d.lnum] = d
                end
            end
            -- Pass the filtered diagnostics (with our custom namespace) to
            -- the original handler
            local filtered_diagnostics = vim.tbl_values(max_severity_per_line)
            orig_signs_handler.show(ns, bufnr, filtered_diagnostics, opts)
        end,
        hide = function(_, bufnr) orig_signs_handler.hide(ns, bufnr) end
    }
end

return M
