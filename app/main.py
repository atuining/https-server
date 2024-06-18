import socket
from threading import Thread
import sys


def extract(data:bytes)->str:
    decoded_data = data.decode().split('\r\n')[0].split(' ')[1]

    if decoded_data == "/":
        return "/"
    elif "/echo/" in decoded_data:
        return decoded_data.split('/')[2]
    elif decoded_data == "/user-agent":
        return data.decode().split('\r\n')[2].split(' ')[1]
    elif decoded_data.startswith("/files"):
        return decoded_data
    else:
        return ""


def response(str:str)->bytes:
    response = ""
    response += "HTTP/1.1"
    Content_Type = "text/plain"
    if str == "":
        response += " 404 Not Found\r\n\r\n"
    else:
        response += " 200 OK\r\n"
        if str == "/":
            response += "\r\n"
        elif str.startswith("/files"):
            directory = sys.argv[2]
            filename = str[7:]
            Content_Type = "application/octet-stream"
            Content_Length = 0
            try:
                with open(f"/{directory}/{filename}", "r") as f:
                    body = f.read()
                    Content_Length = len(body)
            except Exception as e:
                response = "HTTP/1.1 404 Not Found\r\n\r\n"
            else:
                response += f"Content-Type: {Content_Type}\r\nContent-Length: {Content_Length}\r\n\r\n{body}"
        else:
            response += f"Content-Type: {Content_Type}\r\nContent-Length: {len(str)}\r\n\r\n{str}"
    return response.encode()


def handle_client(conn:socket):
    try:
        data = conn.recv(1024)
        str = extract(data)
        conn.send(response(str))
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
