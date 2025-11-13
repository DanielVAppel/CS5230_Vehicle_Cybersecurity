# carla_api_bridge.py
import carla
import logging

class CarlaAPIBridge:
    def __init__(self, host='localhost', port=2000, timeout=10.0):
        self.client = carla.Client(host, port)
        self.client.set_timeout(timeout)
        self.world = self.client.get_world()

    def find_actor_by_station(self, station_id):
        # mapping from station_id to carla actor id must be maintained.
        # simple heuristic: search for actor attributes matching station_id tag
        for a in self.world.get_actors().filter('vehicle.*'):
            # if you added custom attributes to actors at spawn, check them here
            if str(getattr(a, 'station_id', '')) == str(station_id):
                return a
        return None

    def handle_cam(self, cam_msg):
        # Example: set actor transform to spoofed location (dangerous but for testing)
        actor = self.find_actor_by_station(cam_msg.station_id)
        if actor is None:
            logging.debug("No actor for station %s", cam_msg.station_id)
            return
        # Convert lat/lon to Carla world coordinates (you must implement conversion)
        carla_loc = self.latlon_to_carla_transform(cam_msg.lat, cam_msg.lon)
        actor.set_transform(carla_loc)  # be careful: this teleports the vehicle

    def handle_denm(self, denm_msg):
        # Example: if event is EMERGENCY_BRAKING, abruptly brake the target vehicle
        actor = self.find_actor_by_station(denm_msg.station_id)
        if actor is None:
            return
        if denm_msg.event_type == 'emergency_braking':
            # set vehicle control to full brake
            control = carla.VehicleControl(throttle=0.0, brake=1.0)
            actor.apply_control(control)

    def latlon_to_carla_transform(self, lat, lon):
        # **You must implement conversion** from geo coords to CARLA world coordinates.
        # If SUMO/CARLA are co-located in the same coordinate frame, use that mapping.
        raise NotImplementedError
