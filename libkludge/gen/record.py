#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

from decl import Decl
from libkludge.cpp_type_expr_parser import Named
from libkludge.value_name import this_cpp_value_name
from libkludge.this_codec import ThisCodec
from libkludge.result_codec import ResultCodec
from libkludge.param_codec import ParamCodec

class Record(Decl):
  def __init__(
    self,
    ext,
    desc,
    kl_type_name,
    this_type_info,
    base_classes,
    template_basename,
    block_empty_ctor = False
    ):
    Decl.__init__(self, ext, desc)

    self.kl_type_name = kl_type_name
    self.this_value_name = this_cpp_value_name
    self.this_type_info = this_type_info
    self.const_this = ThisCodec(this_type_info, False)
    self.mutable_this = ThisCodec(this_type_info, True)
    self.base_classes = base_classes
    self.template_basename = template_basename
    self.block_empty_ctor = block_empty_ctor

    self.members = []
    self.ctors = []
    self.methods = []

  class Member(object):

    def __init__(self, cpp_name, dqti, getter_kl_name, setter_kl_name):
      self.cpp_name = cpp_name
      self.type_info = dqti.type_info
      self.result = ResultCodec(dqti)
      self.param = ParamCodec(dqti, cpp_name)
      self.getter_kl_name = getter_kl_name
      if not self.getter_kl_name is None and self.getter_kl_name == '':
        self.getter_kl_name = 'get_' + cpp_name
      self.setter_kl_name = setter_kl_name
      if not self.setter_kl_name is None and self.setter_kl_name == '':
        self.setter_kl_name = 'set_' + cpp_name

    def has_getter(self):
        return self.getter_kl_name is not None

    def has_setter(self):
        return self.setter_kl_name is not None
    
  def add_member(self, cpp_name, cpp_type_name, getter='', setter=''):
    cpp_type_expr = self.ext.cpp_type_expr_parser.parse(cpp_type_name)
    dqti = self.ext.type_mgr.get_dqti(cpp_type_expr)
    member = self.Member(cpp_name, dqti, getter, setter)
    self.members.append(member)
    return self

  def get_kl_name(self):
    return self.kl_type_name

  def get_template_basename(self):
    return self.template_basename
