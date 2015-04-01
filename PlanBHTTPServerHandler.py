#!/usr/bin/python
# -*-coding: utf8 -*-

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import mimetypes
from os import curdir, sep
from SocketServer import ThreadingMixIn
import os
import threading


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""


class PlanBHTTPServerHandler(BaseHTTPRequestHandler):

    allowed_extensions = ['.html', '.jpg', '.gif', '.js', '.css', '.tff', '.woff']

    def has_permission_to_reply(self, file_path):
        file_name, file_extension = os.path.splitext(file_path)
        send_reply = file_extension in self.allowed_extensions
        mimetype = mimetypes.guess_type(file_name + file_extension)
        return mimetype, send_reply

    def do_GET(self):
        file_path = self.path
        if file_path == "/":
            file_path = "/index.html"

        try:
            mimetype, send_reply = self.has_permission_to_reply(file_path)

            if True:
                full_path = curdir + sep + "pages" + sep + file_path
                f = open(full_path)
                self.send_response(200)
                self.send_header('Content-type', mimetype)
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
            return
        except IOError:
            self.send_error(404, 'File Not Found: %s' % file_path)


class PlanBHTTPServer():
    def __init__(self):
        pass

    def run(self, port_number):
        threading.Thread(target=self.run_internal, args=[port_number]).start()

    @staticmethod
    def run_internal(port_number):
        try:
            server = ThreadedHTTPServer(('', port_number), PlanBHTTPServerHandler)
            print 'Started httpserver on port ', server.server_port
            server.serve_forever()

        except KeyboardInterrupt:
            print '^C received, shutting down the web server'
            server.socket.close()