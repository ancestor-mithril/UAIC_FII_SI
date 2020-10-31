#!/usr/bin/env python3
# https://docs.python.org/3/library/socketserver.html#socketserver-tcpserver-example


import socket
import sys
import socketserver
import threading
from functions import send_message_request, decrypt_message
from init import get_host_and_port, get_initialization_vector


operation_mode = None
decrypted_key = None


class MyUDPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        global operation_mode
        global decrypted_key

        def kill_server(server):
            server.shutdown()

        data = self.request[0].strip()
        socket = self.request[1]
        close_server_thread = threading.Thread(target=kill_server, args=(self.server,))

        if operation_mode is None:
            if data == b'ECB' or data == b'OFB':
                operation_mode = data.decode('utf-8')
                print("[A ]: wrote:", operation_mode, '\n')
                socket.sendto(data.upper(), self.client_address)
                close_server_thread.start()
            else:
                socket.sendto(b"Not a valid communication mode", self.client_address)
        else:
            socket.sendto(b"Message received", self.client_address)
            encrypted_message = data.decode('utf-8')
            print("[A ]: wrote:", encrypted_message, '\n')
            decrypted_message = decrypt_message(encrypted_message, decrypted_key, operation_mode=operation_mode, iv=iv)
            print("[B ]: decrypted message:", decrypted_message, '\n')

            close_server_thread.start()


class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    pass


def init(node_name: str):
    """

    :param node_name:
    :return: (host, port) for current port, 3rd key from encryption and initialization vector for OFB
    """
    print("[B ]: Node B started!")

    with open("key_3.txt", "r") as fd:
        key_3 = fd.read()

    return get_host_and_port(node_name), key_3, get_initialization_vector()


def wait_for_communication_request(host: str, port: int):
    """
    waits for communication

    :param host:
    :param port:
    :return:
    """
    with socketserver.UDPServer((host, port), MyUDPHandler) as server:
        server.serve_forever()


def prepare_communication():
    """

    :return:
    """
    global operation_mode

    print("[B ]: Operation Mode: ", operation_mode, '\n')

    print("[B ]: Requesting key from KM. Answer received:")
    encrypted_key = send_message_request("KM", operation_mode)
    print("[KM]: Encrypted: ", encrypted_key, '\n')
    decrypted_key = decrypt_message(encrypted_key, key_3)
    print("[KM]: Decrypted: ", decrypted_key, '\n')

    print("[B ]: Notifying Node A to start transmitting")
    print("[B ]: wrote: ", "send now")
    print("[A ]: wrote: ", send_message_request("A", "send now"), '\n')

    return decrypted_key


if __name__ == "__main__":

    (HOST, PORT), key_3, iv = init("B")

    wait_for_communication_request(HOST, PORT)

    decrypted_key = prepare_communication()

    wait_for_communication_request(HOST, PORT)
