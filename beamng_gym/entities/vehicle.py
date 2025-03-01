class Vehicle:
  def __init__(self, name, model, color, pos, rot_quat):
    self.name = name
    self.model = model
    self.color = color
    self.pos = pos
    self.rot_quat = rot_quat

  @classmethod
  def from_dict(cls, data):
    return cls(data['name'], data['model'], data['color'], data['pos'], data['rot_quat'])

  def __repr__(self):
    return f"Vehicle(Name: {self.name}, Model: {self.model}, Color: {self.color}, Pos: {self.pos}, Rot_Quat: {self.rot_quat})\n"