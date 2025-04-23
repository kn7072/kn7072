local null_ls = require("null-ls")
local helpers = require("null-ls.helpers")

local methods = require("null-ls.methods")
local log = require("null-ls.logger")
local u = require("null-ls.utils")

local DIAGNOSTICS_ON_SAVE = methods.internal.DIAGNOSTICS_ON_SAVE
local FORMATTING = methods.internal.FORMATTING

local flake8 = {
    name = "flake8",
    method = methods.internal.DIAGNOSTICS,
    filetypes = {"python", "py"},
    -- null_ls.generator creates an async source
    -- that spawns the command with the given arguments and options
    generator = null_ls.generator({
        command = "flake8",
        args = {
            "--config", vim.fn.stdpath("config") .. "/plugin_configs/.flake8",
            "$FILENAME"
        },
        -- choose an output format (raw, json, or line)
        format = "line",
        check_exit_code = function(code, stderr)
            local success = code <= 1
            if not success then
                -- can be noisy for things that run often (e.g. diagnostics), but can
                -- be useful for things that run on demand (e.g. formatting)
                print(stderr)
            end
            -- print("success", success)
            return success
        end,
        -- use helpers to parse the output from string matchers,
        -- or parse it manually with a function
        on_output = helpers.diagnostics.from_patterns({
            {
                pattern = [[(%g+):(%d+):(%d+): ([%w%d]+) (.*)]],
                groups = {"filename", "row", "col", "code", "message"}
            }
        })
    })
}

local no_really = {
    method = null_ls.methods.DIAGNOSTICS,
    filetypes = {"markdown", "text"},
    generator = {
        fn = function(params)
            local diagnostics = {}
            -- sources have access to a params object
            -- containing info about the current file and editor state
            for i, line in ipairs(params.content) do
                local col, end_col = line:find("really")
                if col and end_col then
                    -- null-ls fills in undefined positions
                    -- and converts source diagnostics into the required format
                    table.insert(diagnostics, {
                        row = i,
                        col = col,
                        end_col = end_col + 1,
                        source = "no-really",
                        message = "Don't use 'really!'",
                        severity = vim.diagnostic.severity.WARN
                    })
                end
            end
            return diagnostics
        end
    }
}

local golang_my = {
    name = "golangci_lint_x",
    meta = {
        url = "https://golangci-lint.run/",
        description = "A Go linter aggregator."
    },
    --    method = DIAGNOSTICS_ON_SAVE,
    method = null_ls.methods.DIAGNOSTICS,

    filetypes = {"go"},
    generator_opts = {
        command = "golangci-lint",
        to_stdin = true,
        from_stderr = false,
        ignore_stderr = true,
        multiple_files = true,
        cwd = helpers.cache.by_bufnr(function(params)
            -- there might be cases when it's needed to setup cwd manually:
            -- check the golangci-lint docs for relative-path-mode.
            -- usually projects contain settings in root so this is sane default.
            return u.root_pattern("go.mod")(params.bufname)
        end),
        args = helpers.cache.by_bufnr(function(params)
            -- params.command respects prefer_local and only_local options
            local version = vim.system({params.command, "version"},
                                       {text = true}):wait().stdout
            -- from observation the version can be either v2.x.x or 2.x.x
            -- depending on packaging
            if version and
                (version:match("version v2") or version:match("version 2")) then
                return {
                    "run", "--fix=false", "--show-stats=false",
                    "--output.json.path=stdout"
                }
            end
            return {"run", "--fix=false", "--out-format=json"}
        end),
        format = "json",
        check_exit_code = function(code)
            return code <= 2
        end,
        on_output = function(params)
            local diags = {}
            if params.output["Report"] and params.output["Report"]["Error"] then
                log:warn(params.output["Report"]["Error"])
                return diags
            end
            local issues = params.output["Issues"]
            if type(issues) == "table" then
                for _, d in ipairs(issues) do
                    table.insert(diags, {
                        source = string.format("golangci-lint: %s", d.FromLinter),
                        row = d.Pos.Line,
                        col = d.Pos.Column,
                        message = d.Text,
                        severity = helpers.diagnostics.severities["warning"],
                        filename = u.pathelpers.join(params.cwd, d.Pos.Filename)
                    })
                end
            end
            return diags
        end
    },
    factory = helpers.generator_factory
}

local p_lint = {
    name = "pylint",
    meta = {
        url = "https://github.com/PyCQA/pylint",
        description = [[
Pylint is a Python static code analysis tool which looks for programming
errors, helps enforcing a coding standard, sniffs for code smells and offers
simple refactoring suggestions.

If you prefer to use the older "message-id" names for these errors (i.e.
"W0612" instead of "unused-variable"), you can customize pylint's resulting
diagnostics like so:

```lua
null_ls = require("null-ls")
null_ls.setup({
  sources = {
    null_ls.builtins.diagnostics.pylint.with({
      diagnostics_postprocess = function(diagnostic)
        diagnostic.code = diagnostic.message_id
      end,
    }),
    null_ls.builtins.formatting.isort,
    null_ls.builtins.formatting.black,
    ...,
  },
})
```
]]
    },
    method = methods.internal.DIAGNOSTICS,
    filetypes = {"python"},
    -- generator_opts = {
    generator = null_ls.generator({
        command = "pylint",
        to_stdin = true,
        args = {"--from-stdin", "$FILENAME", "-f", "json"},
        format = "json",
        check_exit_code = function(code)
            return code ~= 32
        end,
        on_output = helpers.diagnostics.from_json({
            attributes = {
                row = "line",
                col = "column",
                code = "symbol",
                severity = "type",
                message = "message",
                message_id = "message-id",
                symbol = "symbol",
                source = "pylint"
            },
            severities = {
                convention = helpers.diagnostics.severities["information"],
                refactor = helpers.diagnostics.severities["information"]
            },
            offsets = {col = 1, end_col = 1}
        }),
        cwd = helpers.cache.by_bufnr(function(params)
            return
                u.root_pattern( -- https://pylint.readthedocs.io/en/latest/user_guide/usage/run.html#command-line-options
                "pylintrc", ".pylintrc", "pyproject.toml", "setup.cfg",
                "tox.ini")(params.bufname)
        end)
    })
}

local lua_format = {
    name = "lua_format",
    filetypes = {"lua"},
    method = methods.internal.FORMATTING,
    generator = null_ls.generator({
        command = "lua-format",
        to_stdin = false,
        to_temp_file = true, -- чтобы использовать временный файл, в которй сохраняетя буфер, далее этот файл будет подан на вход форматеру(так сделано потому что у lua_format нет параметров для принятия данных по stdin - через stdin обычно передается содержимое буфера)

        args = {
            "--config",
            vim.fn.stdpath("config") .. "/plugin_configs/lua-format.yaml",
            "$FILENAME"
        },
        output = "raw",
        on_output = function(params, done)
            local output = params.output
            print(output)
            -- local metadata_end = output:match(".*====()") + 1
            -- return done({  text = output } )
            -- print(done(output))
            return done({{text = output}})
        end
    })
}

local example_source = {
    name = "example_source",
    filetypes = {["lua"] = true},
    methods = {[require("null-ls").methods.FORMATTING] = true},
    generator = {
        fn = function()
            return "I am a source!"
        end,
        ignore_stderr = true,
        to_stdin = true,

        output = "raw",
        on_output = function(params, done)
            local output = params.output
            -- local metadata_end = output:match(".*====()") + 1
            return output -- done({ { text = output:sub(metadata_end) } })
        end
    }
}
--[[
eslint-d
https://stackoverflow.com/questions/78108133/issue-with-none-ls-configuration-error-with-eslint-d
:NullLsInfo
lua print(vim.inspect(require("null-ls").get_sources()))

/home/stepan/.local/share/nvim/mason/bin/pylint --from-stdin /home/stepan/git_repos/kn7072/ANKI/TelegramBot/convert_sentence.py -f json

/home/stepan/.local/share/nvim/mason/bin/flake8 --config /home/stepan/.config/nvim/plugin_configs/.flake8 /home/stepan/git_repos/kn7072/ANKI/TelegramBot/create_file_for_anki_new.pylint

/home/stepan/.local/share/nvim/mason/bin/stylua --search-parent-directories --stdin-filepath /home/stepan/temp/lua_test/test_2.lua -
cat ./test_2.lua | stylua --stdin-filepath /home/stepan/temp/lua_test/test_2.lua -

--]]

null_ls.register(no_really)
null_ls.register(flake8)
null_ls.register(lua_format)
null_ls.register(example_source)
-- null_ls.register(golang_my)
-- null_ls.register(p_lint)
-- helpers.make_builtin(golang_my)
--
--
null_ls.setup({
    sources = {
        -- null_ls.builtins.formatting.lua_format,
        -- null_ls.builtins.formatting.lua_format.with({
        --     -- https://github.com/Koihik/LuaFormatter/blob/master/docs/Style-Config.md
        --     extra_args = {
        --         "--config",
        --         vim.fn.stdpath("config") .. "/plugin_configs/lua-format.yaml"
        --     }
        -- }),
        -- null_ls.builtins.formatting.stylua,
        null_ls.builtins.formatting.clang_format.with({
            extra_args = {
                -- https://clang.llvm.org/docs/ClangFormatStyleOptions.html
                string.format("--style=file:%s", vim.fn.stdpath("config") ..
                                  "/plugin_configs/.clang-format")
            }
        }), null_ls.builtins.formatting.black.with({filetypes = {"python"}}),
        null_ls.builtins.formatting.isort.with({
            filetypes = {"python"},
            extra_args = {
                string.format("--settings-path=%s", vim.fn.stdpath("config") ..
                                  "/plugin_configs/.isort.cfg")
            }
        }), -- null_ls.builtins.diagnostics.shellcheck,
         null_ls.builtins.diagnostics.pylint.with({
extra_args = {

                string.format("--rcfile=%s", vim.fn.stdpath("config") ..
                                  "/plugin_configs/.pylintrc")}

        }),
        null_ls.builtins.formatting.shfmt.with({
            extra_args = {"-i", "2", "-ci"},
            filetypes = {"bash", "sh"}
        }), null_ls.builtins.formatting.prettierd.with({
            filetypes = {"html", "json", "yaml", "markdown"}
        })
    },

    on_attach = function(client, bufnr)
        if client.supports_method("textDocument/formatting") then
            vim.api.nvim_clear_autocmds({group = augroup, buffer = bufnr})
            vim.api.nvim_create_autocmd("BufWritePre", {
                group = augroup,
                buffer = bufnr,
                callback = function()
                    vim.lsp.buf.format({
                        bufnr = bufnr,
                        filter = function(client)
                            return client.name == "null-ls"
                        end
                    })
                end
            })
        end
    end
})
