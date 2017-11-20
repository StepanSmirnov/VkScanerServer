from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
import os
import requests

import vk
from PIL import Image
import requests
from io import BytesIO
from photoGrabber import PhotoGrabber
from object_detection_tutorial import scanImage


class MyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        args = {}
        idx = max(self.path.find('?'), self.path.find('#'))
        print(self.path)
        if idx >= 0:
            args = cgi.parse_qs(self.path[idx+1:])

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        header = "You must pass code"
        token = ""
        if "code" in args:

            header = "Your access_token is"
            url = "https://oauth.vk.com/access_token"
            params = {"client_id": "6258947",
                      "client_secret" : "7m6jlVFSkE4QgWT3528l",
                      "redirect_uri" : "https://safe-everglades-40623.herokuapp.com",
                      "code" : args["code"][0]
                      }
            response = requests.get(url, params = params)
            print("response_url:".format(response.url))
            response = response.json()
            if "access_token" in response:
                token = response["access_token"]
        
        self.wfile.write(bytes(token, "utf-8"))

    def do_POST(self):
        ctype, pdict = cgi.parse_header(self.headers['content-type'])
        if ctype == 'multipart/form-data':
            args = cgi.parse_multipart(self.rfile, pdict)
        elif ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers['content-length'])
            args = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
        else:
            args = {}
        labels=[]
        if "access_token" in args:
            token = args["access_token"]

            owner_id = ""
            if "owner_id" in args:
                owner_id = args["owner_id"]

            grabber = PhotoGrabber(token)
            urls = grabber.loadPhotos(owner_id)
            for url in urls:
                response = requests.get(url)
                photo = Image.open(BytesIO(response.content))
                labels.append(scanImage(photo))
            self.wfile.write(bytes(labels, "utf-8"))

port = int(os.environ.get("PORT", 5000))
host = "0.0.0.0"
server = HTTPServer((host, port), MyRequestHandler)
print("server started")
server.serve_forever()
