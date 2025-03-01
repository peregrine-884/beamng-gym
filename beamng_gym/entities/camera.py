from beamng_gym.entities.z_utils import str_to_bool

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

  @classmethod
  def from_dict(cls, data):
    return cls(
      data['name'], data['requested_update_time'], data['pos'], data['dir'], data['up'],
      data['resolution'], data['near_far_planes'],
      str_to_bool(data['is_using_shared_memory']),
      str_to_bool(data['is_render_annotations']),
      str_to_bool(data['is_render_instance']),
      str_to_bool(data['is_render_depth']),
      str_to_bool(data['is_visualised']),
      str_to_bool(data['is_streaming']),
      str_to_bool(data['is_dir_world_space'])
    )

  def __repr__(self):
    return (f"Name: {self.name}\n"
            f"Requested Update Time: {self.requested_update_time}, Pos: {self.pos}, Dir: {self.dir}, "
            f"Up: {self.up}, Resolution: {self.resolution}, Near-Far Planes: {self.near_far_planes}, "
            f"Is Using Shared Memory: {self.is_using_shared_memory}, Is Render Annotations: {self.is_render_annotations}, "
            f"Is Render Instance: {self.is_render_instance}, Is Render Depth: {self.is_render_depth}, "
            f"Is Visualised: {self.is_visualised}, Is Streaming: {self.is_streaming}, Is Dir World Space: {self.is_dir_world_space})\n")