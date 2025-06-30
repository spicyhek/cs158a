from socket import *
import threading

hostname = 'localhost'
port = 12000

clients = [] # list of connected clients 
lock = threading.Lock() # manage access to the clients list

def connect_client(client_conn, addr): 
    with lock: # append incoming client to list of clients, allowing only one thread to modify at a timne
        clients.append(client_conn) 
    print(f"Client {addr} connected.")

    while True:
        data = client_conn.recv(1024) # receive data from client
        msg = data.decode() 

        if msg == 'exit': # disconnect if client sends exit
            print(f"Client {addr} disconnected.")
            with lock: # remove client from the list, allowing only one thread to modify at a time
                clients.remove(client_conn)
            client_conn.close()
            break
        else:
            for other_client in clients: # send message to all other clients
                if other_client != client_conn: # do not send message back to sender
                    other_client.send(f"{addr[1]}: {msg}".encode())

def main (): 
    serverSocket = socket(AF_INET, SOCK_STREAM) # create TCP socket
    serverSocket.bind((hostname, port)) # bind socket to hostname and port
    serverSocket.listen() # listen for incoming connections
    print(f"Server listening on {hostname}:{port}") 

    while True:
        client_conn, addr = serverSocket.accept() # accept incoming connection
        client_thread = threading.Thread(target=connect_client, args=(client_conn, addr)) # create new thread for new client
        client_thread.start()

if __name__ == "__main__": 
    main() 

       
