import argparse
import os
import socket
import random
import sys
from threading import Thread


HOSTNAME = 'localhost'


def bind_to_avaliable_port(_socket):
    while True:
        try:
            port = random.randint(5000, 10000)
            _socket.bind((HOSTNAME, port))
        except OSError:
            pass
        else:
            return port


class HTTPHandler():
    """Handles HTTP requests.
    """
    def __init__(self, path):
        self.status_codes = {
            200: "OK",
            400: "Bad Request",
            403: "Forbidden",
            404: "Not Found",
            405: "Method Not Allowed",
            500: "Internal Server Error",
            505: "HTTP Version Not Supported"
        }

        self.content_types = {
            ".html": "text/html",
            ".htm": "text/html",
            ".css": "text/css",
            ".gif": "image/gif",
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".xml": "application/xml",
            ".svg": "image/svg+xml",
            ".txt": "text/plain",
        }

        self.methods = ["GET"]

        self.http_versions = {"HTTP/1.0", "HTTP/1.1"}

        self.path = path

    def is_supported_method(self, method):
        return method in self.methods

    def is_supported_http_version(self, http_version):
        return http_version in self.http_versions

    def generate_header(self, status_code):
        return "HTTP/1.1 {} {}".format(status_code, self.status_codes[status_code])

    def get_content_type(self, extension):
        if extension in self.content_types:
            return self.content_types[extension]
        return "text/plain"

    def generate_response_status_code(self, status_code):
        return (
            self.generate_header(status_code)
            + "\r\nContent-Type: text/html\r\n"
              "\r\n<html><head></head><body><h1>{:} {:}</h1></body></html>\r\n".format(status_code, self.status_codes[status_code])
        ).encode('utf8')

    def generate_header_file(self, file_path):
        print(file_path)
        file_name, extension = os.path.splitext(file_path)
        print(extension)
        content_type = self.get_content_type(extension)
        print(content_type)
        return (
            self.generate_header(200)
            + "\r\nContent-Type: " + content_type + "\r\n\r\n"
        )
        
    def handle(self, request):
        # request should be ended with double "\r\n"
        if request.count("\r\n\r\n") != 1 or request[-4:] != "\r\n\r\n":
            return self.generate_response_status_code(400)

        lines = request[:-4].split("\r\n")
        method, file_path, http_version = lines[0].split()
        file_path = file_path.lstrip('/')

        if not self.is_supported_method(method):
            return self.generate_response_status_code(405)
        if not self.is_supported_http_version(http_version):
            return self.generate_response_status_code(505)
        if not os.path.isfile(os.path.join(self.path, file_path)):
            return self.generate_response_status_code(404)

        with open(self.path + file_path, 'rb') as requested_file:
            content = requested_file.read()

        print(self.generate_header_file(file_path).encode('utf8') + content + '\r\n'.encode('utf8'))
        return self.generate_header_file(file_path).encode('utf8') + content + '\r\n'.encode('utf8')

        
class ClientThread(Thread):
    def __init__(self, socket, path):
        Thread.__init__(self)
        self.socket = socket
        self.handler = HTTPHandler(path)

    def run(self):
        received = self.socket.recv(8192)
        if received == b'':
            return

        received = received.decode('utf8')
        self.socket.send(self.handler.handle(received))
        self.socket.close()


def main():
    parser = argparse.ArgumentParser(description='Simple HTTP server.')
    parser.add_argument(
        '-r', '--root',
        help='Root folder for server.',
        required=True
    )
    parser.add_argument(
        '-p', '--port',
        help='Server port.',
        default=None,
        type=int
    )
    args = parser.parse_args()
    
    root = args.root
    if not os.path.isdir(root) or not os.access(root, os.R_OK):
        raise ValueError('Incorrect or not readable root folder.')

    port = args.port
    server_socket = socket.socket()
    if not port:
        port = bind_to_avaliable_port(server_socket)
    else:
        server_socket.bind((HOSTNAME, port))

    print('Server is listening to port {}.'.format(port))
    server_socket.listen(20)

    while True:
        client_socket, address = server_socket.accept()
        print("Accepted request from {}".format(address))
        thread = ClientThread(client_socket, root)
        thread.start()


if __name__ == '__main__':
    main()
