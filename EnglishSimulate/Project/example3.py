#!/usr/bin/python
from http.server import BaseHTTPRequestHandler, HTTPServer
from os import curdir, sep
from db import query_sql, updata_base
from play_audio import play_sound
import cgi
import json

PORT_NUMBER = 8088


# This class will handles any incoming request from the browser
class MyHandler(BaseHTTPRequestHandler):

    error_message_format = "ERRRRRROR"
    exp = ""

    # Handler for the GET requests
    def do_GET(self):
        if self.path == "/":
            self.path = "/index_example3.html"
        try:
            # Check the file extension required and
            # set the right mime type
            sendReply = False
            if self.path.endswith(".html"):
                mimetype = 'text/html'
                sendReply = True
            if sendReply == True:
                # Open the static file requested and send it
                f = open(curdir + sep + self.path)
                self.send_response(200)
                self.send_header('Content-type', mimetype)
                self.end_headers()
                self.wfile.write(f.read().encode())
                f.close()

            else:
                self.send_error(200, "ERRRRRRROR")
            return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    # Handler for the POST requests
    def _analisis_request(self):
        """"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        ctype, pdict = cgi.parse_header(self.headers['content-type'])
        pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
        fields = cgi.parse_multipart(self.rfile, pdict)
        return fields

    def _start(self, fields):
        start = int(fields["start"][0])
        finish = int(fields["finish"][0])
        sql = """SELECT word, translate, transcription FROM core_word_base WHERE know==0 AND
                        id BETWEEN {start} AND {finish};""".format(start=start, finish=finish)
        res = query_sql(sql)
        if res:
            self.__class__.list_word = res
        else:
            self.__class__.list_word = []

    @classmethod
    def _generate(cls):
        for i in cls.list_word:
            x = yield i
            if x:
                return

    def get_json(self, data):
        temp = json.dumps({"word": data[0], "translate": data[1], "trancription": data[2]}).encode()
        return temp

    def do_POST(self):
        if self.path == "/ru":
            fields = self._analisis_request()
            if fields.get("start"):
                self._start(fields)
                self.__class__.send = self._generate()
                try:
                    word_next = self.__class__.send.__next__()
                    word_json = self.get_json(word_next)
                    self.wfile.write(word_json)
                except StopIteration as e:
                    # TODO ВОЗВРАЩАТЬ ПУСТОЙ ОТВЕТ
                    word_next = {}
                    self.wfile.write(b"The end")
            elif fields.get("know"):
                updata_base(fields)
                try:
                    word_next = self.__class__.send.__next__()
                    word_json = self.get_json(word_next)
                    self.wfile.write(word_json)
                except StopIteration as e:
                    # TODO ВОЗВРАЩАТЬ ПУСТОЙ ОТВЕТ
                    word_next = {}
                    self.wfile.write(b"The end")
            elif fields.get("sound"):
                word = fields["word"][0].decode()
                play_sound(word)
                self.wfile.write(b"sound")
            else:
                print()
            return

        if self.path == "/en":
            pass
        if self.path == "/sound":
            pass

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