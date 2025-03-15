import numpy as np
from gymnasium.spaces import Box, Dict

# Global variable to store the observation space (initialized as None)
observation_space = None

def initialize_observation_space(sensor_manager):
  """
  Initializes and returns the observation space.
  This function defines the space dynamically based on the number of sensors.

  - throttle: 0.0 ~ 1.0
  - brake: 0.0 ~ 1.0
  - steering: -1.0 ~ 1.0
  - speed: 0.0 ~ 100.0
  - LiDAR: (-inf, inf), fixed shape
  - Camera: Shape based on resolution (height, width, 4)

  Args:
      sensor_manager (SensorManager): SensorManager instance containing sensors.

  Returns:
      Dict: A dictionary of observation spaces for each sensor.
  """
  global observation_space

  # Define the range of vehicle-related observations
  obs_lo = np.array([0.0, 0.0, -1.0, 0.0], dtype=np.float32)
  obs_hi = np.array([1.0, 1.0, 1.0, 100.0], dtype=np.float32)

  # Initialize the observation space dictionary
  space_dict = {
    "vehicle": Box(low=obs_lo, high=obs_hi, dtype=np.float32),
  }

  # Add LiDAR sensors to the observation space
  for i, _ in enumerate(sensor_manager.lidars):
    space_dict[f"lidar_{i}"] = Box(low=-np.inf, high=np.inf, shape=(2000000, 3), dtype=np.float32)

  # Add camera sensors to the observation space based on resolution
  for i, cam in enumerate(sensor_manager.cameras):
    width, height = cam.resolution  # Stored as (width, height)
    space_dict[f"camera_{i}"] = Box(low=0, high=255, shape=(height, width, 4), dtype=np.uint8)

  # Store the observation space globally
  observation_space = Dict(space_dict)
  
  print('======= Observation Space =======')
  for key, value in observation_space.spaces.items():
    print(f"{key}: {value}")
  
  return observation_space

def get_observation_space():
  """
  Returns the globally stored observation space.

  Returns:
      Dict: The current observation space.

  Raises:
      ValueError: If the observation space has not been initialized.
  """
  global observation_space
  if observation_space is None:
    raise ValueError("Observation space is not initialized. Call initialize_observation_space() first.")
  return observation_space


def make_observation(vehicle_data, sensor_data):
  """
  Formats sensor data according to the defined observation space.

  Args:
      vehicle_data (dict): Dictionary containing vehicle state and electrics data.
      sensor_data (dict): Dictionary containing LiDAR and camera sensor data.

  Returns:
      dict: Formatted observation data.
  """

  global observation_space
  if observation_space is None:
    raise ValueError("Observation space is not initialized. Call initialize_observation_space() first.")

  # Extract vehicle control and state data
  electrics = vehicle_data["electrics"]
  state = vehicle_data["state"]
  
  throttle = electrics['throttle']
  brake = electrics['brake']
  steering = electrics['steering']
  velocity = np.linalg.norm(np.array(state['vel']))
  
  # Create the observation dictionary
  observation = {
    "vehicle": np.array([throttle, brake, steering, velocity], dtype=np.float32)
  }
  
  # Clip vehicle data to match the observation space constraints
  observation["vehicle"] = np.clip(observation["vehicle"], 
                                   observation_space.spaces["vehicle"].low, 
                                   observation_space.spaces["vehicle"].high)

  # Process LiDAR and camera data based on the observation space

  for key in observation_space.spaces:
    if key.startswith("lidar_"):
      i = int(key.split("_")[1])
      pointcloud = np.array(sensor_data[0][f"lidar_{i}"]['pointCloud'], dtype=np.float32)
      
      max_points = observation_space.spaces[key].shape[0]  # Get max points from observation_space
      if pointcloud.shape[0] < max_points:
        pad = np.zeros((max_points - pointcloud.shape[0], 3), dtype=np.float32)
        pointcloud = np.concatenate([pointcloud, pad], axis=0)
      else:
        pointcloud = pointcloud[:max_points, :]
        
      observation[key] = pointcloud
    
    elif key.startswith("camera_"):
      i = int(key.split("_")[1])
      raw_data = sensor_data[1][f"camera_{i}"]['colour']
      image_data = np.frombuffer(raw_data, dtype=np.uint8)
      
      height, width = observation_space.spaces[key].shape[:2]  # Get resolution from observation_space
      image = image_data.reshape((height, width, 4))  # Reshape to (H, W, 4) RGBA format
      observation[key] = np.clip(image[:, :, :3], 0, 255)  # Keep only RGB channels and clip values

  return observation
