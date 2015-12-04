from kludge.CPPTypeExpr import *

class KLTypeSpec:

  def __init__(self, base, suffix):
    self.base = base
    self.suffix = suffix

  @property
  def compound(self):
    return self.base + self.suffix

class EDKTypeSpec:

  def __init__(self, name):
    self.name = name

class CPPTypeSpec:

  def __init__(self, cpp_type_name):
    self.name = cpp_type_name

class TypeSpec:

  def __init__(
    self,
    kl_base,
    kl_suffix,
    edk_name,
    cpp_type_name,
    child_type_infos,
    ):
    self.kl = KLTypeSpec(kl_base, kl_suffix)
    self.edk = EDKTypeSpec(edk_name)
    self.cpp = CPPTypeSpec(cpp_type_name)
    self.child_type_infos = child_type_infos

  @staticmethod
  def builder(
    kl_base,
    kl_suffix,
    edk_name,
    child_type_infos,
    ):
    return lambda cpp_type_name: TypeSpec(
      kl_base,
      kl_suffix,
      edk_name,
      cpp_type_name,
      child_type_infos,
      )

class SimpleTypeSpec(TypeSpec):

  def __init__(
    self,
    kl_name,
    cpp_type_name,
    ):
    TypeSpec.__init__(
      self,
      kl_name,
      "",
      kl_name,
      cpp_type_name,
      [],
      )

  @staticmethod
  def builder(kl_name):
    return lambda cpp_type_name: SimpleTypeSpec(
      kl_name,
      cpp_type_name,
      )
