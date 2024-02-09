
import os
import logging
import subprocess
import json
from os import path as _p
from subprocess import Popen, PIPE, STDOUT

def do_local(d):
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

    logging.info("do_local: %s" % pfile)

    if type(value) == str:
        mode = "w"
    else:
        mode = "wb"

    with open(pfile, mode) as f:
        f.write(value)

    return "TEST"

def lpd(printer, data, options=""):
    """ Se envía una orden de impresión (stdin=input).
    lp -d printer_name -
    lp -d printer_name -o raw -

    options = "-o raw"
    """

    lp = "lp -d %s" % printer

    if options:
        lp += " " + options

    cmd = [lp, "-"] #"lp -d %s" % (printer, )    
    logging.info("lpd: %s" % str(cmd))

    #p = subprocess.run(cmd, shell=True, stdout=PIPE, stderr=PIPE, input=data, timeout=2)
    #result = p.stdout or p.stderr

    p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell=True)
    p.stdin.write(data)
    p.stdin.flush()
    stdout, stderr = p.communicate(timeout=3)
    result = (stdout or stderr)

    logging.info("lpd: %s" % result)
    return result

def do_cancel(d):
    """ """
    query = d["query"]
    jobid = query["jobid"]
    result = ""

    if jobid:
        cmd = ["cancel %s" % jobid]
        logging.info("do_cancel: %s" % str(cmd))

        p = subprocess.run(cmd, shell=True, stdout=PIPE, stderr=PIPE, timeout=5)

        result = p.stdout or p.stderr or ("Job ID %s, cancelado" % jobid)
        logging.info("do_cancel: %s" % str(result))

    return result

def do_cancel_all(d):
    """ """
    query = d["query"]
    printer = query["printer"]
    result = ""

    if printer:

        if printer != "*":    
            cmd = ["cancel -a %s" % printer]
        else:
            cmd = ["cancel -a"]

        logging.info("do_cancel_all: %s" % str(cmd))

        p = subprocess.run(cmd, shell=True, stdout=PIPE, stderr=PIPE, timeout=5)

        result = p.stdout or p.stderr or ("Job printer %s, cancelado" % printer)
        logging.info("do_cancel_all: %s" % str(result))

    return result

def do_print(d):
    """ """
    query = d["query"]
    data = d["value"]
    printer = query.get("printer") or query.get("recurso")    
    options = query.get("options", "")
    return lpd(printer, data, options)

def do_test(d):
    """ """

    curdir = d["curdir"]
    query = d["query"]

    printer = query["printer"]
    options = query.get("options", "")
    _type = query["type"]

    if _type == "txt":
        pfile = _p.join(curdir, "files/demo.txt")
    elif _type == "pdf":
        pfile = _p.join(curdir, "files/demo.pdf")

    logging.info("read: %s" % pfile)

    try:
        msg = "" #f"Orden de impresión enviada a <{printer}> tipo <{_type}>"
        with open(pfile, "rb") as f:
            msg = lpd(printer, f.read(), options)

    except Exception as e:
        msg = str(e)

    return msg

def get_printers(query=None):
    """
    dispositivo para Deskjet-2050-J510-series: hp:/usb/Deskjet_2050_J510_series?serial=BR166FN0BH05D1
    dispositivo para HP-Deskjet-1010-series: hp:/usb/Deskjet_1010_series?serial=CN39U18K7B05XH
    dispositivo para hp_fatima: smb://192.168.3.107/Deskjet-1010-series
    dispositivo para PDF: cups-pdf:/
    """

    q = ""
    _printer = ""
    if query:
        q = query.get("q", "").lower()
        _printer = query.get("printer", "")

    cmd = "lpstat -v"
    p = subprocess.run([cmd], shell=True, stdout=PIPE, stderr=PIPE)
    data = p.stdout.decode()
    
    printers = []
    lines = data.split("\n")
    for _line in lines:
        line = " ".join(_line.split())
        if not line:
            continue

        device, printer, uri = line.rsplit(" ", 2)
        printer = printer.strip(":")
    
        if _printer and _printer != printer:
            continue

        if q and q not in printer.lower():
            continue

        uri = uri.strip()
        printers.append({
            "printer": printer,
            "uri": uri
        })

    return printers

def get_jobs(printer):
    """
    HP-Deskjet-1010-series-561 jose             55296   lun 20 mar 2023 06:06:06 -03
    HP-Deskjet-1010-series-562 jose              1024   lun 20 mar 2023 06:06:08 -03

    cupstest-3 kajol 8192 Tue Aug 05 13:24:43 2008
    cupstest-4 kajol 8192 Tue Aug 05 13:25:34 2008
    """

    cmd = "lpstat -o"
    if printer:
        cmd += " " + printer

    logging.info("get_jobs: %s" % cmd)
    
    p = subprocess.run([cmd], shell=True, stdout=PIPE, stderr=PIPE)
    data = p.stdout or p.stderr #or "(Cola vacia)"

    data = p.stdout.decode()
    lines = data.split("\n")

    jobs = []
    for _line in lines:

        line = " ".join(_line.split())
        if not line:
            continue

        parts = line.split(" ", 2)
        jobid, user, part2 = parts

        jobid = jobid
        user = user

        printer, pid = jobid.rsplit("-", 1)

        p1, p2 = part2.split(" ", 1)
        p1 = p1
        time, n = p2.rsplit(" ", 1)
        time = time

        jobs.append({
            "printer": printer,
            "jobid": jobid,
            "user": user,
            "time": time
        })

    return jobs

def do_queue(query):
    """ HP-Deskjet-1010-series-422 jose 23552 vie 10 mar 2023 00:41:31 -03 """
    printer = query.get("printer")
    jobs = get_jobs(printer)
    return jobs

def do_running(d):
    """ """
    cmd = "lpstat -r"
    p = subprocess.run([cmd], shell=True, stdout=PIPE, stderr=PIPE)
    data = p.stdout or p.stderr
    return "CUPS: %s" % data.decode()

def do_list(d):
    """ """
    query = d["query"]
    printers = get_printers(query)
    return json.dumps(printers)

def on_get(d):
    """ """

    path = d["path"]
    query = d["query"]
    tmpl = d["tmpl"]
    
    if path == "/queue":
        jobs = do_queue(query)
        status = do_running(d)
        d["headers"] = [("CONTENT-TYPE", "text/html; charset=utf-8")]
        _d = {"jobs": jobs,
              "query": query,
              "status": status}
        return tmpl.get_template("queue.html").render(_d)

    if path == "/printers" or path == "/":
        printers = get_printers(query)
        status = do_running(d)
        d["headers"] = [("CONTENT-TYPE", "text/html; charset=utf-8")]
        _d = {"printers": printers,
              "query": query,
              "status": status}
        return tmpl.get_template("printers.html").render(_d)

    if path == "/list":
        d["headers"] = [("CONTENT-TYPE", "application/json; charset=utf-8")]
        return do_list(d)

    if path == "/cancel":
        return do_cancel(d)

    if path == "/cancel_all":
        return do_cancel_all(d)

    if path == "/test":
        return do_test(d)

    return do_running(d)

def on_post(d):
    """ """

    query = d["query"]
    test = str(query.get("test")).lower() == "true"

    if test:
        result = do_local(d)
    else:
        result = do_print(d)

    logging.info("OUT: %s" % result)
    return result
    
