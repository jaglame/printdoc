from printdoc.app import application
from wsgiref.simple_server import make_server

HOST = "localhost"
PORT = 9191

def start_server():
    """Start the server."""
    httpd = make_server(HOST, PORT, application)
    httpd.serve_forever()

print("RUNNING: %s:%s" % (HOST, str(PORT)))
start_server()
