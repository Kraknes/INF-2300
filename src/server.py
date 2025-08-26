#!/usr/bin/env python3
import socketserver
import os


"""
Written by: Raymon Skjørten Hansen
Email: raymon.s.hansen@uit.no
Course: INF-2300 - Networking
UiT - The Arctic University of Norway
May 9th, 2019
"""

class MyTCPHandler(socketserver.StreamRequestHandler):
    """
    This class is responsible for handling a request. The whole class is
    handed over as a parameter to the server instance so that it is capable
    of processing request. The server will use the handle-method to do this.
    It is instantiated once for each request!
    Since it inherits from the StreamRequestHandler class, it has two very
    usefull attributes you can use:

    rfile - This is the whole content of the request, displayed as a python
    file-like object. This means we can do readline(), readlines() on it!

    wfile - This is a file-like object which represents the response. We can
    write to it with write(). When we do wfile.close(), the response is
    automatically sent.

    The class has three important methods:
    handle() - is called to handle each request.
    setup() - Does nothing by default, but can be used to do any initial
    tasks before handling a request. Is automatically called before handle().
    finish() - Does nothing by default, but is called after handle() to do any
    necessary clean up after a request is handled.
    """
    def handle(self):
        """
        This method is responsible for handling an http-request. You can, and should(!),
        make additional methods to organize the flow with which a request is handled by
        this method. But it all starts here!
        """
        

        req_string = self.rfile.readline()
        decode_string = req_string.decode()
        method, URIreq, version = decode_string.split(" ")
        version = version.replace('\r\n','')
        version = version.encode()

        if method == "GET":
            if URIreq == "/" or URIreq == "/index.html":
                html_file = open("index.html", "rb")
                data = html_file.read()
                ctype = b'text/html'
                status = b'200'
                response = b'OK'
                self.send(version, data, ctype, status, response)
            elif URIreq == '/server.py':
                status = b'403'
                response = b'Forbidden'
                header = version + b" " + status + b" " + response + b"\r\n"
                self.wfile.write(header)
            else:
                status = b'404'
                response = b'Not Found'
                header = version + b" " + status + b" " + response + b"\r\n"
                self.wfile.write(header)

        elif method == 'POST':
            if URIreq == '/test.txt':
                text_file = os.path.join(os.getcwd(), "test.txt")
                text_file = open(text_file, "ab")
                pass
            
            else:
                status = b'404'
                response = b'Not Found'
                header = version + b" " + status + b" " + response + b"\r\n"
                self.wfile.write(header)
        else:
            status = b'404'
            response = b'Not Found'
            header = version + b" " + status + b" " + response + b"\r\n"
            self.wfile.write(header)

        
                
    def send(self, version, data, ctype, status, response):
        v_header = version + b" " + status + b" " + response + b"\r\n"
        ctype_header = b"Content-Type: " + ctype + b"\r\n"
        clen_header = b"Content-Length: " + str(len(data)).encode() + b"\r\n\r\n"
        response_header = v_header + ctype_header + clen_header

        self.wfile.write(response_header + data)
        # self.wfile.write(response_header)
        # self.wfile.close()



if __name__ == "__main__":
    HOST, PORT = "localhost", 8080
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        print("Serving at: http://{}:{}".format(HOST, PORT))
        server.serve_forever()
