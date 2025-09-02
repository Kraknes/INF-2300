from socket import *

serverName = ''
serverPort = 12000 # hvordan vet man serverPort til en ukjent server?
clientSocket = socket(AF_INET, SOCK_STREAM) #SOCK_Stream er TCP, sOCK_DGRAM er UDP
clientSocket.connect((serverName,serverPort))
sentence = input('Input lowercase sentence:')
clientSocket.send(sentence.encode())
modifiedSentence = clientSocket.recv(1024)
print('From Server: ', modifiedSentence.decode())
clientSocket.close()