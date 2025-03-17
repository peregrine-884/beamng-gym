import gymnasium as gym

# beamng
from beamng_gym.beamng.beamng_manager import BeamNGManager
from beamng_gym.beamng.sensor_manager import SensorManager

#env
from beamng_gym.envs.action import *
from beamng_gym.envs.observation import *
from beamng_gym.envs.reset import *
from beamng_gym.envs.step import *

# modules
from beamng_gym.modules.config_loader import load_config_from_json5
import os

class BeamNGEnv(gym.Env):
  def __init__(self, config_path):
    print('config_path:', config_path)
    super().__init__()
    parent_dir = os.path.dirname(os.path.realpath(__file__))
    json5_path = os.path.join(parent_dir, config_path)
    if not os.path.exists(json5_path):
      raise FileNotFoundError(f'Config file not found at {json5_path}')
    # json5_path = '/media/hestia-22/data_hdd/BeamNG/beamng-gym/beamng_gym/config/default.json5'
    (
      self.scenario_data,
      self.ego_vehicle_data,
      self.npc_vehicles_data,
      self.lidar_data,
      self.camera_data
    ) = load_config_from_json5(json5_path)
    
    self.beamng_manager = BeamNGManager(
      self.scenario_data,
      self.ego_vehicle_data,
      self.npc_vehicles_data
    )
    
    self.sensor_manager = SensorManager(
      self.beamng_manager.bng,
      self.beamng_manager.ego_vehicle,
      self.lidar_data,
      self.camera_data
    )
    
    initialize_action_space()
    self.action_space = get_action_space()
    
    initialize_observation_space(self.sensor_manager)
    self.observation_space = get_observation_space()
    
  def reset(self, **kwargs):
    observation, info = reset_environment(self.beamng_manager, self.sensor_manager)
    
    return observation, info
    
  def step(self, action, **kwargs):
    observation, reward, terminated, truncated, info = step_environment(self.beamng_manager, self.sensor_manager, action)
  
    return observation, reward, terminated, truncated, info
  
  def render():
    pass
    
  def close(self):
    self.beamng_manager.close()
    
    
