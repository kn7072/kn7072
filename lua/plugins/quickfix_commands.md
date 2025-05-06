:setlocal makeprg=flake8\ %
:make


:h 'errorformat'
:setglobal errorformat?

https://neo.vimhelp.org/quickfix.txt.html#errorformat - ДОКУМЕНТАЦИЯ
Научить Vim распознавать вывод, генерируемый командой
:make, можно с помощью параметра настройки errorformat (см.
:h 'errorformat'
 http://vimdoc.sourceforge.net/htmldoc/options.
html#'errorformat'). Значение по умолчанию этого параметра можно получить следующей командой:
➾ :setglobal errorformat?
errorformat=%*[^"]"%f"%*\D%l: %m,"%f"%*\D%l: %m, ...[abridged]...




## error-file-format
Basic items
	%f		file name (finds a string)
	%b		buffer number (finds a number)
	%o		module name (finds a string)
	%l		line number (finds a number)
	%e		end line number (finds a number)
	%c		column number (finds a number representing character
			column of the error, byte index, a <tab> is 1
			character column)
	%v		virtual column number (finds a number representing
			screen column of the error (1 <tab> == 8 screen
			columns))
	%k		end column number (finds a number representing
			the character column of the error, byte index, or a
			number representing screen end column of the error if
			it's used with %v)
	%t		error type (finds a single character):
			    e - error message
			    w - warning message
			    i - info message
			    n - note message
	%n		error number (finds a number)
	%m		error message (finds a string)
	%r		matches the "rest" of a single-line file message %O/P/Q
	%p		pointer line (finds a sequence of '-', '.', ' ' or
			tabs and uses the length for the column number)
	%*{conv}	any scanf non-assignable conversion
	%%		the single '%' character
	%s		search text (finds a string)
The "%f" conversion may depend on the current 'isfname' setting.  "~/" is
expanded to the home directory and environment variables are expanded.
The "%f" and "%m" conversions have to detect the end of the string.  This
normally happens by matching following characters and items.  When nothing is
following the rest of the line is matched.  If "%f" is followed by a '%' or a
backslash, it will look for a sequence of 'isfname' characters.
On Windows a leading "C:" will be included in "%f", even when using "%f:".
This means that a file name which is a single alphabetical letter will not be
detected.
The "%b" conversion is used to parse a buffer number.  This is useful for
referring to lines in a scratch buffer or a buffer with no name.  If a buffer
with the matching number doesn't exist, then that line is used as a non-error
line.
The "%p" conversion is normally followed by a "^".  It's used for compilers
that output a line like:

^


or

---------^


to indicate the column of the error.  This is to be used in a multi-line error
message.  See errorformat-javac for a  useful example.
The "%s" conversion specifies the text to search for, to locate the error line.
The text is used as a literal string.  The anchors "^" and "$" are added to
the text to locate the error line exactly matching the search text and the
text is prefixed with the "\V" atom to make it "very nomagic".  The "%s"
conversion can be used to locate lines without a line number in the error
output.  Like the output of the "grep" shell command.
When the pattern is present the line number will not be used.
The "%o" conversion specifies the module name in quickfix entry.  If present
it will be used in quickfix error window instead of the filename.  The module
name is used only for displaying purposes, the file name is used when jumping
to the file.
Changing directory
The following uppercase conversion characters specify the type of special
format strings.  At most one of them may be given as a prefix at the beginning
of a single comma-separated format pattern.
Some compilers produce messages that consist of directory names that have to
be prepended to each file name read by %f (example: GNU make).  The following
codes can be used to scan these directory names; they will be stored in an
internal directory stack.					E379  

	%D		"enter directory" format string; expects a following
			  %f that finds the directory name
	%X		"leave directory" format string; expects following %f
When defining an "enter directory" or "leave directory" format, the "%D" or
"%X" has to be given at the start of that substring.  Vim tracks the directory
changes and prepends the current directory to each erroneous file found with a
relative path.  See quickfix-directory-stack for details, tips and
limitations.
Multi-line messages				errorformat-multi-line  
It is possible to read the output of programs that produce multi-line
messages, i.e. error strings that consume more than one line.  Possible
prefixes are:
	%E		start of a multi-line error message
	%W		start of a multi-line warning message
	%I		start of a multi-line informational message
	%N		start of a multi-line note message
	%A		start of a multi-line message (unspecified type)
	%>		for next line start with current pattern again efm-%>
	%C		continuation of a multi-line message
	%Z		end of a multi-line message
These can be used with '+' and '-', see efm-ignore below.
Using "\n" in the pattern won't work to match multi-line messages.

## Pattern matching

The scanf()-like "%*[]" notation is supported for backward-compatibility
with previous versions of Vim.  However, it is also possible to specify
(nearly) any Vim supported regular expression in format strings.
Since meta characters of the regular expression language can be part of
ordinary matching strings or file names (and therefore internally have to
be escaped), meta symbols have to be written with leading '%':
	%\		The single '\' character.  Note that this has to be
			escaped ("%\\") in ":set errorformat=" definitions.
	%.		The single '.' character.
	%#		The single "*"(!) character.
	%^		The single '^' character.  Note that this is not
			useful, the pattern already matches start of line.
	%$		The single '$' character.  Note that this is not
			useful, the pattern already matches end of line.
	%[		The single '[' character for a [] character range.
	%~		The single '~' character.
When using character classes in expressions (see /\i for an overview),
terms containing the "\+" quantifier can be written in the scanf() "%*"
notation.  Example: "%\\d%\\+" ("\d\+", "any number") is equivalent to "%*\\d".
Important note: The \(...\) grouping of sub-matches can not be used in format
specifications because it is reserved for internal conversions.


https://neovim.io/doc/user/quickfix.html
:vimgrep Error *.c
:vimgrep /_get/ *.c

:copen

https://neovim.io/doc/user/quickfix.html#error-file-format
https://neovim.io/doc/user/options.html#'errorformat'

:set makeprg=make


https://deardevices.com/2018/04/15/vim-errorformat-challenge/
:cfile output
:set errorformat=%f\:%l\:%c

## examples

:set efm=%E%f\\,\ Error\ %n,%Cline\ %l,%Ccolumn\ %c,%Z%m

~/temp/experimental/quickfix/fizzbuzz.js, Error 275
line 42
column 3
' ' expected after '--'
~/temp/experimental/quickfix/fizzbuzz.js, Error 275
line 45
column 8
' ' expected after 'abd'


-----------------------------------------------------------------------------
:set efm=%C\ %.%#,%A\ \ File\ \"%f\"\\,\ line\ %l%.%#,%Z%[%^\ ]%\\@=%m
:set efm=%.%#File\ \"%f\"\\,\ line\ %l%m

==============================================================
FAIL: testGetTypeIdCachesResult (dbfacadeTest.DjsDBFacadeTest)
--------------------------------------------------------------
Traceback (most recent call last):
  File "unittests/dbfacadeTest.py", line 89, in testFoo
    self.assertEquals(34, dtid)
  File "/usr/lib/python3.8/unittest.py", line 286, in
 failUnlessEqual
    raise self.failureException, \
AssertionError: 34 != 33

--------------------------------------------------------------
Ran 27 tests in 0.063s

Note that the %C string is given before the %A here: since the expression
' %.%#' (which stands for the regular expression ' .*') matches every line
starting with a space, followed by any characters to the end of the line,
it also hides line 7 which would trigger a separate error message otherwise.
Error format strings are always parsed pattern by pattern until the first
match occurs.

-----------------------------------------------------------------------------
:setlocal efm=%A%f\,\ line\ %l\,\ character\ %c:%m,%Z%.%#,%-G%.%#


-----------------------------------------------------------------------------
:set efm=%+P[%f],(%l\\,%c)%*[\ ]%t%*[^:]:\ %m,%-Q

[a1.tt]
(1,17)  error: ';' missing
(21,2)  warning: variable 'z' not defined
(67,3)  error: end of file found before string ended

[a2.tt]

[a3.tt]
NEW compiler v1.1
(2,2)   warning: variable 'x' not defined
(67,3)  warning: 's' already defined

-----------------------------------------------------------------------------
set efm=%EError\ in\ line\ %l\ of\ %f:,%Z%m

Error in line 123 of foo.c:
unknown variable "i"
Error in line 125 of fo2.c:
unknown variable "iy"

-----------------------------------------------------------------------------
:set efm=%f:%l:%c%m

./src/except.c: In function ‘Except_raise’:
./src/except.c:11:6: warning: infinite recursion detected [-Winfinite-recursion]
   11 | void Except_raise(const T *e, const char *file, int line) {
      |      ^~~~~~~~~~~~
In file included from ./src/except.c:2:
./include/except.h:62:18: note: recursive call
   62 | #define RAISE(e) Except_raise(&(e), __FILE__, __LINE__)
      |                  ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
./include/assert.h:8:33: note: in expansion of macro ‘RAISE’
    8 | #define assert(e) ((void)((e)||(RAISE(Assert_Failed),0)))
      |                                 ^~~~~
./src/except.c:20:5: note: in expansion of macro ‘assert’
   20 |     assert(e);
      |     ^~~~~~


-----------------------------------------------------------------------------
set efm=%E%f\\,\ line\ %l\\,\ character\ %c:,%Z%m

~/quickfix/fizzbuzz.js, line 2, character 22:
 Unexpected '++'.
for (i=1; i <= 100; i++) {
~/quickfix/fizzbuzz.js, line 3, character 15:
 Expected '===' ...
if(i % 15 == 0) {
~/quickfix/fizzbuzz.js, line 5, character 21:
 Expected '===' ...
} else if(i % 5 == 0) {
~/quickfix/fizzbuzz.js, line 7, character 21:
 Expected '===' ...
} else if(i % 3 == 0) {
~/quickfix/fizzbuzz.js, line 12, character 2:
 Unexpected ';'.
};

-----------------------------------------------------------------------------
set efm=%E%m\ (%f:%l)
cfile valgring_log

==35057== 
==35057== 7 errors in context 6 of 11:
==35057== Conditional jump or move depends on uninitialised value(s)
==35057==    at 0x4A1E0CB: __printf_buffer (vfprintf-process-arg.c:58)
==35057==    by 0x4A43CC5: __vsnprintf_internal (vsnprintf.c:96)
==35057==    by 0x4A1A405: snprintf (snprintf.c:31)
==35057==    by 0x10982B: printWinProperty (list_properties.c:118)
==35057==    by 0x109C4B: main (list_properties.c:204)
-----------------------------------------------------------------------------
:echo printf("Have %d errors", len(getqflist()))
lua for i, qf_i in ipairs(vim.fn.getqflist()) do print(qf_i.text) end

:cexpr system('grep -n xyz *')
:cexpr getline(1, '$')

You can use ":.cc" to jump to the error under the cursor.
---------------------------
packadd cfilter подключаем пакет

Then you can use the following commands to filter a quickfix/location list:
:Cfilter[!] /{pat}/
:Lfilter[!] /{pat}/
The :Cfilter command creates a new quickfix list from the entries matching
{pat} in the current quickfix list. {pat} is a Vim regular-expression
pattern. Both the file name and the text of the entries are matched against
{pat}. If the optional ! is supplied, then the entries not matching {pat} are
used. The pattern can be optionally enclosed using one of the following
characters: ', ", /. If the pattern is empty, then the last used search
pattern is used.
The :Lfilter command does the same as :Cfilter but operates on the current
location list.

---------------------------

getqflist()
lua vim.print(vim.fn.getqflist())

lua print(vim.inspect(vim.fn.getloclist(1))) location list

https://dev.to/vonheikemen/everything-you-need-to-know-to-configure-neovim-using-lua-3h58?ysclid=m658m0brsx548484053
lua vim.opt.errorformat = '%f|%l col %c|%m'

Add an item to the end of the list
    Let's take errorformat as an example. If we want to add to this list using vimscript we do this.
    set errorformat+=%f\|%l\ col\ %c\|%m
    In lua we have a couple of ways to achieve the same goal:
    Using the + operator.
    vim.opt.errorformat = vim.opt.errorformat + '%f|%l col %c|%m'
    Or the :append method.
    vim.opt.errorformat:append('%f|%l col %c|%m')

Add to the beginning
    In vimscript:
    set errorformat^=%f\|%l\ col\ %c\|%m
    Lua:
    vim.opt.errorformat = vim.opt.errorformat ^ '%f|%l col %c|%m'
    -- or try the equivalent
    vim.opt.errorformat:prepend('%f|%l col %c|%m')

Delete an item
    Vimscript:
    set errorformat-=%f\|%l\ col\ %c\|%m
    Lua:
    vim.opt.errorformat = vim.opt.errorformat - '%f|%l col %c|%m'
    -- or the equivalent
    vim.opt.errorformat:remove('%f|%l col %c|%m')


lua vim.opt.errorformat = vim.opt.errorformat + "%E%f\\, line %l\\, character %c:,%Z%m"

https://github.com/neovim/neovim/issues/21313?ysclid=m66j88b6ct70365889
lua vim.cmd.cfile("gcc_output") загружает файл с ошибками
lua vim.cmd.copen() открывате окно с ошибками



    lua print(vim.inspect(vim.fn.getqflist({text = "end of file found before string ended"})))
    lua print(vim.inspect(vim.fn.getqflist({text = "\n' ' expected after '--'"})))
    lua print(vim.inspect(vim.fn.getqflist({lnum = 22})))


    lua print(vim.inspect(vim.fn.getloclist(vim.api.nvim_get_current_win(), {text = "In file included from ./src/except.c:2:"})))
    lua print(vim.inspect(vim.fn.getloclist(vim.api.nvim_get_current_win(), {lnum = 22})))


getqflist([{what}])                                                getqflist()

		Returns a List with all the current quickfix errors.  Each
		list item is a dictionary with these entries:
			bufnr	 number of buffer that has the file name, use bufname() to get the name
			module	 module name
			lnum	 line number in the buffer (first line is 1)
			end_lnum end of line number if the item is multiline
			col	column number (first column is 1)
			end_col	end of column number if the item has range
			vcol	TRUE: "col" is visual column
				FALSE: "col" is byte index
			nr	error number
			pattern	search pattern used to locate the error
			text	description of the error
			type	type of the error, 'E', '1', etc.
			valid	TRUE: recognized error message
			user_data
				custom data associated with the item, can be
				any type.
		When there is no error list or it's empty, an empty list is
		returned. Quickfix list entries with a non-existing buffer
		number are returned with "bufnr" set to zero (Note: some
		functions accept buffer number zero for the alternate buffer,
		you may need to explicitly check for zero).
		Useful application: Find pattern matches in multiple files and
		do something with them:

vimgrep /theword/jg *.c
for d in getqflist()
   echo bufname(d.bufnr) ':' d.lnum '=' d.text
endfor

		If the optional {what} dictionary argument is supplied, then
		returns only the items listed in {what} as a dictionary. The
		following string items are supported in {what}:
			changedtick	get the total number of changes made
					to the list quickfix-changedtick
			context	get the quickfix-context
			efm	errorformat to use when parsing "lines". If
				not present, then the 'errorformat' option
				value is used.
			id	get information for the quickfix list with
				quickfix-ID; zero means the id for the
				current list or the list specified by "nr"
			idx	get information for the quickfix entry at this
				index in the list specified by "id" or "nr".
				If set to zero, then uses the current entry.
				See quickfix-index
			items	quickfix list entries
			lines	parse a list of lines using 'efm' and return
				the resulting entries.  Only a List type is
				accepted.  The current quickfix list is not
				modified. See quickfix-parse.
			nr	get information for this quickfix list; zero
				means the current quickfix list and "$" means
				the last quickfix list
			qfbufnr number of the buffer displayed in the quickfix
				window. Returns 0 if the quickfix buffer is
				not present. See quickfix-buffer.
			size	number of entries in the quickfix list
			title	get the list title quickfix-title
			winid	get the quickfix window-ID
			all	all of the above quickfix properties
		Non-string items in {what} are ignored. To get the value of a
		particular item, set it to zero.
		If "nr" is not present then the current quickfix list is used.
		If both "nr" and a non-zero "id" are specified, then the list
		specified by "id" is used.
		To get the number of lists in the quickfix stack, set "nr" to
		"$" in {what}. The "nr" value in the returned dictionary
		contains the quickfix stack size.
		When "lines" is specified, all the other items except "efm"
		are ignored.  The returned dictionary contains the entry
		"items" with the list of entries.
		The returned dictionary contains the following entries:
			changedtick	total number of changes made to the
					list quickfix-changedtick
			context	quickfix list context. See quickfix-context
				If not present, set to "".
			id	quickfix list ID quickfix-ID. If not
				present, set to 0.
			idx	index of the quickfix entry in the list. If not
				present, set to 0.
			items	quickfix list entries. If not present, set to
				an empty list.
			nr	quickfix list number. If not present, set to 0
			qfbufnr	number of the buffer displayed in the quickfix
				window. If not present, set to 0.
			size	number of entries in the quickfix list. If not
				present, set to 0.
			title	quickfix list title text. If not present, set
				to "".
			winid	quickfix window-ID. If not present, set to 0
		Examples (See also getqflist-examples):

echo getqflist({'all': 1})
echo getqflist({'nr': 2, 'title': 1})
echo getqflist({'lines' : ["F1:10:L10"]})

Parameters:
{what} (table?)
Return: (any)

lua print(vim.inspect(vim.fn.getqflist({nr = "$"}))) колличество qfixов в стеке
:echo getqflist({'nr' : '$'}).nr колличество qfixов в стеке

lua vim.print(vim.fn.getqflist({size=1}))  число элементов в qfix
lua vim.print(vim.fn.getqflist({items=1})) перечислит все элементы
lua vim.print(vim.fn.getqflist({all=1})) все свойста  текущего qfix

посмотреть разные qfix
lua print(vim.inspect(vim.fn.getqflist({nr = 2, items=1})))
lua print(vim.inspect(vim.fn.getqflist({nr = 1, items=1})))

также можно посмотреть полную информацию для разных qfix по id (id обычно равен nr) 
lua vim.print(vim.fn.getqflist({id=1, all=1}))
lua vim.print(vim.fn.getqflist({id=3, all=1}))

3. Using more than one list of errors	

quickfix-error-lists
So far it has been assumed that there is only one list of errors.  Actually
there can be multiple used lists that are remembered; see 'chistory' and
'lhistory'.
When starting a new list, the previous ones are automatically kept.  Two
commands can be used to access older error lists.  They set one of the
existing error lists as the current one.
						:colder :col E380
:col[der] [count]	Go to older error list.  When [count] is given, do
			this [count] times.  When already at the oldest error
			list, an error message is given.
						:lolder :lol
:lol[der] [count]	Same as :colder, except use the location list for
			the current window instead of the quickfix list.
						:cnewer :cnew E381
:cnew[er] [count]	Go to newer error list.  When [count] is given, do
			this [count] times.  When already at the newest error
			list, an error message is given.
						:lnewer :lnew
:lnew[er] [count]	Same as :cnewer, except use the location list for
			the current window instead of the quickfix list.
						:chistory :chi
:[count]chi[story]	Show the list of error lists.  The current list is
			marked with ">".  The output looks like:

  error list 1 of 3; 43 errors   :make
> error list 2 of 3; 0 errors    :helpgrep tag
  error list 3 of 3; 15 errors   :grep ex_help *.c

			When [count] is given, then the count'th quickfix
			list is made the current list. Example:

" Make the 4th quickfix list current
:4chistory

						:lhistory :lhi
:[count]lhi[story]	Show the list of location lists, otherwise like
			:chistory.
When adding a new error list, it becomes the current list.
When ":colder" has been used and ":make" or ":grep" is used to add a new error
list, one newer list is overwritten.  This is especially useful if you are
browsing with ":grep" grep.  If you want to keep the more recent error
lists, use ":cnewer 99" first.
To get the number of lists in the quickfix and location list stack, you can
use the getqflist() and getloclist() functions respectively with the list
number set to the special value '$'. Examples:

echo getqflist({'nr' : '$'}).nr
echo getloclist(3, {'nr' : '$'}).nr


To get the number of the current list in the stack:

echo getqflist({'nr' : 0}).nr

-- создание первого qfix
local bufnr = api.nvim_get_current_buf()
local content = {
    {filename = "/home/stepan/git_repos/kn7072/lua/plugins/commands", lnum = 1, col = 5, text = "1"},
    {bufnr = bufnr, lnum = 2, col = 10, text = "2"},
    {bufnr = bufnr, lnum = 3, col = 13, text = "3"}
}
fn.setqflist(content, ' ')



https://neoland.vercel.app/plugin/8508
https://github.com/kevinhwang91/nvim-bqf?ysclid=m64rwxgkc5817520732
https://neovim.io/doc/user/quickfix.html#_1.-using-quickfix-commands


