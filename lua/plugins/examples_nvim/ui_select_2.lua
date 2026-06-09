vim.keymap.set('n', '<Leader>m', function()
    -- Список действий для меню
    -- Таблица действий, где каждый элемент - это объект с заголовком и функцией
    local actions = {
        {
            title = "📋 Вставить (Paste)",
            action = function()
                vim.cmd('normal! "+p')
            end
        }, {
            title = "📝 Копировать строку",
            action = function()
                vim.cmd('normal! "+yy')
            end
        }, {
            title = "🔍 Найти использования",
            action = function()
                vim.lsp.buf.references()
            end
        }, {
            title = "✏️ Переименовать (Rename)",
            action = function()
                vim.lsp.buf.rename()
            end
        }, {
            title = "💡 Действия кода (LSP)",
            action = function()
                vim.lsp.buf.code_action()
            end
        }, {
            title = "📂 Сохранить файл",
            action = function()
                vim.cmd('write')
            end
        }
    }

    -- Передаем таблицу actions напрямую
    vim.ui.select(actions, {
        prompt = "Контекстное меню:",
        -- Указываем, что именно отображать в списке (поле title)
        format_item = function(item)
            return item.title
        end
    }, function(choice)
        -- choice - это не строка, а весь объект из таблицы actions, который вы выбрали!
        if choice then
            choice.action() -- Просто вызываем его функцию
        end
    end)
end, {desc = 'Открыть контекстное меню Neovim'})
