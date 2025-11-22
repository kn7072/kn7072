-- https://yazi-rs.github.io/docs/tips
Status:children_add(function()
    local h = cx.active.current.hovered
    if not h or ya.target_family() ~= "unix" then
        return ""
    end

    return ui.Line {
        ui.Span(ya.user_name(h.cha.uid) or tostring(h.cha.uid)):fg("magenta"),
        ":",
        ui.Span(ya.group_name(h.cha.gid) or tostring(h.cha.gid)):fg("magenta"),
        " "
    }
end, 500, Status.RIGHT)

-- https://yazi-rs.github.io/docs/tips
Header:children_add(function()
    if ya.target_family() ~= "unix" then
        return ""
    end
    return ui.Span(ya.user_name() .. "@" .. ya.host_name() .. ":"):fg("#fff173")
end, 500, Header.LEFT)

-- https://github.com/dedukun/bookmarks.yazi
require("bookmarks"):setup({
    last_directory = {enable = false, persist = false, mode = "dir"},
    persist = "all",
    desc_format = "parent",
    file_pick_mode = "hover",
    custom_desc_input = false,
    notify = {
        enable = false,
        timeout = 1,
        message = {
            new = "New bookmark '<key>' -> '<folder>'",
            delete = "Deleted bookmark in '<key>'",
            delete_all = "Deleted all bookmarks"
        }
    }
})

-- https://github.com/uhs-robert/recycle-bin.yazi
require("recycle-bin"):setup()
