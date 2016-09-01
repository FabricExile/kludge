#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

from conv_codec import ConvCodec
from value_name import this_cpp_value_name

class ThisCodec:

  def __init__(
    self,
    type_info,
    members,
    is_mutable,
    extends_this = None,
    ):
    self.value_name = this_cpp_value_name
    self.type_info = type_info
    self.members = members
    self.is_mutable = is_mutable
    self.extends_this = extends_this

  @property
  def base_this(self):
    if self.extends_this:
      return self.extends_this.base_this
    return self

  def render_param_edk(self):
    return self.type_info._render("self", "param_edk", "cpp", {
      "this": self,
      })

  def render_defn_kl(self):
    return self.type_info._render("repr", "defn_kl", "kl", {
      "this": self,
      })

  def render_defn_edk(self):
    return self.type_info._render("repr", "defn_edk", "cpp", {
      "this": self,
      })

  def render_simple_ass_op(self, param):
    return self.type_info._render("repr", "simple_ass_op", "cpp", {
      "this": self,
      "param": param,
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

  def render_class_name(self):
    return self.type_info._render("repr", "class_name", "cpp", {
      "this": self,
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
      })

  def render_delete(self):
    return self.type_info._render("repr", "delete", "cpp", {
      "this": self,
      })
