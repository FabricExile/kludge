#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

import inspect, hashlib, abc
from decl import Decl
from test import Test
from libkludge.visibility import Visibility
from this_access import ThisAccess
from massage import *
from libkludge.cpp_type_expr_parser import *
from libkludge.value_name import this_cpp_value_name
from libkludge.this_codec import ThisCodec
from libkludge.result_codec import ResultCodec
from libkludge.param_codec import ParamCodec
from libkludge.dir_qual_type_info import DirQualTypeInfo
from libkludge.util import clean_comment, EmptyCommentContainer

class Methodlike(object):

  def __init__(self, record):
    self.record = record
    self.comments = []
  
  @property
  def ext(self):
    return self.record.ext

  def add_test(self, kl, out):
    self.ext.add_test(kl, out, test_name=self.get_test_name())
    return self

  def add_comment(self, comment):
    self.comments.append(clean_comment(comment))
    return self

  @abc.abstractmethod
  def get_test_name():
    pass

class Ctor(Methodlike):

  def __init__(
    self,
    record,
    params,
    ):
    Methodlike.__init__(self, record)
    self.params = [param.gen_codec(index, record.resolve_dqti) for index, param in enumerate(params)]
  
  def get_edk_symbol_name(self, type_info):
    return self.record.gen_edk_symbol_name('ctor', type_info, self.params)

  def get_test_name(self):
    return self.record.kl_global_name + '__ctor'

  def get_this(self, type_info):
    return self.record.get_this(type_info, True)

  def is_empty(self):
    return len(self.params) == 0

  def is_copy(self, const_ref_type_info):
    return len(self.params) == 1 \
      and (self.params[0].type_info.lib.expr == const_ref_type_info.lib.expr \
        or self.params[0].type_info.lib.expr == const_ref_type_info.direct.lib.expr)

  def param_count(self):
    return len(self.params)

class Method(Methodlike):

  def __init__(
    self,
    record,
    cpp_name,
    returns,
    params,
    this_access,
    kl_name=None,
    ):
    Methodlike.__init__(self, record)
    self.cpp_name = cpp_name
    if not kl_name:
      kl_name = cpp_name
    self.kl_name = kl_name
    self.result = ResultCodec(record.resolve_dqti(returns))
    self.params = [param.gen_codec(index, record.resolve_dqti) for index, param in enumerate(params)]
    self.this_access = this_access
    self.is_const = self.this_access == ThisAccess.const
    self.is_mutable = self.this_access == ThisAccess.mutable
    self.is_static = self.this_access == ThisAccess.static

  @property
  def this_access_suffix(self):
    if self.this_access == ThisAccess.const:
      return '?'
    elif self.this_access == ThisAccess.mutable:
      return '!'
    else:
      assert False
  
  def get_edk_symbol_name(self, type_info):
    return self.record.gen_edk_symbol_name('meth_' + self.cpp_name, type_info, self.params)

  def get_test_name(self):
    return self.record.kl_global_name + '__meth_' + self.cpp_name

  def get_this(self, type_info):
    assert self.this_access != ThisAccess.static
    return self.record.get_this(type_info, self.this_access == ThisAccess.mutable)

class CallOp(Methodlike):

  def __init__(
    self,
    record,
    returns,
    params,
    this_access,
    kl_name=None,
    ):
    Methodlike.__init__(self, record)
    self.result = ResultCodec(record.resolve_dqti(returns))
    self.params = [param.gen_codec(index, record.resolve_dqti) for index, param in enumerate(params)]
    self.this_access = this_access
    self.is_const = self.this_access == ThisAccess.const
    self.is_mutable = self.this_access == ThisAccess.mutable
    self.is_static = self.this_access == ThisAccess.static

  @property
  def this_access_suffix(self):
    if self.this_access == ThisAccess.const:
      return '?'
    elif self.this_access == ThisAccess.mutable:
      return '!'
    else:
      assert False
  
  def get_edk_symbol_name(self, type_info):
    return self.record.gen_edk_symbol_name('call_op', type_info, self.params)

  def get_test_name(self):
    return self.record.kl_global_name + '__call_op'

  def get_this(self, type_info):
    assert self.this_access != ThisAccess.static
    return self.record.get_this(type_info, self.this_access == ThisAccess.mutable)

class UniOp(Methodlike):

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
    Methodlike.__init__(self, record)
    self.resolve_cpp_type_expr = record.resolve_cpp_type_expr
    assert isinstance(kl_method_name, basestring)
    self.kl_method_name = kl_method_name
    self.op = op
    assert isinstance(result_cpp_type_name, basestring)
    self.result = ResultCodec(
      self.ext.type_mgr.get_dqti(
        self.resolve_cpp_type_expr(result_cpp_type_name)
        )
      )

  @property
  def ext(self):
    return self.record.ext
  
  def get_edk_symbol_name(self, type_info):
    return self.record.gen_edk_symbol_name('uni_op_' + self.op_to_edk_op[self.op], type_info)

  def get_test_name(self):
    return self.record.kl_global_name + '__uni_op_' + self.op_to_edk_op[self.op]

  def get_this(self, type_info):
    return self.record.get_mutable_this(type_info)

class BinOp(Methodlike):

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
    params,
    ):
    Methodlike.__init__(self, record)
    self.resolve_cpp_type_expr = record.resolve_cpp_type_expr
    self.result = ResultCodec(
      self.ext.type_mgr.get_dqti(
        self.resolve_cpp_type_expr(result_type)
        )
      )
    self.op = op
    self.params = [param.gen_codec(index, record.resolve_dqti) for index, param in enumerate(params)]

  @property
  def ext(self):
    return self.record.ext
  
  def get_edk_symbol_name(self, type_info):
    return self.record.gen_edk_symbol_name('bin_op_' + self.op_to_edk_op[self.op], type_info, self.params)

  def get_test_name(self):
    return self.record.kl_global_name + '__bin_op_' + self.op_to_edk_op[self.op]

class AssOp(Methodlike):

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
    params,
    ):
    Methodlike.__init__(self, record)
    self.resolve_cpp_type_expr = record.resolve_cpp_type_expr
    self.base_edk_symbol_name = record.kl_global_name + '__ass_op_' + self.op_to_edk_op[op]
    self.op = op
    self.params = [param.gen_codec(index, record.resolve_dqti) for index, param in enumerate(params)]

  @property
  def ext(self):
    return self.record.ext
  
  def get_edk_symbol_name(self, type_info):
    return self.record.gen_edk_symbol_name('ass_op_' + self.op_to_edk_op[self.op], type_info, self.params)

  def get_test_name(self):
    return self.record.kl_global_name + '__ass_op_' + self.op_to_edk_op[self.op]

  def get_this(self, type_info):
    return self.record.get_this(type_info, True)

class Cast(Methodlike):

  def __init__(
    self,
    record,
    dst_cpp_type_name,
    ):
    Methodlike.__init__(self, record)
    self.resolve_cpp_type_expr = record.resolve_cpp_type_expr
    assert isinstance(dst_cpp_type_name, basestring)
    this_dqti = self.ext.type_mgr.get_dqti(
      self.resolve_cpp_type_expr(dst_cpp_type_name)
      )
    self.this = ThisCodec(
      this_dqti.type_info,
      is_mutable=True,
      )

  @property
  def ext(self):
    return self.record.ext
  
  def get_edk_symbol_name(self, type_info):
    return self.record.gen_edk_symbol_name('cast', type_info, self.get_params(type_info))

  def get_test_name(self):
    return self.record.kl_global_name + '__cast'

  def get_param(self, type_info):
    return ParamCodec(
      DirQualTypeInfo(
        DirQual(directions.Direct, qualifiers.Unqualified),
        type_info,
        ),
      "that"
      )

  def get_params(self, type_info):
    return [self.get_param(type_info)]

class Member(object):

  def __init__(self, record, cpp_name, dqti, getter_kl_name, setter_kl_name, visibility):
    self.record = record
    self.cpp_name = cpp_name
    self.kl_name = cpp_name
    self.type_info = dqti.type_info
    self.result = ResultCodec(dqti)
    self.param = ParamCodec(dqti, cpp_name)
    self.getter_kl_name = getter_kl_name
    if not self.getter_kl_name is None and self.getter_kl_name == '':
      self.getter_kl_name = 'GET_' + cpp_name
    self.setter_kl_name = setter_kl_name
    if not self.setter_kl_name is None and self.setter_kl_name == '':
      self.setter_kl_name = 'SET_' + cpp_name
    self.visibility = visibility

  def has_getter(self):
    return self.getter_kl_name is not None

  def has_setter(self):
    return self.setter_kl_name is not None

  def is_public(self):
    return self.visibility == Visibility.public

  def get_getter_edk_symbol_name(self, ti):
    return self.record.gen_edk_symbol_name('getter_' + self.cpp_name, ti)

  def get_setter_edk_symbol_name(self, ti):
    return self.record.gen_edk_symbol_name('setter_' + self.cpp_name, ti)

class KL(object):

  def __init__(self, record, code, vars):
    self.template = record.ext.jinjenv.from_string(code)
    self.vars = vars

  def render(self, type_info):
    vars = {'type_name': type_info.kl.name.compound}
    for k, v in self.vars.iteritems():
      vars[k] = v
    return self.template.render(vars).strip()

class Record(Decl):

  def __init__(
    self,
    parent_namespace,
    extends=None,
    include_empty_ctor=True,
    include_copy_ctor=True,
    include_simple_ass_op=True,
    include_getters_setters=True,
    include_dtor=True,
    forbid_copy=False,
    child_namespace_component=None,
    child_namespace_kl_name=None,
    ):
    Decl.__init__(self, parent_namespace)

    if child_namespace_component:
      assert isinstance(child_namespace_kl_name, basestring)
      self.namespace = parent_namespace.create_child(child_namespace_component, child_namespace_kl_name)
      for namespace_method in inspect.getmembers(
        self.namespace,
        predicate = inspect.ismethod,
        ):
        if namespace_method[0] not in ['add_func']:
          setattr(self, namespace_method[0], namespace_method[1])
    else:
      self.namespace = parent_namespace
    for method_name in ['resolve_cpp_type_expr', 'resolve_dqti']:
      setattr(self, method_name, getattr(self.namespace, method_name))

    self.comments = []
    self.members = []
    self.ctors = []
    self.methods = []
    self.call_ops = []
    self.uni_ops = []
    self.bin_ops = []
    self.ass_ops = []
    self.casts = []
    self.deref_kl_method_name = None
    self.deref_result = None
    self.kls = []

    self.this_value_name = this_cpp_value_name
    assert extends is None or isinstance(extends, Record)
    self.extends = extends
    self.default_visibility = Visibility.public
    self.include_empty_ctor = include_empty_ctor
    self.include_copy_ctor = include_copy_ctor
    self.include_simple_ass_op = include_simple_ass_op
    self.include_getters_setters = include_getters_setters
    self.include_dtor = include_dtor
    self.forbid_copy = forbid_copy
    self.get_ind_op_result = None
    self.get_ind_op_params = None
    self.set_ind_op_params = None

  def get_nested_records(self):
    result = []
    record = self
    while record:
      result = [record] + result
      record = record.extends
    return result

  def get_this(self, type_info, is_mutable):
    return ThisCodec(type_info, is_mutable)

  def get_const_this(self, type_info):
    return self.get_this(type_info, False)
    
  def get_mutable_this(self, type_info):
    return self.get_this(type_info, True)
    
  def get_copy_param(self, type_info):
    return ParamCodec(
      DirQualTypeInfo(DirQual(directions.Direct, qualifiers.Unqualified), type_info),
      "that"
      )

  def get_desc(self):
    return "Record"
  
  def resolve_cpp_type_expr(self, cpp_type_name):
    return self.namespace.resolve_cpp_type_expr(cpp_type_name)

  def add_comment(self, comment):
    self.comments.append(clean_comment(comment))
    return self

  def set_default_visibility(self, visibility):
    self.default_visibility = visibility

  def add_member(self, cpp_name, cpp_type_name, getter='', setter='', visibility=None):
    try:
      if visibility is None:
        visibility = self.default_visibility
      cpp_type_expr = self.resolve_cpp_type_expr(cpp_type_name)
      dqti = self.ext.type_mgr.get_dqti(cpp_type_expr)
      member = Member(self, cpp_name, dqti, getter, setter, visibility=visibility)
      self.members.append(member)
      return self
    except Exception as e:
      self.ext.warning("Ignoring member '%s': %s" % (cpp_name, e))
  
  def add_ctor(self, params=[], opt_params=[]):
    try:
      params = massage_params(params)
      opt_params = massage_params(opt_params)

      if len(params) == 0:
        self.include_empty_ctor = False

      result = None
      for i in range(0, len(opt_params)+1):
        ctor = Ctor(self, params + opt_params[0:i])
        self.ctors.append(ctor)
        if not result:
          result = ctor
      return result
    except Exception as e:
      self.ext.warning("Ignoring ctor: %s" % (e))
      return EmptyCommentContainer()

  def add_method(
    self,
    name,
    returns=None,
    params=[],
    opt_params=[],
    this_access=ThisAccess.const,
    kl_name=None,
    ):
    try:
      assert isinstance(name, basestring)

      returns = massage_returns(returns)
      params = massage_params(params)
      opt_params = massage_params(opt_params)

      result = None
      for i in range(0, len(opt_params)+1):
        method = Method(
          self,
          name,
          returns,
          params + opt_params[0:i],
          this_access=this_access,
          kl_name=kl_name,
          )
        self.methods.append(method)
        if not result:
          result = method
      return result
    except Exception as e:
      self.ext.warning("Ignoring method '%s': %s" % (name, e))
      return EmptyCommentContainer()

  def add_const_method(self, name, returns=None, params=[], opt_params=[], kl_name=None):
    return self.add_method(name, returns, params, opt_params, ThisAccess.const, kl_name=kl_name)

  def add_mutable_method(self, name, returns=None, params=[], opt_params=[], kl_name=None):
    return self.add_method(name, returns, params, opt_params, ThisAccess.mutable, kl_name=kl_name)

  def add_static_method(self, name, returns=None, params=[], opt_params=[], kl_name=None):
    return self.add_method(name, returns, params, opt_params, ThisAccess.static, kl_name=kl_name)

  def add_call_op(
    self,
    returns=None,
    params=[],
    opt_params=[],
    this_access=ThisAccess.const,
    ):
    try:
      assert this_access != ThisAccess.static
      returns = massage_returns(returns)
      params = massage_params(params)
      opt_params = massage_params(opt_params)

      result = None
      for i in range(0, len(opt_params)+1):
        call_op = CallOp(
          self,
          returns,
          params + opt_params[0:i],
          this_access=this_access,
          )
        self.call_ops.append(call_op)
        if not result:
          result = call_op
      return result
    except Exception as e:
      self.ext.warning("Ignoring call operator: %s" % (e))
      return EmptyCommentContainer()
  
  kl_method_name = {
    '++': 'cxxInc',
    '--': 'cxxDec',
    }

  def add_uni_op(
    self,
    op,
    returns,
    kl_method_name=None,
    ):
    try:
      if not kl_method_name:
        kl_method_name = self.kl_method_name[op]
      uni_op = UniOp(
        self,
        op,
        kl_method_name,
        returns,
        )
      self.uni_ops.append(uni_op)
      return uni_op
    except Exception as e:
      self.warning("Ignoring unary operator %s: %s" % (op, e))
      return EmptyCommentContainer()
  
  def add_bin_op(
    self,
    op,
    returns,
    params,
    ):
    try:
      assert isinstance(op, basestring)
      assert isinstance(returns, basestring)
      assert len(params) == 2
      params = massage_params(params)
      bin_op = BinOp(
        self,
        result_type=returns,
        op=op,
        params=params,
        )
      self.bin_ops.append(bin_op)
      return bin_op
    except Exception as e:
      self.warning("Ignoring binary operator %s: %s" % (op, e))
      return EmptyCommentContainer()

  def add_ass_op(
    self,
    op,
    params,
    ):
    try:
      assert isinstance(op, basestring)
      assert len(params) == 1
      params = massage_params(params)
      ass_op = AssOp(
        self,
        op=op,
        params=params,
        )
      self.ass_ops.append(ass_op)
      return ass_op
    except Exception as e:
      self.warning("Ignoring assignment operator %s: %s" % (op, e))
      return EmptyCommentContainer()
      
  def add_cast(
    self,
    dst,
    ):
    try:
      cast = Cast(self, dst)
      self.casts.append(cast)
      return cast
    except Exception as e:
      self.warning("Ignoring cast to %s: %s" % (dst, e))
      return EmptyCommentContainer()

  def add_kl(
    self,
    code,
    **kwargs
    ):
    self.kls.append(KL(self, code, kwargs))
    return self

  def has_kls(self):
    return len(self.kls) > 0

  def add_get_ind_op(
    self,
    value_cpp_type_name,
    this_access = ThisAccess.const
    ):
    self.get_ind_op_result = ResultCodec(
      self.ext.type_mgr.get_dqti(
        self.resolve_cpp_type_expr(value_cpp_type_name)
        )
      )
    self.get_ind_op_params = [
      ParamCodec(
        self.ext.type_mgr.get_dqti(
          self.resolve_cpp_type_expr('size_t')
          ),
        'index'
        ),
      ]
    self.get_ind_op_this_access = this_access
    return self

  def get_get_ind_op_this(self, type_info):
    return self.get_this(type_info, self.get_ind_op_this_access == ThisAccess.mutable)

  def add_set_ind_op(
    self,
    value_cpp_type_name,
    this_access = ThisAccess.mutable
    ):
    self.set_ind_op_params = [
      ParamCodec(
        self.ext.type_mgr.get_dqti(
          self.resolve_cpp_type_expr('size_t')
          ),
        'index'
        ),
      ParamCodec(
        self.ext.type_mgr.get_dqti(
          self.resolve_cpp_type_expr(value_cpp_type_name)
          ),
        'value'
        ),
      ]
    self.set_ind_op_this_access = this_access
    return self

  def get_set_ind_op_this(self, type_info):
    return self.get_this(type_info, self.set_ind_op_this_access == ThisAccess.mutable)

  def add_deref(
    self,
    returns,
    this_access = ThisAccess.const,
    kl_method_name = 'cxxDeref',
    ):
    assert not self.deref_kl_method_name
    assert isinstance(kl_method_name, basestring)
    self.deref_kl_method_name = kl_method_name
    assert isinstance(returns, basestring)
    self.deref_result = ResultCodec(
      self.ext.type_mgr.get_dqti(
        self.resolve_cpp_type_expr(returns)
        )
      )
    self.deref_this_access = this_access
    return self

  def get_deref_this(self, type_info):
    assert self.deref_this_access != ThisAccess.static
    return self.get_this(type_info, self.deref_this_access == ThisAccess.mutable)

  def gen_edk_symbol_name(self, name, type_info, params=[]):
    h = hashlib.md5()
    prefixes = [self.ext.name, str(type_info.kl.name), name]
    for prefix in prefixes:
      h.update(prefix)
    for param in params:
      h.update(param.type_info.edk.name)
    prefixes.append(h.hexdigest())
    return '__'.join(prefixes)
    
  def get_empty_ctor_edk_symbol_name(self, type_info):
    return self.gen_edk_symbol_name('empty_ctor', type_info)
    
  def get_copy_ctor_edk_symbol_name(self, type_info):
    return self.gen_edk_symbol_name('copy_ctor', type_info)
    
  def get_simple_ass_op_edk_symbol_name(self, type_info):
    return self.gen_edk_symbol_name('simple_ass_op', type_info)
    
  def get_deref_edk_symbol_name(self, type_info):
    return self.gen_edk_symbol_name('deref', type_info)

  def get_get_ind_op_edk_symbol_name(self, type_info):
    return self.gen_edk_symbol_name('get_ind_op', type_info)

  def get_set_ind_op_edk_symbol_name(self, type_info):
    return self.gen_edk_symbol_name('set_ind_op', type_info)
  
  def get_dtor_edk_symbol_name(self, type_info):
    return self.gen_edk_symbol_name('dtor', type_info)

  def get_test_name(self):
    return self.kl_global_name

  @property
  def kl_global_name(self):
    return '_'.join(self.namespace.nested_kl_names)

  def get_template_path(self):
    return 'generate/record/record'

  def get_template_aliases(self):
    return ['record']

  def has_ctors(self):
    return len(self.ctors) > 0

  def has_methods(self):
    return len(self.methods) > 0

  def has_call_ops(self):
    return len(self.call_ops) > 0

  def has_uni_ops(self):
    return len(self.uni_ops) > 0

  def has_bin_ops(self):
    return len(self.bin_ops) > 0

  def has_ass_ops(self):
    return len(self.ass_ops) > 0

  def has_casts(self):
    return len(self.casts) > 0

  def public_members(self):
    return [member for member in self.members if member.is_public()]

  def nested_public_members(self):
    result = []
    for record in self.get_nested_records():
      result.extend(record.public_members())
    return result

  def has_char_const_ptr_ctor(self):
    for ctor in self.ctors:
      if len(ctor.params) == 1 and ctor.params[0].type_info.lib.expr == PointerTo(Const(Char())):
        return True
    return False

  def has_std_string_const_ref_ctor(self):
    for ctor in self.ctors:
      if len(ctor.params) == 1 and ctor.params[0].type_info.lib.expr == ReferenceTo(Const(Named([Simple('std'), Simple('string')]))):
        return True
    return False
