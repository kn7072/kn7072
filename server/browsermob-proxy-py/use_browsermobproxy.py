from browsermobproxy import Server, Client
server = Server(r"d:\Python\browsermob-proxy-2.0-beta-9-bin\browsermob-proxy-2.0-beta-9\bin\browsermob-proxy",{"port":9090})
server.start()
client = Client("localhost:9090")
client.port
client.new_har('google')
client.har