
import configparser
from os import path as p
from wsgiref.simple_server import make_server
from printdoc.app import application

# Config.
path = p.abspath(p.dirname(__file__))
config = configparser.ConfigParser()
config.read(p.join(path, "config.ini"))
devel = config["devel"]

HOST = devel["host"]
PORT = int(devel["port"])

def start_server():
    """Start the server."""
    httpd = make_server(HOST, PORT, application)
    httpd.serve_forever()

print("RUNNING: http://%s:%s" % (HOST, str(PORT)))
start_server()
