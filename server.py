from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
import os
import requests

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
            params = {"client_id": "6222407",
                      "client_secret" : "ODTeys6TQsNU9geZtcZ7",
                      "redirect_uri" : "https://safe-everglades-40623.herokuapp.com/",
                      "code" : args["code"][0]
                      }
            
            response = requests.get(url, params = params)
            token = response
        
        self.wfile.write(bytes("<!DOCTYPE html>\
                        <html>\
                        <head>\
                                <title></title>\
                        </head>\
                        <body>\
                                <h1>{}</h1>\
                                <p>{}</p>\
                        </body>\
                        </html>".format(header, token), "utf-8"))
port = int(os.environ.get("PORT", 5000))
host = "localhost"#"0.0.0.0"
server = HTTPServer((host, port), MyRequestHandler)
print("server started")
server.serve_forever()
