#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

from conv_codec import ConvCodec
from value_name import this_cpp_value_name

class ThisCodec:

  def __init__(self, type_codec, is_mutable):
    self.value_name = this_cpp_value_name
    self.type = type_codec
    self.is_mutable = is_mutable

  @property
  def type_info(self):
    return self.type.type_info

  def render_param_edk(self):
    return self.type._render("self", "param_edk", "cpp", {
      "this": self,
      })
