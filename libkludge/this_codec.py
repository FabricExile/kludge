#
# Copyright (c) 2010-2017 Fabric Software Inc. All rights reserved.
#

from conv_codec import ConvCodec
from value_name import this_cpp_value_name
from generate.this_access import ThisAccess

class ThisCodec:

  def __init__(
    self,
    type_info,
    is_mutable,
    ):
    self.value_name = this_cpp_value_name
    self.type_info = type_info
    self.is_mutable = is_mutable

  @property
  def base_type_info(self):
    return self.type_info.base_type_info

  def render_validate_edk(self):
    return self.type_info._render("repr", "validate_edk", "cpp", {
      "value_name": self.value_name,
      "type_info": self.type_info,
      })
  
  def render_param_edk(self):
    return self.type_info._render("self", "param_edk", "cpp", {
      "this": self,
      })

  def render_new_begin(self):
    return self.type_info._render("repr", "new_begin", "cpp", {
      "this": self,
      })

  def render_new_end(self):
    return self.type_info._render("repr", "new_end", "cpp", {
      "this": self,
      })

  def render_empty_ctor(self):
    return self.type_info._render("repr", "empty_ctor", "cpp", {
      "this": self,
      })

  def render_copy_ctor(self, param):
    return self.type_info._render("repr", "copy_ctor", "cpp", {
      "this": self,
      "param": param,
      })

  def render_abstract_copy_ctor_kl(self):
    return self.type_info._render("repr", "abstract_copy_ctor", "kl", {})

  def render_class_name_cpp(self):
    return self.type_info._render("repr", "class_name", "cpp", {
      "this": self,
      })

  def render_simple_ass_op(self, param):
    return self.type_info._render("repr", "simple_ass_op", "cpp", {
      "this": self,
      "param": param,
      })

  def render_wrapper_ref(self):
    return self.type_info._render("repr", "wrapper_ref", "cpp", {
      "this": self,
      })

  def render_ref(self):
    return self.type_info._render("repr", "ref", "cpp", {
      "this": self,
      })

  def render_member_ref(self, cpp_member_name):
    return self.type_info._render("repr", "member_ref", "cpp", {
      "this": self,
      "cpp_member_name": cpp_member_name,
      "member": self.type_info.record.get_member(cpp_member_name),
      "ThisAccess": ThisAccess
      })

  def render_delete(self):
    return self.type_info._render("repr", "delete", "cpp", {
      "this": self
      })
