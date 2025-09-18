
# INF-2300 ASSIGNMENT 2: TODO list

These codes were given and created in the second assingment if the course INF-2300.

These files include such as:
- index.html
- server.py

## File layout
```bash
server root/
  - server.py
  - templates/
     index.html
```


## Requirements

- Python
- Web client (Firefox, Chrome, Explorer, etc)
- Standard library only (flask, json, os, ast)

### Installation of Flask
#### Create & activate a virtual env (optional)
```bash python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

#### Install deps
```bash
pip install Flask flask-cors
```


#### Run the server
```bash
python3 server.py
```

Server on http://localhost:8080



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
| `GET` | `/ or /index.html` | Will yield the .html file - Return HTML|
| `GET` | `/api/items ` | Return all items - Return JSON|
| `GET` | `/api/items/<id>` | Returns item with the ID - Return JSON|
| `POST` | `/api/items` | Submits a new item to the list - Return JSON |
| `PUT` | `/api/items/<id>` | Alters text of existing item of ID - Return JSON  |
| `DELETE` | `/api/items/<id>` | Delete item in list of ID - return JSON  |






## Curl examples

In this section some examples of curl commands to retrieve the information from CRUD operation will be shown. 

To retrieve `index.html` with headers:
``` bash
  curl -i http://localhost:8080 
```

To get all items from `items`
```bash
curl -i http://localhost:8080/api/items
```

Creating a TODO to append `items`
```bash
curl -X POST -H "Content-Type: application/json" -d '{"text": "insert text her"}' http://localhost:8080/api/items
```

To update an item with new text in `items`
```bash
curl -X PUT -H "Content-Type: application/json" -d '{"text":"updated text"}' http://localhost:8080/api/items/1
```
As one can see, the id number must be known to change state of item.

To delete an item in `items`
```bash
curl -X DELETE http://localhost:8080/api/items/1
```
As one can see, the id number must be known to change state of item.
## Frontend

### Buttons/forms 
- Call functions like submitQuery, submitID, putID, deleteID, getText.

- Each function uses fetch() to hit the endpoints, then updates the table.

- Forms use onsubmit="return ..." and e.preventDefault() to avoid page reloads.

## Feedback/Support

If you have any feedback or support, please reach out to us at ewi012@uit.no.

## Date
18.09.2025

