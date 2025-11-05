# carla_client.py

from __future__ import annotations

import socket
from typing import Iterable

from messages import v2x_to_wire, V2XMessage
from config import NETWORK


class CarlaClient:
    """
    Sends V2X messages to CARLA.

    Expected wire format: one JSON object per line, see `messages.v2x_to_wire`.
    """

    def __init__(self, host: str | None = None, port: int | None = None) -> None:
        self.host = host or NETWORK.carla_host
        self.port = port or NETWORK.carla_port
        self._sock: socket.socket | None = None

    def connect(self) -> None:
        if self._sock is not None:
            return
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.connect((self.host, self.port))

    def send(self, msg: V2XMessage) -> None:
        if self._sock is None:
            self.connect()
        wire = v2x_to_wire(msg) + "\n"
        self._sock.sendall(wire.encode("utf-8"))

    def send_many(self, msgs: Iterable[V2XMessage]) -> None:
        for m in msgs:
            self.send(m)

    def close(self) -> None:
        if self._sock is not None:
            self._sock.close()
            self._sock = None
