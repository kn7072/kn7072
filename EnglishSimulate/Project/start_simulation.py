# coding="utf-8"
from http.server import HTTPServer
from example3 import MyHandler
from threading import Thread
from db import creata_work_base


class Simulation:
    """"""

    def __init__(self, serv_port=8088):
        self.serv_port = serv_port
        pass

    def _models(self, data):
        print("Модель")
        result = b"test"
        fun = lambda: None
        if "server_close" in data.keys():
            result = b"finish server"
            fun = self._shutdown_server
        return result, fun

    def _start_server(self):
        try:
            # Create a web server and define the handler to manage the incoming request
            MyHandler.modeles = self._models
            self.server = HTTPServer(('', self.serv_port), MyHandler)
            print('Started httpserver on port ', self.serv_port)
            # Wait forever for incoming http requests
            self.server.serve_forever()
        except KeyboardInterrupt:
            print('^C received, shutting down the web server')
            self.server.socket.close()

    def _shutdown_server(self):
        print("Завершем работу сервера")

        def kill_me_please(server):
            server.shutdown()

        t = Thread(target=kill_me_please, args=(self.server,))
        t.daemon = True
        t.start()
        # self.server.shutdown()
        #self.server.socket.close()
        # self.server.server_close()


if __name__ == "__main__":
    try:
        creata_work_base("core_word_base.db")
        inst = Simulation()
        inst._start_server()
    except:
        inst._shutdown_server()