import cgi
import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

from common import create_file, generate_word_report_html, get_data_file, sound
from urllib.parse import unquote, unquote_plus


PORT_NUMBER = 8090 # 8088
path_to_all_words = "all_words_new.json"
path_to_known_examples = "../Предложения.txt"
file_to_save_words = "WORDS_FOR_LEARN.txt"
file_to_save_sentence = "SENTENCE_TO_LEAR.txt"

macmillan_words = json.loads(get_data_file("./macmillan_ipa_stars.json"))


def write_file(path_file: str, data_file: str) -> None:
    """Записывает data_file в файл, перезаписывая сожержимое файла."""
    with open(path_file, encoding="utf-8", mode="w") as f:
        f.write(data_file)


def get_word_for_stars(obj: dict, count_star: int) -> list:
    """Отбирает слова по количеству звезд."""
    temp = []
    for word, word_val in obj.items():
        if word_val["stars"] == count_star:
            temp.append(word)
    return temp

list_three_stars = get_word_for_stars(macmillan_words, 1)


def write_word_as_known(path_to_file) -> None:
    """Записывает слова которые запрашивались."""
    with open(path_to_file, mode='a', encoding='utf-8') as f:
        while True:
            word = yield
            f.write(word)
            f.flush()


generator_for_write_word = write_word_as_known(file_to_save_words)
next(generator_for_write_word)

generator_for_write_sentence = write_word_as_known(file_to_save_sentence)
next(generator_for_write_sentence)

# This class will handles any incoming request from the browser
class MyHandler(BaseHTTPRequestHandler):

    error_message_format = "ERRRRRROR"
    exp = ""
    all_words_json = json.loads(get_data_file(path_to_all_words))

    # Handler for the POST requests
    def _analisis_request(self):
        """"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET')
        self.end_headers()
        ctype, pdict = cgi.parse_header(self.headers['content-type'])
        pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
        fields = cgi.parse_multipart(self.rfile, pdict)
        return fields

    def get_know_words(self) -> dict:
        """Возвращаем множество изученных слов."""
        all_word_dict = {}
        for str_i in open(path_to_known_examples, encoding="utf-8"):
            str_i = str_i.strip()
            if str_i:
                know_words_str, example_eng, example_rus = str_i.split(";")
                know_words_list = [word_i.strip() for word_i in know_words_str.split(",")]
                for known_word_i in know_words_list:
                    is_added = all_word_dict.get(known_word_i)
                    if is_added:
                        all_word_dict[known_word_i]["examples"].append((example_eng, example_rus))
                    else:
                        all_word_dict[known_word_i] = {}
                        all_word_dict[known_word_i]["examples"] = []
                        all_word_dict[known_word_i]["examples"].append((example_eng, example_rus))
        return all_word_dict

    def parsing_known_examples(self, word: str, *, all_examples: bool) -> tuple:
        """Парсим известные слова.
        all_examples - выводить все примеры, даже если слово уже изучено.
        """
        all_knonw_word_dict = self.get_know_words()
        temp_list_examples = {"word": word,
                              "examples": [],
                              "is_known": False
                              }

        transcription = self.all_words_json[word]["transcription"]
        translate = self.all_words_json[word]["translate"]
        mnemonic = self.all_words_json[word]["mnemonic"]
        comments = self.all_words_json[word]["comment"]

        # word_for_sentence = set(list_three_stars) - set(all_knonw_word_dict)
        # word_for_sentence = [word.lower() for word in word_for_sentence]
        # word_for_write = "\n".join(word_for_sentence)
        # write_file("./word_for_sentence.txt", word_for_write)

        if not all_examples and word in all_knonw_word_dict:
            temp_list_examples["is_known"] = True
            for example_eng, exampe_rus in all_knonw_word_dict[word]["examples"]:
                temp_list_examples["examples"].append((example_eng, exampe_rus, [], []))
            return translate, transcription, mnemonic, temp_list_examples, comments

        examples = self.all_words_json[word]["examples"]

        for example_eng_i, example_rus_i in examples:
            words_sentence = example_rus_i["words"]
            translate_sentence = example_rus_i["translate"]
            diff_words = list(set(words_sentence) - set(all_knonw_word_dict.keys()))
            diff_words.sort()
            str_for_save = f"{example_eng_i}"
            temp_list_examples["examples"].append((str_for_save, translate_sentence, diff_words, words_sentence))

        temp_list_examples["examples"].sort(key=lambda x: (len(x[2]), len(x[3])))
        return translate, transcription, mnemonic, temp_list_examples, comments

    def get_contant_to_send(self, content: dict, translate_word: str, transcription: str, mnemonic: list, comments: list) -> str:
        """Возвращает бинарные дынные ответа."""
        msg_all = ""
        separate = "#" * 30
        delimiter = " " * 4
        mnemonic_str = "\n".join(mnemonic)

        examples_list = content["examples"]
        if content["is_known"]:
            for example_eng, example_rus, _, _ in examples_list:
                msg = f"{content['word']} - Уже изучено\n\n{example_eng}\n{example_rus}\n{'-' * 5}\n\n"
                msg_all += msg
        else:
            for example_eng, example_rus, _, words_in_sentence in examples_list:
                words_diff = ', '.join(words_in_sentence)
                text_to_save = f"{words_diff};{delimiter}{example_eng};{delimiter}{example_rus}"
                msg = f"{example_eng}\n{example_rus}\n\n{text_to_save}\n{'-' * 5}\n\n"
                msg_all += msg
        comments = "\n".join(comments)
        msg_all = f"{msg_all}{separate}\n{transcription} - {translate_word}\n\n{separate}\nМнемоника\n\n{mnemonic_str}\n\n{separate}\nКомментарии\n\n{comments}"
        msg_all = msg_all.replace("%", "%%")
        return msg_all.encode("utf-8")

    def do_POST(self):
        all_knonw_word_dict = self.get_know_words()
        if self.path in ["/word"]:
            fields = self._analisis_request()
            if fields.get("word"):
                try:
                    word = fields["word"][0].strip().replace(",", "").replace(".", "").replace(":", "").replace(";", "").lower()
                    bin_data_word = generate_word_report_html(word, self.all_words_json[word], all_knonw_word_dict, all_examples=False)
                    create_file("temp.html", bin_data_word)
                    translate, transcription, mnemonic, content_list, comments = self.parsing_known_examples(word, all_examples=False)
                    content_bin = self.get_contant_to_send(content_list, translate, transcription, mnemonic, comments)
                    self.wfile.write(content_bin)
                except StopIteration as e:
                    res = b"StopIteration"
                    self.wfile.write(res)
                else:
                    generator_for_write_word.send(f"{word}\n")
        elif self.path in ["/word_all_examples"]:
            fields = self._analisis_request()
            if fields.get("word"):
                try:
                    word = fields["word"][0].strip().replace(",", "").replace(".", "").lower()
                    translate, transcription, mnemonic, content_list, comments = self.parsing_known_examples(word, all_examples=True)
                    content_bin = self.get_contant_to_send(content_list, translate, transcription, mnemonic, comments)
                    self.wfile.write(content_bin)
                except StopIteration as e:
                    res = b"StopIteration"
                    self.wfile.write(res)
                else:
                    generator_for_write_word.send(f"{word}\n")
        elif self.path in ["/sentence"]:
            fields = self._analisis_request()
            word = fields["word"][0].strip()
            generator_for_write_sentence.send(f"{word}\n")
            self.wfile.write(b"ok")

        if self.path in ["/sound"]:
            fields = self._analisis_request()
            if fields.get("word"):
                try:
                    word = fields["word"][0].strip().replace(",", "").replace(".", "").lower()
                    if os.name == "nt":
                        play_sound(word, count_sound=1)
                    else:
                        sound(word, count_sound=1)
                    res = b"true"
                    self.wfile.write(res)
                except StopIteration as e:
                    res = b"StopIteration"
                    self.wfile.write(res)
        else:
            self.wfile.write(b"\n\nno sound")    

    def do_GET(self):
        all_knonw_word_dict = self.get_know_words()

        # url = unquote(self.path)
        url2 = unquote_plus(self.path)
        print(url2)
        if self.path in ["/word"]:
            fields = self._analisis_request()
            if fields.get("word"):
                print("xxxx")
        self.wfile.write(b"123")


if __name__ == "__main__":
    try:
        # Create a web server and define the handler to manage the incoming request
        server = HTTPServer(('', PORT_NUMBER), MyHandler)
        print('Started httpserver on port ', PORT_NUMBER)
        generator_for_write_word.send("##########\n")
        # Wait forever for incoming htto requests
        server.serve_forever()
    except KeyboardInterrupt:
        print('^C received, shutting down the web server')
        server.socket.close()
        raise
