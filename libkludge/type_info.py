#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

class KLTypeName:

  def __init__(self, base, suffix):
    self.base = base
    self.suffix = suffix

  @property
  def compound(self):
    return self.base + self.suffix

class KLTypeInfo:

  def __init__(self, name_base, name_suffix):
    self.name = KLTypeName(name_base, name_suffix)

class EDKTypeName:

  def __init__(self, toplevel, local):
    self.toplevel = toplevel
    self.local = local

class EDKTypeInfo:

  def __init__(self, name_toplevel, name_local):
    self.name = EDKTypeName(name_toplevel, name_local)

class LibTypeInfo:

  def __init__(self, expr):
    self.name = expr.get_desc()
    self.expr = expr

class TypeInfo:

  def __init__(
    self,
    lib_expr,
    name = None,
    edk_name_toplevel = None,
    edk_name_local = None,
    kl_name_base = None,
    kl_name_suffix = None,
    ):
    if kl_name_base:
      self.kl = KLTypeInfo(kl_name_base, kl_name_suffix)
    else:
      self.kl = KLTypeInfo(name, "")
    if edk_name_toplevel:
      self.edk = EDKTypeInfo(edk_name_toplevel, edk_name_local)
    else:
      self.edk = EDKTypeInfo("::Fabric::EDK::KL::" + name, name)
    self.lib = LibTypeInfo(lib_expr)
