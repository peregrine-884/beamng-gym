from gymnasium.envs.registration import register

# Register the custom environment in Gymnasium
register(
    id="BeamNG-v0", # Environment ID (used in gym.make("BeamNG-v0"))
    entry_point="beamng_gym.env:BeamNGEnv", # Path to the custom environment class
    kwargs={"config_path": "config/default.json5"}
)
register(
    id="BeamNG-c1-nuscenes",
    entry_point="beamng_gym.env:BeamNGEnv",
    kwargs={"config_path": "config/c1_nuscenes_01.json5"}
)
