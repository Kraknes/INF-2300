#!/usr/bin/env python3
import socketserver


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
        # 1) Request line
        reqline = self.rfile.readline().decode("iso-8859-1").strip()
        print("Request line:", reqline)

        # 2) Headers
        headers = self._read_headers()
        print("Headers:", headers)

        # 3) Fixed response (same as Ex.1)
        body = b"Denne body er 29 bits langt" + b"\r\n"
        headers_out = (
            b"HTTP/1.1 200 OK\r\n"
            b"Content-Type: text/plain\r\n"
            b"Content-Length: " + str(len(body)).encode("ascii") + b"\r\n"
            b"\r\n"
        )
        self.wfile.write(headers_out + body)



    def _read_headers(self):
        """Read HTTP headers until blank line. Return dict with lowercased keys."""
        headers = {}
        while True:
            line = self.rfile.readline()
            if not line or line == b"\r\n":
                break
            # Decode and split only on the first colon
            try:
                k, v = line.decode("iso-8859-1").split(":", 1)
            except ValueError:
                # Malformed header line; ignore or log
                continue
            headers[k.strip().lower()] = v.strip()
        return headers



if __name__ == "__main__":
    HOST, PORT = "localhost", 8080
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        print("Serving at: http://{}:{}".format(HOST, PORT))
        server.serve_forever()
