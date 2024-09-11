# -*- conding: utf-8 -*-
import json

path_firs_eng = "first_eng.txt"
paht_firs_rus = "first_rus.txt"

path_second_eng = "second_eng.txt"
path_second_rus = "second_rus.txt"

path_questions_rus = "Questions/rus.txt"
path_questions_eng = "Questions/eng.txt"


def create_file(obj, name_file):
    obj_str = json.dumps(obj, ensure_ascii=False, indent=4)
    with open(name_file, mode="w", encoding="utf-8") as f:
        f.write(obj_str)


def generate_json(path_eng, path_rus):
    eng_list = [i.replace("\n", "").replace("\t", "") for i in open(path_eng, encoding="utf-8")]
    rus_list = [i.replace("\n", "").replace("\t", "") for i in open(path_rus, encoding="utf-8")]
    assert len(eng_list) == len(rus_list), "Число примеров должно быть одинаковым"
    return [{"rus": rus, "eng": eng} for rus, eng in zip(rus_list, eng_list)]


questions = generate_json(path_questions_eng, path_questions_rus)
# first_preposition = generate_json(path_firs_eng, paht_firs_rus)
# second_preposition = generate_json(path_second_eng, path_second_rus)

create_file(questions, "Questions/questions_with_prepositions.json")
# create_file(first_preposition, "first_prepositon.json")
# create_file(second_preposition, "second_preposition.json")

print()
