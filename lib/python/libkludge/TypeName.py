class TypeName:

  class KL:

    def __init__(self, base, suffix):
      self.base = base
      self.suffix = suffix
      self.compound = base + suffix

  def __init__(self, kl_base, kl_suffix, edk_name, cpp_name):
    self.kl = TypeName.KL(kl_base, kl_suffix)
    self.edk = edk_name
    self.cpp = cpp_name


class SimpleTypeName(TypeName):

  def __init__(self, kl_name, cpp_name):
    TypeName.__init__(self, kl_name, "", kl_name, cpp_name)
