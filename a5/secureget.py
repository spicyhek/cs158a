from socket import *
import ssl

HOST = "www.google.com"
PORT = 443 # HTTPS port
REQUEST = (
    "GET / HTTP/1.1\r\n" #HTTP/1.1 since it's more widely supported
    f"Host: {HOST}\r\n"
    "Accept-Encoding: identity\r\n" # avoid compression 
    "Connection: close\r\n"
    "\r\n"
)

def main():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT) # create TLS context
    context.check_hostname = True # verify server hostname

    context.verify_mode = ssl.CERT_REQUIRED #require certificate for security
    context.load_default_certs()

    with socket(AF_INET, SOCK_STREAM) as tcp:
        tcp.connect((HOST, PORT))
        with context.wrap_socket(tcp, server_hostname=HOST) as tls: # wrap socket with TLS
            tls.sendall(REQUEST.encode()) # 
            chunks = [] # receive data in chunks for large responses
            while True:
                data = tls.recv(4096)
                if not data:
                    break
                chunks.append(data)

    raw = b"".join(chunks) # combine all received chunks
    separate = b"\r\n\r\n" # separate header from body in HTTP response

    if separate in raw: # split header and body
        parts = raw.split(separate, 1) 
        body = parts[1]   
    else:
        body = raw 

    with open("response.html", "wb") as f: # write response body to file, wb to write in binary mode
        f.write(body)

if __name__ == "__main__":
    main()
