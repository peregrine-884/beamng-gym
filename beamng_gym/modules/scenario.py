# 走行するMAP
class Scenario:
  def __init__(self, level, name):
    self.level = level
    self.name = name
    self.vehicles = []
    
  def __repr__(self):
    return F"Scenario(Level: {self.level}, Name: {self.name})\n"
  
# 使用する車両
class Vehicle:
  def __init__(self, name, model, color, pos, rot_quat):
    self.name = name
    self.model = model
    self.color = color
    self.pos = pos
    self.rot_quat = rot_quat
    
  def __repr__(self):
    return F"Vehicle(Name: {self.name}, Model: {self.model}, Color: {self.color}, Pos: {self.pos}, Rot_Quat: {self.rot_quat})\n"
  
# 使用するセンサー
class Lidar:
  def __init__(self, name, requested_update_time, pos, dir, up, vertical_resolution,
                horizontal_angle, is_rotate_mode, is_360_mode, is_using_shared_memory,
                is_visualised, is_streaming, is_dir_world_space):
    self.name = name
    self.requested_update_time = requested_update_time
    self.pos = pos
    self.dir = dir
    self.up = up
    self.vertical_resolution = vertical_resolution
    self.horizontal_angle = horizontal_angle
    self.is_rotate_mode = is_rotate_mode
    self.is_360_mode = is_360_mode
    self.is_using_shared_memory = is_using_shared_memory
    self.is_visualised = is_visualised
    self.is_streaming = is_streaming
    self.is_dir_world_space = is_dir_world_space

  def __repr__(self):
    return (f"Name: {self.name}\n"
            f"Requested Update Time: {self.requested_update_time}, Pos: {self.pos}, Dir: {self.dir}, "
            f"Up: {self.up}, Vertical Resolution: {self.vertical_resolution}, Horizontal Angle: {self.horizontal_angle}, "
            f"Is Rotate Mode: {self.is_rotate_mode}, Is 360 Mode: {self.is_360_mode}, Is Using Shared Memory: {self.is_using_shared_memory}, "
            f"Is Visualised: {self.is_visualised}, Is Streaming: {self.is_streaming}, Is Dir World Space: {self.is_dir_world_space})\n")


class Camera:
  def __init__(self, name, requested_update_time, pos, dir, up, resolution, near_far_planes,
                is_using_shared_memory, is_render_annotations, is_render_instance,
                is_render_depth, is_visualised, is_streaming, is_dir_world_space):
    self.name = name
    self.requested_update_time = requested_update_time
    self.pos = pos
    self.dir = dir
    self.up = up
    self.resolution = resolution
    self.near_far_planes = near_far_planes
    self.is_using_shared_memory = is_using_shared_memory
    self.is_render_annotations = is_render_annotations
    self.is_render_instance = is_render_instance
    self.is_render_depth = is_render_depth
    self.is_visualised = is_visualised
    self.is_streaming = is_streaming
    self.is_dir_world_space = is_dir_world_space

  def __repr__(self):
    return (f"Name: {self.name}\n"
            f"Requested Update Time: {self.requested_update_time}, Pos: {self.pos}, Dir: {self.dir}, "
            f"Up: {self.up}, Resolution: {self.resolution}, Near-Far Planes: {self.near_far_planes}, "
            f"Is Using Shared Memory: {self.is_using_shared_memory}, Is Render Annotations: {self.is_render_annotations}, "
            f"Is Render Instance: {self.is_render_instance}, Is Render Depth: {self.is_render_depth}, "
            f"Is Visualised: {self.is_visualised}, Is Streaming: {self.is_streaming}, Is Dir World Space: {self.is_dir_world_space})\n")
