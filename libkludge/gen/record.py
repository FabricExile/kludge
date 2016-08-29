#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

from decl import Decl
from test import Test
from libkludge.cpp_type_expr_parser import Void, Named
from libkludge.value_name import this_cpp_value_name
from libkludge.this_codec import ThisCodec
from libkludge.result_codec import ResultCodec
from libkludge.param_codec import ParamCodec
import hashlib

class Record(Decl):

  public = 0
  protected = 1
  private = 2

  def __init__(
    self,
    ext,
    desc,
    kl_type_name,
    this_type_info,
    base_classes,
    block_empty_ctor = False,
    include_getters_setters = True,
    include_dtor = True,
    ):
    Decl.__init__(self, ext, desc)

    self.members = []
    self.ctors = []
    self.methods = []

    self.nested_name = [kl_type_name]
    self.kl_type_name = kl_type_name
    self.this_value_name = this_cpp_value_name
    self.this_type_info = this_type_info
    self.const_this = ThisCodec(this_type_info, self.members, False)
    self.mutable_this = ThisCodec(this_type_info, self.members, True)
    self.base_classes = base_classes
    self.default_access = self.public
    self.block_empty_ctor = block_empty_ctor
    self.include_getters_setters = include_getters_setters
    self.include_dtor = include_dtor

  def set_default_access(self, access):
    self.default_access = access

  class Member(object):

    def __init__(self, record, cpp_name, dqti, getter_kl_name, setter_kl_name, access):
      self._record = record
      self.cpp_name = cpp_name
      self.kl_name = cpp_name
      self.type_info = dqti.type_info
      self.result = ResultCodec(dqti)
      self.param = ParamCodec(dqti, cpp_name)
      self.getter_kl_name = getter_kl_name
      if not self.getter_kl_name is None and self.getter_kl_name == '':
        self.getter_kl_name = 'get_' + cpp_name
      self.setter_kl_name = setter_kl_name
      if not self.setter_kl_name is None and self.setter_kl_name == '':
        self.setter_kl_name = 'set_' + cpp_name
      self.access = access

    def has_getter(self):
      return self.getter_kl_name is not None

    def has_setter(self):
      return self.setter_kl_name is not None

    def is_public(self):
      return self.access == self._record.public
    
  def add_member(self, cpp_name, cpp_type_name, getter='', setter='', access=None):
    if access is None:
      access = self.default_access
    cpp_type_expr = self.ext.cpp_type_expr_parser.parse(cpp_type_name)
    dqti = self.ext.type_mgr.get_dqti(cpp_type_expr)
    member = self.Member(self, cpp_name, dqti, getter, setter, access=access)
    self.members.append(member)
    return self

  class Ctor(object):

    def __init__(self, record):
      self._record = record
      self._nested_function_name = record.nested_name + ['__ctor__']
      self.result = None
      self.this = self._record.mutable_this
      self.params = []

    @property
    def ext(self):
      return self._record.ext
    
    @property
    def edk_symbol_name(self):
      h = hashlib.md5()
      for name in self._nested_function_name:
        h.update(name)
      for param in self.params:
        h.update(param.type_info.edk.name.toplevel)
      return "_".join([self.ext.name] + self._nested_function_name + [h.hexdigest()])

    def get_test_name(self):
      return self.edk_symbol_name

    def add_param(self, cpp_type_name, name = None):
      if not isinstance(name, basestring):
        name = "arg%d" % len(self.params)
      self.params.append(
        ParamCodec(
          self.ext.type_mgr.get_dqti(
            self.ext.cpp_type_expr_parser.parse(cpp_type_name)
            ),
          name
          )
        )
      return self
    
    def add_test(self, kl, out):
      self._record.tests.append(Test(
        self.get_test_name() + '_' + str(len(self._record.tests)),
        self.ext.jinjenv, kl, out,
        ))
  
  def add_ctor(self, param_cpp_type_names = []):
    ctor = self.Ctor(self)
    for param_cpp_type_name in param_cpp_type_names:
      ctor.add_param(param_cpp_type_name)
    self.ctors.append(ctor)
    return ctor

  class Method(object):

    def __init__(self, record, cpp_name):
      self._record = record
      self._nested_function_name = record.nested_name + [cpp_name]
      self.result = ResultCodec(self.ext.type_mgr.get_dqti(Void()))
      self.cpp_name = cpp_name
      self.this = self._record.mutable_this
      self.params = []

    @property
    def ext(self):
      return self._record.ext
    
    @property
    def kl_name(self):
      return self.cpp_name
    
    @property
    def edk_symbol_name(self):
      h = hashlib.md5()
      for name in self._nested_function_name:
        h.update(name)
      for param in self.params:
        h.update(param.type_info.edk.name.toplevel)
      return "_".join([self.ext.name] + self._nested_function_name + [h.hexdigest()])

    def get_test_name(self):
      return self.edk_symbol_name

    def returns(self, cpp_type_name):
      self.result = ResultCodec(
        self.ext.type_mgr.get_dqti(
          self.ext.cpp_type_expr_parser.parse(cpp_type_name)
          )
        )
      return self

    def add_param(self, cpp_type_name, cpp_name = None):
      if not isinstance(cpp_name, basestring):
        cpp_name = "arg%d" % len(self.params)
      self.params.append(
        ParamCodec(
          self.ext.type_mgr.get_dqti(
            self.ext.cpp_type_expr_parser.parse(cpp_type_name)
            ),
          cpp_name
          )
        )
      return self
    
    def add_test(self, kl, out):
      self._record.tests.append(Test(
        self.get_test_name() + '_' + str(len(self._record.tests)),
        self.ext.jinjenv, kl, out,
        ))
  
  def add_method(
    self,
    cpp_name,
    return_cpp_type_name=None,
    param_cpp_type_names=[],
    ):
    method = self.Method(self, cpp_name)
    self.methods.append(method)
    if return_cpp_type_name:
      method.returns(return_cpp_type_name)
    for param_cpp_type_name in param_cpp_type_names:
      method.add_param(param_cpp_type_name)
    return method
  
  @property
  def dtor_edk_symbol_name(self):
    nested_name = self.nested_name + ['__dtor__']
    h = hashlib.md5()
    for name in nested_name:
      h.update(name)
    return "_".join([self.ext.name] + nested_name + [h.hexdigest()])

  def get_kl_name(self):
    return self.kl_type_name

  def get_template_basename(self):
    return 'record'
