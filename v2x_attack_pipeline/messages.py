# messages.py

from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
from typing import Any, Dict, Literal, Union
import json
import time


class MessageType(str, Enum):
    CAM = "CAM"
    DENM = "DENM"


@dataclass
class CAM:
    station_id: int
    timestamp: float
    lat: float
    lon: float
    speed: float  # m/s
    heading: float  # degrees


class DenmEventType(str, Enum):
    EMERGENCY_BRAKING = "emergency_braking"
    TRAFFIC_JAM = "traffic_jam"
    TRACTION_LOSS = "traction_loss"
    OTHER = "other"


@dataclass
class DENM:
    station_id: int
    timestamp: float
    lat: float
    lon: float
    event_type: DenmEventType
    severity: int  # e.g., 1–5


V2XMessage = Union[CAM, DENM]


def now_ts() -> float:
    return time.time()


def cam_from_json(payload: Dict[str, Any]) -> CAM:
    return CAM(
        station_id=int(payload["station_id"]),
        timestamp=float(payload.get("timestamp", now_ts())),
        lat=float(payload["lat"]),
        lon=float(payload["lon"]),
        speed=float(payload["speed"]),
        heading=float(payload["heading"]),
    )


def denm_from_json(payload: Dict[str, Any]) -> DENM:
    return DENM(
        station_id=int(payload["station_id"]),
        timestamp=float(payload.get("timestamp", now_ts())),
        lat=float(payload["lat"]),
        lon=float(payload["lon"]),
        event_type=DenmEventType(payload["event_type"]),
        severity=int(payload.get("severity", 1)),
    )


def v2x_from_wire(raw: str) -> V2XMessage:
    """
    Expect JSON like:
      {"msg_type": "CAM", "payload": {...}}
    or  {"msg_type": "DENM", "payload": {...}}
    """
    obj = json.loads(raw)
    msg_type = MessageType(obj["msg_type"])
    payload = obj["payload"]

    if msg_type == MessageType.CAM:
        return cam_from_json(payload)
    else:
        return denm_from_json(payload)


def v2x_to_wire(msg: V2XMessage) -> str:
    if isinstance(msg, CAM):
        msg_type: Literal["CAM"] = "CAM"
    elif isinstance(msg, DENM):
        msg_type = "DENM"
    else:
        raise TypeError(f"Unsupported message type: {type(msg)}")

    return json.dumps(
        {
            "msg_type": msg_type,
            "payload": asdict(msg),
        }
    )
