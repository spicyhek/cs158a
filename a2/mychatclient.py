from socket import *
import threading

hostname = 'localhost'
port = 12000

def receive_messages(client_socket): # recieve messages from server
    while True:
        data = client_socket.recv(1024)
        print(data.decode())

def send_message(client_socket): # send messages to server
    while True:
        msg = input()
        try:
            client_socket.send(msg.encode())
        except:
            break
        if msg == 'exit':
            break    

def main():
    client_socket = socket(AF_INET, SOCK_STREAM) # create TCP socket
    client_socket.connect((hostname, port)) # connect to server

    print("Connected to chat server. Type 'exit' to leave.\n")
    # create a thread to receive messages from the server
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,)) 

    # create a thread to send messages to the server
    send_thread = threading.Thread(target=send_message, args=(client_socket,))

    receive_thread.start()
    send_thread.start()

    send_thread.join() # wait for the send thread to finish before closing the socket
    print("Disconnected from server.") 
    client_socket.close()

if __name__ == "__main__":
    main()
