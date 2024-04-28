import socket

server_ip = "127.0.0.1"
server_port = 4221

def main():
    server_socket = socket.create_server((server_ip, server_port))
    client_socket, client_address = server_socket.accept()
    print(f"client_socket: {client_socket}")
    print(f"Accepted connection from {client_address[0]}:{client_address[1]}")




if __name__ == "__main__":
    main()
