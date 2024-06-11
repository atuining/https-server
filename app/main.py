import socket


def extract_str(data):
    decoded_data = data.decode().split('\r\n')[0].split(' ')[1].split('/')
    
    if decoded_data[1] == 'echo':
        str = decoded_data[2]
        return str
    else:
        return None

def extract_user_agent(data):
    decoded_data = data.decode().split('\r\n')
    
    if decoded_data[0].split(' ')[1] == "/user-agent":
        ua = decoded_data[2].split(' ')[1]
        return ua
    else:
        return None

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    conn, addr = server_socket.accept() # wait for client
    
    with conn:
        print(f"connection from {addr} established.")
        while True:
            data = conn.recv(4096)
            if not data:
                break
            str = extract_str(data)
            ua = extract_user_agent(data)
            if "GET / " in data.decode('utf-8'):
                conn.send(b"HTTP/1.1 200 OK\r\n\r\n")
            elif str is None and ua is None:
                conn.send(b"HTTP/1.1 404 Not Found\r\n\r\n")
            elif ua is not None:
                format = "text/plain"
                response = f"HTTP/1.1 200 OK\r\nContent-Type: {format}\r\nContent-Length: {len(ua)}\r\n\r\n{ua}"
                conn.send(response.encode())
            else:
                format = "text/plain"
                response = f"HTTP/1.1 200 OK\r\nContent-Type: {format}\r\nContent-Length: {len(str)}\r\n\r\n{str}"
                conn.send(response.encode())
                
       
    
    


if __name__ == "__main__":
    main()
