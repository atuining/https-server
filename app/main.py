import socket
from threading import Thread

def extract(data):
    decoded_data = data.decode().split('\r\n')[0].split(' ')[1]

    if decoded_data=="/":
        return "/"
    elif "/echo/" in decoded_data:
        return decoded_data.split('/')[2]
    elif decoded_data=="/user-agent":
        return data.decode().split('\r\n')[2].split(' ')[1]
    else:
        return ""

def response(str):
    response = ""
    response += "HTTP/1.1"
    Content_Type = "text/plain"
    if str == "":
        response += " 404 Not Found\r\n\r\n"
    else:
        response += " 200 OK\r\n"
        if str == "/":
            response += "\r\n"
        else:
            response += f"Content-Type: {Content_Type}\r\nContent-Length: {len(str)}\r\n\r\n{str}"
    return response.encode()        
    
def handle_client(conn):
    try:
        data = conn.recv(1024)
        str = extract(data)
        conn.send(response(str))
    except Exception as e:
        print(f"handle_client error: {e}")
    

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    
    while True:
        conn, addr = server_socket.accept()  # wait for client
        Thread(target=handle_client, args=[conn]).start()
        

    


if __name__ == "__main__":
    main()
