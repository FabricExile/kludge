#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

from decl import Decl
from test import Test
from member_access import MemberAccess
from this_access import ThisAccess
from libkludge.cpp_type_expr_parser import Void, Named, DirQual, directions, qualifiers
from libkludge.value_name import this_cpp_value_name
from libkludge.this_codec import ThisCodec
from libkludge.result_codec import ResultCodec
from libkludge.param_codec import ParamCodec
from libkludge.dir_qual_type_info import DirQualTypeInfo
import hashlib

class Record(Decl):

  def __init__(
    self,
    ext,
    desc,
    kl_type_name,
    this_type_info,
    extends = None,
    include_empty_ctor = True,
    include_copy_ctor = True,
    include_simple_ass_op = True,
    include_getters_setters = True,
    include_dtor = True,
    ):
    Decl.__init__(self, ext, desc)

    self.members = []
    self.ctors = []
    self.methods = []
    self.uni_ops = []
    self.bin_ops = []
    self.ass_ops = []
    self.casts = []

    self.kl_type_name = kl_type_name
    self.this_value_name = this_cpp_value_name
    self.this_type_info = this_type_info
    if extends:
      extends_const_this = extends.const_this
    else:
      extends_const_this = None
    self.const_this = ThisCodec(
      this_type_info,
      self.members,
      False,
      extends_this = extends_const_this
      )
    if extends:
      extends_mutable_this = extends.mutable_this
    else:
      extends_mutable_this = None
    self.mutable_this = ThisCodec(
      this_type_info,
      self.members,
      True,
      extends_this = extends_mutable_this
      )
    self.extends = extends
    self.default_access = MemberAccess.public
    self.include_empty_ctor = include_empty_ctor
    self.include_copy_ctor = include_copy_ctor
    self.include_simple_ass_op = include_simple_ass_op
    self.include_getters_setters = include_getters_setters
    self.include_dtor = include_dtor
    self.get_ind_op_result = None
    self.get_ind_op_params = None
    self.set_ind_op_params = None
    copy_param_cpp_type_name = this_type_info.lib.name.compound + ' const &'
    self.copy_params = [
      ParamCodec(
        self.ext.type_mgr.get_dqti(
          self.ext.cpp_type_expr_parser.parse(copy_param_cpp_type_name)
          ),
        'that'
        )
      ]

  @property
  def cpp_type_expr_parser(self):
    return self.ext.cpp_type_expr_parser
  
  @property
  def empty_ctor_edk_symbol_name(self):
    base_edk_symbol_name = self.kl_type_name + '__empty_ctor'
    h = hashlib.md5()
    h.update(base_edk_symbol_name)
    return "_".join([self.ext.name, base_edk_symbol_name, h.hexdigest()])
  
  @property
  def copy_ctor_edk_symbol_name(self):
    base_edk_symbol_name = self.kl_type_name + '__copy_ctor'
    h = hashlib.md5()
    h.update(base_edk_symbol_name)
    for param in self.copy_params:
      h.update(param.type_info.edk.name.toplevel)
    return "_".join([self.ext.name, base_edk_symbol_name, h.hexdigest()])
  
  @property
  def simple_ass_op_edk_symbol_name(self):
    base_edk_symbol_name = self.kl_type_name + '__simple_ass_op'
    h = hashlib.md5()
    h.update(base_edk_symbol_name)
    for param in self.copy_params:
      h.update(param.type_info.edk.name.toplevel)
    return "_".join([self.ext.name, base_edk_symbol_name, h.hexdigest()])

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
      return self.access == MemberAccess.public
    
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
      self.base_edk_symbol_name = record.kl_type_name + '__ctor'
      self.this = self._record.mutable_this
      self.params = []

    @property
    def ext(self):
      return self._record.ext
    
    @property
    def edk_symbol_name(self):
      h = hashlib.md5()
      h.update(self.base_edk_symbol_name)
      for param in self.params:
        h.update(param.type_info.edk.name.toplevel)
      return "_".join([self.ext.name, self.base_edk_symbol_name, h.hexdigest()])

    def get_test_name(self):
      return self.base_edk_symbol_name

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
      self.ext.add_test(self.get_test_name(), kl, out)
  
  def add_ctor(self, params = []):
    ctor = self.Ctor(self)
    assert isinstance(params, list)
    for param in params:
      ctor.add_param(param)
    if len(ctor.params) == 0:
      self.include_empty_ctor = False
    self.ctors.append(ctor)
    return ctor

  class Method(object):

    def __init__(self, record, cpp_name, this_access=ThisAccess.const):
      self._record = record
      self.base_edk_symbol_name = record.kl_type_name + '__meth_' + cpp_name
      self.result = ResultCodec(self.ext.type_mgr.get_dqti(Void()))
      self.cpp_name = cpp_name
      self.this = self._record.mutable_this
      self.params = []
      self.this_access = this_access
      self.is_const = self.this_access == ThisAccess.const
      self.is_mutable = self.this_access == ThisAccess.mutable
      self.is_static = self.this_access == ThisAccess.static

    @property
    def ext(self):
      return self._record.ext
    
    @property
    def kl_name(self):
      return self.cpp_name

    @property
    def this_access_suffix(self):
      if self.this_access == ThisAccess.const:
        return '?'
      elif self.this_access == ThisAccess.mutable:
        return '!'
      else:
        assert False
    
    @property
    def edk_symbol_name(self):
      h = hashlib.md5()
      h.update(self.base_edk_symbol_name)
      for param in self.params:
        h.update(param.type_info.edk.name.toplevel)
      return "_".join([self.ext.name, self.base_edk_symbol_name, h.hexdigest()])

    def get_test_name(self):
      return self.base_edk_symbol_name

    def returns(self, cpp_type_name):
      assert isinstance(cpp_type_name, basestring)
      self.result = ResultCodec(
        self.ext.type_mgr.get_dqti(
          self.ext.cpp_type_expr_parser.parse(cpp_type_name)
          )
        )
      return self

    def add_param(self, cpp_type_name, cpp_name = None):
      assert isinstance(cpp_type_name, basestring)
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
      self.ext.add_test(self.get_test_name(), kl, out)
  
  def add_method(
    self,
    name,
    returns = None,
    params = [],
    this_access = ThisAccess.const,
    ):
    assert isinstance(name, basestring)
    method = self.Method(self, name, this_access=this_access)
    self.methods.append(method)
    if returns:
      method.returns(returns)
    assert isinstance(params, list)
    for param in params:
      method.add_param(param)
    return method

  def add_const_method(self, name, returns=None, params=[]):
    return self.add_method(name, returns, params, ThisAccess.const)

  def add_mutable_method(self, name, returns=None, params=[]):
    return self.add_method(name, returns, params, ThisAccess.mutable)

  def add_static_method(self, name, returns=None, params=[]):
    return self.add_method(name, returns, params, ThisAccess.static)

  class UniOp(object):

    op_to_edk_op = {
      "++": 'INC',
      "--": 'DEC',
    }

    def __init__(
      self,
      record,
      op,
      kl_method_name,
      result_cpp_type_name,
      ):
      self._record = record
      self.base_edk_symbol_name = record.kl_type_name + '__uni_op_'+self.op_to_edk_op[op]
      assert isinstance(kl_method_name, basestring)
      self.kl_method_name = kl_method_name
      self.op = op
      self.this = record.mutable_this
      assert isinstance(result_cpp_type_name, basestring)
      self.result = ResultCodec(
        self.ext.type_mgr.get_dqti(
          self.ext.cpp_type_expr_parser.parse(result_cpp_type_name)
          )
        )

    @property
    def ext(self):
      return self._record.ext
    
    @property
    def edk_symbol_name(self):
      h = hashlib.md5()
      h.update(self.base_edk_symbol_name)
      return "_".join([self.ext.name, self.base_edk_symbol_name, h.hexdigest()])

    def get_test_name(self):
      return self.base_edk_symbol_name
    
    def add_test(self, kl, out):
      self.ext.add_test(self.get_test_name(), kl, out)
  
  def add_uni_op(
    self,
    op,
    kl_method_name,
    returns,
    ):
    uni_op = self.UniOp(
      self,
      op,
      kl_method_name,
      returns,
      )
    self.uni_ops.append(uni_op)
    return uni_op

  class BinOp(object):

    op_to_edk_op = {
      "+": 'ADD',
      "-": 'SUB',
      "*": 'MUL',
      "/": 'DIV',
      "%": 'MOD',
      "==": 'EQ',
      "!=": 'NE',
      "<": 'LT',
      "<=": 'LE',
      ">": 'GT',
      ">=": 'GE',
      "===": 'EX_EQ',
      "!==": 'EX_NE',
      "|": 'BIT_OR',
      "&": 'BIT_AND',
      "^": 'BIT_XOR',
      "<<": 'SHL',
      ">>": 'SHR',
    }

    def __init__(
      self,
      record,
      result_type,
      op,
      lhs_param_name,
      lhs_param_type,
      rhs_param_name,
      rhs_param_type,
      ):
      self._record = record
      self.base_edk_symbol_name = record.kl_type_name + '__bin_op_'+self.op_to_edk_op[op]
      self.result = ResultCodec(
        self.ext.type_mgr.get_dqti(
          self.ext.cpp_type_expr_parser.parse(result_type)
          )
        )
      self.op = op
      self.params = [
        ParamCodec(
          self.ext.type_mgr.get_dqti(
            self.ext.cpp_type_expr_parser.parse(lhs_param_type)
            ),
          lhs_param_name
          ),
        ParamCodec(
          self.ext.type_mgr.get_dqti(
            self.ext.cpp_type_expr_parser.parse(rhs_param_type)
            ),
          rhs_param_name
          ),
        ]

    @property
    def ext(self):
      return self._record.ext
    
    @property
    def edk_symbol_name(self):
      h = hashlib.md5()
      h.update(self.base_edk_symbol_name)
      for param in self.params:
        h.update(param.type_info.edk.name.toplevel)
      return "_".join([self.ext.name, self.base_edk_symbol_name, h.hexdigest()])

    def get_test_name(self):
      return self.base_edk_symbol_name
    
    def add_test(self, kl, out):
      self.ext.add_test(self.get_test_name(), kl, out)
  
  def add_bin_op(
    self,
    op,
    returns='bool',
    params=None,
    ):
    if not params:
      params = [self.this_type_info.lib.name.compound + ' const &', self.this_type_info.lib.name.compound + ' const &']
    assert len(params) == 2
    bin_op = self.BinOp(
      self,
      result_type=returns,
      op=op,
      lhs_param_name='lhs',
      lhs_param_type=params[0],
      rhs_param_name='rhs',
      rhs_param_type=params[1],
      )
    self.bin_ops.append(bin_op)
    return bin_op

  class AssOp(object):

    op_to_edk_op = {
      "=": 'SIMPLE',
      "+=": 'ADD',
      "-=": 'SUB',
      "*=": 'MUL',
      "/=": 'DIV',
      "%=": 'MOD',
      "|=": 'BIT_OR',
      "&=": 'BIT_AND',
      "^=": 'BIT_XOR',
      "<<=": 'SHL',
      ">>=": 'SHR',
    }

    def __init__(
      self,
      record,
      op,
      param_type,
      param_name,
      ):
      self._record = record
      self.base_edk_symbol_name = record.kl_type_name + '__ass_op_' + self.op_to_edk_op[op]
      self.this = self._record.mutable_this
      self.op = op
      self.params = [
        ParamCodec(
          self.ext.type_mgr.get_dqti(
            self.ext.cpp_type_expr_parser.parse(param_type)
            ),
          param_name
          ),
        ]

    @property
    def ext(self):
      return self._record.ext
    
    @property
    def edk_symbol_name(self):
      h = hashlib.md5()
      h.update(self.base_edk_symbol_name)
      for param in self.params:
        h.update(param.type_info.edk.name.toplevel)
      return "_".join([self.ext.name, self.base_edk_symbol_name, h.hexdigest()])

    def get_test_name(self):
      return self.base_edk_symbol_name
    
    def add_test(self, kl, out):
      self.ext.add_test(self.get_test_name(), kl, out)
  
  def add_ass_op(
    self,
    op,
    params,
    ):
    assert len(params) == 1
    ass_op = self.AssOp(
      self,
      op=op,
      param_name='arg',
      param_type=params[0],
      )
    self.ass_ops.append(ass_op)
    return ass_op

  class Cast(object):

    def __init__(
      self,
      record,
      dst_cpp_type_name,
      ):
      self._record = record
      assert isinstance(dst_cpp_type_name, basestring)
      this_dqti = self.ext.type_mgr.get_dqti(
        self.ext.cpp_type_expr_parser.parse(dst_cpp_type_name)
        )
      self.base_edk_symbol_name = this_dqti.type_info.kl.name.compound + '__cast'
      self.this = ThisCodec(
        this_dqti.type_info,
        [],
        True, # is_mutable
        )
      self.params = [
        ParamCodec(
          DirQualTypeInfo(
            DirQual(directions.Reference, qualifiers.Const),
            record.const_this.type_info,
            ),
          "that"
          ),
        ]

    @property
    def ext(self):
      return self._record.ext
    
    @property
    def edk_symbol_name(self):
      h = hashlib.md5()
      h.update(self.base_edk_symbol_name)
      for param in self.params:
        h.update(param.type_info.edk.name.toplevel)
      return "_".join([self.ext.name, self.base_edk_symbol_name, h.hexdigest()])

    def get_test_name(self):
      return self.base_edk_symbol_name
    
    def add_test(self, kl, out):
      self.ext.add_test(self.get_test_name(), kl, out)
  
  def add_cast(
    self,
    dst,
    ):
    cast = self.Cast(self, dst)
    self.casts.append(cast)
    return cast

  def add_get_ind_op(
    self,
    value_cpp_type_name,
    this_access = ThisAccess.const
    ):
    self.get_ind_op_result = ResultCodec(
      self.ext.type_mgr.get_dqti(
        self.ext.cpp_type_expr_parser.parse(value_cpp_type_name)
        )
      )
    self.get_ind_op_params = [
      ParamCodec(
        self.ext.type_mgr.get_dqti(
          self.ext.cpp_type_expr_parser.parse('size_t')
          ),
        'index'
        ),
      ]
    if this_access == ThisAccess.mutable:
      self.get_ind_op_this = self.mutable_this
    else:
      self.get_ind_op_this = self.const_this
    return self

  def add_set_ind_op(
    self,
    value_cpp_type_name,
    this_access = ThisAccess.mutable
    ):
    self.set_ind_op_params = [
      ParamCodec(
        self.ext.type_mgr.get_dqti(
          self.ext.cpp_type_expr_parser.parse('size_t')
          ),
        'index'
        ),
      ParamCodec(
        self.ext.type_mgr.get_dqti(
          self.ext.cpp_type_expr_parser.parse(value_cpp_type_name)
          ),
        'value'
        ),
      ]
    if this_access == ThisAccess.const:
      self.set_ind_op_this = self.const_this
    else:
      self.set_ind_op_this = self.mutable_this
    return self

  @property
  def get_ind_op_edk_symbol_name(self):
    base_edk_symbol_name = self.kl_type_name + '__get_ind_op'
    h = hashlib.md5()
    h.update(base_edk_symbol_name)
    return "_".join([self.ext.name, base_edk_symbol_name, h.hexdigest()])

  @property
  def set_ind_op_edk_symbol_name(self):
    base_edk_symbol_name = self.kl_type_name + '__set_ind_op'
    h = hashlib.md5()
    h.update(base_edk_symbol_name)
    return "_".join([self.ext.name, base_edk_symbol_name, h.hexdigest()])

  def get_test_name(self):
    return self.kl_type_name
  
  @property
  def dtor_edk_symbol_name(self):
    base_edk_symbol_name = self.kl_type_name + '__dtor'
    h = hashlib.md5()
    h.update(base_edk_symbol_name)
    return "_".join([self.ext.name, base_edk_symbol_name, h.hexdigest()])

  def get_kl_name(self):
    return self.kl_type_name

  def get_template_basename(self):
    return 'record'
