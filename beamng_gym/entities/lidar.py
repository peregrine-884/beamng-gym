from beamng_gym.entities.z_utils import str_to_bool

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

  @classmethod
  def from_dict(cls, data):
    return cls(
      data['name'], data['requested_update_time'], data['pos'], data['dir'], data['up'],
      data['vertical_resolution'], data['horizontal_angle'],
      str_to_bool(data['is_rotate_mode']),
      str_to_bool(data['is_360_mode']),
      str_to_bool(data['is_using_shared_memory']),
      str_to_bool(data['is_visualised']),
      str_to_bool(data['is_streaming']),
      str_to_bool(data['is_dir_world_space'])
    )

  def __repr__(self):
    return (f"Name: {self.name}\n"
            f"Requested Update Time: {self.requested_update_time}, Pos: {self.pos}, Dir: {self.dir}, "
            f"Up: {self.up}, Vertical Resolution: {self.vertical_resolution}, Horizontal Angle: {self.horizontal_angle}, "
            f"Is Rotate Mode: {self.is_rotate_mode}, Is 360 Mode: {self.is_360_mode}, Is Using Shared Memory: {self.is_using_shared_memory}, "
            f"Is Visualised: {self.is_visualised}, Is Streaming: {self.is_streaming}, Is Dir World Space: {self.is_dir_world_space})\n")