class ValueName:

  def __init__(self, kl_name):
    self.kl = kl_name

  @property
  def edk(self):
      return "_KLUDGE_EDK_" + self.kl

  @property
  def cpp(self):
      return "_KLUDGE_CPP_" + self.kl
