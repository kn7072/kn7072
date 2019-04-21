# -*- coding: utf-8 -*-

html_body = """
<html>
    <head>
        <title>3000 words</title>
        <meta content="">
        <meta charset="utf-8">
        <script src="script.js"></script>
        <link rel="stylesheet" href="style.css"/>
        <link rel="shortcut icon" type="image/ico" href="favicon.ico"/>
    </head>
    <body>
            <div>
                {body}
            </div>
    </body>
</html>
"""

element_group = """
<a href='#{group_name}' class="buttom">{group_name}</a>
"""

element_group_all_words = """
<a href='#{word}' class="buttom">all_words</a>
"""

"""
<div class="green mrg-tom-5">aaaa bbbb cccc ddddd eeeee</div>
    <div class="red-dark mrg-tom-5">ffffff ooooooo nnnnnn xxxxxx</div>
    <div class="mrg-tom-5">Мнемоника</div>
    <div class="mrg-tom-5">Примеры</div>
"""

mnemonic = """
<div class="mrg-tom-5">{text}</div>
"""

examples = """
<div class="mrg-tom-5">{text}</div>
"""

synonyms = """
<div class="green mrg-tom-5">{text}</div>
"""

antonyms = """
<div class="red-dark mrg-tom-5">{text}</div>
"""

comment = """
<div class="green mrg-tom-5">{text}</div>
"""

contant_word = """
<div class="flex flex-column container width-32 justify-content-between">
    <div class="flex">
        <div><a name='{word}'>{word}</a></div>
        <div class="red font-weight-700 mrg-left-5">{transcription}</div>
    </div>
    <div class="blue">{translate}</div>
    {additional_content}
    <div class="flex">
        {contant_list_groups}
    </div>
</div>
"""

group_all_words = """
<div class="group"><a name='all_words'></a>
    <div class="header-group">all_words</div>
        <div class="flex flex-wrap justify-content-center">
            {contant_word}
        </div>
    </div>
"""

group_words = """
<div class="container group"><a name="{group_name}"></a>
    <div class="header-group">{group_name}</div>
        <div class="flex">
            {contant_word}
        </div>
    </div>
</div>
"""
