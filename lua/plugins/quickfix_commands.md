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


https://neoland.vercel.app/plugin/8508
https://github.com/kevinhwang91/nvim-bqf?ysclid=m64rwxgkc5817520732


