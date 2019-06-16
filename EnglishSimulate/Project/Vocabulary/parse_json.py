# -*- coding: utf-8 -*-
import json
import os
import templates

path_to_json_file = "words.json"
dict_groups = {"all_words": "group_all_words"}
content_all = {}

with open(path_to_json_file, "r", encoding="utf-8") as f:
    data_json = json.loads(f.read())


def analisis_json(data_json):
    """Разделяет слова на группы"""
    struct_groups = {}
    for word_i, value_i in data_json.items():
        for group_i in value_i["grups"]:
            value_i["word"] = word_i
            is_exist = struct_groups.get(group_i)
            if not is_exist:
                struct_groups[group_i] = []
            struct_groups[group_i].append(value_i)
    return struct_groups


def get_html_groups(list_groups, word):
    """Возвращает верстку Прупп"""
    list_html = []
    for name_group_i in list_groups:
        if name_group_i == "all_words":
            temp = templates.element_group_all_words.format(group_name=name_group_i, word=word)
        else:
            temp = templates.element_group.format(group_name=name_group_i)
        list_html.append(temp)
    return "\n".join(list_html)


def get_additional_content(content_word):
    """

    :param content_word:
    :return:
    """
    mnemonic = content_word["mnemonic"]
    examples = content_word["examples"]
    antonyms = content_word["antonyms"]
    synonyms = content_word["synonyms"]
    comment = content_word["comment"]
    content_list = []

    if examples:
        temp_examples = templates.examples
        content_examples = temp_examples.format(text=" ".join(examples))
        content_list.append(content_examples)
    if synonyms:
        temp_synonyms = templates.synonyms
        content_synonyms = temp_synonyms.format(text=" ".join(synonyms))
        content_list.append(content_synonyms)
    if antonyms:
        temp_antonyms = templates.antonyms
        content_antonyms = temp_antonyms.format(text=" ".join(antonyms))
        content_list.append(content_antonyms)
    if mnemonic:
        temp_mnemonic = templates.mnemonic
        content_mnemonic = temp_mnemonic.format(text=" ".join(mnemonic))
        content_list.append(content_mnemonic)
    if comment:
        temp_comment = templates.comment
        content_comment = temp_comment.format(text=" ".join(comment))
        content_list.append(content_comment)
    html_content = "\n".join(content_list)
    return html_content


def create_html_doc(content_all):
    """Собирает верстку документа"""
    temp_content = []
    path_to_html = os.path.join("html", "created_doc.html")
    with open(path_to_html, mode="w", encoding="utf-8") as f:
        for group_name, content_obj in content_all.items():
            contant_word = "\n".join(content_obj["content"])
            temp_group = templates.__dict__[dict_groups.get(group_name, "group_words")]
            content_group = temp_group.format(contant_word=contant_word, group_name=group_name,
                                              count_words=content_obj["count_word_group"])
            temp_content.append(content_group)
        body_content_all = "\n".join(temp_content)
        html_content_all = templates.html_body.format(body=body_content_all)
        f.write(html_content_all)

res = analisis_json(data_json)

url_forvo = r"https://ru.forvo.com/word/{word}/#en"
for group_i, value_i in res.items():
    exist_content = content_all.get(group_i)
    if not exist_content:
        content_all[group_i] = {"count_word_group": 0,
                                "content": []}
    for content_word_i in value_i:
        contant_list_groups = get_html_groups(content_word_i["grups"], content_word_i["word"])
        additional_content = get_additional_content(content_word_i)
        html_word_i = templates.contant_word.format(word=content_word_i["word"],
                                                    translate=content_word_i["translate"],
                                                    transcription=content_word_i["transcription"],
                                                    additional_content=additional_content,
                                                    contant_list_groups=contant_list_groups,
                                                    url_forvo=url_forvo.format(word=content_word_i["word"]))
        content_all[group_i]["content"].append(html_word_i)
    content_all[group_i]["count_word_group"] = len(value_i)

create_html_doc(content_all)
print()


