#!/usr/bin/env python3
import socketserver
import os
import json
import ast


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


        req_data =  self.rfile.read1()
        reclist = req_data.decode().rsplit("\r\n")
        method, URIreq, version = reclist[0].rsplit(" ")

        version = version.encode()
        if method == "GET":
            if URIreq == "/" or URIreq == "/index.html":
                html_file = os.path.join(os.getcwd(), "index.html")
                html_file = open(html_file, "rb")
                data = html_file.read()
                ctype = b'text/html'
                status = b'200'
                response = b'OK'
                self.send(version, data, ctype, status, response)
            elif "server.py" in URIreq or "README.md" in URIreq:
                status = b'403'
                response = b'Forbidden'
                self.send(version, None, None, status, response)
            elif "messages" in URIreq:
                json_file = open('messages.json', 'r')
                msg_list = json.load(json_file)
                string = json.dumps(msg_list, indent=4)
                b_string = str(string + "\n").encode()
                ctype = b'text/json'
                status = b'200'
                response = b'OK'
                self.send(version, b_string, ctype, status, response)
                
            else:
                status = b'404'
                response = b'Not Found'
                self.send(version, None, None, status, response)

        # POST request
        elif method == 'POST':

            # POST request to "test.txt"
            if "test.txt" in URIreq:
                body = (reclist[len(reclist)-1] + " \r\n").encode()
                text_path = os.path.join(os.getcwd(), "test.txt")
                f = open(text_path, "ab")
                f.write(body)
                f = open(text_path, "rb") 
                body = f.read()
                ctype = b'text/plain'
                status = b'200'
                response = b'OK'
                self.send(version, body, ctype, status, response)

            # POST request to FORBIDDEN files
            elif "server.py" in URIreq or "README.md" in URIreq:
                status = b'403'
                response = b'Forbidden'
                self.send(version, None, None, status, response)

            # POST request to 'messages.json'
            elif "messages" in URIreq: 
                body = (reclist[len(reclist)-1])
                if "{" not in body and "}" not in body and "text" not in body:
                    self.send(version, None, None, '404', 'Not correct .json format') 

                # Preparing POST .json request
                body_dict = ast.literal_eval(body)
                
                # If file not exist - Make and write to new file
                if not os.path.exists('messages.json'):
                    body_dict.update({'id': 1})
                    with open('messages.json', 'w') as json_file:
                        json.dump([body_dict], json_file, indent=4, sort_keys=True)
                
                # Else, open existing file, list append and write to existing file
                else:
                    with open('messages.json', 'r') as json_file:
                        msg_list = json.load(json_file)
                    body_id = len(msg_list) + 1
                    body_dict.update({'id': body_id})
                    msg_list.append(body_dict)

                    with open('messages.json', 'w') as json_file:
                        json.dump(msg_list, json_file, indent=4, sort_keys=True)
                
                # Header respons for accomplished POST request
                status = b'201'
                response = b'OK'
                ctype = b'text/json'
                unsort_data = msg_list[len(msg_list)-1]
                sort_data = dict(sorted(unsort_data.items()))
                data = (str(sort_data) + '\r\n').encode()
                self.send(version, data, ctype, status, response)                
            else:
                status = b'404'
                response = b'Not Found'
                self.send(version, None, None, status, response)
        else:
            status = b'400'
            response = b'Bad Request'
            self.send(version, None, None, status, response)
                
    def send(self, version, data, ctype, status, response):
        v_header = version + b" " + status + b" " + response + b"\r\n"
        if data == None:
            self.wfile.write(v_header)
        if ctype == None:
            ctype = b''
        else:
            ctype_header = b"Content-Type: " + ctype + b"\r\n"
            clen_header = b"Content-Length: " + str(len(data)).encode() + b"\r\n\r\n"
            response_header = v_header + ctype_header + clen_header
            self.wfile.write(response_header + data)



if __name__ == "__main__":
    HOST, PORT = "localhost", 8080
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        print("Serving at: http://{}:{}".format(HOST, PORT))
        server.serve_forever()
