[источник](https://archive.kernel.org/oldwiki/git.wiki.kernel.org/index.php/Aliases.html#Advanced_aliases_with_arguments)

# Aliases

With aliases, you can avoid typing the same commands over and over again. Aliases were added in Git version 1.4.0.

_Table of contents:_

|   |
|---|
|## Contents<br><br>- [1 Aliases](https://archive.kernel.org/oldwiki/git.wiki.kernel.org/index.php/Aliases.html#Aliases)<br>- [2 Introduction](https://archive.kernel.org/oldwiki/git.wiki.kernel.org/index.php/Aliases.html#Introduction)<br>- [3 Simple](https://archive.kernel.org/oldwiki/git.wiki.kernel.org/index.php/Aliases.html#Simple)<br>    - [3.1 A shortcut for seeing the fetched commits](https://archive.kernel.org/oldwiki/git.wiki.kernel.org/index.php/Aliases.html#A_shortcut_for_seeing_the_fetched_commits)<br>    - [3.2 Undo the last commit](https://archive.kernel.org/oldwiki/git.wiki.kernel.org/index.php/Aliases.html#Undo_the_last_commit)<br>- [4 Aliases with arguments](https://archive.kernel.org/oldwiki/git.wiki.kernel.org/index.php/Aliases.html#Aliases_with_arguments)<br>    - [4.1 'ci'](https://archive.kernel.org/oldwiki/git.wiki.kernel.org/index.php/Aliases.html#.27ci.27)<br>    - [4.2 Shortcut for displaying dates in your local timezone](https://archive.kernel.org/oldwiki/git.wiki.kernel.org/index.php/Aliases.html#Shortcut_for_displaying_dates_in_your_local_timezone)<br>    - [4.3 Simple diff wrappers](https://archive.kernel.org/oldwiki/git.wiki.kernel.org/index.php/Aliases.html#Simple_diff_wrappers)<br>    - [4.4 Use of quotes inside an alias](https://archive.kernel.org/oldwiki/git.wiki.kernel.org/index.php/Aliases.html#Use_of_quotes_inside_an_alias)<br>- [5 Advanced](https://archive.kernel.org/oldwiki/git.wiki.kernel.org/index.php/Aliases.html#Advanced)<br>    - [5.1 Calling "gitk"](https://archive.kernel.org/oldwiki/git.wiki.kernel.org/index.php/Aliases.html#Calling_.22gitk.22)<br>    - [5.2 What's new?](https://archive.kernel.org/oldwiki/git.wiki.kernel.org/index.php/Aliases.html#What.27s_new.3F)<br>    - [5.3 Poor man's "stash"](https://archive.kernel.org/oldwiki/git.wiki.kernel.org/index.php/Aliases.html#Poor_man.27s_.22stash.22)<br>    - [5.4 Serve repo on the spot](https://archive.kernel.org/oldwiki/git.wiki.kernel.org/index.php/Aliases.html#Serve_repo_on_the_spot)<br>    - [5.5 Prune all your stale remote branches](https://archive.kernel.org/oldwiki/git.wiki.kernel.org/index.php/Aliases.html#Prune_all_your_stale_remote_branches)<br>- [6 Advanced aliases with arguments](https://archive.kernel.org/oldwiki/git.wiki.kernel.org/index.php/Aliases.html#Advanced_aliases_with_arguments)<br>    - [6.1 Spelunking of the project's history](https://archive.kernel.org/oldwiki/git.wiki.kernel.org/index.php/Aliases.html#Spelunking_of_the_project.27s_history)<br>    - [6.2 A 'debug' alias to help debugging builtins](https://archive.kernel.org/oldwiki/git.wiki.kernel.org/index.php/Aliases.html#A_.27debug.27_alias_to_help_debugging_builtins)<br>    - [6.3 Calling "interdiff" between commits](https://archive.kernel.org/oldwiki/git.wiki.kernel.org/index.php/Aliases.html#Calling_.22interdiff.22_between_commits)<br>- [7 Collection of aliases by Git users](https://archive.kernel.org/oldwiki/git.wiki.kernel.org/index.php/Aliases.html#Collection_of_aliases_by_Git_users)<br>    - [7.1 Getting the diff of only one function](https://archive.kernel.org/oldwiki/git.wiki.kernel.org/index.php/Aliases.html#Getting_the_diff_of_only_one_function)<br>    - [7.2 simple diff ignoring line number changes](https://archive.kernel.org/oldwiki/git.wiki.kernel.org/index.php/Aliases.html#simple_diff_ignoring_line_number_changes)<br>    - [7.3 Editing/adding conflicted files](https://archive.kernel.org/oldwiki/git.wiki.kernel.org/index.php/Aliases.html#Editing.2Fadding_conflicted_files)<br>    - [7.4 Use graphviz for display](https://archive.kernel.org/oldwiki/git.wiki.kernel.org/index.php/Aliases.html#Use_graphviz_for_display)<br>    - [7.5 Cherrypick Style Recording](https://archive.kernel.org/oldwiki/git.wiki.kernel.org/index.php/Aliases.html#Cherrypick_Style_Recording)<br>    - [7.6 Shortcuts](https://archive.kernel.org/oldwiki/git.wiki.kernel.org/index.php/Aliases.html#Shortcuts)<br>    - [7.7 git k](https://archive.kernel.org/oldwiki/git.wiki.kernel.org/index.php/Aliases.html#git_k)<br>    - [7.8 alias](https://archive.kernel.org/oldwiki/git.wiki.kernel.org/index.php/Aliases.html#alias)<br>    - [7.9 Sending multiple messages from a single file](https://archive.kernel.org/oldwiki/git.wiki.kernel.org/index.php/Aliases.html#Sending_multiple_messages_from_a_single_file)<br>    - [7.10 SVN-like aliases](https://archive.kernel.org/oldwiki/git.wiki.kernel.org/index.php/Aliases.html#SVN-like_aliases)<br>    - [7.11 Getting pretty logs](https://archive.kernel.org/oldwiki/git.wiki.kernel.org/index.php/Aliases.html#Getting_pretty_logs)<br>    - [7.12 Finding the right commit](https://archive.kernel.org/oldwiki/git.wiki.kernel.org/index.php/Aliases.html#Finding_the_right_commit)<br>    - [7.13 Listing the tips of branches in pu that are not in next](https://archive.kernel.org/oldwiki/git.wiki.kernel.org/index.php/Aliases.html#Listing_the_tips_of_branches_in_pu_that_are_not_in_next)<br>    - [7.14 Obtaining the Empty Tree SHA1](https://archive.kernel.org/oldwiki/git.wiki.kernel.org/index.php/Aliases.html#Obtaining_the_Empty_Tree_SHA1)<br>    - [7.15 Getting the diff of a branch since it forked from another branch, or since the last merge](https://archive.kernel.org/oldwiki/git.wiki.kernel.org/index.php/Aliases.html#Getting_the_diff_of_a_branch_since_it_forked_from_another_branch.2C_or_since_the_last_merge)<br>        - [7.15.1 Usage](https://archive.kernel.org/oldwiki/git.wiki.kernel.org/index.php/Aliases.html#Usage)<br>        - [7.15.2 Example](https://archive.kernel.org/oldwiki/git.wiki.kernel.org/index.php/Aliases.html#Example)<br>    - [7.16 Untrack a file](https://archive.kernel.org/oldwiki/git.wiki.kernel.org/index.php/Aliases.html#Untrack_a_file)<br>    - [7.17 Checkout recursive submodules](https://archive.kernel.org/oldwiki/git.wiki.kernel.org/index.php/Aliases.html#Checkout_recursive_submodules)|

  

---

# Introduction

To show how to use aliases, suppose you wish you could write _git ci_ instead of _git commit_. You can achieve this by adding the following section to _~/.gitconfig_:

[alias]
        ci = commit

Some people are uncomfortable editing the config file themselves. They can edit the config by calling _git config alias.ci commit_ instead.

If you want to have the alias available everywhere on your local machine, you can either

- edit _~/.gitconfig_, or

- use the _--global_ flag:

git config --global alias.ci commit

# Simple

## A shortcut for seeing the fetched commits

If you want to be able to say _git lc_ to list all new commits after you fetched, with stats, but excluding merges, add this alias:

[alias]
        lc = log ORIG_HEAD.. --stat --no-merges

## Undo the last commit

[alias]
        undo=reset --soft HEAD^

# Aliases with arguments

Right from the start, aliases were meant as an easy way to avoid really simple, really short scripts. Therefore, they can take arguments, which are appended to the command.

## 'ci'

That's right. The simplest alias on this page takes arguments, so you can call:

$ git ci -m message file1 file2 dir1

## Shortcut for displaying dates in your local timezone

Here's how to create an alias _git llog_ that will behave just like _git log_, but will display dates in your local timezone.

[alias]
        llog = log --date=local

## Simple diff wrappers

These two aliases wrap commonly used options to _git diff_, and accept the full range of arguments that diff accepts:

[alias]
        changes=diff --name-status -r
        diffstat=diff --stat -r

## Use of quotes inside an alias

In more complex aliases, the quoting rules can also appear complex. One issue isn't with Git's alias mechanism, but a quirk of how "sh -c" works, taking the first non-option argument as $0, not $1.

Some of the key points are discussed in the thread [https://lore.kernel.org/git/CAHMHMxVajKxjBweG=mps0gLwE1o8M69DvPb1iUQYgLXx0VO5AA@mail.gmail.com/](https://lore.kernel.org/git/CAHMHMxVajKxjBweG=mps0gLwE1o8M69DvPb1iUQYgLXx0VO5AA@mail.gmail.com/)

# Advanced

Since version 1.5.0, Git supports aliases executing non-git commands, by prefixing the value with "!":

## Calling "gitk"

Since _gitk_ does not follow the common form _git-<name>_, and is no builtin either, you have to use the prefix "!" to call _gitk_ from an alias:

[alias]
        gitkconflict = !gitk --left-right HEAD...MERGE_HEAD

## What's new?

To see what new commits have been created by the last command (typically after a "git pull") :

[alias]
        new = !sh -c 'git log $1@{1}..$1@{0} "$@"'

Use like

git pull
git new
git new origin/master

## Poor man's "stash"

A concatenation of git programs can also be achieved by the prefix "!":

[alias]
        stsh = !CURRENT=$(git symbolic-ref HEAD) && git symbolic-ref HEAD refs/heads/stash && git commit -a -m stashed && git checkout $CURRENT

## Serve repo on the spot

This fires up a git daemon for the repo you are currently in:

[alias]
        serve = !git daemon --reuseaddr --verbose  --base-path=. --export-all ./.git

It makes use of the fact that (currently, as of git 1.5.6.1) non-git alias are executed from the top-level dir of a repo. The simpler version

[alias]
        serve = daemon --reuseaddr --verbose  --base-path=. --export-all ./.git

works only when called from the top-level dir. In any case, you can connect simply by _git ls-remote [git://127.0.0.1/](git://127.0.0.1/)_ etc.

## Prune all your stale remote branches

There's no way to tell `git remote update` to prune stale branches, and `git remote prune` does not understand `--all`. So here is an alias to do the job:

[alias]
        prune-all = !git remote | xargs -n 1 git remote prune

# Advanced aliases with arguments

Starting with version 1.5.3, git supports appending the arguments to commands prefixed with "!", too. If you need to perform a reordering, or to use an argument twice, you can use this trick:

[alias]
        example = !sh -c 'ls $2 $1' -

The final dash is so that arguments start with $1, not with $0.

_NOTE: later on the page presents a nice trick using a shell function instead of_ sh -c_. Most aliases could be converted to use that style._

## Spelunking of the project's history

Here are two aliases suggested on the mailing list by Junio Hamano:

[alias]
        whois = "!sh -c 'git log -i -1 --pretty=\"format:%an <%ae>\n\" --author=\"$1\"' -"
        whatis = show -s --pretty='tformat:%h (%s, %ad)' --date=short

Try then by yourself! The first takes the name of a person or their email address. The second takes a commit name.

## A 'debug' alias to help debugging builtins

When debugging builtins, you often use gdb to analyze the runtime state. However, you have to disable the pager, and often you have to call the program with arguments. If the program to debug is a builtin, you can use this alias:

[alias]
        debug = !GIT_PAGER= gdb --args git

Suppose you want to debug _git log HEAD..next_, you can call _gdb_ by _git debug log HEAD..next_ now.

## Calling "interdiff" between commits

If upstream applied a slightly modified patch, and you want to see the modifications, you should use the program _interdiff_ of the _patchutils_ package. Then you can add the alias _intercommit_:

[alias]
        intercommit = !sh -c 'interdiff <(git show $1) <(git show $2) | less -FRS' -

This accept two commits, typically the first coming from upstream (e.g. _origin/master_) and the second coming from your own topic branch.

# Collection of aliases by Git users

Here is a collection of some Git users' aliases. If you know a simpler way to achieve the same, please add some notes.

## Getting the diff of only one function

When you want to see just the differences of one function in one file in two different commits, you can do this:

$ git config alias.funcdiff '!sh -c "git show \"\$0:\$2\" | sed -n \"/^[^ \t].*\$3[ \t]*(/,/^}/p\" > .tmp1 &&
        git show \"\$1:\$2\" | sed -n \"/^[^ \t].*\$3[ \t]*(/,/^}/p\" > .tmp2 &&
        git diff --no-index .tmp1 .tmp2"' -

The idea is to create two temporary files which contain only the function, and call _git diff_ on them. Use this alias this way: _git funcdiff <old-rev> <new-rev> <path> <function>_.

## simple diff ignoring line number changes

If anyone knows of a way to do this that gives prettier output, please do share :-)

If you've eg. moved around a bunch of lines in data files, and want a diff of what _else_ happened, you can use the following alias

[alias]
	sortdiff = !sh -c 'git diff "$@" | grep "^[+-]" | sort --key=1.2 | uniq -u -s1'

(sort --key=1.2 ignores the leading + or -, as does -s to uniq, while -u removes any consequtive lines; I would `grep -v '^\(+++ b\|--- a\)'` but that gave me "bad config file" for some reason)

You could probably include line numbers here too, by using the field features of sort/uniq

## Editing/adding conflicted files

You get a lot of merge conflicts and want to quickly solve them using an editor and then add the conflicted files. Try this:

[alias]
        edit-unmerged = "!f() { git diff --name-status --diff-filter=U | cut -f2 ; }; vim `f`"
        add-unmerged = "!f() { git diff --name-status --diff-filter=U | cut -f2 ; }; git add `f`"

You should replace "vim" by your favorite editor.

Then just use

$ git edit-unmerged
... edit ...
$ ... test ...
$ git add-unmerged
$ git commit  # or git rebase --continue or whatever

## Use graphviz for display

[alias]
        graphviz = "!f() { echo 'digraph git {' ; git log --pretty='format:  %h -> { %p }' \"$@\" | sed 's/[0-9a-f][0-9a-f]*/\"&\"/g' ; echo '}'; }; f"

This produces output that can be displayed using dotty, for example:

$ git graphviz HEAD~100..HEAD~60 | dotty /dev/stdin
$ git graphviz --first-parent master | dotty /dev/stdin

Note how defining a function eliminates the need to use sh -c.

## Cherrypick Style Recording

This approximates what happens with hg/darcs record (i.e. ask interactively which patch hunk to commit, and then do the commit) :

[alias]
  record = ! sh -c '(git add -p -- $@ && git commit) || git reset' --

It will not only do 'git add -p' (with an optional file list), but it will also immediately do the commit. Upon abandonment of either the add or the commit it will reset the index.

## Shortcuts

[alias]
    st = status
    ci = commit
    br = branch
    co = checkout
    df = diff
    dc = diff --cached
    lg = log -p
    who = shortlog -s --

## git k

If you use gitk in your git sessions quite frequently, you have perhaps misused your history and done:

$ gitk foo..bar
$ gitk checkout baz

Using `git k` instead of `gitk` may solve your problem:

[alias]
        k = !gitk

## alias

Now that you know all about aliases, it might be handy to define some, using an alias:

[alias]
        alias = "!sh -c '[ $# = 2 ] && git config --global alias.\"$1\" \"$2\" && exit 0 || echo \"usage: git alias <new alias> <original command>\" >&2 && exit 1' -"

then define new aliases with:

$ git alias new_alias original_command

Note that you must enclose the entire _original_command_ in single or double quotes, so that the shell interprets it as a single expression.

Going further, to get a list of your defined aliases:

[alias]
        aliases = !git config --get-regexp 'alias.*' | colrm 1 6 | sed 's/[ ]/ = /'

## Sending multiple messages from a single file

This can be useful to use send-email on the output of _git format-patch --stdout_

[alias]
        send-mbox = "!bash -c 'eval f=\\$$#; eval set -- `seq -f\"\\$%.0f\" 1 $(($#-1))`; mkdir .mboxsplit || exit; trap \"st=\\$?; rm -rf .mboxsplit; exit \\$?\" 0 INT TERM; if last=`git mailsplit -d4 -o.mboxsplit -b -- \"$f\"`; then echo Found $last messages in \"$f\"; git send-email \"$@\" .mboxsplit; fi' -"

Most of the complication is because the last argument must be passed to _git mailsplit_, while the others must be passed to _git send-email_.

## SVN-like aliases

Here are some aliases to help git-svn users migrate away from SVN. Be careful though - trying to completely recreate an SVN environment with aliases will cause problems when commands don't _quite_ do what you expect.

[alias]
        st = status

        # SVN-compatible versions of commands
        # "foo-svn" is used here instead of "svn-foo" so that it's suggested when people tab-complete "git fo..."
        cherry-pick-svn = !GIT_EDITOR='sed -i /^git-svn-id:/d' git cherry-pick -e
        branch-svn = svn branch
        merge-svn = merge --squash
        push-svn = svn dcommit

        # The next two lines are recommended, as their strengths outweigh their weaknesses.
        # Strength: they make transitioning from SVN easier
        # Weakness: they make teaching `git pull` harder when you move to git on the server
        # Weakness: they encourage people to think that rebasing is a safe default
        up = svn rebase
        update = svn rebase

        # The next line *is not* recommended, as its weaknesses outweigh its strengths.
        # Strength: it makes transitioning from SVN easier
        # Weakness: it makes teaching `git add`, `git commit -a`, the index, etc. harder
        # Weakness: it encourages people to think that a git commit is analogous to an SVN commit
        #ci = commit

## Getting pretty logs

There is my _git lg_ alias:

[alias]
    lg = log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit --date=relative

Full details are in my "[pimping out git log](http://www.jukie.net/bart/blog/pimping-out-git-log)" blog entry.

## Finding the right commit

If you use shortened hashes, sometimes you may encounter a collision. The following alias prints out all commits whose hash start with given string.

[alias]
        abbr = "!sh -c 'git rev-list --all | grep ^$1 | while read commit; do git --no-pager log -n1 --pretty=format:\"%H %ci %an %s%n\" $commit; done' -"

## Listing the tips of branches in pu that are not in next

Suppose you have two aliases defined like so:

[alias]
        oneline ="!_() { $(test $# -eq 0 && echo xargs -L1) git log --no-walk --decorate --oneline \"$@\"; }; _"
        tips = "!_() { t=$(git rev-list --no-merges --max-count=1 \"$@\"); if test -n \"$t\"; then echo $t; _ \"$@\" ^$t; fi; }; _"

Then:

git tips origin/pu ^origin/next | git oneline

might show something like this:

9dcca58 filter-branch.sh: de-dent usage string
704c335 On Cygwin support both UNIX and DOS style path-names
1c460f9 t3030: fix accidental success in symlink rename
9e81372 test-path-utils: Add subcommand "prefix_path"
ad733bd revert: Propagate errors upwards from do_pick_commit
76cf946 fixup! xdiff/xhistogram: rework handling of recursed results
df6a9c7 fixup! describe: Refresh the index when run with --dirty
c9f57a0 squash! ls-files: fix pathspec display on error
a1288bc add--interactive: add option to autosplit hunks
365b78a t5800: point out that deleting branches does not work
c997182 limit "contains" traversals based on commit generation
914b6fb doc/fast-import: document feature import-marks-if-exists
b792c06 branch -v: honor core.abbrev
b166408 mergetool: Don't assume paths are unmerged
b29d76f merge: mark the final "Merge made by..." message for l10n
942cf39 receive-pack: Allow server to refuse pushes with too many objects

which is a list of the tips of linear sequences of commits that are in pu, but not in next.

## Obtaining the Empty Tree SHA1

While the empty tree sha1 4b825dc642cb6eb9a060e54bf8d69288fbee4904 is known to git, you may need to generate it.

[alias]
        empty-tree-sha1 = hash-object -t tree /dev/null

Diffing against the empty tree can be useful for things like generating a patch which represents the creation of an entire slice of your working tree (squashing the effect of all commits so far into a single patch):

$ git diff -p $(git empty-tree-sha1) some-interesting-subdir/

You can even get a complete listing of any whitespace violations in the current working tree:

$ git diff --check $(git empty-tree-sha1)

## Getting the diff of a branch since it forked from another branch, or since the last merge

Update: This alias is unnecessary.

git diff A...B 

does the same thing.

To see the changes in a branch since it was forked from another branch, or since the last merge with the origin branch, you can add this 'forkdiff' alias to $HOME/.gitconfig:

[alias]
    forkdiff = !bash -c 'git diff $(git merge-base "$1" "$2") "$2" "${@: 3}" ' -

It uses git-merge-base to determine the fork-point (the commit that is common to both the branches) and does a git-diff between that commit and the second branch.

### Usage

git forkdiff <forked from branch> <forked branch> [git-diff-options]

### Example

  git forkdiff origin/master my_forked_branch --stat

## Untrack a file

In some scenarios it's necessary to untrack a particular file in say a production branch to avoid developer content spilling into it. As a rare activity it can be difficult to locate in the manuals. The _git rm_ man page 'Discussion' section gives additional details regarding the blobbing of filenames.

[alias]
        untrack = rm --cache --

## Checkout recursive submodules

Checking out a repo and it's submodules is not part of the regular 'git checkout' command. Normally you need a two command sequence

git checkout *oldcommit*
git submodule update --recursive

These can be combined using the tricks above, and using '&&' for command chaining to prevent losing work when you mistype the submodule name, into a simple alias

[alias]
        co-recurse = !sh -c 'git checkout $1 && git submodule update --recursive' -