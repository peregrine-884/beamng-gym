from beamng_gym.envs.action import *
from beamng_gym.envs.observation import *

def step_environment(beamng_manager, sensor_manager, action):
  """
  Executes a single step in the environment by applying an action and retrieving new observations.

  This function applies the given action to the vehicle, updates the environment state,
  collects sensor data, and returns the updated observation along with reward, done status,
  and additional information.

  Args:
      beamng_manager: An instance of the BeamNG environment manager.
      sensor_manager: An instance of SensorManager that handles LiDAR and Camera sensors.
      action (tuple): The action to apply (throttle, brake, steering).

  Returns:
      tuple: A tuple containing:
          - observation (dict): The updated observation after applying the action.
          - reward (float): The reward for the step (to be implemented).
          - terminated (bool): A flag indicating if the episode has terminated.
          - truncated (bool): A flag indicating if the episode was truncated.
          - info (dict): Additional debugging information.
  """

  # Apply the action to the ego vehicle in the environment
  apply_action(beamng_manager.ego_vehicle, action)
  
  # Step the simulation by 30 steps (equivalent to 0.5 second)
  beamng_manager.step_simulation(6)
  
  # Retrieve updated vehicle state and electrics data
  vehicle_data = beamng_manager.get_vehicle_data()
  
  # Retrieve updated sensor data (LiDAR & Camera)
  sensor_data = sensor_manager.get_sensor_data()
  
  # Format the retrieved data into a structured observation
  observation = make_observation(vehicle_data, sensor_data)
  
  # Reward calculation (to be implemented)
  reward = 0.0  
  
  # Termination condition (to be implemented)
  terminated = beamng_manager.validate_collision(damage_threshold=0.01)
  
  # Truncation condition (to be implemented)
  truncated = False
  
  # Additional information (useful for debugging or extra details)
  info = {}
  
  return observation, reward, terminated, truncated, info
