#
# Copyright (c) 2010-2017 Fabric Software Inc. All rights reserved.
#

from decl import Decl
from libkludge.cpp_type_expr_parser import Void
from libkludge.result_codec import ResultCodec
from libkludge.param_codec import ParamCodec
from libkludge import cpp_type_expr_parser
import hashlib
from libkludge import util

class Func(Decl):
  def __init__(
    self,
    parent_namespace,
    cpp_global_name,
    kl_global_name,
    returns_cpp_type_expr,
    params,
    ):
    Decl.__init__(
      self,
      parent_namespace,
      )

    self.cpp_global_name = cpp_global_name
    self.kl_global_name = kl_global_name

    self.result = ResultCodec(
      self.type_mgr.get_dqti(
        self.cpp_type_expr_parser.parse(returns_cpp_type_expr)
        )
      )
    self.params = []
    for param_index in range(0, len(params)):
      param = params[param_index]
      param_codec = param.gen_codec(param_index, parent_namespace.resolve_dqti)
      if not param_codec:
        raise Exception("cannot parse type for parameter %d" % (param_index + 1))
      self.params.append(param_codec)
    self.comments = []
  
  def get_edk_symbol_name(self):
    base_edk_symbol_name = self.kl_global_name
    h = hashlib.md5()
    h.update(base_edk_symbol_name)
    for param in self.params:
      h.update(param.type_info.edk.name)
    return "_".join([self.ext.name, base_edk_symbol_name, h.hexdigest()])

  def add_comment(self, comment):
    self.comments.append(util.clean_comment(comment))
    return self

  def get_desc(self):
    return "Function KL[%s] C++[%s]" % (self.kl_global_name, self.cpp_global_name)
  
  def get_test_name(self):
    return self.kl_global_name

  def get_template_path(self):
    return 'generate/func/func'
  
  def get_template_aliases(self):
    return ['func']
  
  def get_promotion_data(self):
    param_sigs = []
    cost = 0
    for param in self.params:
      simplifier = param.type_info.simplifier
      type_info = param.type_info
      param_sigs.append("%s %s" % (
        simplifier.render_param_pass_type(type_info),
        simplifier.param_type_name(type_info).compound,
        ))
      this_cost = simplifier.param_cost(type_info)
      if this_cost > cost:
        cost = this_cost
    sig = "%s(%s)" % (self.kl_global_name, ','.join(param_sigs))
    return (sig, cost)

  @property
  def should_promote(self):
    promotion_sig, _ = self.get_promotion_data()
    return self.ext.func_promotions[promotion_sig][0] is self
