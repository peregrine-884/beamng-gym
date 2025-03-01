import numpy as np
from gymnasium.spaces import Box

# Global variable to store the action space (initialized as None)
action_space = None

def initialize_action_space():
  """
  Initializes and returns the action space for the environment.

  - throttle: 0.0 ~ 1.0
  - brake: 0.0 ~ 1.0
  - steering: -1.0 ~ 1.0

  Returns:
      Box: A Gymnasium Box space representing the valid action range.
  """
  global action_space
  
  action_lo = np.array([0.0, 0.0, -1.0], dtype=np.float32)
  action_hi = np.array([1.0, 1.0, 1.0], dtype=np.float32)
  
  action_space = Box(low=action_lo, high=action_hi, dtype=np.float32)
  
  print('======= Action Space =======')
  print(action_space)
  
  return action_space

def get_action_space():
  """
  Returns the globally stored action space.

  Returns:
      Box: The current action space.

  Raises:
      ValueError: If the action space has not been initialized.
  """
  global action_space
  if action_space is None:
    raise ValueError("Action space is not initialized. Call initialize_action_space() first.")
  return action_space

def apply_action(vehicle, action):
  """
  Applies the given action to the vehicle.

  Args:
      vehicle: BeamNGpy Vehicle object.
      action: Tuple of (throttle, brake, steering).

  Raises:
      ValueError: If the action space has not been initialized.
  """
  global action_space
  if action_space is None:
    raise ValueError("Action space is not initialized. Call initialize_action_space() first.")

  # Clip the action values within the defined action space range
  action = np.clip(action, action_space.low, action_space.high)
  
  throttle, brake, steering = action
  vehicle.control(throttle=throttle, brake=brake, steering=steering)
