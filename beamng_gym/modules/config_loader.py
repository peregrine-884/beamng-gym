import json5

from beamng_gym.entities.scenario import Scenario
from beamng_gym.entities.vehicle import Vehicle
from beamng_gym.entities.lidar import Lidar
from beamng_gym.entities.camera import Camera

def load_config_from_json5(json5_path):
  with open(json5_path, 'r', encoding='utf-8') as f:
    data = json5.load(f)
    
    scenario_data = data.get('scenario', {})
    scenario = Scenario.from_dict(scenario_data)
    
    ego_vehicle_data = data.get('ego_vehicle', {})
    ego_vehicle = Vehicle.from_dict(ego_vehicle_data)
    
    npc_vehicles = [
      Vehicle.from_dict(v) for v in data.get('npc_vehicles', [])
    ]
    
    lidars = [
      Lidar.from_dict(l) for l in data.get('lidars', [])
    ]
    
    cameras = [
      Camera.from_dict(c) for c in data.get('cameras', [])
    ]
    
    return scenario, ego_vehicle, npc_vehicles, lidars, cameras
