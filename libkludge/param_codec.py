#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

from conv_codec import ConvCodec
from value_name import ValueName

class ParamCodec:

  def __init__(self, dqti, name):
    self.value_name = ValueName(name)
    self.conv = ConvCodec(dqti, self.value_name.cpp)

  @property
  def type_info(self):
    return self.conv.type_info

  @property
  def is_mutable(self):
    return self.conv.is_mutable
  
  @property
  def reference_prefix(self):
    return self.conv.reference_prefix
  
  @property
  def make_pointer_prefix(self):
    return self.conv.make_pointer_prefix
  
  @property
  def undo_pointer_prefix(self):
    return self.conv.undo_pointer_prefix

  def _render(self, obj, lang):
    return self.type_info._render("param", obj, lang, {
      "param": self,
      })

  def render_edk(self):
    return self._render("edk", "cpp")

  def render_edk_to_lib_decl(self):
    return self._render("edk_to_lib_decl", "cpp")

  def render_kl(self):
    return self._render("kl", "kl")

  def render_lib(self):
    return self._render("lib", "cpp")

  def render_lib_to_edk(self):
    return self._render("lib_to_edk", "cpp")
