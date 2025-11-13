# convert_artery_to_json.py
import json
from messages import v2x_to_wire, CAM, DENM, DenmEventType

def artery_native_to_json_line(native: dict) -> str:
    # Transform Artery’s native structure into our schema.
    # Example only—replace key names as needed:
    if native["type"] == "cam":
        msg = CAM(
            station_id=native["id"],
            timestamp=native["t"],
            lat=native["geo"]["lat"],
            lon=native["geo"]["lon"],
            speed=native["kph"] / 3.6,
            heading=native["heading_deg"],
        )
    else:
        msg = DENM(
            station_id=native["id"],
            timestamp=native["t"],
            lat=native["geo"]["lat"],
            lon=native["geo"]["lon"],
            event_type=DenmEventType(native["event"].lower()),
            severity=native.get("severity", 2),
        )
    return v2x_to_wire(msg)  # JSON string ready to send line-by-line
