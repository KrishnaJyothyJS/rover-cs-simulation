from coppeliasim_zmqremoteapi_client import RemoteAPIClient

# Connect to the simulator
client = RemoteAPIClient()
sim = client.require('sim')

print("Successfully connected to CoppeliaSim!")

# Get every object currently loaded in the scene
all_objects = sim.getObjectsInTree(sim.handle_scene, sim.handle_all, 0)
print(f"Found {len(all_objects)} objects. Here is what Python sees:")

for obj_handle in all_objects:
    # Get the exact alias name CoppeliaSim expects
    name = sim.getObjectAlias(obj_handle)
    
    # We only want to print the main objects, not every tiny camera or joint
    if "Pioneer" in name or "source" in name or "Floor" in name:
        print(f" -> EXACT NAME: '{name}'")