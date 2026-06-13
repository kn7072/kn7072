# Использование `executeCommandProvider` в LSP (на примере gopls)

```
executeCommandProvider = {
    commands = {
 "gopls.add_dependency",
 "gopls.add_import",
 "gopls.add_telemetry_counters",
 "gopls.add_test",
 "gopls.apply_fix",
 "gopls.assembly",
 "gopls.change_signature",
 "gopls.check_upgrades",
 "gopls.client_open_url",
 "gopls.diagnose_files",
 "gopls.doc",
 "gopls.edit_go_directive",
 "gopls.extract_to_new_file",
 "gopls.fetch_vulncheck_result",
 "gopls.free_symbols",
 "gopls.gc_details",
 "gopls.generate",
 "gopls.go_get_package",
 "gopls.list_imports",
 "gopls.list_known_packages",
 "gopls.maybe_prompt_for_telemetry",
 "gopls.mem_stats",
 "gopls.modules",
 "gopls.package_symbols",
 "gopls.packages",
 "gopls.regenerate_cgo",
 "gopls.remove_dependency",
 "gopls.reset_go_mod_diagnostics",
 "gopls.run_go_work_command",
 "gopls.run_govulncheck",
 "gopls.run_tests",
 "gopls.scan_imports",
 "gopls.start_debugging",
 "gopls.start_profile",
 "gopls.stop_profile",
 "gopls.tidy",
 "gopls.update_go_sum",
 "gopls.upgrade_dependency",
 "gopls.vendor",
 "gopls.views",
 "gopls.vulncheck",
 "gopls.workspace_stats"
}
  },
```

Это «золотая жила» конкретного языкового сервера.

Список `commands` внутри `executeCommandProvider` — это **эксклюзивные, специфичные для этого сервера действия**, которые не входят в стандартный набор LSP.

Стандартный LSP умеет делать общие вещи (автодополнение, переход к определению). Но только сам `gopls` знает, как запустить тесты, почистить `go.mod` или показать статистику сборки. Чтобы клиент (Neovim) мог вызвать эти суперспособности, он использует универсальный LSP-метод **`workspace/executeCommand`**, передавая в него одно из этих строк-названий.

Вот как это используется на практике, от простого к продвинутому.

---

## 1. Базовый принцип вызова

Чтобы выполнить любую из этих команд, вы вызываете метод `workspace/executeCommand` и передаете ему два параметра: `command` (строку из списка) и `arguments` (массив аргументов, если они нужны, часто это пустой массив `{}`).

**Пример: выполнение `gopls.tidy` (аналог `go mod tidy`)**

Скопируйте и вставьте это в командную строку Neovim (`:`), находясь в Go-файле:

```vim
lua << EOF
local clients = vim.lsp.get_clients({ name = 'gopls', bufnr = 0 })
local client = clients[1]

if client then
    client.request('workspace/executeCommand', {
        command = 'gopls.tidy',
        arguments = {} -- Для tidy аргументы обычно не нужны
    }, function(err, result)
        if err then
            vim.notify("Ошибка gopls.tidy: " .. vim.inspect(err), vim.log.levels.ERROR)
        else
            vim.notify("go mod tidy успешно выполнен!", vim.log.levels.INFO)
            -- Часто после tidy нужно перезагрузить буфер или обновить diagnostics
            vim.cmd('e') -- перечитать файл, чтобы увидеть изменения
        end
    end)
else
    vim.notify("gopls не активен", vim.log.levels.WARN)
end
EOF
```

---

## 2. Как сделать это удобным (Привязка к клавишам)

Никто не вводит такие команды вручную. Обычно их вешают на хоткеи внутри `on_attach` для конкретного сервера.

Вот как это выглядит в реальном конфиге (например, в вашем `lsp/gopls.lua` или в глобальном `LspAttach`):

```lua
-- Внутри функции on_attach для gopls:
if client.name == 'gopls' then
    -- 1. Очистка go.mod (gopls.tidy)
    vim.keymap.set('n', '<leader>gt', function()
        client.request('workspace/executeCommand', {
            command = 'gopls.tidy',
            arguments = {}
        }, function(err, _)
            if not err then vim.notify('Gopls: go mod tidy выполнен', vim.log.levels.INFO) end
        end)
    end, { buffer = bufnr, desc = 'Gopls: Tidy go.mod' })

    -- 2. Показать детали сборщика мусора (gopls.gc_details)
    vim.keymap.set('n', '<leader>gg', function()
        client.request('workspace/executeCommand', {
            command = 'gopls.gc_details',
            arguments = {}
        }, function(err, result)
            if not err and result then
                -- result часто содержит WorkspaceEdit, который применяет изменения,
                -- или просто текст, который можно показать
                vim.notify('Gopls: GC details запрошены', vim.log.levels.INFO)
            end
        end)
    end, { buffer = bufnr, desc = 'Gopls: Show GC details' })
end
```

---

## 3. Команды с аргументами (Продвинутый уровень)

Некоторые команды требуют контекста. Например, `gopls.add_import` (добавить импорт) или `gopls.run_tests` (запустить тесты).

В спецификации LSP аргументы для `executeCommand` зависят исключительно от документации **конкретного сервера**. Для `gopls` документация находится [здесь](https://github.com/golang/tools/blob/master/gopls/doc/settings.md#commands).

Например, чтобы добавить импорт, `gopls` может ожидать аргументом URI файла и путь к пакету. Но на практике **большинство этих команд лучше вызывать не напрямую, а через Code Actions**.

---

## 4. Связь с Code Actions (Важный нюанс!)

Обратите внимание: многие команды из этого списка (например, добавление импорта, исправление ошибок) **дублируются** в системе Code Actions.

Если вы наведете курсор на неиспользуемый импорт или ошибку и вызовете:

```vim
:lua vim.lsp.buf.code_action()
```

...вы увидите в меню пункт вроде _"Organize Imports"_ или _"Fix"_. Под капотом, когда вы выбираете этот пункт в меню, Neovim как раз и отправляет серверу запрос `workspace/executeCommand` с нужной строкой (например, `"gopls.apply_fix"`).

**Правило большого пальца:**

1. Если действие зависит от контекста (где находится курсор, какая ошибка) → используйте **`vim.lsp.buf.code_action()`**.
2. Если это глобальное действие над проектом/файлом, не зависящее от курсора (например, `gopls.tidy`, `gopls.vendor`, `gopls.run_tests`) → привязывайте его к хоткею через **`workspace/executeCommand`**, как показано в пункте 2.

---

## Резюме

Массив `commands` в `executeCommandProvider` — это официальное "меню" скрытых возможностей сервера. Вы берете строку из этого меню, подставляете её в `client.request('workspace/executeCommand', { command = "..." })`, и получаете доступ к функциям, которые разработчики сервера не смогли (или не захотели) вписать в строгие рамки стандартного LSP.
