import json
import os

dir_for_search_files = "/home/stepan/git_repos/kn7072/ANKI/WORDS"
path_script = os.getcwd()
path_anki = os.path.split(path_script)[0]
path_words_json = os.path.join(path_anki, "words.json")
unique_groups = set()


def get_path_file(root_dir: str, file_name: str) -> str:
    return os.path.join(root_dir, file_name)


def get_data_file(path_file: str) -> str:
    with open(path_file, encoding="utf-8") as f:
        return f.read()


def print_all_groups(group_set: set) -> None:
    print("\n".join(group_set))


def create_file(data_json, name_file):
    str_json = json.dumps(data_json, ensure_ascii=False, indent=4)
    with open(name_file, mode="w", encoding="utf-8") as f:
        f.write(str_json)


data_all_words_json = get_data_file(path_words_json)
data_file_json = json.loads(data_all_words_json)

for root_dir, _, files in os.walk(dir_for_search_files):
    if files:
        for file_i in files:
            try:
                path_word_i = get_path_file(root_dir, file_i)
                data_file_i = get_data_file(path_word_i)
                data_file_i_json = json.loads(data_file_i)
            except Exception as e:
                print(e)
            for word, val in data_file_i_json.items():
                is_grups = False  # флаг чтобы понять что название ключа непрвильное и его нужно заменить
                word_groups_list = val.get("groups")
                if not word_groups_list:
                    word_groups_list = val.get("grups")  # codespell:ignore grups
                    is_grups = True

                # собираем уникальные группы - просто чтобы посмотреть какие есть
                groups_for_replace = []
                for group_i in word_groups_list:
                    # собираем уникальные группы - просто чтобы посмотреть какие есть
                    if group_i not in unique_groups:
                        unique_groups.add(group_i)
                    # формируем новые списки групп - заменяя пробел на символ '_'
                    groups_for_replace.append(group_i.replace(" ", "_"))

                val["groups"] = groups_for_replace
                if is_grups:
                    del val["grups"]  # codespell:ignore grups
                # обновляем файл
                new_object = {word: val}
                create_file(new_object, path_word_i)
                # обновили общий json файл
                data_file_json[word] = val
        # перезаписываем общий json файл
        create_file(data_file_json, path_words_json)

print_all_groups(unique_groups)
pass
