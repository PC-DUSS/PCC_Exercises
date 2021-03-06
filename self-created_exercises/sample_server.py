"""
Pierre-Charles Dussault
May 3, 2021

Exploring HTTP
Also creating a file server.
Created along while reading 'Web Application from Scratch', at www.defn.io
"""
import mimetypes
import os
import socket

from sample_server_request import Request


HOST = '127.0.0.1'
PORT = 9000
SERVER_ROOT = os.path.abspath("www")

# Write a response to the user connecting to this socket.
FILE_RESPONSE_TEMPLATE = """\
HTTP/1.1 200 OK
Content-type: {content_type}
Content-length: {content_length}

""".replace("\n", "\r\n")

NOT_FOUND_RESPONSE = b"""\
HTTP/1.1 404 Not Found
Content-type: text/plain
Content-length: 9

Not Found
""".replace(b"\n", b"\r\n")

BAD_REQUEST_RESPONSE = b"""\
HTTP/1.1 400 Bad Request
Content-type: text/plain
Content-length: 11

Bad Request
""".replace(b"\n", b"\r\n")

METHOD_NOT_ALLOWED_RESPONSE = b"""\
HTTP/1.1 405 Method Not Allowed
Content-type: text/plain
Content-length: 18

Method Not Allowed
""".replace(b"\n", b"\r\n")


def serve_file(sock: socket.socket, path: str) -> None:
    """Given a socket, and the relative path to a file (relative to
    SERVER_SOCK), send that file to the socket if it exists. If the file does
    not exist, send a '404 Not Found' response."""
    if path == "/":
        path = "/index.html"

    # This seems a little overkill, but okay.
    abspath = os.path.normpath(os.path.join(SERVER_ROOT, path.lstrip("/")))
    if not abspath.startswith(SERVER_ROOT):
        sock.sendall(NOT_FOUND_RESPONSE)
        return None

    try:
        with open(abspath, 'rb') as f_obj:
            stat = os.fstat(f_obj.fileno())
            content_type, encoding = mimetypes.guess_type(abspath)
            if content_type is None:
                content_type = "application/octet-stream"

            if encoding is not None:
                content_type += f"; charset={encoding}"

            response_headers = FILE_RESPONSE_TEMPLATE.format(
                content_type=content_type,
                content_length=stat.st_size
            ).encode('ascii')

            sock.sendall(response_headers)
            sock.sendfile(f_obj)
    except FileNotFoundError:
        sock.sendall(NOT_FOUND_RESPONSE)
        return None


def main():
    # By default socket.socket() creates TCP sockets.
    # (Transmission Control Protocol)
    with socket.socket() as server_sock:
        # This tells the kernel to reuse sockets that are in 'TIME_WAIT' state.
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind((HOST, PORT))
        # This server is going to process 1 connection at a time, we want to
        # refuse any additional connections.
        server_sock.listen(0)
        print(f"Listening on {HOST}:{PORT}...")

        # Now we need to make our socket accept a client on that connection.
        while True:
            client_sock, client_addr = server_sock.accept()
            print(f"New connection from {client_addr}")
            with client_sock:
                try:
                    request = Request.from_socket(client_sock)
                    if "100-continue" in request.headers.get('expect', ''):
                        client_sock.sendall(b"HTTP/1.1 100 Continue\r\n\r\n")

                    try:
                        content_length = int(request.headers.get(
                            "content-length", '0'))
                    except ValueError:
                        content_length = 0

                    if content_length:
                        body = request.body.read(content_length)
                        print("Request body", body)

                    if request.method != 'GET':
                        client_sock.sendall(METHOD_NOT_ALLOWED_RESPONSE)
                        continue

                    serve_file(client_sock, request.path)
                except Exception as e:
                    print(f"Failed to parse request: {e}")
                    client_sock.sendall(BAD_REQUEST_RESPONSE)


if __name__ == "__main__":
    main()
