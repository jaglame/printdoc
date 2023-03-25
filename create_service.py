"""
# Agregar servicio.
sudo systemctl daemon-reload
sudo systemctl enable printdoc.service
sudo systemctl is-enabled printdoc.service

# Iniciar servicio
sudo systemctl start printdoc.service
sudo systemctl status printdoc.service
sudo systemctl stop printdoc.service
sudo systemctl restart printdoc.service
"""

import os
import subprocess
from os import path as _p

SCRIPT = "printdoc.sh"
SERVICE = "printdoc.service"

output_service = """
[Unit]
Description=%(description)s
After=network.target

[Service]
User=%(user)s
ExecStart=%(shell)s %(script_path)s
Type=simple
Restart=always

[Install]
WantedBy=multi-user.target
"""

output_script = """
# Esto es llamado por /etc/systemd/system/printdoc.service
cd %(parent_path)s
. env/bin/activate
cd printdoc
./serve_uwsgi
"""

def get_service_data(d):
    """ """
    _d = {
        "description": "Printer Document Server",
        "user": "jose",
        "exec": "/home/jose/Escritorio/proyectos/github/printdoc/printdoc/serve_uwsgi",
    }

    _d.update(d)
    return output_service % _d

def create_script(d):
    """ printdoc.sh """
    parent_path = d["parent_path"]
    script_path = d["script_path"]
    out = output_script % d


    print("==========SCRIPT==============")
    print(out)

    write_file(script_path, out)

def create_service(d):
    """ """
    etc_path = d["parent_path"]
    service_path = d["service_path"]
    if os.path.isdir(etc_path):

        data = get_service_data(d)
        print("===========(printdoc.service)===============")
        print(data)

        with open(service_path, "w") as f:
            f.write(data)

        print("Service path: %s" % service_path)
    else:
        raise ValueError("No existe directorio de servicios %s" % service_path)

def write_file(path, data):
    """ """
    with open(path, "w") as f:
        f.write(data)
    return f

def run_service(d):
    """ """

    script_path = d["script_path"]

    cmd = """
    chmod +x %(script_path)s;
    systemctl daemon-reload;
    systemctl enable %(service)s;
    systemctl is-enabled %(service)s;
    systemctl stop %(service)s;
    systemctl start %(service)s;
    systemctl status %(service)s;
    """ % d

    print("** run_service ***")
    print(cmd)

    #ret = subprocess.run([cmd], capture_output=True, shell=True)
    ret = subprocess.run([cmd], stdout=subprocess.PIPE, shell=True)
    out = ret.stdout.decode()
    print(out)

def run():
    """ """

    env = os.environ
    user = env["USER"]
    shell = env["SHELL"]
    parent_path = _p.dirname(_p.abspath(__file__))
    script_path = _p.join(parent_path, SCRIPT)
    
    etc_path = "/etc/systemd/system"
    service_path = _p.join(etc_path, SERVICE)

    d = {"user": user,
         "service": SERVICE,
         "shell": shell, #"/usr/bin/bash",
         "etc_path": etc_path,   
         "service_path": service_path,
         "parent_path": parent_path,
         "script_path": script_path}

    create_script(d)
    create_service(d)
    run_service(d)

if __name__ == "__main__":
    """ """
    run()



