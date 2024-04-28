import socket

server_ip = "127.0.0.1"
server_port = 4221

def main():
    server_socket = socket.create_server((server_ip, server_port))
    conn, addr = server_socket.accept()
    data = conn.recv(1024).decode()

    if data:
        res = create_response()
        conn.send(res)

def create_response(opts = {}):
    protocol = "HTTP/1.1"
    status_code = opts.get("status_code", 200)
    status = opts.get("status", "OK")

    return bytes(f"{protocol} {status_code} {status}\r\n\r\n", "utf-8")

if __name__ == "__main__":
    main()
