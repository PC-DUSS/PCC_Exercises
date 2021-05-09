import socket
import io
import typing

from sample_server_headers import Headers


class BodyReader(io.IOBase):
    def __init__(self, sock: socket.socket, *, buff: bytes = b"",
                 bufsize: int = 16_384) -> None:
        self._sock = sock
        self._buff = buff
        self._bufsize = bufsize

    def readable(self) -> bool:
        return True

    def read(self, n: int) -> bytes:
        """Read up to n number of bytes from the request body."""
        while len(self._buff) < n:
            data = self._sock.recv(self._bufsize)
            if not data:
                break

            self._buff += data

        # Save result of reading until n number of bytes.
        result = self._buff[:n]
        # Save remaining contents from recv(self._bufsize) in buffer.
        self._buff = self._buff[n:]

        return result


class Request(typing.NamedTuple):
    method: str
    path: str
    headers: Headers
    body: BodyReader

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

        headers = Headers()
        buff = b""
        # Now parse the rest of the request...
        while True:
            try:
                line = next(lines)
            except StopIteration as e:
                # StopIteration.value contains return value of the generator.
                buff = e.value
                break

            try:
                # Split each line by 'header', ':', ' value'. ':' is discarded.
                header_name, _, value = line.decode('ascii').partition(':')
                # Save the name of each line-header item with its value.
                # Strip the leftmost character in ' value', which is a space.
                headers.add(header_name, value.lstrip())
            except ValueError:
                raise ValueError(f"Malformed header line {line!r}.")

        body = BodyReader(sock=sock, buff=buff)
        return cls(method=method.upper(), path=path, headers=headers,
                   body=body)


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
                    # If an empty string is reached, return remaining data.
                    return buff
                # Otherwise, yield the current line.
                yield line
            except IndexError:
                # If you have gone past the limits of all the data, stop
                # iterating.
                break
