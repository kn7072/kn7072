# -*- coding:utf-8 -*-
import os
from common import get_list_words, get_info_word


path_file_to_save = os.path.join(os.getcwd(), "new_words.txt")

list_new_words = get_list_words(path_file_to_save)
for word_i in list_new_words:
    get_info_word(word_i)


print(list_new_words)

