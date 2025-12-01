import os
import re

pattern_mnemo = "{{(?P<mnemo>.+?)}}"
pattern_examples = "\+.+?###"
pattern_search_word_in_text = r"(?<!\w)(?P<word>%s)(?!\w)"
pattern_mnemo_galagoliy = r"\b(?P<word>%s)\s+"


compl_mnemo = re.compile(pattern_mnemo, flags=re.DOTALL | re.MULTILINE)
compl_examples = re.compile(pattern_examples, flags=re.DOTALL | re.MULTILINE)


path_script = os.getcwd()
path_anki = os.path.split(path_script)[0]
path_repo = os.path.split(path_anki)[0]
path_dir = os.path.join(path_anki, "WORDS_NOTEPAD")
path_dir_mp3 = os.path.normpath(
    os.path.join(
        path_repo, os.path.join("EnglishSimulate", "Project", "sound_longman_mono")
    )
)
dir_for_search_files = r"/home/stepan/git_repos/kn7072/ANKI/WORDS"


path_file_words = os.path.join(path_script, "ПОВТОРИТЬ.txt")
path_last_word = os.path.join(path_script, "last_word.txt")
path_file_not_learn = os.path.join(path_script, "ПРОПУСТИТЬ.txt")
path_synonyms_dir = os.path.join(path_anki, "Синонимы")
path_word_building_dir = os.path.join(path_anki, "СловоОбразование")
path_to_save_reports = "TEMP_REPORTS"
# path_to_learnt_sentence = "Предложения.txt"
path_to_learnt_sentence = "/home/stepan/GIT/kn7072/ANKI/Предложения.txt"

word_block = """
 <div class="wrap_delete">
        {word} {ipa} [sound:{word}.mp3]
        {stars_block} 
        </div>
"""


comment_block = """
<div class="phrase odd">
    <div>
       {title_block}
    </div>
    <div class="payload"> 
    {content_block}
    </div>
</div>
"""

container_block = '<div class="wrap_delete">{content}</div>'
div_block = "<div>{content}</div>"

star_comment_block = '<div class="star"></div>'
star_span_block = '<span class="star"></span>'
