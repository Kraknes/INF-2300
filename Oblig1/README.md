
# INF-2300 ASSIGNMENT 1 HTTP server and RESTful API

These codes were given and created in the first assingment if the course INF-2300.

These files depicts a python server based that handles HTTP CRUD operations from clients on some files with RESTful behaviour. 

These files include such as:
- test.txt
- index.html
- server.py
- messages.json

Server.py file was written by Ering Heimstad Willassen.

Use as you wish, but with care since it does not come with any safety features and will not promise a functional server. 

## Requirements

- Python
- Standard library only (socketserver, json, os, ast)
## Deployment

To deploy the server run the following in the directory of the server.py file:

```bash
  python3 server.py
```

or in some cases:

```bash
  python server.py
```

When done, the server is running on a localhost with port 8080.

This can be changed in the main() function of the server.py if wished. 



## API Reference

#### GET request

Quick list of operations and paths to certain elements on the server.


| Operation | path     | Description                |
| :-------- | :------- | :------------------------- |
| `GET` | `/ or /index.html` | Will yield the .html file |
| `GET` | `/messages or /messages.json` | Return all messages as JSON |
| `POST` | `/test.txt` | Appends to new line in file |
| `POST` | `/messages or /messages.json` | Appends a new message to file  |
| `PUT` | `/messages or /messages.json` | Alters the text of an existing message  |
| `DELETE` | `/messages or /messages.json` | Deletes the text of an existing message  |


## Curl examples

In this section some examples of curl commands to retrieve the information from CRUD operation will be shown. 

To retrieve `index.html` with headers:
``` bash
  curl -i http://localhost:8080 
```

To read messages from `messages.json`
```bash
curl -i http://localhost:8080/messages
```

To append to `test.txt`
```bash
curl -X POST --data 'hello world' http://localhost:8080/test.txt
```

Creating a message to append `messages.json`
```bash
curl -X POST -d '{"text": "insert text her"}' http://localhost:8080/messages
```

To update a message with new text in `messages.json`
```bash
curl -X PUT -d '{"id":1, "text":"updated text"}' http://localhost:8080/messages
```
As one can see, the id number must be known to change state of message.

To delete a message in `messages.json`
```bash
curl -X PUT -d '{"id":1}' http://localhost:8080/messages
```
As one can see, the id number must be known to change state of message.
## Feedback/Support

If you have any feedback or support, please reach out to us at ewi012@uit.no.

## Date
02.09.2025

