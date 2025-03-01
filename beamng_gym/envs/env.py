import gymnasium as gym
from gymnasium.spaces import Box, Dict
import numpy as np
import time
import matplotlib.pyplot as plt
import cv2

# beamngpy
from beamngpy import BeamNGpy, Scenario, Vehicle
from beamngpy.sensors import Lidar, Camera, Electrics

# modules
from beamng_gym.modules.scenario_loader import load_scenario_from_json5

class BeamNGEnv(gym.Env):
  def __init__(self):
    """
    環境の初期化
    """
    super().__init__()
    
    # JSON5からシナリオをロード
    json5_path = 'C:\\Users\\hayat\\beamng_gym\\beamng_gym\\config\\default.json5'
    self.scenario_data, self.ego_vehicle_data, self.npc_vehicles_data, self.lidar_data, self.camera_data = load_scenario_from_json5(json5_path)
    
    # BeamNG launch
    self.bng = BeamNGpy('localhost', 64256)
    self.bng.open(launch=False)
    
    # 走行するMAP
    print('=========== SCENARIO ===========')
    print(self.scenario_data)
    self.scenario = Scenario(self.scenario_data.level, self.scenario_data.name)
    
    # 自車(Ego Vehicle)のセットアップ
    self.ego_vehicle = None
    if self.ego_vehicle_data:
      print('=========== EGO VEHICLE ===========')
      print(self.ego_vehicle_data)
      self.ego_vehicle = Vehicle(self.ego_vehicle_data.name, model=self.ego_vehicle_data.model, color=self.ego_vehicle_data.color)
      self.scenario.add_vehicle(self.ego_vehicle, pos=self.ego_vehicle_data.pos, rot_quat=self.ego_vehicle_data.rot_quat)
    
    # NPC 車両のセットアップ
    self.npc_vehicles = []
    print('=========== NPC VEHICLES ===========')
    for vehicle_data in self.npc_vehicles_data:
      print(vehicle_data)
      vehicle = Vehicle(vehicle_data.name, model=vehicle_data.model, color=vehicle_data.color)
      self.scenario.add_vehicle(vehicle, pos=vehicle_data.pos, rot_quat=vehicle_data.rot_quat)
      self.npc_vehicles.append(vehicle)
      
    # BeamNGの実行
    self.scenario.make(self.bng)
    
    self.bng.settings.set_deterministic(60)
    self.bng.scenario.load(self.scenario)
    self.bng.ui.hide_hud()
    self.bng.scenario.start()
    self.bng.control.pause()
    
    # センサーのセットアップ
    self.lidars = []
    print('=========== LIDAR ===========')
    for l in self.lidar_data:
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
    print('=========== CAMERA ===========')
    for c in self.camera_data:
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
      
    self.ego_vehicle.sensors.attach('electrics', Electrics())
      
    # action_space, observation_space の設定
    self.action_space = self._action_space()
    print('=========== ACTION SPACE ===========')    
    print(self.action_space)
    print()

    self.observation_space = self._observation_space(self.lidars, self.cameras)
    print('=========== OBSERVATION SPACE ===========')
    for key, space in self.observation_space.spaces.items():
      print(f"{key}: {space}")
    
    self._make_observation(self.ego_vehicle.sensors, self.lidars, self.cameras)
    
  def reset(self):
    """
    環境をリセットし、初期状態を返す
    """
    
    # 自車(Ego Vehicle)のリセット
    self.ego_vehicle.control(throttle=0.0, brake=0.0, steering=0.0)
    self.ego_vehicle.teleport(pos=self.ego_vehicle_data.pos, rot_quat=self.ego_vehicle_data.rot_quat, reset=True)
    
    # NPC 車両のリセット
    for npc_vehicle, npc_data in zip(self.npc_vehicles, self.npc_vehicles_data):
      npc_vehicle.control(throttle=0.0, brake=0.0, steering=0.0)
      npc_vehicle.teleport(pos=npc_data.pos, rot_quat=npc_data.rot_quat, reset=True)
      
    time.sleep(2)
    
    self.bng.scenario.restart() # シナリオのリスタート、一時的に追加した車両が削除
    self.bng.control.step(30) # シナリオを少し進めて、車両を安定させる
    self.bng.control.pause() # シナリオを一時停止
    self.ego_vehicle.set_shift_mode('realistic_automatic')
    self.ego_vehicle.control(gear=2)
    
    observation = self._make_observation(self.ego_vehicle.sensors, self.lidars, self.cameras)
    
    info = {}
    
    return observation, info
    
  def step(self, action):
    """
    アクションを受け取って次の状態と報酬を計算する
    """
    
    throttle, brake, steering = action
    self.ego_vehicle.control(throttle=throttle, brake=brake, steering=steering)
    
    self.bng.step(30)
    
    observation = self._make_observation(self.ego_vehicle.sensors, self.lidars, self.cameras)
    
    # 報酬は環境を利用する側で設定
    reward = 0.0
    
    # 終了条件を設定
    done = False
    
    # その他の情報
    info = {}
    
    return observation, reward, done, info
    
  def render(self):    
    """
    環境を可視化
    """
    
  def close(self):
    """
    環境を閉じる
    """
    self.bng.close()
    
  def _action_space(self):
    """
    環境で取りうるアクションのスペースを返す
    throttle: 0.0 ~ 1.0
    brake: 0.0 ~ 1.0
    steering: -1.0 ~ 1.0
    """
    
    action_lo = np.array([0.0, 0.0, -1.0], dtype=np.float32)
    action_hi = np.array([1.0, 1.0, 1.0], dtype=np.float32)
    
    return Box(low=np.array(action_lo), high=np.array(action_hi), dtype=np.float32)  
    
  def _observation_space(self, lidars, cameras):
    """
    環境から取得できる値のスペースを返す
    使用するセンサーの数によって変更される

    throttle: 0.0 ~ 1.0
    brake: 0.0 ~ 1.0
    steering: -1.0 ~ 1.0
    speed: 0.0 ~ 100.0

    lidar: (-inf, inf) 固定
    camera: resolution に基づいて (height, width, 4)
    """
    
    obs_lo = np.array([0.0, 0.0, -1.0, 0.0], dtype=np.float32)
    obs_hi = np.array([1.0, 1.0, 1.0, 100.0], dtype=np.float32)
    
    space_dict = {
      "vehicle": Box(low=np.array(obs_lo), high=np.array(obs_hi), dtype=np.float32),
    }

    # LiDARの数に応じて space に追加
    for i, _ in enumerate(lidars):
      space_dict[f"lidar_{i}"] = Box(low=-np.inf, high=np.inf, shape=(2000000, 3), dtype=np.float32)

    # カメラの数と解像度に応じて space に追加
    for i, cam in enumerate(cameras):
      width, height = cam.resolution  # width, height の順番で格納されている
      space_dict[f"camera_{i}"] = Box(low=0, high=255, shape=(height, width, 4), dtype=np.uint8)
    
    return Dict(space_dict)
  
  def _make_observation(self, sensors, lidars, cameras):
    """"
    センサーから取得したデータをobservation_spaceに従って整形して返す
    """
    
    self.ego_vehicle.sensors.poll()
    electrics = sensors['electrics']
    state = sensors['state']
    
    # print("Electrics Keys:", electrics.keys())
    # print("State Keys:", state.keys())
    
    throttle = electrics['throttle']
    brake = electrics['brake']
    steering = electrics['steering']
    # print("Throttle:", throttle)
    # print("Brake:", brake)
    # print("Steering:", steering)
    velocity = np.linalg.norm(np.array(state['vel']))
    
    observation = {
      "vehicle": np.array([throttle, brake, steering, velocity], dtype=np.float32)
    }
    
    MAX_POINTS = 2000000
    for i, lidar in enumerate(lidars):
      pointcloud = np.array(lidar.poll()['pointCloud'], dtype=np.float32)
  
      # ポイントクラウドの数が MAX_POINTS より少ない場合はパディング
      if pointcloud.shape[0] < MAX_POINTS:
        pad = np.zeros((MAX_POINTS - pointcloud.shape[0], pointcloud.shape[1]), dtype=np.float32)
        pointcloud = np.concatenate([pointcloud, pad], axis=0)
      else:
        pointcloud = pointcloud[:MAX_POINTS, :]
  
      observation[f"lidar_{i}"] = pointcloud
      
    for i, camera in enumerate(cameras):
      raw_data = camera.stream_raw()['colour']  # 共有メモリからバイナリデータ取得
      image_data = np.frombuffer(raw_data, dtype=np.uint8)  # NumPy配列に変換
      width, height = camera.resolution  # カメラの解像度を取得
      image = image_data.reshape((height, width, 4))  # RGBA (H, W, 4) にリシェイプ
      observation[f"camera_{i}"] = image[:, :, :3]  # RGBのみ取得
      
    return observation
    
if __name__ == '__main__':
  env = BeamNGEnv()
    
    