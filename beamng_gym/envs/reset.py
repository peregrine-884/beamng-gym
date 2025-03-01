from beamng_gym.envs.observation import *

def reset_environment(beamng_manager, sensor_manager):
  """
  Resets the environment and returns the initial observation.

  This function resets the BeamNG environment, retrieves the vehicle 
  and sensor data, and formats it into an observation that follows 
  the defined observation space.

  Args:
      beamng_manager: An instance of the BeamNG environment manager.
      sensor_manager: An instance of SensorManager that handles LiDAR and Camera sensors.

  Returns:
      tuple: A tuple containing:
          - observation (dict): The initial observation formatted based on sensor data.
          - info (dict): Additional information (empty by default).
  """

  # Reset the BeamNG environment to its initial state
  beamng_manager.reset()
  
  # Retrieve vehicle state and electrics data
  vehicle_data = beamng_manager.get_vehicle_data()
  
  # Retrieve sensor data from the SensorManager (LiDAR & Camera)
  sensor_data = sensor_manager.get_sensor_data()
  
  # Format the retrieved data into a structured observation
  observation = make_observation(vehicle_data, sensor_data)
  
  # Additional information (can be used for debugging or extra details)
  info = {}
  
  return observation, info
