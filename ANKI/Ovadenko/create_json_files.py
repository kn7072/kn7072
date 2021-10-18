# coding=utf-8
import os, json, glob, json
from parse_exercise import get_text_exercise, get_list_sentance, get_files_of_dir, create_file, read_file

path_to_ovadenko = "/home/stapan/GIT/kn7072/ANKI/Ovadenko"
path_dir_exercises = os.path.join(path_to_ovadenko, "Упражнения")
path_dir_exercises_num = os.path.join(path_dir_exercises, "20")

def create_json_files_exercises(path_to_dir: str) -> str:
    """
    Создает json файлы упражнений
    path_to_dir путь к каталогу где лежат файлы(упражнения и ответы)
    """
    list_files_dir = get_files_of_dir(path_to_dir)
    for rus_name, eng_name in list_files_dir:
        text_exercise_rus = get_text_exercise(os.path.join(path_to_dir, rus_name))
        get_list_sentance_rus = get_list_sentance(text_exercise_rus)

        text_exercise_eng = get_text_exercise(os.path.join(path_to_dir, eng_name))
        get_list_sentance_eng = get_list_sentance(text_exercise_eng)

        len_list_sentance_rus = len(get_list_sentance_rus)
        len_list_sentance_eng = len(get_list_sentance_eng)
        if len_list_sentance_rus == len_list_sentance_eng:
            dict_exercise = {rus_name: list(zip(get_list_sentance_rus, get_list_sentance_eng))}
            data_str = json.dumps(dict_exercise, ensure_ascii=False, indent=4)
            path_json = os.path.join(path_to_dir, rus_name + ".json")
            create_file(path_json, data_str)
        else:
            print(f"Проблемы ${path_to_dir}/{rus_name}\n    len_rus {len_list_sentance_rus}\n    len_eng {len_list_sentance_eng}")

def create_full_json(path_to_dir: str) -> str:
    """
    Создает единый файл json для всех упражнений
    """
    all_exercises = {}
    for dir_i in os.listdir(path_to_dir):
        all_exercises[dir_i] = {}
        path_dir_exercisee = os.path.join(path_to_dir, dir_i)
        list_files = glob.glob(f'{path_dir_exercisee}/*.json')
        for path_file_exercise in list_files:
            data_file_dict = json.loads(read_file(path_file_exercise))
            all_exercises[dir_i].update(data_file_dict)

    data_str = json.dumps(all_exercises, ensure_ascii=False, indent=4)
    path_json = os.path.join(path_to_ovadenko, "exercise" + ".json")
    create_file(path_json, data_str)


for i in os.listdir("Упражнения"):
    path_dir_exercises_num = os.path.join(path_dir_exercises, i)
    create_json_files_exercises(path_dir_exercises_num)

# create_json_files_exercises(path_dir_exercises_num)
create_full_json(path_dir_exercises)


