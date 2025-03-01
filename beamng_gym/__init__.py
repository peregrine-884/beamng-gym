from gymnasium.envs.registration import register

# Register the custom environment in Gymnasium
register(
    id="BeamNG-v0", # Environment ID (used in gym.make("BeamNG-v0"))
    entry_point="beamng_gym.env:BeamNGEnv", # Path to the custom environment class
)
