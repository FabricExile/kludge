#
# Copyright (c) 2010-2017 Fabric Software Inc. All rights reserved.
#

from conv_codec import ConvCodec
from value_name import result_cpp_value_name

class ResultCodec:

  def __init__(self, dqti):
    self.value_name = result_cpp_value_name
    self.is_pointer = dqti.dir_qual.is_pointer
    self.is_reference = dqti.dir_qual.is_reference
    self.is_mutable_ref = dqti.dir_qual.is_mutable_ref
    self.is_mutable_ptr = dqti.dir_qual.is_mutable_ptr
    self.conv = ConvCodec(dqti, result_cpp_value_name)

  @property
  def will_promote(self):
    return self.conv.will_promote
  
  @property
  def type_info(self):
    return self.conv.type_info
  
  @property
  def base_type_info(self):
    return self.conv.base_type_info
  
  @property
  def reference_prefix(self):
    return self.conv.reference_prefix
  
  @property
  def take_pointer_prefix(self):
    return self.conv.take_pointer_prefix
  
  @property
  def deref_pointer_prefix(self):
    return self.conv.deref_pointer_prefix

  def _render(self, obj, lang):
    return self.conv.type_info._render("result", obj, lang, {
      "result": self,
      })

  def render_type_kl(self):
    return self._render("type_kl", "kl")

  def render_return_kl(self):
    return self._render("return_kl", "kl")

  def render_direct_type_edk(self):
    return self._render("direct_type_edk", "cpp")

  def render_indirect_param_edk(self):
    return self._render("indirect_param_edk", "cpp")

  def render_indirect_init_edk(self):
    return self._render("indirect_init_edk", "cpp")

  def render_decl_lib(self):
    return self._render("decl_lib", "cpp")

  def render_decl_and_assign_lib_begin(self):
    return self._render("decl_and_assign_lib_begin", "cpp")

  def render_decl_and_assign_lib_end(self):
    return self._render("decl_and_assign_lib_end", "cpp")

  def render_indirect_lib_to_edk(self):
    return self._render("indirect_lib_to_edk", "cpp")

  def render_direct_return_edk(self):
    return self._render("direct_return_edk", "cpp")
