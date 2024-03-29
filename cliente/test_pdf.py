"""
lp -d HP-Deskjet-1010-series sample.pdf

"""

import json
import requests
from urllib.parse import urlencode

HOST = "localhost"
PORT = 9191


data = open("sample.pdf", "rb")
#query = {"printer": "HP-Deskjet-1010-series"}
query = {"printer": "PDF"}

#headers = {"CONTENT-TYPE": "application/pdf"}
headers = {"CONTENT-TYPE": "application/octet-stream"}

qstring = urlencode(query)
response = requests.post("http://%s:%s?%s" % (HOST, PORT, qstring), data=data, headers=headers)

print(response.text)


