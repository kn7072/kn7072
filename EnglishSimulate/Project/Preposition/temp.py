import json

path_first = "first_prepositon.json"
path_second = "second_preposition.json"


def read_file(path_file):

    with open(path_file, mode="r", encoding="utf-8") as f:
        obj_json = json.loads(f.read())
        return obj_json

def create_file_for_print(name_file, obj):
    with open(name_file, mode="w", encoding="utf-8") as f:
        f.write("\n".join(["%s;%s" % (i["rus"], i["eng"]) for i in obj]))


dict_first = read_file(path_first)
dict_second = read_file(path_second)

create_file_for_print("beginer.txt", dict_first)
create_file_for_print("advance.txt", dict_second)

print()
