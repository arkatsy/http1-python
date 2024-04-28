import socket

server_ip = "127.0.0.1"
server_port = 4221

def main():
    server_socket = socket.create_server((server_ip, server_port))
    conn, addr = server_socket.accept()
    data = conn.recv(1024).decode()

    if data:
        req_info = parse_request(data)
        path = req_info.get("path")
        response = None
        match path:
            case "/":
                response = create_response()
            case _:
                response = create_response({"status_code": 404, "status": "Not Found"})

    conn.send(response)

def create_response(opts = {}):
    protocol = "HTTP/1.1"
    status_code = opts.get("status_code", 200)
    status = opts.get("status", "OK")

    return bytes(f"{protocol} {status_code} {status}\r\n\r\n", "utf-8")

def parse_request(data):
    lines = data.split("\r\n")
    method, path, protocol = lines[0].split(" ")
    host, port = lines[1].split(":", 1)
    # TODO: Parse headers
    return {
        "method": method,
        "path": path,
        "protocol": protocol,
        "host": host,
        "port": port
    }

if __name__ == "__main__":
    main()
