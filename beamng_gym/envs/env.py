import gymnasium as gym
from gymnasium import spaces
import numpy as np
import time

# beamngpy
from beamngpy import BeamNGpy, Scenario, Vehicle
from beamngpy.sensors import Lidar, Camera

# modules
from modules.scenario_loader import load_scenario_from_json5


class BeamNGEnv(gym.Env):
  def __init__(self):
    """
    環境の初期化
    """
    super().__init__()
    
    # JSON5からシナリオをロード
    json5_path = 'C:\\Users\\hayat\\beamng_gym\\beamng_gym\\config\\default.json5'
    scenario_data, ego_vehicle_data, npc_vehicles_data, lidar_data, camera_data = load_scenario_from_json5(json5_path)
    
    # BeamNG launch
    self.bng = BeamNGpy('localhost', 64256)
    self.bng.open(launch=False)
    
    # 走行するMAP
    print(scenario_data)
    self.scenario = Scenario(scenario_data.level, scenario_data.name)
    
    # 自車(Ego Vehicle)のセットアップ
    self.ego_vehicle = None
    if ego_vehicle_data:
      self.ego_vehicle = Vehicle(ego_vehicle_data.name, model=ego_vehicle_data.model, color=ego_vehicle_data.color)
      self.scenario.add_vehicle(self.ego_vehicle, pos=ego_vehicle_data.pos, rot_quat=ego_vehicle_data.rot_quat)
    
    # NPC 車両のセットアップ
    self.npc_vehicles = []
    for vehicle_data in npc_vehicles_data:
      vehicle = Vehicle(vehicle_data.name, model=vehicle_data.model, color=vehicle_data.color)
      self.scenario.add_vehicle(vehicle, pos=vehicle_data.pos, rot_quat=vehicle_data.rot_quat)
      self.npc_vehicles.append(vehicle)
      
    # BeamNGの実行
    self.scenario.make(self.bng)
    
    self.bng.settings.set_deterministic(60)
    self.bng.scenario.load(self.scenario)
    self.bng.ui.hide_hud()
    self.bng.scenario.start()
    
    # センサーのセットアップ
    self.lidars = []
    for l in lidar_data:
      print(l)
      lidar = Lidar(
          l.name,
          self.bng,
          self.ego_vehicle,
          requested_update_time=l.requested_update_time,
          pos=tuple(l.pos),
          dir=tuple(l.dir),
          up=tuple(l.up),
          vertical_resolution=l.vertical_resolution,
          horizontal_angle=l.horizontal_angle,
          is_rotate_mode=l.is_rotate_mode,
          is_360_mode=l.is_360_mode,
          is_using_shared_memory=l.is_using_shared_memory,
          is_visualised=l.is_visualised,
          is_streaming=l.is_streaming,
          is_dir_world_space=l.is_dir_world_space
      )
      self.lidars.append(lidar)
      
    self.cameras = []
    for c in camera_data:
      print(c)
      camera = Camera(
          c.name,
          self.bng,
          self.ego_vehicle,
          requested_update_time=c.requested_update_time,
          pos=tuple(c.pos),
          dir=tuple(c.dir),
          up=tuple(c.up),
          resolution=tuple(c.resolution),
          near_far_planes=tuple(c.near_far_planes),
          is_using_shared_memory=c.is_using_shared_memory,
          is_render_annotations=c.is_render_annotations,
          is_render_instance=c.is_render_instance,
          is_render_depth=c.is_render_depth,
          is_visualised=c.is_visualised,
          is_streaming=c.is_streaming,
          is_dir_world_space=c.is_dir_world_space
      )
      self.cameras.append(camera)
      
      
    # observation space
    
    # action space
    
  def reset(self):
    """"
    環境をリセットし、初期状態を返す
    """
    
    
  def step(self):
    """"
    アクションを受け取って次の状態と報酬を計算する
    """
    
  def render(self):    
    """
    環境を可視化
    """
    
  def close(self):
    """
    環境を閉じる
    """
    self.bng.close()
    
if __name__ == '__main__':
  env = BeamNGEnv()
    
    