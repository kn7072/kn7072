# This is a sample commands.py.  You can add your own commands here.
#
# Please refer to commands_full.py for all the default commands and a complete
# documentation.  Do NOT add them all here, or you may end up with defunct
# commands when upgrading ranger.

# A simple command for demonstration purposes follows.
# -----------------------------------------------------------------------------

from __future__ import (absolute_import, division, print_function)

# You can import any python module as needed.
import os

# You always need to import ranger.api.commands here to get the Command class:
from ranger.api.commands import Command


# Any class that is a subclass of "Command" will be integrated into ranger as a
# command.  Try typing ":my_edit<ENTER>" in ranger!
class my_edit(Command):
    # The so-called doc-string of the class will be visible in the built-in
    # help that is accessible by typing "?c" inside ranger.
    """:my_edit <filename>

    A sample command for demonstration purposes that opens a file in an editor.
    """

    # The execute method is called when you run this command in ranger.
    def execute(self):
        # self.arg(1) is the first (space-separated) argument to the function.
        # This way you can write ":my_edit somefilename<ENTER>".
        if self.arg(1):
            # self.rest(1) contains self.arg(1) and everything that follows
            target_filename = self.rest(1)
        else:
            # self.fm is a ranger.core.filemanager.FileManager object and gives
            # you access to internals of ranger.
            # self.fm.thisfile is a ranger.container.file.File object and is a
            # reference to the currently selected file.
            target_filename = self.fm.thisfile.path

        # This is a generic function to print text in ranger.
        self.fm.notify("Let's edit the file " + target_filename + "!")

        # Using bad=True in fm.notify allows you to print error messages:
        if not os.path.exists(target_filename):
            self.fm.notify("The given file does not exist!", bad=True)
            return

        # This executes a function from ranger.core.acitons, a module with a
        # variety of subroutines that can help you construct commands.
        # Check out the source, or run "pydoc ranger.core.actions" for a list.
        self.fm.edit_file(target_filename)

    # The tab method is called when you press tab, and should return a list of
    # suggestions that the user will tab through.
    # tabnum is 1 for <TAB> and -1 for <S-TAB> by default
    def tab(self, tabnum):
        # This is a generic tab-completion function that iterates through the
        # content of the current directory.
        return self._tab_directory_content()

class fzf_select(Command):
    """
    :fzf_select

    Find a file using fzf.

    With a prefix argument select only directories.

    See: https://github.com/junegunn/fzf
    """
    def execute(self):
        import subprocess
        import os.path
        if self.quantifier:
            # match only directories
            command="find -L . \( -path '*/\.*' -o -fstype 'dev' -o -fstype 'proc' \) -prune \
            -o -type d -print 2> /dev/null | sed 1d | cut -b3- | fzf +m"
        else:
            # match files and directories
            command="find -L . \( -path '*/\.*' -o -fstype 'dev' -o -fstype 'proc' \) -prune \
            -o -print 2> /dev/null | sed 1d | cut -b3- | fzf +m"
        fzf = self.fm.execute_command(command, universal_newlines=True, stdout=subprocess.PIPE)
        stdout, stderr = fzf.communicate()
        if fzf.returncode == 0:
            fzf_file = os.path.abspath(stdout.rstrip('\n'))
            if os.path.isdir(fzf_file):
                self.fm.cd(fzf_file)
            else:
                self.fm.select_file(fzf_file)


class sound_word(Command):
    """
    http://www.mplayerhq.hu/DOCS/HTML/ru/
    https://github.com/ranger/ranger/blob/9c585e48e14525f11d2405ea0bb9b5eba92e63e9/ranger/config/commands.py

    """
    def execute(self):
        import subprocess
        import os.path
        if self.quantifier:
            # match only directories
            command="mplayer -delay -1 -loop 2  /home/stepan/git/kn7072/EnglishSimulate/Project/audio/able.mp3"
        else:
            # match files and directories
            command="mplayer -delay -1 -loop 2  /home/stepan/git/kn7072/EnglishSimulate/Project/audio/able.mp3"

        # self.fm.notify(self.fm.thisdir)
        # self.fm.run(['mplayer', '-delay', '-1', '-loop', '2', '/home/stepan/git/kn7072/EnglishSimulate/Project/audio/able.mp3'])    
        
        
        fzf = self.fm.execute_command(command, universal_newlines=True, stdout=subprocess.PIPE)
        stdout, stderr = fzf.communicate()

        # command = "dddddd"
        # self.fm.notify(command)
        
        
        
        # self.fm.notify('Wrong number of arguments', bad=True)
        # return         
        # fzf = self.fm.execute_console(command)
        # stdout, stderr = fzf.communicate()
        # if fzf.returncode == 0:
        #     pass
        # else:
        #     print("Проблема")
        # return "111"


class sound(Command):
    """:rename_append [-FLAGS...]

    Opens the console with ":rename <current file>" with the cursor positioned
    before the file extension.

    Flags:
     -a    Position before all extensions
     -r    Remove everything before extensions
    """
    def __init__(self, *args, **kwargs):
        super(sound, self).__init__(*args, **kwargs)

        flags, _ = self.parse_flags()
        self._flag_ext_all = 'x' in flags
        # self._flag_remove = 'r' in flags

    def execute(self):
        from ranger import MACRO_DELIMITER, MACRO_DELIMITER_ESC

        tfile = self.fm.thisfile
        relpath = tfile.relative_path.replace(MACRO_DELIMITER, MACRO_DELIMITER_ESC)
        basename = tfile.basename.replace(MACRO_DELIMITER, MACRO_DELIMITER_ESC)

        # if basename.find('.') <= 0 or os.path.isdir(relpath):
        #     self.fm.open_console('sound ' + relpath)
        
        name_file = relpath.replace(".txt", ".mp3")
        # self.fm.open_console('sound ' + name_file)

        import subprocess
        if self.quantifier:
            # match only directories
            command=r"mplayer -delay -1 -loop 2  /home/stepan/git/kn7072/EnglishSimulate/Project/sound_longman_mono/%s" % name_file
        else:
            # match files and directories
            command=r"mplayer -delay -1 -loop 2  /home/stepan/git/kn7072/EnglishSimulate/Project/sound_longman_mono/%s" % name_file

        # self.fm.notify(self.fm.thisdir)
        # self.fm.run(['mplayer', '-delay', '-1', '-loop', '2', '/home/stepan/git/kn7072/EnglishSimulate/Project/audio/able.mp3'])    
        
        
        fzf = self.fm.execute_command(command, universal_newlines=True, stdout=subprocess.PIPE)  # , flags='w'
        stdout, stderr = fzf.communicate()
        return

        # if self._flag_ext_all:
        #     pos_ext = re.search(r'[^.]+', basename).end(0)
        # else:
        #     pos_ext = basename.rindex('.')
        # pos = len(relpath) - len(basename) + pos_ext

        # if self._flag_remove:
        #     relpath = relpath[:-len(basename)] + basename[pos_ext:]
        #     pos -= pos_ext

        # self.fm.open_console('rename ' + relpath, position=(7 + pos))