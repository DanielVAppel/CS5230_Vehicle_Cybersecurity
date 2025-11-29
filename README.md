# CS5230_Vehicle_Cybersecurity
Our intent is to build upon the combined integration of the 3 simulators, Sumo, Carla, and Artery.

Malicious CAM and DENM messages will be injected (from a python program) along with realistic messages from Artery.

This allows for the simultaneous simulation of both real and fake messages in a V2X network. 

The simulated attacks from the group’s CAM injections will include: Position Attack and Offset Attack. 
The simulated DENM attacks will include: Emergency Braking Attack, Traffic Jam Attack, and Traction Loss Attack

  High-level roles:
messages.py – typed models for CAM / DENM, plus (de)serialization helpers.
attacks.py – Strategy pattern for attacks; one class per attack.
artery_client.py – Source of real messages (from Artery).
carla_client.py – Sink for messages into CARLA.
router.py – Orchestrates: read → choose attack strategy → emit real + spoofed.
config.py – Central config (ports, probabilities, offsets, etc.).
main.py – Wires everything together and runs the loop.

Assuming Artery sends JSON over TCP (Can easily change later to ZMQ, files, REST, etc.).

Process to run:

Step 1 - Create venv (first time Only)
python -m venv .venv

Step 2 - Activate venv
.\.venv\Scripts\activate

Step 3 — Install dependencies (only first time)
python -m pip install numpy

Step 4 — If you are using CARLA API (simulator only)

(Skip this if running the demo)
$env:PYTHONPATH = "$env:PYTHONPATHC:\CARLA\WindowsNoEditor\PythonAPI\carla\dist\carla-<version>.eggC:\CARLA\WindowsNoEditor\PythonAPI\carla"

Step 5 — Start simulators (simulator only)

SUMO → Artery → CARLA
(simulator ONLY)
1. Launch SUMO
2. Launch Artery
3. Launch CARLA 

Step 6 — Start the  Python server 

(for demo)
python run_server_demo.py

(for simulators)
python run_server_to_carla_api.py

Step 7 — Start message source

(for demo) Open a second terminal
cd [your path]\CS5230_Vehicle_Cybersecurity\v2x_attack_pipeline.\.venv\Scripts\activate
python fake_artery_sender.py

Configure Artery to connect to your PC’s IP on port 9000.