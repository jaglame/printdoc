
import os
import logging
import subprocess
from os import path as _p
from subprocess import Popen, PIPE, STDOUT

def do_test(d):
    """ El archivo se guarda localmente """

    curdir = d["curdir"]
    query = d["query"]
    value = d["value"]
    pout = _p.join(_p.dirname(curdir), "output")

    try:
        os.mkdir(pout)
    except OSError as error:
        pass  # File exists: ...

    filename = query.get("filename", "out")
    pfile = _p.join(pout, filename)

    logging.info("write: %s" % pfile)

    if type(value) == str:
        mode = "w"
    else:
        mode = "wb"

    with open(pfile, mode) as f:
        f.write(value)

    return "TEST OK"

def do_cups(d):
    """ Se envía una orden de impresión (stdin=input).
    lp -d recurso -
    """
    query = d["query"]
    value = d["value"]

    recurso = query["recurso"]    
    cmd = "lp -d %s -" % (recurso, )    

    logging.info("SEND:", cmd)
    p = subprocess.run([cmd], shell=True, stdout=PIPE, stderr=PIPE, input=value)

    result = p.stdout or p.stderr
    return result

def controller(d):
    """ """

    query = d["query"]
    test = str(query.get("test")).lower() == "true"

    if test:
        result = do_test(d)
    else:
        result = do_cups(d)

    logging.info("OUT: %s" % result)
    return result
    

      


