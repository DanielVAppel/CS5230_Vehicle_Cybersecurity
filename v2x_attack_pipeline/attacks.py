# attacks.py

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import replace
from typing import Optional, List
import math
import random

from messages import CAM, DENM, V2XMessage, DenmEventType
from config import ATTACKS


class AttackStrategy(ABC):
    """
    Strategy base class: individual attacks implement `apply`.
    """

    @abstractmethod
    def applies_to(self, msg: V2XMessage) -> bool:
        ...

    @abstractmethod
    def apply(self, msg: V2XMessage) -> Optional[V2XMessage]:
        """
        Return a spoofed message derived from `msg` or None if no spoof should be emitted.
        """
        ...


# ---------- CAM attacks ----------

class PositionAttack(AttackStrategy):
    """
    Replace position with totally bogus but plausible coordinates.
    """

    def __init__(self, probability: float) -> None:
        self.probability = probability

    def applies_to(self, msg: V2XMessage) -> bool:
        return isinstance(msg, CAM)

    def apply(self, msg: V2XMessage) -> Optional[V2XMessage]:
        if not isinstance(msg, CAM):
            return None

        if random.random() > self.probability:
            return None

        # Example: send car far away while keeping speed/heading same.
        # You can replace with more realistic coordinates (e.g., different city).
        fake_lat = msg.lat + 0.5  # ~55 km north
        fake_lon = msg.lon + 0.5  # ~55 km east

        return replace(msg, lat=fake_lat, lon=fake_lon)


class OffsetAttack(AttackStrategy):
    """
    Slightly offset position to cause mis-localization, e.g., for lane-level confusion.
    """

    def __init__(self, probability: float, offset_xy_meters: tuple[float, float]) -> None:
        self.probability = probability
        self.offset_x_m, self.offset_y_m = offset_xy_meters

    def applies_to(self, msg: V2XMessage) -> bool:
        return isinstance(msg, CAM)

    def apply(self, msg: V2XMessage) -> Optional[V2XMessage]:
        if not isinstance(msg, CAM):
            return None

        if random.random() > self.probability:
            return None

        # Convert approximate meter offsets to degrees (very rough, OK for sim)
        # 1 deg lat ≈ 111_320 m; 1 deg lon ≈ 111_320 * cos(lat)
        lat_scale = 1.0 / 111_320.0
        lon_scale = 1.0 / (111_320.0 * math.cos(math.radians(msg.lat)))

        dlat = self.offset_y_m * lat_scale
        dlon = self.offset_x_m * lon_scale

        return replace(msg, lat=msg.lat + dlat, lon=msg.lon + dlon)


# ---------- DENM attacks ----------

class EmergencyBrakingAttack(AttackStrategy):
    def __init__(self, probability: float) -> None:
        self.probability = probability

    def applies_to(self, msg: V2XMessage) -> bool:
        return isinstance(msg, DENM)

    def apply(self, msg: V2XMessage) -> Optional[V2XMessage]:
        if not isinstance(msg, DENM):
            return None
        if random.random() > self.probability:
            return None

        return replace(
            msg,
            event_type=DenmEventType.EMERGENCY_BRAKING,
            severity=max(msg.severity, 3),
        )


class TrafficJamAttack(AttackStrategy):
    def __init__(self, probability: float) -> None:
        self.probability = probability

    def applies_to(self, msg: V2XMessage) -> bool:
        return isinstance(msg, DENM)

    def apply(self, msg: V2XMessage) -> Optional[V2XMessage]:
        if not isinstance(msg, DENM):
            return None
        if random.random() > self.probability:
            return None

        return replace(
            msg,
            event_type=DenmEventType.TRAFFIC_JAM,
            severity=max(msg.severity, 2),
        )


class TractionLossAttack(AttackStrategy):
    def __init__(self, probability: float) -> None:
        self.probability = probability

    def applies_to(self, msg: V2XMessage) -> bool:
        return isinstance(msg, DENM)

    def apply(self, msg: V2XMessage) -> Optional[V2XMessage]:
        if not isinstance(msg, DENM):
            return None
        if random.random() > self.probability:
            return None

        return replace(
            msg,
            event_type=DenmEventType.TRACTION_LOSS,
            severity=max(msg.severity, 3),
        )


def default_attacks() -> List[AttackStrategy]:
    """
    Simple factory that uses ATTACKS config.
    """
    return [
        PositionAttack(ATTACKS.position_attack_prob),
        OffsetAttack(ATTACKS.offset_attack_prob, ATTACKS.cam_offset_xy_meters),
        EmergencyBrakingAttack(ATTACKS.emergency_brake_attack_prob),
        TrafficJamAttack(ATTACKS.traffic_jam_attack_prob),
        TractionLossAttack(ATTACKS.traction_loss_attack_prob),
    ]
