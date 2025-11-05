# router.py

from __future__ import annotations

from typing import Iterable, List

from artery_client import ArteryClient
from carla_client import CarlaClient
from attacks import AttackStrategy, default_attacks
from messages import V2XMessage


class AttackRouter:
    """
    Reads real messages from Artery, creates spoofed copies using attack strategies,
    and forwards both to CARLA.

    This class is decoupled from specific networking details; Artery/Carla are
    simple Source/Sink collaborators.
    """

    def __init__(
        self,
        artery: ArteryClient,
        carla: CarlaClient,
        attacks: Iterable[AttackStrategy] | None = None,
    ) -> None:
        self.artery = artery
        self.carla = carla
        self.attacks: List[AttackStrategy] = list(attacks or default_attacks())

    def _spoof(self, msg: V2XMessage) -> List[V2XMessage]:
        spoofed: List[V2XMessage] = []
        for attack in self.attacks:
            if attack.applies_to(msg):
                fake = attack.apply(msg)
                if fake is not None:
                    spoofed.append(fake)
        return spoofed

    def run(self) -> None:
        """
        Blocking loop: for each real message, forward it and any spoofed variants.
        """
        try:
            for real_msg in self.artery.message_stream():
                # Always forward the real message
                self.carla.send(real_msg)

                # Generate spoofed variants (0..N)
                spoofed_msgs = self._spoof(real_msg)
                if spoofed_msgs:
                    self.carla.send_many(spoofed_msgs)
        finally:
            self.carla.close()
