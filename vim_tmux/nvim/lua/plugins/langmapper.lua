local function escape(str)
	-- You need to escape these characters to work correctly
	local escape_chars = [[;,."|\]]
	return vim.fn.escape(str, escape_chars)
end

-- Recommended to use lua template string
local en = [[`qwertyuiop[]asdfghjkl;'zxcvbnm]]
local ru = [[ёйцукенгшщзхъфывапролджэячсмить]]
local en_shift = [[~QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>]]
local ru_shift = [[ËЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ]]

vim.opt.langmap = vim.fn.join({
	-- | `to` should be first     | `from` should be second
	escape(ru_shift)
		.. ";"
		.. escape(en_shift),
	escape(ru) .. ";" .. escape(en),
}, ",")

local langmapper = require("langmapper")
local default_config = {
	---@type boolean Add mapping for every CTRL+ binding or not.
	map_all_ctrl = true,
	---@type string[] Modes to `map_all_ctrl`
	---Here and below each mode must be specified, even if some of them extend others.
	---E.g., 'v' includes 'x' and 's', but must be listed separate.
	ctrl_map_modes = { "n", "o", "i", "c", "t", "v" },
	---@type boolean Wrap all keymap's functions (nvim_set_keymap etc)
	hack_keymap = true,
	---@type string[] Usually you don't want insert mode commands to be translated when hacking.
	---This does not affect normal wrapper functions, such as `langmapper.map`
	disable_hack_modes = { "i" },
	---@type table Modes whose mappings will be checked during automapping.
	automapping_modes = { "n", "v", "x", "s" },
	---@type string Standart English layout (on Mac, It may be different in your case.)
	default_layout = [[ABCDEFGHIJKLMNOPQRSTUVWXYZ<>:"{}~abcdefghijklmnopqrstuvwxyz,.;'[]`]],
	---@type string[] Names of layouts. If empty, will handle all configured layouts.
	use_layouts = {},
	---@type table Fallback layouts
	---Custom description builder:
	---  old_desc - original description,
	---  method - 'translate' (map translated lhs) or 'feedkeys' (call `nvim_feedkeys` with original lhs)
	---  lhs - original left-hand side for translation
	---should return new description as a string. If error is occurs or non-string is returned, original builder with `LM ()` prefix will use
	---@type nil|function(old_desc, method, lhs): string
	custom_desc = nil,
	layouts = {
		---@type table Fallback layout item. Name of key is a name of language
		ru = {
			---@type string Name of your second keyboard layout in system.
			---It should be the same as result string of `get_current_layout_id()`
			id = "com.apple.keylayout.RussianWin",
			---@type string Fallback layout to translate. Should be same length as default layout
			layout = "ФИСВУАПРШОЛДЬТЩЗЙКЫЕГМЦЧНЯБЮЖЭХЪËфисвуапршолдьтщзйкыегмцчнябюжэхъё",
			---@type string if you need to specify default layout for this fallback layout
			default_layout = nil,
		},
	},
	os = {
		-- Darwin - Mac OS, the result of `vim.loop.os_uname().sysname`
		Darwin = {
			---Function for getting current keyboard layout on your OS
			---Should return string with id of layout
			---@return string
			get_current_layout_id = function()
				local cmd = "im-select"
				if vim.fn.executable(cmd) then
					local output = vim.split(vim.trim(vim.fn.system(cmd)), "\n")
					return output[#output]
				end
			end,
		},
	},
}
langmapper.setup() -- default_config
