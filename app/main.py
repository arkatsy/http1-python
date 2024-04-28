import socket
import logging
import sys

server_ip = "127.0.0.1"
server_port = 4221

logger = logging.getLogger(__name__)

def main():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    server_socket = socket.create_server((server_ip, server_port))
    conn, addr = server_socket.accept()
    data = conn.recv(1024).decode()

    if data:
        req_info = parse_request(data)
        path = req_info.get("path")
        basepath, *rest = parse_path(path)
        logger.info(f"basepath: {basepath}")
        # print(f"basepath: {basepath}, rest: {rest}")
        response = None
        match basepath:
            case "": # "/"
                logger.info("matched path '/'")
                response = create_response()
            case "echo":
                logger.info("matched path '/echo/:rest'")
                echoed = "".join(rest)
                response = create_response({"headers": {"Content-Type": "text/plain"}, "data": echoed})
            case _:
                logger.info("matched catch-all route")
                response = create_response({"status_code": 404, "status": "Not Found"})

    conn.send(response)

def create_response(opts = {}):
    # Default response: HTTP/1.1 200 OK
    # Content-Length header is added automatically
    protocol = "HTTP/1.1"
    status_code = opts.get("status_code", 200)
    status = opts.get("status", "OK")
    headers = opts.get("headers", {})
    data = opts.get("data", "")
    if data:
        headers["Content-Length"] = len(bytes(data, "utf-8"))
    stringified_headers = stringify_headers(headers) if headers else "\r\n"

    response = f"{protocol} {status_code} {status}\r\n{stringified_headers}\r\n{data}"

    logger.info(f"crafted response: \n{response}")
    
    return bytes(response, "utf-8")

def parse_request(data):
    lines = data.split("\r\n")
    method, path, protocol = lines[0].split(" ")
    host, port = lines[1].split(":", 1)
    return {
        "method": method,
        "path": path,
        "protocol": protocol,
        "host": host,
        "port": port
    }

def stringify_headers(headers = {}):
    stringified_headers = ""
    for key in headers:
        stringified_headers += f"{key}: {headers[key]}\r\n"
    return stringified_headers
        

def parse_path(path):
    return path.split("/")[1:]


if __name__ == "__main__":
    main()
