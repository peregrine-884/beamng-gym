def str_to_bool(value):
  return value.lower() == 'true' if isinstance(value, str) else value