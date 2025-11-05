# config.py

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class NetworkConfig:
    artery_host: str = "127.0.0.1"
    artery_port: int = 9000
    carla_host: str = "127.0.0.1"
    carla_port: int = 9100


@dataclass(frozen=True)
class AttackConfig:
    # CAM attacks
    position_attack_prob: float = 0.1
    offset_attack_prob: float = 0.1

    # DENM attacks
    emergency_brake_attack_prob: float = 0.1
    traffic_jam_attack_prob: float = 0.1
    traction_loss_attack_prob: float = 0.1

    # Offset parameters for CAM OffsetAttack (in meters)
    cam_offset_xy_meters: Tuple[float, float] = (50.0, 0.0)


NETWORK = NetworkConfig()
ATTACKS = AttackConfig()
