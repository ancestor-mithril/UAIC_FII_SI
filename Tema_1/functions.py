import socket
from init import get_host_and_port
from Crypto.Cipher import AES
import Crypto
import base64


DECRYPT_SIZE = 44
BLOCK_SIZE = 32

PADDING_CHAR = "|"


def pad(s: str) -> str:
    """

    :param s: string to be padded
    :return: padded string
    """
    global BLOCK_SIZE
    global PADDING_CHAR
    if len(s) % BLOCK_SIZE == 0:
        return s
    return s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING_CHAR


def get_encoded_string(cipher, string: str) -> bytes:
    """

    :param cipher:
    :param string:
    :return: encoded padded string using cipher
    """
    # print("String to be encoded:", string)
    # print("String to be encoded:", pad(string))
    # print("String to be encoded:", pad(string).encode())
    # print("String to be encoded:", pad(string).encode())
    # print("String to be encoded:", cipher.encrypt(pad(string).encode()))
    # print("String to be encoded:", base64.b64encode(cipher.encrypt(pad(string).encode())))
    return base64.b64encode(cipher.encrypt(pad(string).encode()))


def get_decoded_string(cipher, string: bytes) -> str:
    """

    :param cipher:
    :param string: encrypted string
    :return: decrypted and unpadded string using cipher
    """
    # print("String to be decoded:", string)
    # print("Result 1:", base64.b64decode(string))
    # print("Result 2:", cipher.decrypt(base64.b64decode(string)))
    # print("Result 3:", cipher.decrypt(base64.b64decode(string)).decode('utf-8'))
    # print("Result 4:", cipher.decrypt(base64.b64decode(string)).decode('utf-8').rstrip(PADDING_CHAR))
    return cipher.decrypt(base64.b64decode(string)).decode('utf-8').rstrip(PADDING_CHAR)


def string_xor(s1: str, s2: str) -> str:
    """

    :param s1: string one
    :param s2: string 2
    :return: xor of the 2 strings
    """
    return ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(s1, s2))


def split_string_into_chunks(input_string: str, chunk_size: int) -> list:
    """

    :param input_string: string to be split
    :param chunk_size: size of each besides the last chunk
    :return: list of split strings
    """
    return [input_string[i: i + chunk_size] for i in range(0, len(input_string), chunk_size)]


def send_message_request(receiver: str, message: str) -> str:
    """

    :param receiver: index of receiver for current message
    :param message: the message to be sent
    :return: str containing answer received from receiver
    """
    host, port = get_host_and_port(receiver)
    data = message
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(bytes(data + "\n", "utf-8"), (host, port))
    received = str(sock.recv(1024), "utf-8")
    return received


def decrypt_message(encrypted_message: str, key: str, operation_mode: str = None, iv: str = None) -> str:
    """

    :param encrypted_message:
    :param key:
    :param operation_mode: If None then encrypted message is treated as block. Else, ECB or OFB. Otherwise, throws error
    :param iv:initialization vector for OFB. If None and OFB, throws error
    :return: decrypted message
    """
    if operation_mode is not None and operation_mode != "ECB" and operation_mode != "OFB":
        raise TypeError("Operation mode must be ECB or OFB")
    key = pad(key)
    cipher = AES.new(key.encode())
    chunks = split_string_into_chunks(encrypted_message, DECRYPT_SIZE)
    print(chunks)
    if operation_mode == "OFB":
        if iv is None:
            raise ValueError("iv must be initialized for OFB")
        decoded_string = ""
        for chunk in chunks:
            iv = get_encoded_string(cipher, iv).decode('utf-8')[0:32]
            # decoded_string += Crypto.Util.strxor.strxor(iv, chunk)
            decoded_string += string_xor(iv, chunk)
    else:
        decoded_string = "".join([get_decoded_string(cipher, chunk.encode()) for chunk in chunks])
    return decoded_string


def encrypt_message(message: str, key: str, operation_mode: str = None, iv: str = None) -> str:
    """

    :param message:
    :param key:
    :param operation_mode: If None then message is encrypted as block. Else, ECB or OFB. Otherwise, throws error
    :param iv: initialization vector for OFB. If None and OFB, throws error
    :return: encrypted message
    """
    if operation_mode is not None and operation_mode != "ECB" and operation_mode != "OFB":
        raise TypeError("Operation mode must be ECB or OFB")
    # TODO: de padat cheia pentru ca in linux cheia de 16 e de 17
    key = pad(key)
    cipher = AES.new(key.encode())
    if operation_mode == "OFB" and iv is None:
        raise ValueError("iv must be initialized for OFB")
    chunks = split_string_into_chunks(message, BLOCK_SIZE)
    print(chunks)
    if operation_mode == "OFB":
        encoded_string = ""
        if iv is None:
            raise ValueError("iv must be initialized for OFB")
        for chunk in chunks:
            iv = get_encoded_string(cipher, iv).decode('utf-8')[0:32]
            # encoded_string += Crypto.Util.strxor.strxor(iv, chunk)
            encoded_string += string_xor(iv, chunk)
    else:
        encoded_string = "".join([get_encoded_string(cipher, chunk).decode('utf-8') for chunk in chunks])
    return encoded_string



