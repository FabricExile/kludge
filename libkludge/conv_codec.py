#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

from value_name import ValueName

class ConvCodec:

  def __init__(self, dqti, cpp_value_name):
    self.type_info = dqti.type_info
    self.value_name = cpp_value_name
    self.is_mutable_indirect = dqti.dir_qual.is_mutable_indirect
    self.is_pointer = dqti.dir_qual.is_pointer
    self.child = []
    for i in range(0, len(self.type_info.child_dqtis)):
      self.child.append(
        ConvCodec(
          self.type_info.child_dqtis[i],
          cpp_value_name.child(i)
          )
        )
  
  @property
  def reference_prefix(self):
    if self.is_mutable_indirect:
      return "&"
    else:
      return "const &"
  
  @property
  def take_pointer_prefix(self):
    if self.is_pointer:
      return "&"
    else:
      return ""
  
  @property
  def deref_pointer_prefix(self):
    if self.is_pointer:
      return "*"
    else:
      return ""
  
  @staticmethod
  def make_safe_edk_name_toplevel(name):
    if name.startswith("_KLUDGE_EDK_"):
      return name
    else:
      return "_KLUDGE_EDK_" + name

  @staticmethod
  def make_safe_lib_name(name):
    if name.startswith("_KLUDGE_LIB_"):
      return name
    else:
      return "_KLUDGE_LIB_" + name

  def _render(self, obj):
    return self.type_info._render("conv", obj, "cpp", {
      "conv": self,
      })

  def render_edk_to_lib(self):
    return self._render("edk_to_lib")

  def render_edk_to_lib_decl(self):
    return self._render("edk_to_lib_decl")

  def render_lib_to_edk(self):
    return self._render("lib_to_edk")

  def render_lib_to_edk_decl(self):
    return self._render("lib_to_edk_decl")
