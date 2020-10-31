#!/usr/bin/env python3
# https://docs.python.org/3/library/socketserver.html#socketserver-tcpserver-example


import socket
import threading
import socketserver

from functions import encrypt_message


class MyUDPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        print("{} wrote:".format(self.client_address[0]))
        data = data.decode('utf-8')
        print(data)
        with open("keys.txt", "r") as fd:
            key_1 = fd.readline()
            key_2 = fd.readline()
        with open("key_3.txt", "r") as fd:
            key_3 = fd.read()
        if data == "ECB":
            encrypted_key = encrypt_message(key_1, key_3)
            text = encrypted_key
        elif data == "OFB":
            encrypted_key = encrypt_message(key_2, key_3)
            text = encrypted_key
        else:
            text = "ERROR, not ECB or OFB"
        socket.sendto(text.encode(encoding="utf-8"), self.client_address)


class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    pass


def client(ip, port, message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((ip, port))
        sock.sendall(bytes(message, 'utf-8'))
        response = str(sock.recv(1024), 'utf-8')
        print("Received: {}".format(response))


if __name__ == "__main__":
    HOST, PORT = "localhost", 9997

    server = ThreadedUDPServer((HOST, PORT), MyUDPHandler)
    with server:
        ip, port = server.server_address

        server_thread = threading.Thread(target=server.serve_forever)

        server_thread.daemon = True
        server_thread.start()

        input("press anything to terminate server\n")
        server.shutdown()
