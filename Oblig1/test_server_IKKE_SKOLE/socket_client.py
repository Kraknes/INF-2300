import socket

def client_program():
    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    try:
        client_socket.connect((host, port))  # connect to the server
    except ConnectionRefusedError:
        print("The connection to the server was refused")
        return

    message = input(" -> ")  # take in the user's message

    while message.lower().strip() != 'bye':
        client_socket.send(message.encode())  # send in the socket and in networking
        data = client_socket.recv(1024).decode()  # receive in the client
        print('Response from the server : ' + data)  # in the client console
        message = input(" -> ")

    client_socket.close()  # close the connection

if __name__ == '__main__':
    client_program()