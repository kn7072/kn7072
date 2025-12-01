Search and Replace in Multiple Buffers

There are multiple ways to search and replace a pattern in multiple buffers. We can use the commands listed below to search and replace a pattern in multiple buffers.

    :argdo — Execute the command for each file in the argument list
    :bufdo — Execute the command in each buffer in the buffer list
    :tabdo — Execute the command in each tab page
    :windo — Execute the command in each window
    :cdo — Execute the command in each valid entry in the quickfix list
    :cfdo — Execute the command in each file in the quickfix list

###############################################################
Vim search replace all files in current (project) folder

f you want to perform the search/replace in a project tree, you can use Vim's argument list.

Simply open Vim and then use the :args command to populate the argument list. You can pass in multiple filenames or even globs.

For example, :args **/\*.rb will recursively search the current directory for ruby files. Notice that this is also like opening Vim
with vim **/\*.rb. You can even use the shell's find command to get a list of all files in the current directory by running:

:args `find . -type f`

You can view the current args list by running :args by itself. If you want to add or delete files from the list,
you can use the :argadd or the :argdelete commands respectively.

Once you're happy with the list, now you can use Vim's powerful :argdo command which runs a command for every file in the argument list: :argdo %s/search/replace/g

Here are some tips for searching (based on some of the comments):

    Use a word boundary if you wanted to search for "foo" but not "foo_bar". Use the \< and \> constructs around the search pattern like so: :argdo %s/\<search\>/foobar/g
    Use a /c search flag if you want Vim to ask for confirmation before replacing a search term.
    Use a /e search flag if you want to skip the "pattern not found" errors.
    You can also choose to save the file after performing the search: :argdo %s/search/replace/g | update. Here, :update is used because it will only save the file if it has changed.

Open buffers
If you already have buffers open you want to do the search/replace on, you can use :bufdo, which runs a command for every file in your buffer list (:ls).
The command is very similar to :argdo: :bufdo %s/search/replace/g
Similar to :argdo and :bufdo, there is :windo and :tabdo that act on windows and tabs respectively. They are less often used but still useful to know.

###############################################################

1. Set working directory

Make sure Vim's current working directory is the root of the project:

     :cd {path to root directory}

You can use :pwd to print the current working directory and ensure that it is correct. 2. Find files that contain 'Sam'

Use Vim's :vimgrep command to search for all occurrences of Sam within the project:

    :vimgrep /Sam/gj **/*

Notes:

    Sam is the search "pattern" sandwiched between two forward slashes
    The **/* says to search in all files recursively
    The g flag says to search for all occurrences in each line (this is actually overkill here, but it does not hurt either)
    The j flag prevents vim from automatically jumping to the first match

This will populate the quickfix list with all instances of Sam. If you want to view the quickfix list, you can use the Vim command :copen

enter image description here 3. Substitute within all files that contain 'Sam'

Now we want to run Vim's :substitute command inside every file in the quickfix list. We can do this using the :cfdo {cmd} command which executes {cmd} in each file in the quickfix list. The specific {cmd} we want to use is :substitute or :s for short. Adding the update command at the end ensures that each file is saved before moving on to the next one (this is necessary if you don't :set hidden). The full line would look like:

    :cfdo %s/Sam/Bob/gc | update

If you do :set hidden, you can optionally leave off | update, and then do :cfdo update or :wall.
Notes:

    The % is a line range that specifies every line
    The g flag says to substitute all occurrences in each line
    The c flag causes vim to ask you to confirm each replacement individually (you might want to leave this out)

While :cdo is doing its work, several files may be opened in Vim buffers. To close each one, use the :cfdo command to execute :bd. Instead of iterating over each entry in the list, :cfdo iterates over each referenced file in the list.

:cfdo bd

update files and close buffers
cfdo %s/;/!!!/ge | update | bd
