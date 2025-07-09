from socket import *
import threading, time, json, uuid

class Message:
    # constructor for message
    def __init__(self, uuid_str, flag):
        self.uuid = uuid_str
        self.flag = flag

    def to_json(self):
        return json.dumps({'uuid': self.uuid, 'flag': self.flag}) + '\n' # newline added as delimiter

    @staticmethod # called before instantiation
    def from_json(s): # deserialize from JSON string to Message object
        data = json.loads(s)
        return Message(data['uuid'], data['flag'])

# start TCP server
def start_server(host, port):
    server = socket(AF_INET, SOCK_STREAM)
    server.bind((host, port))
    server.listen(1)
    conn, host = server.accept()
    return conn

# connect to neighbor TCP server
def connect_neighbor(host, port):
    client = socket(AF_INET, SOCK_STREAM)
    while True: # retry until a neighbor is connected
        try:
            client.connect((host, port))
            return client
        except ConnectionRefusedError:
            time.sleep(1)

# parse config file to get server and neighbor addresses/ports
with open('config.txt') as txt:
    server_host, server_port = txt.readline().strip().split(',')
    neighbor_host, neighbor_port = txt.readline().strip().split(',')
    server_port, neighbor_port = int(server_port), int(neighbor_port)

my_id = uuid.uuid4()
state = 0 # 0 if electing, 1 for leader found
leader_id = None
forwarded = False 

log_file = f"log{server_port % 10}.txt" # for demo, use port % 10 to get log file name
log = open(log_file, 'a', buffering=1) # open for appending w/ newline buffering

def log_send(msg): # log sent messages from my process
    log.write(f"Sent: uuid={msg.uuid}, flag={msg.flag}\n")

def log_receive(msg, comparison): # log received messages from neighbor
    extra = f", leader={leader_id}" if state == 1 else ''
    log.write(f"Received: uuid={msg.uuid}, flag={msg.flag}, {comparison}, state={state}{extra}\n")

ready = threading.Event() # to synchronize server and client connections before starting election
server_conn = None
neighbor_conn = None

def mark_ready():
    if server_conn and neighbor_conn:
        ready.set()

# start server and mark ready for connections
def server(host, port): 
    global server_conn
    server_conn = start_server(host, port)
    mark_ready()

# start server in a thread
threading.Thread(target=server, args=(server_host, server_port)).start()

# connect to neighbor and mark ready for connections
def connect(host, port): 
    global neighbor_conn
    neighbor_conn = connect_neighbor(host, port)
    mark_ready()

# connect to neighbor in a thread
threading.Thread(target=connect, args=(neighbor_host, neighbor_port)).start()

# wait for server and neighbor to be ready
ready.wait()

# send initial message to neighbor
def send(msg):
    neighbor_conn.sendall(msg.to_json().encode())
    log_send(msg)

send(Message(str(my_id), 0))

# election logic
buffer = ''
while True:
    data = server_conn.recv(4096).decode()
    buffer += data
    while '\n' in buffer: # delimit messages by newline
        line, buffer = buffer.split('\n', 1)
        msg = Message.from_json(line)
        sender_id = uuid.UUID(msg.uuid)
        
        if sender_id > my_id:
            comparison = 'greater'
        elif sender_id < my_id:
            comparison = 'less'
        else:
            comparison = 'same'
        log_receive(msg, comparison)

        if msg.flag == 0 and state == 0:
            if comparison == 'greater':
                send(msg) # forward message to neighbor if it is greater
            elif comparison == 'same':
                # declare myself as leader if i receive my own uuid and announce it
                state = 1
                leader_id = my_id 
                send(Message(str(my_id), 1))
        elif msg.flag == 1:
            # if i receive a leader announcement and im not the leader, set sender as leader
            if state == 0:
                state = 1; 
                leader_id = sender_id 
                send(msg); forwarded = True # forward the leader message
            elif not forwarded and sender_id == leader_id: # if i receive a message with flag 1 from the leader, forward it
                send(msg); forwarded = True

    if state == 1 and forwarded:
        break

print(f"leader is {leader_id}")
log.close()
server_conn.close()
neighbor_conn.close()
