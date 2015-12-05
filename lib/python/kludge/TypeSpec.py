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

  def __init__(self, unqual_cpp_type_name, cpp_type_expr):
    self.name = unqual_cpp_type_name
    self.expr = cpp_type_expr

  @property
  def qual_name(self):
    return str(self.expr)

class TypeSpec:

  def __init__(
    self,
    kl_base,
    kl_suffix,
    edk_name,
    unqual_cpp_type_name,
    cpp_type_expr,
    child_type_infos,
    ):
    self.kl = KLTypeSpec(kl_base, kl_suffix)
    self.edk = EDKTypeSpec(edk_name)
    self.cpp = CPPTypeSpec(unqual_cpp_type_name, cpp_type_expr)
    self.child_type_infos = child_type_infos

class SimpleTypeSpec(TypeSpec):

  def __init__(
    self,
    kl_name,
    unqual_cpp_type_name,
    cpp_type_expr,
    ):
    TypeSpec.__init__(
      self,
      kl_name,
      "",
      kl_name,
      unqual_cpp_type_name,
      cpp_type_expr,
      [],
      )

  @staticmethod
  def builder(kl_name, unqual_cpp_type_name):
    return lambda cpp_type_expr: SimpleTypeSpec(
      kl_name,
      unqual_cpp_type_name,
      cpp_type_expr,
      )
