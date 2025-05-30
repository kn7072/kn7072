-- https://yazi-rs.github.io/docs/term   - терминалогия
-- Lua API
--     cx: Synchronous context state.
--     rt: Runtime information, such as user terminal emulator properties and global user preferences.
--     th: Theme system configuration.
--     fs: File system API.
--     ui: Layout system.
--     ya: Utility API, including functions for system time, debugging, shell commands, etc.
--     ps: Publish-subscribe system/data distribution service.
-- Show user/group of files in status bar
-- https://yazi-rs.github.io/docs/tips#user-group-in-status
--
Status:children_add(function()
    local h = cx.active.current.hovered
    if h == nil or ya.target_family() ~= "unix" then
        return ""
    end

    return ui.Line {
        ui.Span(ya.user_name(h.cha.uid) or tostring(h.cha.uid)):fg("magenta"),
        ":",
        ui.Span(ya.group_name(h.cha.gid) or tostring(h.cha.gid)):fg("magenta"),
        " "
    }
end, 500, Status.RIGHT)
