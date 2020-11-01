from Crypto.Cipher import AES
import base64
import os

BLOCK_SIZE = 32

PADDING_CHAR = " "


def pad(s: str) -> str:
    """

    :param s: string to be padded
    :return: padded string
    """
    global BLOCK_SIZE
    global PADDING_CHAR
    return s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING_CHAR


def get_encoded_string(cipher, string: str) -> bytes:
    """

    :param cipher:
    :param string:
    :return: encoded padded string using cipher
    """
    return base64.b64encode(cipher.encrypt(pad(string).encode()))


def get_decoded_string(cipher, string: bytes) -> str:
    """

    :param cipher:
    :param string: encrypted string
    :return: decrypted and unpadded string using cipher
    """
    return cipher.decrypt(base64.b64decode(string)).decode('utf-8').rstrip(PADDING_CHAR)


secret_key = os.urandom(BLOCK_SIZE)
secret_key = "cheiau2udeu16lgi"
print(secret_key)
print(type(secret_key))


a = b'LkZDybReN8OCMLz88Q8UXRS9AostHBWQop97STkeRuTW'

cipher = AES.new(secret_key)
initialization_vector = "\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x01\x02\x03\x04" \
                        "\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x0e\x0f"
print(len(initialization_vector))
encoded = get_encoded_string(cipher, 'dadadadadadadada')
print(encoded)

decoded = get_decoded_string(cipher, encoded)
print(decoded)
