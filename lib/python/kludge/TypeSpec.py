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

  def __init__(self, unqual_cpp_type_name, qual_cpp_type_name):
    self.unqual = unqual_cpp_type_name
    self.qual = qual_cpp_type_name

class TypeSpec:

  def __init__(
    self,
    kl_base,
    kl_suffix,
    edk_name,
    unqual_cpp_type_name,
    qual_cpp_type_name,
    child_type_infos,
    ):
    self.kl = KLTypeSpec(kl_base, kl_suffix)
    self.edk = EDKTypeSpec(edk_name)
    self.cpp = CPPTypeSpec(unqual_cpp_type_name, qual_cpp_type_name)
    self.child_type_infos = child_type_infos

class SimpleTypeSpec(TypeSpec):

  def __init__(
    self,
    kl_name,
    unqual_cpp_type_name,
    qual_cpp_type_name,
    ):
    TypeSpec.__init__(
      self,
      kl_name,
      "",
      kl_name,
      unqual_cpp_type_name,
      qual_cpp_type_name,
      [],
      )

  @staticmethod
  def builder(kl_name, unqual_cpp_type_name):
    return lambda qual_cpp_type_name: SimpleTypeSpec(
      kl_name,
      unqual_cpp_type_name,
      qual_cpp_type_name,
      )
