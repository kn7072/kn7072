# coding=utf-8
import json
import os

dir_for_search_files = "/home/stapan/GIT/kn7072/ANKI/WORDS"
list_word_no_comment = []
single_words = [
    "whirl",
    "fox",
    "immoral",
    "casual",
    "concrete",
    "coroner",
    "corridor",
    "cow",
    "click",
    "crude",
    "cocaine",
    "space",
    "silk",
    "ceiling",
    "watch",
    "envelope",
    "vocabulary",
    "expansion",
    "elite",
    "pump",
    "egg",
    "exotic",
    "ethical",
    "toast",
    "trim",
    "they",
    "entrance",
    "erase",
    "echo",
    "ethnic",
    "envisage",
    "enemy",
    "panel",
    "cake",
    "fuel",
    "fever",
    "adjective",
    "plural",
    "traffic",
    "elbow",
    "oxygen",
    "staff",
    "senior",
    "fibre",
    "soldier",
    "hurt",
]


def get_data_file(path_file):
    with open(path_file, encoding="utf-8") as f:
        return f.read()


def write_file(list_word):
    path_file = "not_comment.txt"
    with open(path_file, encoding="utf-8", mode="w") as f:
        for word_i in list_word:
            if word_i not in single_words:
                word_i = word_i.split(".")[0]
                f.write(f"{word_i}  ?{word_i}?_re\n")


def get_path_file(root_dir, file_name):
    return os.path.join(root_dir, file_name)


for root_dir, sub_dirs, files in os.walk(dir_for_search_files):

    if files:
        for file_i in files:
            try:
                path_word_i = get_path_file(root_dir, file_i)
                data_file_i = get_data_file(path_word_i)
                data_file_i_json = json.loads(data_file_i)
            except Exception as e:
                print(e)
                print

            for word, val in data_file_i_json.items():
                new_comment_list = val["comment"]
                if not new_comment_list:
                    list_word_no_comment.append(word)

print(f"Нет коментария {len(list_word_no_comment)}")
write_file(list_word_no_comment)
print
