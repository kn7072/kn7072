local fn = vim.fn

-- vim.opt.errorformat = vim.opt.errorformat +
--                           "%E%f\\, line %l\\, character %c:,%Z%m"

function _G.prepare_qf(items)
    local filtered_items = {}
    for _, item_i in ipairs(items) do
        print(vim.inspect(item_i))
        if item_i.col > 18 then
            table.insert(filtered_items, item_i)
        end
    end
    return filtered_items
end

local items = vim.fn.getqflist()
items = prepare_qf(items)

fn.setqflist({}, 'r', {items = items, title = 'new'})
