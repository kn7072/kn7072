# coding:utf-8
import json, os
from parse_exercise import read_file, create_file

count_lessens_in_file = 7
count_sentence_in_slide = 3
count_symbols_in_slide = 1300
path_to_exercises = "exercise.json"
path_script = os.getcwd()
path_to_slides = os.path.join(path_script, "carusel", "slides")

if not os.path.isdir(path_to_slides):
    os.mkdir(path_to_slides)

dict_exercises = json.loads(read_file(path_to_exercises))

def melt_data(data: list) -> tuple:
    
    melt_list = []
    for num_lessens, data_exercise_dict in data:
        for num_exercise, data_exercise_list in data_exercise_dict.items():
            for sentence_question, sentence_answer in data_exercise_list:
                question = f"{sentence_question}({num_lessens}/{num_exercise})"
                answer = f"{sentence_answer}({num_lessens}/{num_exercise})"
                melt_list.append([question, answer])
    return melt_list


def spLit_exercise() -> list:
    temp_count = 0
    temp_list = []
    for num_exercise, data_exercise in dict_exercises.items():
        if temp_count < count_lessens_in_file:
            temp_list.append([num_exercise, data_exercise])
            temp_count += 1
        else:
            yield temp_list
            temp_count = 0
            temp_list = []

def get_slides(melt_list: list) -> list:
    content_slide_question = ""
    content_slide_answer = ""
    list_slides = []
    count = 0
    for question, answer in melt_list:
        if len(question) > count_symbols_in_slide or len(answer) > count_symbols_in_slide:
            raise Exception(f"Слишком длинное предложение")

        if count < count_sentence_in_slide:
            temp_len_question_slide = len(content_slide_question) + len(question)
            temp_len_answer_slide = len(content_slide_answer) + len(answer)
            if temp_len_question_slide < count_symbols_in_slide and temp_len_answer_slide < count_symbols_in_slide:
                content_slide_question += f"\n{question}"
                content_slide_answer += f"\n{answer}"
                count += 1
            else:
                count = 1
                if content_slide_question and content_slide_answer:
                    list_slides.append(content_slide_question + "#\n")
                    list_slides.append(content_slide_answer + "#\n")
                    content_slide_question = question
                    content_slide_answer = answer
                else:
                    raise Exception("Слайд пустой")    
        else:
            count = 1
            list_slides.append(content_slide_question + "#\n")
            list_slides.append(content_slide_answer + "#\n")
            content_slide_question = question
            content_slide_answer = answer
    return list_slides


generator = spLit_exercise()
slide_number = 1
for data_exercises in generator:
    melt_list = melt_data(data_exercises)
    slide_list_i = get_slides(melt_list)
    slide_text_i = "".join(slide_list_i)
    path_to_slide = os.path.join(path_to_slides, f"{slide_number}.txt")
    create_file(path_to_slide, slide_text_i)
    slide_number += 1
