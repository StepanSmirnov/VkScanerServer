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
            rpath = self.path[:idx]
            args = cgi.parse_qs(self.path[idx+1:])
        else:
            rpath = self.path
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
            token = response.json()
            if "access_token" in token:
                token = token["access_token"]
                grabber = PhotoGrabber(token)
                photos = grabber.loadPhotos()
                labels = []
                for photo in photos:
                    labels.append(scanImage(photo))
                print("labels:{}".format(labels))
        
        self.wfile.write(bytes("<!DOCTYPE html>\
                        <html>\
                        <head>\
                                <title></title>\
                        </head>\
                        <body>\
                                <h1>{}</h1>\
                                <p>{}</p>\
                        </body>\
                        </html>".format(header, lebles), "utf-8"))
port = int(os.environ.get("PORT", 5000))
host = "0.0.0.0"
server = HTTPServer((host, port), MyRequestHandler)
print("server started")
server.serve_forever()
