```lua
-- Открытие документа
client.notify('textDocument/didOpen', {
    textDocument = {
        uri = vim.uri_from_bufnr(0),
        languageId = "python",
        version = 1,
        text = vim.api.nvim_buf_get_lines(0, 0, -1, false)
    }
})

-- Изменение документа
client.notify('textDocument/didChange', {
    textDocument = {
        uri = vim.uri_from_bufnr(0),
        version = 2
    },
    contentChanges = {
        { text = "new content" }
    }
})

-- Запрос автодополнения
client.request('textDocument/completion', {
    textDocument = { uri = vim.uri_from_bufnr(0) },
    position = { line = 10, character = 5 }
}, function(err, result)
    print(vim.inspect(result))
end)

-- Запрос hover
client.request('textDocument/hover', {
    textDocument = { uri = vim.uri_from_bufnr(0) },
    position = { line = 10, character = 5 }
}, function(err, result)
    vim.notify(result.contents.value)
end)

-- Запрос определения
client.request('textDocument/definition', {
    textDocument = { uri = vim.uri_from_bufnr(0) },
    position = { line = 10, character = 5 }
}, function(err, result)
    -- Переход к определению
end)

-- Запрос диагностики
client.request('textDocument/diagnostic', {
    textDocument = vim.lsp.util.make_text_document_params(0)
}, function(err, result)
    print(vim.inspect(result))
end)
```
