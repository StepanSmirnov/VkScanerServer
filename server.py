from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
import os

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
        header = "You don`t pass acsess_token"
        token = ""
        if "access_token" in args:
            header = "Your access_token is"
            token = args["access_token"][0]
        
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
port = int(os.environ.get("PORT", 5000)
server = HTTPServer(("0.0.0.0",port), MyRequestHandler)
print("server started")
server.serve_forever()
