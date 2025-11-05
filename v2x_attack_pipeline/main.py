# main.py

from artery_client import ArteryClient
from carla_client import CarlaClient
from router import AttackRouter
from attacks import default_attacks


def main() -> None:
    artery = ArteryClient()
    carla = CarlaClient()
    attacks = default_attacks()

    router = AttackRouter(artery=artery, carla=carla, attacks=attacks)
    router.run()


if __name__ == "__main__":
    main()
