import config
from common import get_all_exercise, get_exercise_type
from groups_verbs import info_groups
import sys

# res = get_exercise_type("group_1", "rus_eng")

all_exercise = get_all_exercise()
list_group = "\n ".join([i for i in info_groups])
print("Выберите номер группы:\n %s" % list_group)

while True:
    chosen_group = input()
    if chosen_group in info_groups or chosen_group=="q":
        break
    else:
        print("Проверьте правильность написания выбранной группы. Для завершения работы введите - q")

if chosen_group == "q":
    sys.exit(0)

list_type_exercises = ["rus_eng", "eng_rus", "bracket"]
print("Выберите тип упражений:\n%s" % "\n".join(list_type_exercises))
while True:
    chosen_type_exercises = input()
    if chosen_type_exercises in list_type_exercises or chosen_type_exercises=="q":
        break
    else:
        print("Проверьте правильность написания выбранного типа упражений. Для завершения работы введите - q")

if chosen_type_exercises == "q":
    sys.exit(0)

# list_exercise_type = get_exercise_type("group_1", "rus_eng")
list_exercise_type = get_exercise_type(chosen_group, chosen_type_exercises)
for exercise_i, answer_i in list_exercise_type:
    print(exercise_i)
    answer_input = input()
    print(answer_i)
    print("#"*50 + "\n")
    if answer_input=="q":
        sys.exit(0)

# while True:
#
#     res = input()
#
#     if res == "q":
#         break