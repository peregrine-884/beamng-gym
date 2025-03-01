import json5
from beamng_gym.modules.scenario import Scenario, Vehicle, Lidar, Camera

def str_to_bool(value):
  """ 文字列の 'True' / 'False' を bool 型に変換 """
  if isinstance(value, str):
    return value.lower() == 'true'
  return value

def load_scenario_from_json5(json5_path):
  """ JSON5 ファイルからシナリオをロード """
  with open(json5_path, 'r', encoding='utf-8') as f:
    data = json5.load(f)

  # シナリオ情報の読み込み
  scenario_data = data['scenario']
  scenario = Scenario(scenario_data['level'], scenario_data['name'])

  # Ego Vehicle の読み込み
  ego_vehicle_data = data.get('ego_vehicle', None)
  ego_vehicle = None
  if ego_vehicle_data:
    ego_vehicle = Vehicle(
      ego_vehicle_data['name'],
      ego_vehicle_data['model'],
      ego_vehicle_data['color'],
      ego_vehicle_data['pos'],
      ego_vehicle_data['rot_quat']
    )

  # NPC Vehicles の読み込み
  npc_vehicles = [
    Vehicle(v['name'], v['model'], v['color'], v['pos'], v['rot_quat'])
    for v in data.get('npc_vehicles', [])
  ]

  # LiDAR センサーの読み込み
  lidars = [
    Lidar(
      l['name'], 
      l['requested_update_time'], 
      l['pos'], 
      l['dir'], 
      l['up'],
      l['vertical_resolution'], 
      l['horizontal_angle'], 
      str_to_bool(l['is_rotate_mode']),
      str_to_bool(l['is_360_mode']),
      str_to_bool(l['is_using_shared_memory']),
      str_to_bool(l['is_visualised']),
      str_to_bool(l['is_streaming']),
      str_to_bool(l['is_dir_world_space'])
    ) for l in data.get('lidars', [])
  ]

  # カメラの読み込み
  cameras = [
    Camera(
      c['name'], 
      c['requested_update_time'], 
      c['pos'], 
      c['dir'], 
      c['up'],
      c['resolution'], 
      c['near_far_planes'], 
      str_to_bool(c['is_using_shared_memory']),
      str_to_bool(c['is_render_annotations']),
      str_to_bool(c['is_render_instance']),
      str_to_bool(c['is_render_depth']),
      str_to_bool(c['is_visualised']),
      str_to_bool(c['is_streaming']),
      str_to_bool(c['is_dir_world_space'])
    ) for c in data.get('cameras', [])
  ]

  return scenario, ego_vehicle, npc_vehicles, lidars, cameras
