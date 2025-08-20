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
        # --- 1) Request line
        reqline = self.rfile.readline().decode("iso-8859-1").strip()
        if not reqline:
            print("Empty request line")
            return
        try:
            method, path, version = reqline.split(" ", 2)
        except ValueError:
            print("Bad request line:", reqline)
            return self._send(400, b"Bad Request", "text/plain")

        # --- 2) Headers
        headers = {}
        while True:
            line = self.rfile.readline()
            if not line or line == b"\r\n":
                break
            if b":" not in line:
                continue
            k, v = line.decode("iso-8859-1").split(":", 1)
            headers[k.strip().lower()] = v.strip()

        # --- 3) Body (exactly Content-Length bytes)
        clen = int(headers.get("content-length", "0") or 0)
        body = self.rfile.read(clen) if clen > 0 else b""

        # --- DEBUG LOGS (so we can see what's happening)
        # print(f"[REQ] {method} {path} {version}")
        # print(f"[HDR] content-length={clen}, content-type={headers.get('content-type')}")
        # print(f"[DBG] cwd={os.getcwd()}")
        # print(f"[DBG] first 60 body bytes: {body[:60]!r}")

        # --- 4) Minimal route: only POST /test.txt for now
        if method == "POST":
            if path == "/test.txt":
                file_path = os.path.join(os.getcwd(), "test.txt")
                try:
                    with open(file_path, "ab") as f:
                        f.write(body)
                    with open(file_path, "rb") as f:
                        data = f.read()
                    print(f"[OK ] wrote {len(body)} bytes to {file_path}; file now {len(data)} bytes")
                    return self._send(200, data, "text/plain")
                except Exception as e:
                    print("[ERR] writing file:", e)
                    return self._send(500, b"Internal Server Error", "text/plain")
            
        if method == 'GET':
            if path == '/index.html' or path == '/':
                with open('index.html', 'rb') as f: data= f.read()
                return self._send(200, data, 'text/html')
            if path == 'server.py' or path == '/server.py':
                status = 403
                msg = f"ERROR {status} - Forbidden resource - Forbidden to perform method: {method} on path: {path}\r\n"
            if path == "../":

                
            else:
                status = 404
                msg = msg = f"ERROR {status} - Not able to perform method: {method} on path: {path}\r\n"

        # --- 5) Fallback (still fixed response for other paths)
        return self._send(status, msg, 'text/plain')


    def _send(self, status, body, content_type):
        reasons = {200: "OK", 201: "Created", 400: "Bad Request", 403: "Forbidden", 404: "Not Found"}
        reason = reasons.get(status, "OK")
        if not isinstance(body, (bytes, bytearray)):
            body = str(body).encode("utf-8")
        head = (
            f"HTTP/1.1 {status} {reason}\r\n"
            f"Content-Type: {content_type}\r\n"
            f"Content-Length: {len(body)}\r\n"
            "\r\n"
        ).encode("iso-8859-1")
        self.wfile.write(head + body)



    def setup(self):
        super().setup()

    def finish(self):
        super().finish()




if __name__ == "__main__":
    HOST, PORT = "localhost", 8080
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        print("Serving at: http://{}:{}".format(HOST, PORT))
        server.serve_forever()
