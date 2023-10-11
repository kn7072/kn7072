local M = {}

local _config = {}

function M.setup(config)
    -- simple variant
    _config = config
end

function M.do_something()
    local option_x = _config.option_x or "some_default_value"
    return option_x
end

return M
