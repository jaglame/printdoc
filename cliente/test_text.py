"""
lp -d HP-Deskjet-1010-series sample_text.txt

"""

import json
import requests
from urllib.parse import urlencode

HOST = "localhost"
PORT = 9191

data = open("sample_text.txt", "r")
query = {"recurso": "HP-Deskjet-1010-series",
         "filename": "recurso.txt",
         "test": "false"}

headers = {"CONTENT-TYPE": "text/plain"}
qstring = urlencode(query)
response = requests.post("http://%s:%s?%s" % (HOST, PORT, qstring), data=data, headers=headers)

print(response.text)


