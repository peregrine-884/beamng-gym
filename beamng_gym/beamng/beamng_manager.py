from beamngpy import BeamNGpy, Scenario, Vehicle
from beamngpy.sensors import Electrics, GPS, Damage

class BeamNGManager:
  def __init__(self, scenario_data, ego_vehicle_data, npc_data):
    self.scenario_data = scenario_data
    self.ego_vehicle_data = ego_vehicle_data
    self.npc_data = npc_data
    
    self.bng = BeamNGpy('localhost', 25252)
    self.bng.open(launch=False)
    
    self.scenario = Scenario(scenario_data.level, scenario_data.name)
    
    self.ego_vehicle = Vehicle(
      ego_vehicle_data.name,
      model=ego_vehicle_data.model,
      color=ego_vehicle_data.color
    )
    self.scenario.add_vehicle(
      self.ego_vehicle,
      pos=ego_vehicle_data.pos,
      rot_quat=ego_vehicle_data.rot_quat
    )
    
    self.npc_vehicles = []
    for vehicle_data in npc_data:
      vehicle = Vehicle(
        vehicle_data.name,
        model=vehicle_data.model,
        color=vehicle_data.color
      )
      self.scenario.add_vehicle(
        vehicle,
        pos=vehicle_data.pos,
        rot_quat=vehicle_data.rot_quat
      )
      self.npc_vehicles.append(vehicle)
      
    self.scenario.make(self.bng)
    
    self.bng.settings.set_deterministic(60)
    self.bng.scenario.load(self.scenario)
    self.bng.ui.show_hud()
    self.bng.scenario.start()
    self.bng.control.pause()
    
    self.ego_vehicle.sensors.attach('electrics', Electrics())
    self.ego_vehicle.sensors.attach('damage', Damage())
    ref_lon, ref_lat = 8.8017, 53.0793
    self.gps = GPS(
      "gps",
      self.bng,
      self.ego_vehicle,
      pos=(0, 0, 1.0),
      ref_lon=ref_lon,
      ref_lat=ref_lat,
      is_visualised=False,
    )
    
  def reset(self):
    self.ego_vehicle.control(throttle=0, brake=0, steering=0)
    self.ego_vehicle.teleport(
      pos=self.ego_vehicle_data.pos,
      rot_quat=self.ego_vehicle_data.rot_quat,
      reset=True
    )
    
    for vehicle, data in zip(self.npc_vehicles, self.npc_data):
      vehicle.control(throttle=0, brake=0, steering=0)
      vehicle.teleport(pos=data.pos, rot_quat=data.rot_quat, reset=True)
      
    self.bng.scenario.restart()
    self.step_simulation(30)
    self.bng.control.pause()
    self.ego_vehicle.set_shift_mode('realistic_automatic')
    self.ego_vehicle.control(gear=2)
    
  def close(self):
    self.bng.close()
    
  def step_simulation(self, steps=1):
    self.bng.control.step(steps)
    
  def get_vehicle_data(self):
    self.ego_vehicle.sensors.poll()
    gps_data = self.gps.poll()
    current_index = len(gps_data) - 1 if len(gps_data) > 0 else 0
    return {
      "electrics": self.ego_vehicle.sensors['electrics'],
      "state": self.ego_vehicle.sensors['state'],
      "gps": gps_data[current_index]
    }
  
  def validate_collision(self, damage_threshold=0.1):
    def calculate_damage(damage):
      damage = damage["deform_group_damage"]
      total_damage = 0
      for key in damage.keys():
          total_damage += damage[key]["damage"]
      return total_damage
    ego_damage = calculate_damage(self.ego_vehicle.sensors['damage'])
    return ego_damage > damage_threshold