# artery_tcp_server.py
import socket
import threading
import logging
from typing import Callable

from messages import v2x_from_wire, V2XMessage

logging.basicConfig(level=logging.INFO)


class ArteryTCPServer:
    """
    Simple TCP server that accepts a single connection from Artery (or multiple).
    Expects one JSON object per line. For each incoming line it calls `on_message`.
    """

    def __init__(self, host="0.0.0.0", port=9000, on_message: Callable[[V2XMessage], None] | None = None):
        self.host = host
        self.port = port
        self.on_message = on_message
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._running = False

    def start(self):
        self._sock.bind((self.host, self.port))
        self._sock.listen(1)
        logging.info("ArteryTCPServer listening on %s:%s", self.host, self.port)
        self._running = True
        threading.Thread(target=self._accept_loop, daemon=True).start()

    def _accept_loop(self):
        while self._running:
            conn, addr = self._sock.accept()
            logging.info("Artery connected from %s", addr)
            threading.Thread(target=self._reader_thread, args=(conn,), daemon=True).start()

    def _reader_thread(self, conn: socket.socket):
        with conn:
            f = conn.makefile("r")
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    msg = v2x_from_wire(line)
                except Exception as e:
                    logging.exception("Failed to parse line: %s", line)
                    continue
                if self.on_message:
                    self.on_message(msg)

    def stop(self):
        self._running = False
        self._sock.close()
