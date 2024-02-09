
import jinja2
import os
import threading
import logging
import traceback
from cgi import FieldStorage
from urllib.parse import parse_qsl, unquote
from printdoc.controller import on_post, on_get

session = threading.local() # Si se ejecutan varios hilos. 
logging.basicConfig(level=logging.INFO)
p = os.path

def get_path():
    """ """
    path = p.abspath(p.dirname(__file__))
    return path

ENV_PATH = get_path()

def response_data(data):
    """ """
    t = type(data)
    if t == str:
        data = [data.encode()]
    elif t == bytes:
        data = [data]
    return data

def read_input(d):
    """ """
    content_type = d["content_type"]
    data = d["input"].read(d["content_length"]) 
    #for ct in content_type:
    #    if "utf-8" in ct.lower():
    #        return data.decode("utf-8")  # json.
    return data

loader = jinja2.FileSystemLoader(p.join(ENV_PATH, "template"))
tmpl = jinja2.Environment(loader=loader)

def application(environ, response):
    """ """

    path = environ["PATH_INFO"]
    method = environ["REQUEST_METHOD"] 
    query = environ.get("QUERY_STRING", "")
    _input = environ.get("wsgi.input")
    content_type = environ.get("CONTENT_TYPE", "").split(";")
    content_length = int(environ.get("CONTENT_LENGTH") or 0)
    test_local = environ.get("TEST-LOCAL", "")
    query = dict(parse_qsl(query))

    d = {"curdir": ENV_PATH,
         "path": path,
         "method": method,
         "input": _input,
         "query": query,
         "content_type": content_type,
         "content_length": content_length,
         "test_local": test_local,
         "tmpl": tmpl}

    session.d = d

    d["status"] = "200 OK"
    d["headers"] = [("CONTENT-TYPE", "text/plain; charset=utf-8")]

    if method == "GET":

        d["value"] = ""

        try:
            result = on_get(d)
            d["data"] = result
        except Exception as e:
            msg = traceback.format_exc()
            logging.exception(msg)
            d["status"] = "500 Internal Server Error"
            d["data"] = "ERROR"

    else:
        # POST.
        value = read_input(d)
        d["value"] = value

        try:
            result = on_post(d)
            d["data"] = result

        except Exception as e:
            msg = traceback.format_exc()
            logging.exception(msg)
            d["status"] = "500 Internal Server Error"
            d["data"] = "ERROR"

    del session.d    
    response(str(d["status"]), list(d["headers"]))
    data = response_data(d["data"])
    return data


