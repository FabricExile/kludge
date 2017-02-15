#
# Copyright (c) 2010-2017 Fabric Software Inc. All rights reserved.
#

from value_name import ValueName

class ConvCodec:

  def __init__(self, dqti, cpp_value_name):
    self.type_info = dqti.type_info
    self.value_name = cpp_value_name
    self.is_mutable_indirect = dqti.dir_qual.is_mutable_indirect
    self.is_pointer = dqti.dir_qual.is_pointer
    self.is_reference = dqti.dir_qual.is_reference
    self.is_mutable_ref = dqti.dir_qual.is_mutable_ref
    self.is_mutable_ptr = dqti.dir_qual.is_mutable_ptr
    self.child = []
    for i in range(0, len(self.type_info.child_dqtis)):
      self.child.append(
        ConvCodec(
          self.type_info.child_dqtis[i],
          cpp_value_name.child(i)
          )
        )
  
  @property
  def will_promote(self):
    return self.type_info.will_promote

  @property
  def base_type_info(self):
    return self.type_info.base_type_info
  
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
  def make_safe_lib_name(name):
    if name.startswith("_KLUDGE_LIB_"):
      return name
    else:
      return "_KLUDGE_LIB_" + name

  def _render(self, obj, **kwargs):
    vars = {
      "conv": self,
      }
    vars.update(dict(kwargs))
    return self.type_info._render("conv", obj, "cpp", vars)

  def render_validate_edk(self):
    return self.type_info._render("repr", "validate_edk", "cpp", {
      "type_info": self.type_info,
      "value_name": self.value_name,
      })

  def render_edk_to_lib(self, ind_name="__i"):
    return self._render("edk_to_lib", ind_name=ind_name)

  def render_edk_to_lib_decl(self):
    return '\n'.join([
      self.render_validate_edk(),
      self._render("edk_to_lib_decl"),
      ])

  def render_lib_to_edk(self, ind_name="__i"):
    return self._render("lib_to_edk", ind_name=ind_name)

  def render_lib_to_edk_decl(self):
    return self._render("lib_to_edk_decl")

  def render_assign_lib(self, lhs_name, rhs_name, ind_name="__i"):
    return self.type_info._render("repr", "assign_lib", "cpp", {
      "conv": self,
      "lhs_name": lhs_name,
      "rhs_name": rhs_name,
      "ind_name": ind_name,
      })

  def render_assign_edk(self, lhs_name, rhs_name, ind_name="__i"):
    return self.type_info._render("repr", "assign_edk", "cpp", {
      "conv": self,
      "lhs_name": lhs_name,
      "rhs_name": rhs_name,
      "ind_name": ind_name,
      })
