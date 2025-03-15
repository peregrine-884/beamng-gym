from beamngpy import BeamNGpy, Scenario, Vehicle
from beamngpy.sensors import Electrics

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
    self.bng.ui.hide_hud()
    self.bng.scenario.start()
    self.bng.control.pause()
    
    self.ego_vehicle.sensors.attach('electrics', Electrics())
    
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
    return {
      "electrics": self.ego_vehicle.sensors['electrics'],
      "state": self.ego_vehicle.sensors['state']
    }
