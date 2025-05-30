-- https://yazi-rs.github.io/docs/plugins/overview/#sync-context
return {
    entry = function(self, job)
        ya.dbg(job.args[1]) -- "foo"
        ya.dbg(job.args.bar) -- true
        ya.dbg(job.args.baz) -- "qux"
    end
}

-- https://yazi-rs.github.io/docs/plugins/overview/#logging
-- https://yazi-rs.github.io/docs/plugins/utils#ya.dbg
--
-- YAZI_LOG=debug yazi  сначала выполнить команду чтобы включить логирование
-- логи находятся тут /home/stepan/.local/state/yazi
