import math
from coppeliasim_zmqremoteapi_client import RemoteAPIClient

# Connect to the CoppeliaSim ZeroMQ server
client = RemoteAPIClient()
sim = client.require('sim')

print("Connected to simulator. Scanning scene for objects...")

def get_obj(name_to_find):
    all_objects = sim.getObjectsInTree(sim.handle_scene)
    for obj_handle in all_objects:
        if sim.getObjectAlias(obj_handle) == name_to_find:
            return obj_handle
    print(f"CRITICAL ERROR: Cannot find '{name_to_find}'.")
    exit()

# Grab the unique objects
rover = get_obj('PioneerP3DX')
leftMotor = get_obj('leftMotor')
rightMotor = get_obj('rightMotor')
gasSource = get_obj('gas_source')
heatSource = get_obj('heat_source')

# Grab all 16 ultrasonic sensors at once by looking for their shared name
usSensors = []
all_objects = sim.getObjectsInTree(sim.handle_scene)
for obj_handle in all_objects:
    if sim.getObjectAlias(obj_handle) == 'ultrasonicSensor':
        usSensors.append(obj_handle)

print(f"Successfully found {len(usSensors)} ultrasonic sensors!")
print("Starting simulation...")
sim.startSimulation()

# --- KEEP YOUR EXISTING TRY/EXCEPT WHILE LOOP HERE ---

try:
    while True:
        # --- 1. Sensing Logic ---
        rPos = sim.getObjectPosition(rover, -1)
        gPos = sim.getObjectPosition(gasSource, -1)
        hPos = sim.getObjectPosition(heatSource, -1)
        
        # Calculate Euclidean distance
        distGas = math.sqrt((rPos[0]-gPos[0])**2 + (rPos[1]-gPos[1])**2)
        distHeat = math.sqrt((rPos[0]-hPos[0])**2 + (rPos[1]-hPos[1])**2)
        
        gasPPM = 5000 / (distGas**2 + 1)
        tempC = 25 + (100 / (distHeat + 1))
        
        print(f"Telemetry -> Gas: {gasPPM:.1f} PPM | Temp: {tempC:.1f} C", flush=True)
        
        # --- 2. Obstacle Avoidance Actuation ---
        detectLeft = False
        detectRight = False
        threshold = 0.5
        
        for i in range(4):
            result, distance, *_ = sim.readProximitySensor(usSensors[i])
            if result > 0 and distance < threshold:
                detectLeft = True
                
        for i in range(4, 8):
            result, distance, *_ = sim.readProximitySensor(usSensors[i])
            if result > 0 and distance < threshold:
                detectRight = True
                
        # --- ADJUST SPEED HERE ---
        # Changed from 5.0 down to 2.0 for a controlled, realistic walking pace
        leftVel = 2.0  
        rightVel = 2.0 
        
        if detectLeft:
            leftVel = 2.0
            rightVel = -1.0  # Slightly reverse the right wheel to turn right
        elif detectRight:
            leftVel = -1.0   # Slightly reverse the left wheel to turn left
            rightVel = 2.0
            
        sim.setJointTargetVelocity(leftMotor, leftVel)
        sim.setJointTargetVelocity(rightMotor, rightVel)
        
except KeyboardInterrupt:
    sim.stopSimulation()
    print("\nSimulation stopped.")