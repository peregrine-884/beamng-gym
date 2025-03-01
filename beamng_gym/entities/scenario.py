class Scenario:
  def __init__(self, level, name):
    self.level = level
    self.name = name
    
  @classmethod
  def from_dict(cls, data):
    return cls(data['level'], data['name'])
  
  def __repr__(self):
    return F"Scenario(Level: {self.level}, Name: {self.name})\n"