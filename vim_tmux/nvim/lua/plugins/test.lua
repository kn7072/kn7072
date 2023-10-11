local plugin = require("example-plugin")
local ok, whid = pcall(require, "whid")
if not ok then print("error") end
-- plugin.x()
