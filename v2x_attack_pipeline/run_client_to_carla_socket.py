# run_client_to_carla_socket.py
from artery_client import ArteryClient
from carla_client import CarlaClient
from router import AttackRouter
from attacks import default_attacks

artery = ArteryClient(host="127.0.0.1", port=9000)  # Artery’s server
carla = CarlaClient(host="127.0.0.1", port=9100)    # CARLA’s V2X listener
router = AttackRouter(artery=artery, carla=carla, attacks=default_attacks())

router.run()
