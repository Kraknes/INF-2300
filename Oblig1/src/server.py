#!/usr/bin/env python3
import socketserver
import os
import json
import ast
import sys


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
        This method is responsible for handling an htt"p-request. You can, and should(!),
        make additional methods to organize the flow with which a request is handled by
        this method. But it all starts here!
        """

# TO DO: 
# 1. Lag en mer universal send() der data ikke trengs å enkode + \r\n i hver funksjon
# 1.1. Fiks odd-cases hvis .html, .txt eller .json fil ikke eksistere i databasen, eller har ingen info
# 1.2. Lag en Dict av responses og status
# 2. Fiks if statements for URIreq til å være mer spesific Urireq == xxx
# 3. Fiks kommentara
# 4. Generell opprydning



        # Splitting REQUEST string to get REQUEST information
        req_data =  self.rfile.read1()
        try:
            reclist = req_data.decode().rsplit("\r\n")
            method, URIreq, version = reclist[0].rsplit(" ")
            version = version.encode()
            print((method + " to" + URIreq + " REQUEST from client: " + str(self.client_address) +"\n"))
        
        except Exception: # If problems with dissecting request
            status = 403
            print(f"Problem with:\n{e}")
            self.send(b'HTTP/1.1 ', None, None, status)
            return
        
        try:
            json_path = os.path.join(os.getcwd(), "messages.json")
            if not os.path.exists(json_path):
                with open(json_path, 'w') as json_file:
                    data = []
                    json.dump(data, json_file, indent=4)
            with open(json_path, 'r') as json_file:
                msg_list = json.load(json_file)
        except Exception as e: 
            status = 500
            data = b'Cannot open file for reading, contact system administrator for help\r\n'
            self.send(version, data, None, status)
            print(f"Problem with {method} to {URIreq}:\n{e}")
            return

        # GET REQUEST
        if method == "GET":
            if URIreq == "/" or URIreq == "/index.html":
                try:
                    html_file = os.path.join(os.getcwd(), "index.html")
                    html_file = open(html_file, "rb")
                except Exception as e:
                    status = 500
                    data = b'Cannot open file for reading, contact system administrator for help\r\n'
                    self.send(version, data, None, status)
                    print(f"Problem with {method} to {URIreq}:\n{e}")
                    return
                data = html_file.read()
                html_file.close()
                ctype = b'text/html'
                status = 200
                self.send(version, data, ctype, status)
                print(f"{method} request to {URIreq} - OK\n")

            elif URIreq == '/messages' or URIreq == '/messages.json':
                json_file = open('messages.json', 'r')
                msg_list = json.load(json_file)
                string = json.dumps(msg_list, indent=4)
                data = str(string + "\n").encode()
                ctype = b'text/json'
                status = 200
                self.send(version, data, ctype, status)
                print(f"{method} request to {URIreq} - OK\n")

            elif 'server' in URIreq or 'README' in URIreq:
                status = 403
                self.send(version, None, None, status)
                
            else:
                status = 404
                self.send(version, None, None, status)

        # POST REQUEST
        elif method == 'POST':
            if URIreq == '/test.txt' or URIreq == 'test.txt':   
                body = (reclist[len(reclist)-1] + " \r\n").encode()
                text_path = os.path.join(os.getcwd(), "test.txt")
                f = open(text_path, "ab")
                f.write(body)
                f = open(text_path, "rb") 
                data = f.read()
                ctype = b'text/plain'
                status = 200
                self.send(version, data, ctype, status)
                print(f"{method} request to {URIreq} - OK\n")

            elif "messages" in URIreq: 
                body = reclist[len(reclist)-1]
                # In case request body is not to form
                if "{" not in body or "}" not in body or '\"text\"' not in body:
                    status = 404
                    self.send(version, None, None, status)
                    return
                # In case creation or altering the dictionary of body string cause problems
                try: 
                    body_dict = ast.literal_eval(body)
                    with open('messages.json', 'r') as json_file:
                        msg_list = json.load(json_file)
                    body_id = len(msg_list) + 1
                    body_dict.update({'id': body_id})
                except Exception as e:
                    status = 400
                    print(f"Problem with:\n{e}")
                    self.send(version, None, None, status)
                    return
                msg_list.append(body_dict)
                with open(json_path, 'w') as json_file:
                    json.dump(msg_list, json_file, indent=4, sort_keys=True)
                data = (str(json.dumps(body_dict, sort_keys=True, indent=4)) + "\r\n").encode()
                ctype = b'application/json'
                status = 201
                self.send(version, data, ctype, status)
                print(f"{method} request to {URIreq} - OK\n")    

            elif "server" in URIreq or "README" in URIreq:   
                status = 403
                self.send(version, None, None, status) 

            else:
                status = 404
                self.send(version, None, None, status)

        # PUT REQUEST
        elif method == "PUT":
            if "messages" in URIreq:
                body = reclist[len(reclist)-1]
                if "{" not in body or "}" not in body or '\"text\"' not in body or "id" not in body:
                    status = 400
                    self.send(version, None, None, status)
                    return
                
                try: # In case of failure 
                    with open(json_path, 'r') as json_file:
                        msg_list = json.load(json_file)
                    body_dict = ast.literal_eval(body)
                except Exception as e:
                    status = 400
                    self.send(version, None, None, status)
                    print(f"Problem with {method} to {URIreq}:\n{e}")
                    return
                found = False
                for x in msg_list:
                    if x['id'] == body_dict['id']:
                        x['text'] = body_dict['text']
                        found = True
                        break
                if found == True:
                    with open('messages.json', 'w') as json_file:
                        json.dump(msg_list, json_file, indent=4, sort_keys=True)
                    status = 200
                    self.send(version, None, None, status)
                    print(f"{method} request to {URIreq} - OK\n")
                else:
                    status = 404
                    self.send(version, None, None, status)
            else: 
                status = 404
                self.send(version, None, None, status)
        
        # DELETE REQUEST
        elif method == 'DELETE':
            if "messages" in URIreq:
                body = reclist[len(reclist)-1]
                if "{" not in body or "}" not in body or '\"id\"' not in body:
                    status = 400
                    self.send(version, None, None, status)
                else:
                    with open(json_path, 'r') as json_file:
                        msg_list = json.load(json_file)
                    try: 
                        body_dict = ast.literal_eval(body)
                    except Exception as e:
                        status = 400
                        self.send(version, None, None, status)
                        print(f"Problem with {method} to {URIreq}:\n{e}")
                        return
                    found = False
                    for x in msg_list:
                        if x['id'] == body_dict['id']:
                            x['text'] = ''
                            found = True
                            break
                    if found == True:
                        with open('messages.json', 'w') as json_file:
                            json.dump(msg_list, json_file, indent=4, sort_keys=True)
                        status = 200
                        self.send(version, None, None, status)
                        print(f"{method} request to {URIreq} - {status} OK\n")
                    else:
                        status = 404
                        self.send(version, None, None, status)
            else: 
                status = 404
                self.send(version, None, None, status)

        else: 
            status = 404
            self.send(version, None, None, status)
                
    def send(self, version, data, ctype, status):
        status_dict = {200: 'OK', 201: 'OK', 400: 'Bad Request', 
                       403: 'Forbidden', 404: 'Not Found', 
                       500: 'Internal Server Error'}
        v_header = version + b" " + str(status).encode() + b" " + status_dict.get(status).encode() + b"\r\n"
        if ctype == None:
            ctype = b''
        if data == None:
            self.wfile.write(v_header)
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
