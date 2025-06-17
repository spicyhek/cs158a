from socket import *

serverName = 'localhost' # IP address 
serverPort = 12000 # Port number

# TCP SOCKET_STREAM
clientSocket = socket(AF_INET, SOCK_STREAM)
# Connect to the server
clientSocket.connect((serverName, serverPort))

sentence = input('Input lowercase sentence: ')

# Send the sentence to the server
clientSocket.send(sentence.encode()) 

# Recieve the modified sentence from the server
modifiedSentence = clientSocket.recv(64) 

# Print the modified message
print('From Server: ', modifiedSentence.decode())

# Close the socket
clientSocket.close()
