-- source ./completion.lua
-- 1. Получаем всех активных клиентов pyright для текущего буфера (0)
local clients = vim.lsp.get_clients({name = 'pyright', bufnr = 0})
local client = clients[1]

if client then
    -- 2. Получаем текущую позицию курсора и URI буфера
    local pos = vim.api.nvim_win_get_cursor(0) -- возвращает {line, col} (line 1-индексирован, col 0-индексирован)
    local uri = vim.uri_from_bufnr(0)

    -- 3. Формируем параметры запроса (LSP требует 0-индексированные line и character)
    local params = {
        textDocument = {uri = uri},
        position = {line = pos[1] - 1, character = pos[2]}
    }

    -- 4. Отправляем запрос
    client.request('textDocument/completion', params, function(err, result)
        if err then
            vim.notify("LSP Error: " .. vim.inspect(err), vim.log.levels.ERROR)
        else
            -- Выводим результат в сообщения (или можно использовать vim.print для удобного чтения)
            vim.print(result)
        end
    end)
else
    vim.notify(
        "Клиент 'pyright' не найден для текущего буфера!",
        vim.log.levels.WARN)
end
