from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from common import get_data_file
import cgi

PORT_NUMBER = 8088
path_to_all_words = "all_words_new.json"
path_to_known_examples = "../Предложения_new.txt"


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

    def get_know_words(self) -> set:
        """Возвращаем множество изученных слов."""
        all_word_set = set()
        for str_i in open(path_to_known_examples, encoding="utf-8"):
            know_words_str = str_i.split(";")[0]
            know_words_list = set([word_i.strip() for word_i in know_words_str.split(",")])
            all_word_set = all_word_set.union(know_words_list)
        return all_word_set

    def parsing_known_examples(self, word: str, examples: list) -> list:
        """Парсим известные слова."""
        all_word_set = self.get_know_words()
        temp_list_examples = []
        if word in all_word_set:
            temp_list_examples = [(word, "уже довавлено в список предложений", "")]
            return temp_list_examples
        for example_eng, example_rus in examples:
            example_i, words = example_eng
            diff_words = list(set(words) - all_word_set)
            diff_words.sort()
            str_for_save = f"{', '.join(words)};    {example_i}"
            temp_list_examples.append((str_for_save, example_rus, diff_words))

        temp_list_examples.sort(key=lambda x: len(x[2]))
        return temp_list_examples

    def get_contant_to_send(self, content: list) -> str:
        """Возвращает бинарные дынные ответа."""
        msg_all = ""
        separate = "#" * 30
        for example_eng, example_rus, diff_word in content:
            words, *x = example_eng.split(";")
            example_rus_for_print = " " * (len(words) + 5) + example_rus
            msg = f"{example_eng}\n{example_rus_for_print}\n{diff_word}\n{'-' * 5}\n\n"
            msg_all += msg
        msg_all = f"{msg_all}{separate}\n"
        return msg_all.encode("utf-8")

    def do_POST(self):
        if self.path in ["/word"]:
            fields = self._analisis_request()
            if fields.get("word"):
                try:
                    word = fields["word"][0].strip()
                    examples_eng = self.all_words_json[word]["examples"]
                    examples_rus = self.all_words_json[word]["example_translate"]
                    examples = zip(examples_eng, examples_rus)
                    content_list = self.parsing_known_examples(word, examples)
                    content_bin = self.get_contant_to_send(content_list)
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