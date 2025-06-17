from socket import *

serverPort = 12000 # Port number

# Create TCP socket
serverSocket = socket(AF_INET, SOCK_STREAM)

# Bind the socket to the port
# The empty string means that the server will listen on all 
# available interfaces
serverSocket.bind(('', serverPort))

# Listen for incoming connections
serverSocket.listen(1)


while True:
    # Accept 
    cnSocket, addr = serverSocket.accept()
    print(f"Connection from {addr}")

    # Receive
    sentence = cnSocket.recv(64).decode()

    msg_len = int(sentence[:2]) # Takes the first 2 characters of the string (the length)
    print("msg_len: " , msg_len)

    # Process
    plainMessage = sentence[2:2 + msg_len] # Takes characters starting from index 2
    processedMessage = plainMessage.upper()

    print("processed: " + processedMessage)

    # Send
    cnSocket.send(processedMessage.encode())
    print("msg_len_sent: " , msg_len)

    # Close
    cnSocket.close()
    print("Connection closed")
    print("...")