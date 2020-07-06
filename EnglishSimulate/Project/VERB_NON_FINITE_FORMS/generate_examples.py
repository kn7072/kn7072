# -*-coding:utf-8 -*-
import json

path_infinitive_eng = "infinitive_eng.txt"
paht_infinitive_rus = "infinitive_rus.txt"

path_gerund_eng = "gerund_eng.txt"
paht_gerund_rus = "gerund_rus.txt"

path_participle_eng = "participle_eng.txt"
paht_participle_rus = "participle_rus.txt"

def create_file(obj, name_file):
    obj_str = json.dumps(obj, ensure_ascii=False, indent=4)
    with open(name_file, mode="w", encoding="utf-8") as f:
        f.write(obj_str)


def generate_json(path_eng, path_rus):
    eng_list = [i.replace("\n", "").replace("\t", "") for i in open(path_eng, encoding="utf-8")]
    rus_list = [i.replace("\n", "").replace("\t", "") for i in open(path_rus, encoding="utf-8")]
    assert len(eng_list) == len(rus_list), "Число примеров должно быть одинаковым"
    return [{"rus": rus, "eng": eng} for rus, eng in zip(rus_list, eng_list)]

infinitive = generate_json(path_infinitive_eng, paht_infinitive_rus)
gerund = generate_json(path_gerund_eng, paht_gerund_rus)
participle = generate_json(path_participle_eng, paht_participle_rus)


create_file(infinitive, "infinitive.json")
create_file(gerund, "gerund.json")
create_file(participle, "participle.json")
