[источник](https://dev.to/iggredible/learning-vim-regex-26ep)
# Learning Vim Regex

[#vim](https://dev.to/t/vim) [#neovim](https://dev.to/t/neovim) [#regex](https://dev.to/t/regex) [#search](https://dev.to/t/search)

# [](https://dev.to/iggredible/learning-vim-regex-26ep#learning-vim-regex)Learning Vim Regex

Learning regular expressions is like learning latin. It is not pleasant but it is good for your soul. They are incredibly useful but also hard to read. People who master them are hailed as gods. Many desired to learn them but a few actually did.

To a programmer, regex (regular expression) is a tool. It can be learned (and mastered). Learning it is a lifetime investment. Here's why: First, regex is portable. Sure, there are different regex flavors, but the basic principle is the same across all flavors. Regex knowledge in one domain will transfer everywhere. Second, regex is powerful and knowing it can save you a lot of time. Programming is all about creating and updating text. Regex allows you to search and modify texts efficiently. Many powerful programs (like parsers) are built on top of regexes. Third, it is fun (once you get to a certain proficiency).

Regex knowledge boosts your Linux-fu. You'll unlock more powerful commands using programs like sed, awk, grep, find, vim, and more. In this article, we will focus on learning and understanding regexes in Vim.

This article is by no means a complete regex tutorial. In fact, I'll be honest right now, that this article probably contains less than a third of what Vim regex can do. But they are the ones that I find very useful. I call them the good parts.

Many of the regex information you will be learning here is also transferable. Although the syntax may vary slightly in different environments, the principle is the same. If you understand everything in this article, you should be well on your way to use regex in other environments.

## [](https://dev.to/iggredible/learning-vim-regex-26ep#using-regex-in-vim)Using Regex in Vim

Many of Vim's search features allow you to use regular expressions. Some of them are:

- The search commands (`/` and `?`)
- The global and substitute command-line (ex) commands (`:g` and `:s`)
- The grep commands (`:vimgrep` and `:grep`)

There are other places where you can use regex, but based on my experience, these three are the main places I would use regex in.

Finally, this is not a guide about how to use the global command, or grep, or whatever. This is more of a regex guide than a Vim guide. Think of it as a regex guide that uses Vim. It will show you how to use regex in Vim.

I am going to limit the command to only the search command. Almost everything you see here is done using the search command `/` (I may release more guides in the future with different commands).

## [](https://dev.to/iggredible/learning-vim-regex-26ep#to-magic-or-not)To Magic or Not

If you are acquainted with Vim regex, you might be aware of Vim's special "flavor" of Regex. You can read more in `:h /magic`.

Basically Vim allows you to pass an option where certain characters are treated as literal characters while others as special characters.

In this guide, I won't use any magic option - meaning no `\v`, `\m`, `\V`, or `\M` (you basically will see a lot of backslashes).

Enough with introductory stuff, let's start!

# [](https://dev.to/iggredible/learning-vim-regex-26ep#the-good-parts-of-vim-regex)The Good Parts of Vim Regex

## [](https://dev.to/iggredible/learning-vim-regex-26ep#basic-search-raw-endraw-)Basic Search `/`

The most basic search that you could do is to search for a literal word. If you want to search for the string `donut`, run `/donut`. Vim will look for a literal word donut. It won't match `d0nut`, `Donut`, or `DONUT` (unless you have `'smartsearch'` option on, but that's another topic).

In real life, things are not that simple. Maybe you need to look for variations of `foo` string including `food`, `fool`, and `foos`. Maybe you need to match a phone-number-looking pattern like `xxx-xxx-xxxx` where x could be _any_ integer. So you want this pattern to match `123-123-1234` and `333-444-5555`, but not `1234-123-123`.

Practically speaking, we often need to search for a _pattern_, not a literal word. This is where knowing a little bit of regex goes a long way. In fact, just by knowing a handful of regex concepts in this article, you should be able to handle 99% of your searching needs.

## [](https://dev.to/iggredible/learning-vim-regex-26ep#any-character-raw-endraw-)Any Character `.`

The most simple, versatile, and almost universal regex pattern is the dot symbol (`.`). It matches any single character.

For example, if you need to search for a 3-letter string that starts with an n and ends with a t, and you don't care what goes in the middle, you can use the pattern `n.t`.

`/n.t` will match the strings `not`, `nut`, `net`, `n0t`, and even `n t` (space between n and t).

You can also use it multiple times, so `/n..b` matches any 4 character string that starts with n, followed by any character, followed by any character, and ends with b. So it will match `noob`, `n00b`, `n3wt`. It will not match `nob` or `nooob`.

## [](https://dev.to/iggredible/learning-vim-regex-26ep#the-character-class)The Character Class

The dot syntax is useful, but sometimes you want to classify your search. Recall that `/n.t` matches any three-lettered word that starts with n, ends with t, and anything goes in the middle. What if we only want alphabetic characters, so it would match `not`, `nut`, and `net` but not `n0t`, `n t`, and `n?t`.

To match only between a set of characters, a character class can help you.

### [](https://dev.to/iggredible/learning-vim-regex-26ep#character-class-raw-endraw-)Character Class `[]`

A character class or a collection, is a sequence / set of characters that you can use to match any _single_ character in the collection.

In this case, to match lowercase and uppercase alphabetic characters (a-z and A-Z), we can use `/n[a-zA-Z]t`. This will match `net`, `nUt`, and `not`.

If you need to match only lowercase alphabets, you can instead use `/n[a-z]t`. It will now match `net`, `nut`, and `not`, but it won't match `nEt`, `nUt`, and `nOt`.

To match only vowels, use `/n[aeiou]t`.

To match only numbers, use `/n[0-9]t`.

To match only numbers 0 to 5, use `/n[0-5]t`.

To match only uppercase A-F _and_ numbers 0-9, use `/n[A-F0-9]t`.

You are not limited to alphabets and numbers, if you want it to match either a space, an exclamation mark, and a question mark, you can do something like `/n[ !?]t`.

### [](https://dev.to/iggredible/learning-vim-regex-26ep#negated-char-class-raw-endraw-)Negated Char Class `[^]`

There is a special behavior that you need to know with the character class `[]`. If you put a caret (`^`) as the first character in it, it will act as a negation character. `[^a]` means "not a". `[^0-9]` means any non-number character. `[^aeiou]` means any non-vowel character.

The command `/n[^ue]t` means any non-u or non-e character. It will not match `nut` and `net`, but it will match any `not`, `nUt`, and `n0t`.

## [](https://dev.to/iggredible/learning-vim-regex-26ep#special-characters)Special Characters

Vim comes with a predefined special character set.

If you want to match a number, instead of using `/[0-9]`, you can also do `/\d` (digit). If you want to match a non-number, instead of using `/[^0-9]`, you can use `/\D`.

If you want to match a lowercase alphabet character, instead of using `/[a-z]`, you can use `/\l`. If you want to match a non-lowercase, alphabet character, instead of `/[^a-z]`, you can use `/\L`. To match an uppercase, use `/\u`. For the non-uppercase, use `/\U`.

If you want to match a hex digit, instead of `/[0-9A-Fa-f]`, you can use `/\x`. To match a non-hex digit, use `/\X`. You should see a pattern of using the uppercase letter to indicate the negated version of that special character.

If you want to match a whitespace character (tab and space), use `/\s`. To match a non-whitespace character, use `/\S`.

To match a "word" character (lower and uppercase alphabets, numbers, and underscore), use `/\w`. To match a non-word character, use `/\W`.

If you know your predefined characters, you can save a few keystrokes (`/\d` is 3 strokes vs `/[0-9]` 6 strokes).

## [](https://dev.to/iggredible/learning-vim-regex-26ep#quantifiers)Quantifiers

Repeating patterns are common when searching. For example, maybe you need to look for repeating digits in a phone number pattern. Nobody wants to type `[0-9][0-9][0-9]-[0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]` to match 123-123-1234 and 111-222-3333.Instead typing the characters many times, you can use quantifiers to simplify the search.

### [](https://dev.to/iggredible/learning-vim-regex-26ep#minmax)Min/Max

The pattern `123-123-1234` consists of a set of 3 consecutive numbers, followed by a dash, then another set of 3 consecutive numbers, followed by another dash, then another set of 4 consecutive numbers.

You can use the `{n}` (where n is an integer) quantifiers to do the job. The `{n}` quantifier expects the preceding character to repeat n times. The `{}` syntax is a special character and needs to be escaped (without the escape, Vim will treat `{3}` as a literal {3}. The search command `/[0-9]\{3}-[0-9]\{3}-[0-9]\{4}` will match the phone number pattern. In the case of `/[0-9]\{3}`, it expects the digit to be repeated 3 times. It will match `123` or `777`, but not `12` or `7`.

The search command to find the phone number 123-123-1234 looks like: `/[0-9]\{3}-[0-9]\{3}-[0-9]\{4}`. That's a lot simpler than typing `/[0-9][0-9][0-9]-[0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]`.

There are variations in the min/max quantifier:  

```
{n}
{n,m}
{n,}
{,m}
{}
```

#### [](https://dev.to/iggredible/learning-vim-regex-26ep#exact-match-raw-n-endraw-)Exact Match `{n}`

You have already seen the first one, `{n}`. It means the preceding character is repeated _exactly_ n times.

`/a\{5}` will match `aaaaa`. `/[a-z]\{3}` will match `abc` and `zzz`.

#### [](https://dev.to/iggredible/learning-vim-regex-26ep#min-max-match-raw-nm-endraw-)Min Max Match `{n,m}`

Let's explore the second one, `{n,m}`. It expects the preceding character to be repeated a minimum of n times and a max of m times (n and m are integers).

When we search using `/[0-9]\{2,4}`, it searches for any numbers 0-9 repeated between two and four times. It will match 99, 789, and 1234, but not 9, 78, and 12345 (although it will match the first 4 digits)

The command `/fo\{2,5}` searches for a string that starts with an f, followed by the letter o repeated 2 to 5 times. It matches foo, foooo, and fooooo, but not fo and foooooo (if will match up to fooooo).

The command `/fo\{2,5}d` will match food and foooood, but not fooooood. It expects no more than 5 o's between f and d, whereas it finds 6 o's.

#### [](https://dev.to/iggredible/learning-vim-regex-26ep#min-match-raw-n-endraw-)Min Match `{n,}`

The next form, `{n,}`, expects a minimum of n, up to infinity.

The search `/fo\{3,}` looks for the letter f, followed by 3 or more o. It matches fooo, foooo, and foooooooooooooooooooo. It won't match fo or foo.

The search `/[0-9]\{2,}` looks for 2 or more digits. It matches 11, 123, 1234567, and 999999999999999999.

#### [](https://dev.to/iggredible/learning-vim-regex-26ep#max-match-raw-m-endraw-)Max Match `{,m}`

The next form, `{,m}`, expects a minimum of zero, up to m occurrence.

The search `/fo\{,5}` looks for the letter f, followed by no o, up to 5 o's. It matches f, fo, foo, and fooooo. It won't match foooooo (it will only the first 5 o's).

#### [](https://dev.to/iggredible/learning-vim-regex-26ep#zero-or-more-match-raw-endraw-)Zero or More Match `{}`

The final variation of the min/max quantifier is `{}` (or `{,}`, personally this syntax makes more sense to me). It means zero or more.

`/fo\{}` expects an f, followed by zero o and up to unlimited o's. It will match f, fo, fooooo, fooooooooooooooo.

### [](https://dev.to/iggredible/learning-vim-regex-26ep#zero-or-more-raw-endraw-)Zero or More `*`

The zero or more quantifier matches zero or more of the preceding character and is expressed with an asterisk `*`. It doesn't need to be escaped.

If you run `/fo*`, Vim looks for the letter f, followed by zero o, up to infinite o's. It will match f, fo, foo, fooooooooooooooo.

If you think about it, it is similar to `/fo\{,}`, but instead of typing all those brackets, you just type an asterisk.

### [](https://dev.to/iggredible/learning-vim-regex-26ep#one-or-more-raw-endraw-)One or More `+`

The one or more quantifier matches one or more of the preceding character and is expressed with a plus `+`. It needs to be escaped, otherwise Vim treats it as a literal plus sign.

If you run `/fo\+`, Vim looks for the letter f, followed by one or more o's. It will match fo, fooooo, and foooooooooooooo. It won't match an f.

It is also equivalent to `/fo\{1,}`.

### [](https://dev.to/iggredible/learning-vim-regex-26ep#zero-or-one-raw-endraw-)Zero or One `?`

The zero or one quantifier matches either zero or one of the preceding characters. It is expressed with a question mark `?`. It needs to be escaped, otherwise it would be treated as a literal `?`.

If you run `/fo\?`, it will match both f and fo, but not foo.

Its min/max equivalent is `/fo\{,1}`.

## [](https://dev.to/iggredible/learning-vim-regex-26ep#greedy-vs-lazy)Greedy Vs Lazy

There are two different quantifiers: greedy and lazy. _By the way, in regex, there's also a third quantifier type, possessive, but I won't cover that here._

### [](https://dev.to/iggredible/learning-vim-regex-26ep#greedy)Greedy

You actually have seen greedy quantifier in action. `*` is one example.

Suppose that you have the following sentence:  

```
I say, "I use Vim". You say, "I don't use Vim". Uh-oh.
```

In this case, when you do `/".*"` (a string that starts with a double-quote, then zero or more of any character, then a double quote), Vim finds one match: `"I use Vim". You say, "I don't use Vim"`. This is because by using a greedy quantifier, you will get the largest possible value.

But what if you want to match for the smallest pattern? You need to use a lazy quantifier.

### [](https://dev.to/iggredible/learning-vim-regex-26ep#lazy)Lazy

If you look at lazy quantifiers, they look a lot like the min/max quantifiers, except that they have a `-`:  

```
{-}
{-n,m}
{-n,}
{-,m}
{-n}
```

Let's go over the first one. Recall that `{}` has the same effect as `*`: zero or more of the preceding character, _the largest possible match_. `{-}` is the lazy version of `{}`. It matches zero or more of the preceding character, _the smallest possible match_.

Going back to our sentence earlier:  

```
I say, "I use Vim". You say, "I don't use Vim". Uh-oh.
```

Let's use the lazy search: `/".\{-}"`. You will see _two_ matches: "I use Vim" and "I don't use Vim". Cool!

Let's go over the second variation, `{-n,m}`. If `{n,m}` matches at least n and at most m of the preceding character, _the largest possible match_, then `{-n,m}` matches at least n and at most m of the preceding character, _the smallest possible match_.

Suppose that you have the following:  

```
fo
foo
fooooo
foooooooooo
```

If you do `/fo\{-2,5}`:

- On the first string it will find no match, because it doesn't meet the string requirement of at least two o's.
- On the second string, it will match foo, the minimum requirement. - On the third match, instead of matching fooooo, it only matches foo, the least available match (two o's).
- On the fourth string, it also only matches foo, the smallest number of possible match.

I will leave the remaining lazy quantifiers, `{-n,}`, `{-,m}`, and `{-n}`, to you. They behave similar to the greedy quantifiers, but instead of finding the largest number of matches, they find the smallest number of matches.

## [](https://dev.to/iggredible/learning-vim-regex-26ep#anchors)Anchors

Sometimes you need to find a match not based on its content, but based on _where_ it is. To search by location, we use anchors.

### [](https://dev.to/iggredible/learning-vim-regex-26ep#beginning-of-line-raw-endraw-)Beginning of line `^`

The caret matches the start of the line.

If you have:  

```
donut is life
life is donut
a donut a day
```

If you do `/^donut`, it will match "donut is life" because the word donut is at the start of the line. "life is donut" and "a donut a day" do not have a donut at the start of the line, so they won't match.

### [](https://dev.to/iggredible/learning-vim-regex-26ep#end-of-line-raw-endraw-)End of Line `$`

The opposite of the start-of-the-line anchor is the end-of-the-line anchor, `$`. If you do `/donut$`, it will match the donut in "life is donut" because the word donut is at the end of the line.

### [](https://dev.to/iggredible/learning-vim-regex-26ep#word-boundaries-raw-lt-gt-endraw-)Word Boundaries `< >`

Another useful anchor is the word boundary anchors.

Given the following sentence:  

```
Without further ado, I do like donut very much
```

If you do (pun not intended :P) `/do`, Vim will match the do in: `ado`, `do`, and `donut`. What if you only want to match for the do in the word `do`, not in `ado` and `donut`?

Word boundaries can help. The syntax is `< >`. `<` means the start of a word and `>` means the end of a word. You need to escape them, otherwise Vim will match for literal `<` and `>`. `/\<do\>` will match only the standalone `do`, and not the do in `ado` and `donut`.

If you want to match the do in donut and the word do, then you are looking for the start-of-the-word do, so you can use `/\<do`.

Likewise, to match the do in ado and the word do, it is the same as looking for the end-of-the-word do, hence you can use `/do\>`.

## [](https://dev.to/iggredible/learning-vim-regex-26ep#or-raw-endraw-)Or `|`

Sometimes you need to look for either A or B or C. In Vim, you can search for alternatives with the OR (bar) syntax `|`. You need to escape the bar syntax, otherwise Vim will match a literal bar symbol.

If you need to search for either pancake or waffle (part of a tasty breakfast :D), you can do `/pancake\|waffle`.

If you need to search for a line that starts with either foo or bar, you can do `/^foo\|^bar`.

## [](https://dev.to/iggredible/learning-vim-regex-26ep#groups)Groups

Earlier you learned about quantifiers. They can help you search for repeating characters. However, more often than not, you need to look for repeated groups, not individual characters. You can do that with capture groups.

### [](https://dev.to/iggredible/learning-vim-regex-26ep#capture-group-subexpression-raw-endraw-)Capture Group (Sub-Expression) `( )`

The capture group is represented by a set of parentheses `()`. In Vim, they need to be escaped `\(\)` or they will match literal parentheses.

If I need to look for one or more donuts, like donutdonutdonut, I can use `/\(donut\)\+`. Recall that way earlier I said that quantifiers like `+` search for one or more the _preceding character_. I lied. Technically, it searches for the preceding character _or_ group. In Vim, they are called atoms.

So `/fo\+` looks for an f, followed by one or more o's, and matches fo, foo, and fooooo. While `/\(fo\)\+` looks for one or more fo's and will match fo and fofofofo.

Capture groups can be used with quantifiers. `/\(foo\)*` looks for zero or more foos, `/\(foo\)\{3,4}` looks for 3 or 4 foo's (greedy), `/\(foo\)\{-3}` looks for at least 3 foos (lazy).

Let's combine what we've learned together. What kind of string do you think `/\(super\|duper\)\{1,2} yummy\( in my tummy\)\?` matches? Think about it before you scroll down!


Ok, it will match these:  

```
super yummy
superduper yummy
supersuper yummy
dupersuper yummy in my tummy
duper yummy in my tummy
```

Do you understand why? If you don't, look back at the previous sections and make sure that you understand how they work!

### [](https://dev.to/iggredible/learning-vim-regex-26ep#backreferences-raw-n-endraw-)Backreferences `\n`

The capture group sure is very useful. It allows us to construct a pattern group that can be treated as a unit. It works great with quantifiers. But that's not all! Capture groups also work with backreferences.

Back...what?

A backreference lets you match the same text previously matched by a capturing group. You can spot a backreference when you see a backslash followed by a number: `\1`, `\2`, `\3`, ... `\9`.

For example, when you use `/\(foo\).*\1` against:  

```
foobarfoo
foo bar foo
```

They would match the entire string. How?

- The first capture group `\(foo\)` captures the string foo.
- Then we have zero or more of any character, `.*`. This matches any string between the first foo and the last foo.
- Finally, `\1` is a _backreference_ to the first capture group `\(foo\)`.

`/\(foo\).*\1` is effectively the same as doing `/foo.*foo`, but using `\1` gives you far more flexibility as you'll see in a little bit.

You can use multiple backreferences, like `/\(foo\)\(bar\).*\2\1\1`. Here, the first capture group is foo and is referenced with `\1`. The second capture group is bar and is referenced with `\2`. The search above is effectively similar to `/foobar.*barfoofoo`.

Suppose that you want to match an opening and closing of an XML tag:  

```
<foo>Hello</foo>
<bar>Greetings</bar>
<baz>Hello and greetings</baz>
```

Since XML opening tags need to match closing tags, we do not want it to match mismatched tags like:  

```
<foo>Nope</bar>
```

You can use: `/<\([^>]*\)>.*<\/\1>`.

Whoa, that got messy and hard-to-read quickly. Let's break it down!

Without escape characters, we actually have `<([^>]*)>.*</\1>`. A little simpler, but still a lot of symbols. Let's further break it apart into smaller sub-components.

The pattern above is composed of three components: `<([^>]*)>`, `.*`, and `</\1>`. Let's investigate each starting from the first one.

In `<([^>]*)>`, the outermost `<` and `>` are literal angle brackets to match `<` and `>` in `<foo>` and `<bar>`. The pair of parentheses are the first capture group. So what's that weird `[^>]*` syntax inside? Recall that `[]` is a character class and when you have a caret as the first character inside a `[]`, it means negation. So `[^>]` means a non-`>` character. Finally you are looking for zero or more of this non-`>` character. `[^>]*` will match `foo`, `bar`, and `baz`. Overall, this pattern effectively matches `<foo>`, `<bar>`, `<baz>`, etc. The capture group captures the contents _inside_ the `< >`. It captures and temporarily stores the texts `foo`, `bar`, and `baz`.

The second pattern, `.*`, is a familiar one: zero or more of any character. This matches any text between the HTML tags.

The third pattern is `</\1>`. The opening and closing angle brackets `<` and `>` match literal opening and closing HTML tags. `/` matches a literal forward slash. Finally, `\1` is a backreference to the first capture group, which as you recall was the content of the HTML tags: `foo`, `bar`, and `baz`. Putting the capture group and backreference together, this means that your opening XML tag needs to match the closing XML tag. If the starting XML tag was `<foo>`, then the closing HTML tag needs to be `</foo>`.

### [](https://dev.to/iggredible/learning-vim-regex-26ep#whole-match-raw-0-endraw-)Whole Match `\0`

There is one more special backreference in Vim: `\0`. It represents the whole regex match. So if your search pattern is `/foo`, then `\0` is foo. If your search pattern is `/foo[0-9]` and the string is foo9, then `\0` is foo9.

This can come in handy in substitution.

Suppose that you have:  

```
const one = 1;
const two = 2;
const ten = 10;
```

If you want to enclose the numbers 1, 2, and 10 in double quotes, the fastest way to do it using the substitute command is `:%s/[0-9]\+/"\0"`

I won't go over how the substitute command works because it is not the scope of this article, but I want to highlight the patterns:

- `[0-9]\+`, matches one or more digits (therefore it matches 1, 2, and 10).
- The new substitute pattern, `"\0"` efficiently encloses all the matches with double-quotes. In the first line, `\0` is `1`. `"\0"` is the same as `"1"`. In the third line, `\0` is 10. `"\0"` then is the same as `"10"`.

By the way, `\0` can also be aliased with `&`. `:s/\d/"\0"/g` is the same as `:s/\d/"&"/g`. It is one less character to type, if you prefer `&` over `\0`.

### [](https://dev.to/iggredible/learning-vim-regex-26ep#noncapture-group-raw-endraw-)Non-Capture Group `%( )`

All capture groups come with the backreference feature. If you don't want the backreference capability, use `%()` pattern to use a non-capture group instead of the regular capture group `()`. So `/\%(foo\)\+` still looks for one or more foo, but you won't be able to backreference it with `\1`.

So why would anyone want to not backreference it?

Performance. Backreferencing comes at performance cost. If you don't store backreference, you get some performance boosts. However, in my experience, I never really noticed any difference. But it wouldn't hurt to know about it.

## [](https://dev.to/iggredible/learning-vim-regex-26ep#atoms)Atoms

Earlier I mentioned about atoms. What on earth are atoms?

In Vim regex, an atom is a unit match. Technically almost everything in this article can be considered as atoms. The `a` in `/a` is an atom. The `^` in `/^hello` is an atom. The `[0-9]` in `/[0-9]` (any single-digit integer) is an atom. The `what` in `/\(what\)\+` (group match) is an atom. An atom can be an individual character match, an anchor, or a group match.

## [](https://dev.to/iggredible/learning-vim-regex-26ep#zerowidth)Zero-Width

"Zero-width" is a regex term. It is also mentioned in Vim help a few times and earned its place as an entry (`:h /zero-width`).

So what is zero width? A zero-width pattern is a pattern that doesn't actually match any character. If I search for the letter a (`/a`), it has a width of one. If I search for the letter a followed by any number (`/a[0-9]`), it has a width of two. The regex engine looks for a literal letter a. Anchors are good examples of zero-width patterns. If I search for the letter a at the start of the line (`/^a`), although the pattern `a` looks for a literal match of the letter a, the caret `^` does not match any character. This makes the caret anchor a zero-width pattern. It is there to specify location, not to match a character.

`^`, `$`, `\<` and `\>` are examples of zero-width patterns. There are other zero-width patterns that I haven't mentioned yet: look-arounds.

## [](https://dev.to/iggredible/learning-vim-regex-26ep#lookarounds)Look-Arounds

So what are look-arounds and why do we need them?

Look-arounds are useful when you have to search for a pattern relative to another pattern. If you need to search for foo _only_ when it is before bar, a look-around can help you.

There are two types of look-arounds: look-aheads and look-behinds.

### [](https://dev.to/iggredible/learning-vim-regex-26ep#lookaheads)Look-Aheads

Vim's lookahead syntax is `\ze`. Think of the e as "ending".

To match a foo that is followed by a bar (foobar), you can search `/foo\zebar`. The way I think about it is, `/foo` searches and matches for foo. Then you tell Vim to end the match with `\ze`. But the pattern doesn't stop there. The search continues. There's a bar after that. But you don't want bar to be part of the match. You're really searching for foobar (`/foobar`). So up to `\ze`, it will be searched and matched. After `\ze`, it will still be searched, but won't be matched. Note that in this section, I am making a subtle distinction between a "match" and a "search". A search is a pattern that the regex engine looks out for. A match is what is being selected / highlighted. All searches are matches but not all matches are searches.

`/foo\zebar` matches `foobar`, but not `foobaz` or `foo`.

The look-ahead pattern has another form: `\@=`. If you are familiar with the Perl regex, this is similar to the `(?=pattern)`.

When used in Vim, it matches the preceding atom. The syntax works differently from `\ze`, but the idea is the same.

To search for foo in foobar (but not in foobaz or foo), run `/foo\(bar\)\@=`. Note that you are using a capture group on bar, `\(bar\)`.

If the syntax is confusing, don't worry, you're not alone. It took me a while to grasp it when I started to learn about it.

The best way to understand it is, whatever character or capture group that precedes `\@=` won't be matched or highlighted, but it will still be used as a part of the search pattern. Think of it as a veil that covers it. `\(bar\)\@=`. It takes a stretch of imagination, but I see `\@=` as a magician, `@=` is the head (looks like a duck magician) and `\` is his left hand. `\(bar\)` is a veil containing the word "bar". He is covering it so it won't be highlighted. So `/foo\(bar\)\@=` to me is like a giant text that spells "foobar", whereas a duck-magician person comes and covers up the "bar" part so it won't be visible to the audience... sort-of kind-of... Well, anyway, let's go to the next look-around, look-behinds!

### [](https://dev.to/iggredible/learning-vim-regex-26ep#lookbehinds)Look-Behinds

Look-behinds are principally similar to look-aheads, except they work backwards.

In Vim, you can use `\zs`. Think of the s as "start". If you want to match bar but only if it is followed by foo (foobar), do `/foo\zsbar`. Again, the search pattern is technically `/foobar`. However, the matching only start after `\zs`, hence only bar is highlighted while foo is not.

Both `\ze` and `\zs` are Vim inventions. But they both have regex look-ahead and look-behind syntax counterparts. Just like `\ze` has a `\@=` regex counterpart, `\zs` also has a regex counterpart and it is `\@<=` (it's like `\@=`, except now it also has an arrow pointing back). The way it works, is that the atom that precedes it won't be matched (highlighted), although it will still be used as a part of the search pattern.

To search for bar in foobar, use `/\(foo\)\@<=bar`. To search for baz in foobaz, use `/\(foo\)\@<=baz`.

If the whole look-behind syntax pattern is confusing, I find the duck-magician imagery helps. `\(foo\)\@<=` is our pattern. `@<=` looks like a duck magician that shoots a beam. `\` is his left hand. `\(foo\)` is the veil that covers up the word foo. Again, whatever word/pattern that the magician veils will be hidden (not highlighted). So I imagine `\(foo\)\@<=bar` like a giant "foobar" text and this duck-magician guy veils up the word foo so it won't be visible to the audience.

## [](https://dev.to/iggredible/learning-vim-regex-26ep#lookahead-and-lookbehind)Look-Ahead and Look-Behind

You can definitely use both look-aheads and look-behinds in a pattern.

If you need to match and highlight the bar only if it comes after foo and before baz (foobarbaz), not in bazbarfoo, foobar, or barbaz, use `/foo\zsbar\zebaz`. Alternatively, you can also use `/\(foo\)\@<=bar\(baz\)\@=`.

### [](https://dev.to/iggredible/learning-vim-regex-26ep#negative-lookaheads)Negative Look-Aheads

Negative look-aheads are the negative version of the look-aheads. The syntax is `\@!` (as opposed to `\@=`).

Negative look-aheads search for a match NOT followed by the given pattern. To match foo _not_ followed by baz, run `/foo\(baz\)\@!`. This will match foo and foobar, not foobaz.

### [](https://dev.to/iggredible/learning-vim-regex-26ep#negative-lookbehinds)Negative Look-Behinds

There are also negative look-behinds. The syntax is `\@<!` (as opposed to `\@<=`). It finds a match NOT preceded by the pattern.

To match bar not preceded by foo, run `/\(foo\)\@<!bar`. This will match bazbar and bar, not foobar.

## [](https://dev.to/iggredible/learning-vim-regex-26ep#more-vim-regex)More Vim regex

The following are patterns exclusive in Vim. They are not available in most regex engines outside of Vim.

### [](https://dev.to/iggredible/learning-vim-regex-26ep#optional-match-raw-endraw-)Optional Match `\%[ ]`

You can search for optional, sequential matches with the `\%[]` pattern. It will match if the string contains, sequentially, any of the characters inside the square brackets.

`/do%[nut]` will match either `do`, `don`, `donu`, and `donut`.

### [](https://dev.to/iggredible/learning-vim-regex-26ep#multiple-lines-raw-x-endraw-)Multiple Lines `\_x`

Sometimes you need to search for patterns that may or may not be separated by newlines and/or whitespaces.

If you need to match the chocolate donut string, one separated by a whitespace and another separated by a newline:  

```
chocolate donut

chocolate
donut
```

You can search with `/chocolate\_sdonut`.

Recall that `\s` is a special character for a whitespace character. By adding an underscore, `\_s` now also includes a newline.

So if you want to match:  

```
chocolate donut

chocolatedonut

chocolate
donut

chocolate



donut
```

You can use zero-or-more quantifier (`*`), `/chocolate\_s*donut`.

### [](https://dev.to/iggredible/learning-vim-regex-26ep#start-and-end-of-file-raw-endraw-)Start and End of File `\%^ \%$`

Sometimes you need to search for a pattern at the start of the file. You can use the `\%^` pattern. If you need to search for foo that is at the start of the file, use `/\%^foo`.

To search for a pattern at the end of the file, use `\%$`. If you need to search for foo at the end of the file, use `/foo\%$`.

### [](https://dev.to/iggredible/learning-vim-regex-26ep#start-within-visual-area-raw-v-endraw-)Start Within Visual Area `\%V`

Vim has a Visual mode (`v`, `V`, or `Ctrl-V`) that allows you to highlight a certain area of text. I assume that you know what the visual mode is, if not, check out `:h visual-mode`.

When you are currently highlighting a visual area, you can search for a pattern _within_ that visual area with `\%V`.

If you have the text:  

```
barfoobazfoobarfoobazfoobarfoobazfoo

foobarfoobazfoobarfoobazfoobarfoobaz
```

While you are currently Visually highlighting the first line, you can search for foo within the visual highlight if you do `/\%Vfoo`.

### [](https://dev.to/iggredible/learning-vim-regex-26ep#magic-and-very-magic-raw-v-m-endraw-)Magic and Very Magic `\v \m`

Earlier I mentioned about `\v`, `\V`, `\m`, and `\M`. Some regex syntaxes require them to be escaped for them to be treated as special characters.

For example, to match one or more foo, normally you would do `/\(foo\)\+`. Note that the group match `()` and the one-or-more quantifier `+` are escaped.

If you don't want to escape them, you can use `\v`. The `v` stands for "very magic". Your search would look like this: `/\v(foo)+`. Vim treats `()` and `+` as a special character instead of treating them as literal parentheses and plus signs.

So how do you know which characters no longer need to be escaped and which characters still need to be escaped? The rule of thumb is, all characters except for word characters (digits 0-9, lowercase alphabets a-z, uppercase alphabets A-Z, and underscore _) are treated as special characters. As you've seen earlier, `()` and `+` are not word characters, so under very magic, they are treated as special characters. Also, special characters like `\d` (digits) and `\l` (lowercase alphabets) still need to be escaped.

Likewise, in very magic mode, since it automatically treats non-word characters as special characters, previously literal characters would need to be escaped if you want to match them literally. So if you need to match a literal parentheses while under very magic mode, like `(foo)`, then you'd have to escape it: `/\v\(foo\)`.

"Very magic" has a sibling, "magic". You actually have been acquainted with this magic mode. How so? Because Vim by default uses magic mode! If you run `:set magic?`, it will return `magic`. Everything that you've used so far is done under magic mode.

Vim also has two more modes: "no magic" (`\M`) and "no very magic" (`\V`). I won't cover them here because I personally think their usage is limited in everyday editing (I could be mistaken). But if you're curious, check out `:h /\V` and `:h /\M`.

## [](https://dev.to/iggredible/learning-vim-regex-26ep#conclusion)Conclusion

I think this is a good place to stop.

I hope that you gained valuable insight from this guide. Regex is a lot of fun once you know how to use it. It is an invaluable skill for any programmer. You don't need to master it, you just need to be good enough. Most popular programming languages employ regex to a certain extent. By learning regex in the Vim domain, you will inevitably know how to use it anywhere else. You will also be able to find and edit things much faster. Finally, it simply looks so darn cool.

Take the time reading this. No rush. Make it into your muscle memory. Understanding beats superficial knowledge. Test your knowledge. Have fun with it!

Happy coding!

В POSIX имеются свои классы символов, которые вы можете использовать в регулярных выражениях:
Класс символов 	Описание
[:alnum:] 	Алфавитно-цифровые символы. В ASCII эквивалентно: [A-Za-z0-9]
[:word:] 	То же самое, что и [:alnum:], с дополнительным символом подчёркивания (_).
[:alpha:] 	Алфавитные символы. В ASCII эквивалентно: [A-Za-z]
[:blank:] 	Включает символы пробела и табуляции.
[:cntrl:] 	Управляющие коды ASCII. Включает ASCII символы с 0 до 31 и 127.
[:digit:] 	Цифры от нуля до девяти.
[:graph:] 	Видимые символы. В ASCII сюда включены символы с 33 по 126.
[:lower:] 	Буквы в нижнем регистре.
[:punct:] 	Символы пунктуации. В ASCII эквивалентно: [-!»#$%&'()*+,./:;<=>?@[\\\]_`{|}~]
[:print:] 	Печатные символы. Все символы в [:graph:] плюс символ пробела.
[:space:] 	Символы белых пробелов, включающих пробел, табуляцию, возврат каретки, новую строку, вертикальную табуляцию и разрыв страницы. В ASCII эквивалентно: [ \t\r\n\v\f]
[:upper:] 	Символы в верхнем регистре.
[:xdigit:] 	Символы, используемые для выражения шестнадцатеричных чисел. В ASCII эквивалетно: [0-9A-Fa-f]
