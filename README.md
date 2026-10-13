# Autonomous Mine Exploration Rover Simulation

A modular, real-time autonomous navigation and environmental monitoring simulation for a **Pioneer P3DX** rover navigating hazardous subterranean environments in **CoppeliaSim**. 

Driven entirely by an external Python control loop via the **ZeroMQ Remote API**, the system captures environmental telemetry, evaluates hazard levels, and executes collision avoidance without relying on built-in simulator scripts.

## Key Features
* **ZeroMQ Remote API Integration:** Fully decoupled control logic executed entirely through external Python scripts.
* **Path-Independent Scene Resolution:** Custom hierarchy discovery that dynamically retrieves object handles (`PioneerP3DX`, motors, sensors, targets) regardless of scene folder nesting or path changes.
* **Environmental Telemetry Processing:** Real-time mathematical calculation of hazardous gas levels (PPM) and ambient temperature (°C) derived from Euclidean distance relative to environmental heat/gas source dummies.
* **Reactive Obstacle Avoidance:** Multi-directional sensor array evaluation processing 16 ultrasonic proximity sensors to trigger differential steering manoeuvres around obstacles.
* **Throttled Telemetry Output:** Non-blocking rate-limited execution loop preventing terminal buffer overflow while preserving real-time motor control response.

## Tech Stack
* **Simulator:** CoppeliaSim (V-REP)
* **Language:** Python 3.12
* **API Engine:** `coppeliasim_zmqremoteapi_client`
* **Robot Model:** Adept MobileRobots Pioneer P3DX
