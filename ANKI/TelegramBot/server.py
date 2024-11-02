import cgi
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from common import *

PORT_NUMBER = 8088


# This class will handles any incoming request from the browser
class MyHandler(BaseHTTPRequestHandler):

    error_message_format = "ERRRRRROR"
    exp = ""

    # Handler for the GET requests

    # def do_GET(self):
    #     if self.path == "/":
    #         self.path = "/index_example3.html"
    #     try:
    #         # Check the file extension required and
    #         # set the right mime type
    #         sendReply = False
    #         if self.path.endswith(".html"):
    #             mimetype = 'text/html'
    #             sendReply = True
    #         if sendReply == True:
    #             # Open the static file requested and send it
    #             f = open(curdir + sep + self.path)
    #             self.send_response(200)
    #             self.send_header('Content-type', mimetype)
    #             self.end_headers()
    #             self.wfile.write(f.read().encode())
    #             f.close()
    #
    #         else:
    #             self.send_error(200, "ERRRRRRROR")
    #         return
    #
    #     except IOError:
    #         self.send_error(404, 'File Not Found: %s' % self.path)

    # Handler for the POST requests
    def _analisis_request(self):
        """"""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET")
        self.end_headers()
        # content_len = int(self.headers.get('Content-Length'))
        # post_body_bin = self.rfile.read(content_len)
        # post_body = json.loads(post_body_bin.decode().replace("\r\n", ""))
        # return post_body
        ctype, pdict = cgi.parse_header(self.headers["content-type"])
        pdict["boundary"] = bytes(pdict["boundary"], "utf-8")
        fields = cgi.parse_multipart(self.rfile, pdict)
        return fields

    def do_POST(self):
        if self.path in ["/sound"]:
            fields = self._analisis_request()
            if fields.get("word"):
                try:
                    word_sound_t = fields["word"][0].strip()
                    word_sound = word_sound_t.split("|")[0].strip()
                    if os.name == "nt":
                        play_sound(word_sound, count_sound=1)
                    else:
                        sound(word_sound, count_sound=1)
                    res = b"true"
                    self.wfile.write(res)
                except StopIteration as e:
                    res = b"StopIteration"
                    self.wfile.write(res)

        elif self.path in ["/delete"]:
            fields = self._analisis_request()
            if fields.get("word"):
                try:
                    word_sound_t = fields["word"][0].strip()
                    word = word_sound_t.split("|")[0].strip()
                    not_learn_word(word)
                    res = b"true"
                    self.wfile.write(res)
                except StopIteration as e:
                    res = b"StopIteration"
                    self.wfile.write(res)
        elif self.path in ["/info"]:
            fields = self._analisis_request()
            separate = "*" * 30
            if fields.get("word"):
                try:
                    word_t = fields["word"][0].strip()
                    word = word_t.split(" ")[0].strip().lower()
                    data_word = parse_file(word)
                    translate_word = data_word[0]
                    examples = "\n".join(data_word[2])
                    message = f"{translate_word}\n{examples}\n\n{separate}\n\n".encode("utf-8")
                    self.wfile.write(message)
                except StopIteration as e:
                    res = b"StopIteration"
                    self.wfile.write(res)


if __name__ == "__main__":
    try:
        # Create a web server and define the handler to manage the incoming request
        server = HTTPServer(("", PORT_NUMBER), MyHandler)
        print("Started httpserver on port ", PORT_NUMBER)
        # Wait forever for incoming htto requests
        server.serve_forever()
    except KeyboardInterrupt:
        print("^C received, shutting down the web server")
        server.socket.close()
        raise
