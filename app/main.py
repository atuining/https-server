import socket
from threading import Thread
import sys


def extract(data:bytes)->bytes:
    if data=="":
        return "HTTP/1.1 400 Not Found\r\n\r\n".encode()
    
    req = data.split('\r\n')
    path = req[0].split(' ')[1]
    type = req[0].split(' ')[0]
    
    
    if type == "GET":
        if path == "/":
            return "HTTP/1.1 200 OK\r\n\r\n".encode()
        elif path.startswith("/echo"):
            str = path.split('/')[2]
            return f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(str)}\r\n\r\n{str}".encode()
        elif path == "/user-agent":
            str = req[2].split(' ')[1]
            return f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(str)}\r\n\r\n{str}".encode()
        elif path.startswith("/files"):
            directory = sys.argv[2]
            filename = path[7:]
            Content_Type = "application/octet-stream"
            Content_Length = 0
            try:
                with open(f"/{directory}/{filename}", "r") as f:
                    body = f.read()
                    Content_Length = len(body)
            except Exception as e:
                return "HTTP/1.1 404 Not Found\r\n\r\n".encode()
            else:
                return f"HTTP/1.1 200 OK\r\nContent-Type: {Content_Type}\r\nContent-Length: {Content_Length}\r\n\r\n{body}".encode()
        else:
            return "HTTP/1.1 404 Not Found\r\n\r\n".encode()
    elif type=="POST":
        if path.startswith("/files"):
            directory = sys.argv[2]
            filename = path[7:]
            Content_Type = req[3].split(' ')[1]
            Content_Length = req[2].split(' ')[1]
            body = req[5]
            try:
                with open(f"/{directory}/{filename}", "w") as f:
                    f.write(body)
            except Exception as e:
                return "HTTP/1.1 500 Internal Server Error\r\n\r\n".encode()
            else:
                return "HTTP/1.1 201 Created\r\n\r\n".encode()



def handle_client(conn:socket):
    try:
        data = conn.recv(1024).decode()
        response = extract(data)
        conn.send(response)
    except Exception as e:
        print(f"handle_client error: {e}")


def main()->None:
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    while True:
        conn, addr = server_socket.accept()  # wait for client
        Thread(target=handle_client, args=[conn]).start()


if __name__ == "__main__":
    main()
