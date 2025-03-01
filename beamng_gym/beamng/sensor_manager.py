from beamngpy.sensors import Lidar, Camera, Electrics
import numpy as np

class SensorManager:
  def __init__(self, bng, ego_vehicle, lidar_data, camera_data):
    self.lidars = []
    self.cameras = []
    
    for l in lidar_data:
      lidar = Lidar(
        l.name,
        bng,
        ego_vehicle,
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
      
    for c in camera_data:
      camera = Camera(
        c.name,
        bng,
        ego_vehicle,
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
      
  def get_sensor_data(self):
    lidar_data = {f"lidar_{i}": lidar.poll() for i, lidar in enumerate(self.lidars)}
    camera_data = {f"camera_{i}": camera.stream_raw() for i, camera in enumerate(self.cameras)}
    return lidar_data, camera_data
