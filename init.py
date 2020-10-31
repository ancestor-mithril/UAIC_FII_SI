ports = {
    "A": {
        "host": "localhost",
        "port": 9999,
    },
    "B": {
        "host": "localhost",
        "port": 9998,
    },
    "KM": {
        "host": "localhost",
        "port": 9997,
    },
}

initialization_vector = "\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f"


def get_host_and_port(node_name: str) -> (str, int):
    """

    :param node_name:
    :return:
    """
    return ports[node_name]["host"], ports[node_name]["port"]


def get_initialization_vector() -> str:
    """

    :return: initialization vector for OFB
    """
    return initialization_vector
