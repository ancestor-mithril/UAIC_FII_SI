# https://docs.python.org/3/library/socketserver.html#socketserver-tcpserver-example


from time import sleep
import socket
import sys
import socketserver
import threading
from functions import send_message_request, decrypt_message, encrypt_message
from init import get_host_and_port, get_initialization_vector


class MyUDPHandler(socketserver.BaseRequestHandler):
    """
    This class works similar to the TCP handler class, except that
    self.request consists of a pair of data and client socket, and since
    there is no connection the client address must be given explicitly
    when sending data back via sendto().
    """

    def handle(self):
        def kill_server(server):
            server.shutdown()

        data = self.request[0].strip()
        socket = self.request[1]
        print("[B ]: wrote:", data.decode('utf-8'), '\n')
        if data == b'send now':
            socket.sendto(b"sending now", self.client_address)
            close_server_thread = threading.Thread(target=kill_server, args=(self.server, ))
            close_server_thread.start()
        else:
            socket.sendto(b'awaiting for B confirmation', self.client_address)


class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    pass


def init(node_name: str) -> ((str, int), str, str, str):
    """

    :param node_name:
    :return: (host, port) of current node, text to be sent, 3rd key from encryption and initialization vector for OFB
    """
    if len(sys.argv) < 3:
        print("Example of running")
        print("python client_a.py [OPERATION MODE] [FILE TO BE SENT]")
        print("[OPERATION MODE] must be ECB or OFB")
        print("[FILE TO BE SENT] must be file with text to be encrypted")
        exit()
    if sys.argv[1] != "ECB" and sys.argv[1] != "OFB":
        raise SystemError("Operation Mode is not ECB or OFB")

    with open(sys.argv[2], "r") as fd:
        text = fd.read()

    with open("key_3.txt", "r") as fd:
        key_3 = fd.read()

    return get_host_and_port(node_name), text, key_3, get_initialization_vector()


def prepare_communication() -> str:
    """
    sends message request to B, then requests key from KM and returns it after decryption

    :return: decrypted key received from KM
    """
    decrypted_key = None

    print("[A ]: Node A started!")
    print("[A ]: Operation Mode: ", sys.argv[1], '\n')

    print("[A ]: Sending operation mode to B. Answer received:")
    print("[B ]:", send_message_request("B", sys.argv[1]), '\n')

    print("[A ]: Requesting key from KM. Answer received:")
    encrypted_key = send_message_request("KM", sys.argv[1])
    print("[KM]: Encrypted: ", encrypted_key, '\n')
    decrypted_key = decrypt_message(encrypted_key, key_3, operation_mode="ECB")
    print("[KM]: Decrypted: ", decrypted_key, '\n')

    return decrypted_key


def wait_for_second_node_preparation(host: str, port: int):
    """
    starting UDP server until Node B sends confirmation for starting communication

    :param host:
    :param port:
    :return:
    """
    server = ThreadedUDPServer((host, port), MyUDPHandler)

    with server:
        ip, port = server.server_address
        print("[A ]: Node A started listening for Node B confirmation", '\n')
        server.serve_forever()


def start_communication(text: str, decrypted_key: str, iv: str):
    print("[A ]: Node A sends ", text, " to Node B")
    encrypted_message = encrypt_message(text, decrypted_key, operation_mode=sys.argv[1], iv=iv)
    print("[A ]: Encrypted message: ", encrypted_message, '\n')
    print("[B ]: ", send_message_request("B", encrypted_message), '\n')


if __name__ == "__main__":
    # python client_a.py ECB text.txt

    (HOST, PORT), text, key_3, iv = init("A")

    decrypted_key = prepare_communication()

    wait_for_second_node_preparation(HOST, PORT)

    start_communication(text, decrypted_key, iv)



