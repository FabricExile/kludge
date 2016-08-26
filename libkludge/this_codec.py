#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

from conv_codec import ConvCodec
from value_name import this_cpp_value_name

class ThisCodec:

  def __init__(self, type_info, is_mutable):
    self.value_name = this_cpp_value_name
    self.type_info = type_info
    self.is_mutable = is_mutable

  def render_param_edk(self):
    return self.type_info._render("self", "param_edk", "cpp", {
      "this": self,
      })

  def render_new(self):
    return self.type_info._render("repr", "new", "cpp", {
      "this": self,
      })

  def render_member_cpp(self, cpp_member_name):
    return self.type_info._render("repr", "member", "cpp", {
      "this": self,
      "cpp_member_name": cpp_member_name,
      })

  def render_delete(self):
    return self.type_info._render("repr", "delete", "cpp", {
      "this": self,
      })
