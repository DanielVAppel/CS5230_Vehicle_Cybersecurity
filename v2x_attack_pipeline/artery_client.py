# artery_client.py

from __future__ import annotations

import socket
from typing import Iterator

from messages import v2x_from_wire, V2XMessage
from config import NETWORK


class ArteryClient:
    """
    Connects to Artery and yields incoming V2X messages.

    Expected wire format: one JSON object per line, see `messages.v2x_from_wire`.
    """

    def __init__(self, host: str | None = None, port: int | None = None) -> None:
        self.host = host or NETWORK.artery_host
        self.port = port or NETWORK.artery_port

    def message_stream(self) -> Iterator[V2XMessage]:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, self.port))
        fileobj = sock.makefile("r")

        try:
            for line in fileobj:
                line = line.strip()
                if not line:
                    continue
                yield v2x_from_wire(line)
        finally:
            fileobj.close()
            sock.close()
