#!/usr/bin/python
# -*-coding: utf8 -*-

import threading
from BaseHTTPServer import HTTPServer
from SocketServer import ThreadingMixIn
from httpserverhandler import PlanBHTTPServerHandler


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""


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