#codint:utf-8
import string
import json

file_name = "словарь.txt"
file_name = "clear_dict.txt"
# file_name = "TEST_словарь.txt"
ignore = [i for i in string.ascii_uppercase]
synonyms = "▼"
antonym = "■"
new_page = "\x0c"
examples = " " * 5
desc_word = " " * 3

#  IV V III II I

def get_data_file(path_file):
    delete_list = []
    words_info = []
    word_i = ""
    for line_i in open(path_file, encoding="utf-8"):
        # line_i = f.readline()
        # print(line_i)
        if line_i.startswith(new_page):
            # новая страница
            delete_list.append(line_i)
            continue
        
        temp_line_i = line_i.strip()
        if temp_line_i:
            if temp_line_i in ignore:
                # Буква
                delete_list.append(line_i)
                continue
            if temp_line_i.isdigit():
                # номер страницы
                delete_list.append(line_i)
                continue
            
            if line_i.startswith(" "):
                word_i += line_i
            else:
                if word_i:
                    words_info.append(word_i)
                    word_i = ""
                word_i += line_i
            
            # print(line_i)
    print(len(words_info))
    return words_info
        
        # print(temp_line_i)

def create_file(name_file, data_file):
    with open(name_file, encoding="utf-8", mode="w") as f:
        for i in data_file:
            f.write(i)

def parse(data):
    temp_dict = dict()
    for info_word_i in data:
        first_line, other = info_word_i.split("\n", 1)
        try:
            if "[" in first_line:
                word_i, word_i_other = first_line.split("[", 1)
                word_i = word_i.strip()
                
                for latin_number in ["IV", "V", "III", "II", "I"]:
                    if latin_number in word_i:
                        word_i = word_i.replace(latin_number, "").strip()
                        break
                
                for number in ["1", "2", "3", "4", "5"]:
                    if number in word_i:
                        word_i = word_i.replace(number, "").strip()
                        break
                
                
                ipa, word_i_other_without_ipa = word_i_other.split("]", 1)
                
                crear_info_word_i = word_i_other_without_ipa + "\n" + other
                if temp_dict.get(word_i):
                    temp_dict[word_i]["translate"].append(crear_info_word_i)    
                else:
                    temp_dict[word_i] = {}
                    temp_dict[word_i]["translate"] = []
                    temp_dict[word_i]["ipa"] = ""
                    temp_dict[word_i]["translate"].append(crear_info_word_i)

        except:
            print(f"Ошибка - {first_line}")
    return temp_dict

def create_json_file(res):
    data_json = json.dumps(res, indent=4, ensure_ascii=False)
    with open("words.json", encoding="utf-8", mode="w") as f:
        f.write(data_json)

res = get_data_file(file_name)  
# create_file("clear_dict_test.txt", res)
dict_words = parse(res)
print(len(dict_words.keys()))

create_json_file(dict_words)

for i in dict_words["like"]["translate"]:
    print(i)
print()
