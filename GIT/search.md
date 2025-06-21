[documentation](https://docs.github.com/en/search-github/getting-started-with-searching-on-github/understanding-the-search-syntax)

matches repositories with the word "cats" that were pushed to before July 5, 2012.
cats pushed:<2012-07-05

kn7072 pushed:>2025-06-20

matches repositories with the word "cats" that have more than 10 stars but are not written in JavaScript.
cats stars:>10 -language:javascript

## Searching for repositories

With the in qualifier you can restrict your search to the repository name, repository description, repository topics, contents of the README file, or any combination of these. When you omit this qualifier, only the repository name, description, and topics are searched.

Example
jquery in:name - matches repositories with "jquery" in the repository name.
jquery in:name,description - matches repositories with "jquery" in the repository name or description.
jquery in:topics - matches repositories labeled with "jquery" as a topic.
query in:readme - matches repositories mentioning "jquery" in the repository's README file.
repo:octocat/hello-world - matches a specific repository name.

octocat in:readme - matches repositories mentioning "octocat" in the repository's README file.

### Language qualifier

To narrow down to a specific languages, use the language: qualifier. For example:

language:ruby OR language:cpp OR language:csharp

For a complete list of supported language names, see languages.yaml in github-linguist/linguist. If your preferred language is not on the list, you can open a pull request to add it.

### Path qualifier

content:"avoid typ" AND path:/git_alias.md найдет code 'avoid typ' в файлах git_alias.md
"status" AND path:/^yazi\/theme\.toml$/

To match only a specific filename (and not part of the path), you could use a regular expression:

path:/(^|\/)README\.md$/

Note that the . in the filename is escaped, since . has special meaning for regular expressions. For more information about using regular expressions, see Using regular expressions.

You can also use some limited glob expressions in the path: qualifier.
For example, to search for files with the extension txt, you can use:

path:\*.txt

To search for JavaScript files within a `src` directory, you could use:
path:src/\*.js

    By default, glob expressions are not anchored to the start of the path, so the above expression would still match a path like app/src/main.js. But if you prefix the expression with /, it will anchor to the start. For example:

    path:/src/*.js

    Note that * doesn't match the / character, so for the above example, all results will be direct descendants of the src directory. To match within subdirectories, so that results include deeply nested files such as /src/app/testing/utils/example.js, you can use **. For example:

    path:/src/**/*.js

You can also use the ? global character. For example, to match the path file.aac or file.abc, you can use:
path:\*.a?c

To search for a filename which contains a special character like `*` or `?`, just use a quoted string:
path:"file?"

Glob expressions are disabled for quoted strings, so the above query will only match paths containing the literal string file?.

path:/^yazi\/theme\.toml$/ находит репозитории с файлам /yazi/theme.toml

### Symbol qualifier

You can search for symbol definitions in code, such as function or class definitions, using the symbol: qualifier. Symbol search is based on parsing your code using the open source Tree-sitter parser ecosystem, so no extra setup or build tool integration is required.

For example, to search for a symbol called WithContext:

language:go symbol:WithContext
repo:kn7072/kn7072 language:Go symbol:repeatFn

In some languages, you can search for symbols using a prefix (e.g. a prefix of their class name). For example, for a method deleteRows on a struct Maint, you could search symbol:Maint.deleteRows if you are using Go, or symbol:Maint::deleteRows in Rust.

You can also use regular expressions with the symbol qualifier. For example, the following query would find conversions people have implemented in Rust for the String type:

language:rust symbol:/^String::to\_.\*/

Note that this qualifier only searches for definitions and not references, and not all symbol types or languages are fully supported yet. Symbol extraction is supported for the following languages:

    Bash
    C
    C#
    C++
    CodeQL
    Elixir
    Go
    JSX
    Java
    JavaScript
    Lua
    PHP
    Protocol Buffers
    Python
    R
    Ruby
    Rust
    Scala
    Starlark
    Swift
    Typescript

We are working on adding support for more languages. If you would like to help contribute to this effort, you can add support for your language in the open source Tree-sitter parser ecosystem, upon which symbol search is based.

language:Lua content:/Command\("cb"\)/

### Content qualifier

By default, bare terms search both paths and file content. To restrict a search to strictly match the content of a file and not file paths, use the content: qualifier. For example:

content:README.md

This query would only match files containing the term README.md, rather than matching files named README.md
