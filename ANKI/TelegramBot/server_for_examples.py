from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from common import get_data_file
import cgi

PORT_NUMBER = 8088
path_to_all_words = "all_words_new.json"
path_to_known_examples = "../Предложения.txt"


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

    def parsing_known_examples(self, word: str, examples: list) -> dict:
        """Парсим известные слова."""
        all_knonw_word_dict = self.get_know_words()
        temp_list_examples = {"word": word,
                              "examples": [],
                              "is_known": False
                              }
        if word in all_knonw_word_dict:
            temp_list_examples["is_known"] = True
            for example_eng, exampe_rus in all_knonw_word_dict[word]["examples"]:
                temp_list_examples["examples"].append((example_eng, exampe_rus, [], []))
            return temp_list_examples

        for example_eng, example_rus in examples:
            example_i, words = example_eng
            diff_words = list(set(words) - set(all_knonw_word_dict.keys()))
            diff_words.sort()
            str_for_save = f"{example_i}"
            temp_list_examples["examples"].append((str_for_save, example_rus, diff_words, words))

        temp_list_examples["examples"].sort(key=lambda x: (len(x[2]), len(x[3])))
        return temp_list_examples

    def get_contant_to_send(self, content: dict, translate_word: str, transcription: str) -> str:
        """Возвращает бинарные дынные ответа."""
        msg_all = ""
        separate = "#" * 30
        delimiter = " " * 4

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
        msg_all = f"{msg_all}{separate}\n{transcription} - {translate_word}"
        msg_all = msg_all.replace("%", "%%")
        return msg_all.encode("utf-8")

    def do_POST(self):
        if self.path in ["/word"]:
            fields = self._analisis_request()
            if fields.get("word"):
                try:
                    word = fields["word"][0].strip().replace(",", "").replace(".", "").lower()
                    examples_eng = self.all_words_json[word]["examples"]
                    examples_rus = self.all_words_json[word]["example_translate"]
                    transcription = self.all_words_json[word]["transcription"]
                    translate = self.all_words_json[word]["translate"]
                    examples = zip(examples_eng, examples_rus)
                    content_list = self.parsing_known_examples(word, examples)
                    content_bin = self.get_contant_to_send(content_list, translate, transcription)
                    self.wfile.write(content_bin)
                except StopIteration as e:
                    res = b"StopIteration"
                    self.wfile.write(res)


if __name__ == "__main__":
    try:
        # Create a web server and define the handler to manage the incoming request
        server = HTTPServer(('', PORT_NUMBER), MyHandler)
        print('Started httpserver on port ', PORT_NUMBER)
        # Wait forever for incoming htto requests
        server.serve_forever()
    except KeyboardInterrupt:
        print('^C received, shutting down the web server')
        server.socket.close()
        raise