# CS5230_Vehicle_Cybersecurity
Our intent is to build upon the combined integration of the 3 simulators, Sumo, Carla, and Artery.

Malicious CAM and DENM messages will be injected (from a python program) along with realistic messages from Artery.

This allows for the simultaneous simulation of both real and fake messages in a V2X network. 

The simulated attacks from the group’s CAM injections will include: Position Attack and Offset Attack. 
The simulated DENM attacks will include: Emergency Braking Attack, Traffic Jam Attack, and Traction Loss Attack

v2x_attack_pipeline/
├── config.py
├── messages.py
├── attacks.py
├── artery_client.py
├── carla_client.py
├── router.py
└── main.py

  High-level roles:
messages.py – typed models for CAM / DENM, plus (de)serialization helpers.
attacks.py – Strategy pattern for attacks; one class per attack.
artery_client.py – Source of real messages (from Artery).
carla_client.py – Sink for messages into CARLA.
router.py – Orchestrates: read → choose attack strategy → emit real + spoofed.
config.py – Central config (ports, probabilities, offsets, etc.).
main.py – Wires everything together and runs the loop.

Assuming Artery sends JSON over TCP (Can easily change later to ZMQ, files, REST, etc.).
