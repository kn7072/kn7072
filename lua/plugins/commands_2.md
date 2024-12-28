:h expand()
When {string} starts with '%', '#' or '<', the expansion is
		done like for the |cmdline-special| variables with their
		associated modifiers.  Here is a short overview:

			%		current file name
			#		alternate file name
			#n		alternate file name n
			<cfile>		file name under the cursor
			<afile>		autocmd file name
			<abuf>		autocmd buffer number (as a String!)
			<amatch>	autocmd matched name
			<cexpr>		C expression under the cursor
			<sfile>		sourced script file or function name
			<slnum>		sourced script line number or function
					line number
			<sflnum>	script file line number, also when in
					a function
			<SID>		"<SNR>123_"  where "123" is the
					current script ID  |<SID>|
			<script>	sourced script file, or script file
					where the current function was defined
			<stack>		call stack
			<cword>		word under the cursor
			<cWORD>		WORD under the cursor
			<client>	the {clientid} of the last received
					message
		Modifiers:
			:p		expand to full path
			:h		head (last path component removed)
			:t		tail (last path component only)
			:r		root (one extension removed)
			:e		extension only

		Example: >vim
			let &tags = expand("%:p:h") .. "/tags"
<		Note that when expanding a string that starts with '%', '#' or
		'<', any following text is ignored.  This does NOT work: >vim
			let doesntwork = expand("%:h.bak")
<		Use this: >vim
			let doeswork = expand("%:h") .. ".bak"
<		Also note that expanding "<cfile>" and others only returns the
		referenced file name without further expansion.  If "<cfile>"
		is "~/.cshrc", you need to do another expand() to have the
		"~/" expanded into the path of the home directory: >vim
			echo expand(expand("<cfile>"))

lua print(vim.fn.expand("%"))
lua print(vim.fn.expand("<cword>")) получить слово на котором установлен курсор
lua print(vim.fn.expand("<abuf>"))
lua print(vim.fn.expand("<afile>"))

fold
lua print(vim.inspect(vim.api.nvim_win_get_cursor(0)[1]))
lua print(vim.fn.foldclosed(36)) -- проверяет находится ли указанная строка в закрытом фолде, 
если находится в закрытом фолде тогда возвращает номер строки начала фолда, если строка в открытом фолде тогда -1 

https://neovim.io/doc/user/sign.html
lua print(vim.inspect(vim.fn.sign_getdefined())) 


