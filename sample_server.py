"""
Pierre-Charles Dussault
May 3, 2021

Exploring HTTP
Also creating a file server.
"""
import mimetypes
import os
import socket
import typing

HOST = '127.0.0.1'  # in 'string' format
PORT = 9000  # in 'int' format

SERVER_ROOT = os.path.abspath("www")

# Write a response to the user connecting to this socket.
RESPONSE = b"""\
HTTP/1.1 200 OK
Content-type: text/html
Content-legnth: 15

<h1>Hello!</h1>""".replace(b"\n", b"\r\n")

FILE_RESPONSE_TEMPLATE = """\
HTTP/1.1 200 OK
Content-type: {content_type}
Content-length: {content_length}

""".replace("\n", "\r\n")

NOT_FOUND_RESPONSE = """\
HTTP/1.1 404 Not Found
Content-type: text/plain
Content-length: 9

Not Found""".replace(b"\n", b"\r\n")

BAD_REQUEST_RESPONSE = b"""\
HTTP/1.1 400 Bad Request
Content-type: text/plain
Content-length: 11

Bad Request""".replace(b"\n", b"\r\n")

METHOD_NOT_ALLOWED_RESPONSE = """\
HTTP/1.1 405 Method Not Allowed
Content-type: text/plain
Content-length: 18

Method Not Allowed""".replace(b"\n", b"\r\n")


class Request(typing.NamedTuple):
    method: str
    path: str
    headers: typing.Mapping[str, str]

    @classmethod
    def from_socket(cls, sock: socket.socket) -> "Request":
        """Read and parse the request from a socket object.

        Raises:
            ValueError: When the request cannot be parsed."""
        lines = iter_lines(sock)
        try:
            # Load in the first line of the request.
            request_line = next(lines).decode('ascii')
        except StopIteration:
            raise ValueError("Request line missing.")

        try:
            # This line contains 3 pieces. Save each piece by splitting the
            # string by space-seperated chunks. Save the method name and path.
            # Discard the HTTP/version (assign it to throwaway variable).
            method, path, _ = request_line.split(" ")
        except ValueError:
            raise ValueError(f"Malformed request line {request_line!r}.")

        headers = {}
        # Now parse the rest of the request...
        for line in lines:
            try:
                # Split each line by 'header', ':', ' value'. ':' is discarded.
                name, _, value = line.decode('ascii').partition(':')
                # Save the name of each line-header item with its value.
                # Strip the leftmost character in ' value', which is a space.
                headers[name.lower()] = value.lstrip()
            except ValueError:
                raise ValueError(f"Malformed header line {line!r}.")

        return cls(method=method.upper(), path=path, headers=headers)


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


def iter_lines(sock: socket.socket, bufsize: int = 16_384) \
        -> typing.Generator[bytes, None, bytes]:
    """Given a socket, read all the individual CRLF-seperated lines and yield
    each one until an empty one is found. Returns the remainder after the
    empty line."""
    buff = b""
    while True:
        data = sock.recv(bufsize)
        if not data:
            return b""

        buff += data
        while True:
            try:
                # Place 'i' at the first occurence of CRLF. Tells the program
                # on which line to start the iteration.
                i = buff.index(b"\r\n")
                # Save the current line until it reaches the next CRLF, then
                # prepare a new buffer starting 2 characters further (starting
                # just past the 2 CRLF characters '\r\n'). This means the
                # buffer will shrink on each iteration.
                line, buff = buff[:i], buff[i+2:]
                if not line:
                    # If the end is reached, return the extra data remaining.
                    return buff
                # Otherwise, yield the current line.
                yield line
            except IndexError:
                # If you have gone past the limits of all the data, stop
                # iterating.
                break


def main():
    # By default socket.socket() creates TCP sockets.
    # (Transmission Control Protocol)
    with socket.socket() as server_sock:
        # This tells the kernel to reuse sockets that are in 'TIME_WAIT' state.
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # This tells the server what address to bind to.
        server_sock.bind((HOST, PORT))

        # Takes in as a parameter the number of allowed pending connections,
        # before connections start being refused. Here with 0 we want to refuse
        # all pending connections. This server is going to process 1 connection
        # at a time, we want to refuse any additional connections.
        server_sock.listen(0)
        print(f"Listening on {HOST}:{PORT}...")

        # Now we need to make our socket accept a client on that connection.
        while True:
            client_sock, client_addr = server_sock.accept()
            print(f"New connection from {client_addr}")
            with client_sock:
                try:
                    request = Request.from_socket(client_sock)
                    if request.method != 'GET':
                        client_sock.sendall(METHOD_NOT_ALLOWED_RESPONSE)
                        continue

                    serve_file(client_sock, request.path)
                except Exception as e:
                    print(f"Failed to parse request: {e}")
                    client_sock.sendall(BAD_REQUEST_RESPONSE)


if __name__ == "__main__":
    main()
