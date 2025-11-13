# run_server_to_carla_socket.py
from artery_tcp_server import ArteryTCPServer
from carla_client import CarlaClient
from router import AttackRouter
from attacks import default_attacks

carla = CarlaClient(host="127.0.0.1", port=9100)  # your CARLA V2X listener
router = AttackRouter(artery=None, carla=carla, attacks=default_attacks())

def on_message(msg):
    # real
    carla.send(msg)
    # spoofed
    for fake in router._spoof(msg):
        carla.send(fake)

srv = ArteryTCPServer(host="0.0.0.0", port=9000, on_message=on_message)
srv.start()

try:
    import time
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    srv.stop()
    carla.close()
