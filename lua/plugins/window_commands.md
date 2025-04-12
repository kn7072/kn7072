## nvim_list_wins() 
nvim_list_wins()
Gets the current list of window handles.
Return:
List of window handles

lua print(vim.inspect(vim.api.nvim_list_wins()))

## nvim_win_get_config
nvim_win_get_config({window}) 
Gets window configuration.
The returned value may be given to nvim_open_win().
relative is empty for normal windows.
Parameters:
{window} Window handle, or 0 for current window
Return:
Map defining the window configuration, see nvim_open_win()

lua local list_windows = vim.api.nvim_list_wins(); for i, window_i in ipairs(list_windows) do print(vim.inspect(vim.api.nvim_win_get_config(window_i))) end
lua local window_id = 1000; print(vim.inspect(vim.api.nvim_win_get_config(window_id)))

## nvim_get_current_win
nvim_get_current_win()
Gets the current window.
Return:
Window handle

lua print(vim.inspect(vim.api.nvim_get_current_win()))

## nvim_set_current_win
nvim_set_current_win({window})
Sets the current window.
Attributes:
not allowed when textlock is active or in the cmdwin
Parameters:
{window} Window handle

lua local window_id = 1000; vim.api.nvim_set_current_win(window_id)

## nvim_win_close
nvim_win_close({window}, {force}) 
Closes the window (like :close with a window-ID).
Attributes:
not allowed when textlock is active
Parameters:
{window} Window handle, or 0 for current window
{force} Behave like :close! The last window of a buffer with unwritten changes can be closed. 
The buffer will become hidden, even if 'hidden' is not set.

lua vim.api.nvim_win_close(window, true)

## nvim_win_get_buf
nvim_win_get_buf({window}) 
Gets the current buffer in a window
Parameters:
{window} Window handle, or 0 for current window
Return:
Buffer handle

lua local win_i = 1009; local buf_id = tonumber(vim.inspect(vim.api.nvim_win_get_buf(win_i))); print(buf_id);

## nvim_win_set_height
nvim_win_set_height({window}, {height})
Sets the window height.
Parameters:
{window} Window handle, or 0 for current window
{height} Height as a count of rows

lua local win_i = 1009; vim.api.nvim_win_set_height(win_i, 200);

## nvim_win_set_width
nvim_win_set_width({window}, {width})
Sets the window width. This will only succeed if the screen is split vertically.
Parameters:
{window} Window handle, or 0 for current window
{width} Width as a count of columns

lua local win_i = 1009; vim.api.nvim_win_set_width(win_i, 100)

## nvim_win_set_config
nvim_win_set_config({window}, {config})
Configures window layout. Cannot be used to move the last window in a tabpage to a different one.
When reconfiguring a window, absent option keys will not be changed. row/`col` and relative must be reconfigured together.
Parameters:
{window} Window handle, or 0 for current window
{config} Map defining the window configuration, see nvim_open_win()

показать текущую конфигурацию
lua local win_i = 1009; local origin_config = vim.api.nvim_win_get_config(win_i); print(vim.inspect(origin_config))

сделать float окно
lua local win_i = 1009; local origin_config = vim.api.nvim_win_get_config(win_i); origin_config.split = nil; origin_config.col = 10; origin_config.row = 10; origin_config.relative = 'win'; vim.api.nvim_win_set_config(win_i, origin_config)

вернуть плавающее окно в фиксированное положение внутрь окна win_for_split и расположить слева (split = "left")
lua local win_for_change = 1009; local win_for_split = 1000; local origin_config = vim.api.nvim_win_get_config(win_for_change); origin_config={win=win_for_split, external = false,focusable = true,height = 18, hide = false,relative = "", split = "left",width = 51}; vim.api.nvim_win_set_config(win_for_change, origin_config)


lua local curr_win = vim.api.nvim_get_current_win(); local curr_buf = vim.api.nvim_win_get_buf(curr_win); local buf_name = vim.api.nvim_buf_get_name(curr_buf); print(buf_name); vim.cmd.cfile(buf_name) 

## nvim_win_set_buf
nvim_win_set_buf({window}, {buffer})
Sets the current buffer in a window, without side effects
Attributes:
not allowed when textlock is active Since: 0.3.2
Parameters:
{window} window-ID, or 0 for current window
{buffer} Buffer id

lua local buf_id = 4; local win_id = 1000; vim.api.nvim_win_set_buf(win_id, buf_id)

