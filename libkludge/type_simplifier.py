#
# Copyright (c) 2010-2017 Fabric Software Inc. All rights reserved.
#

import abc

class TypeSimplifier:

  __metaclass__ = abc.ABCMeta

  def __init__(self):
    pass

  @property
  def will_promote(self):
    return True

  def param_cost(self, type_info):
    return 0
    
  def param_type_name_base(self, type_info):
    return type_info.kl.name.base

  def param_type_name_suffix(self, type_info):
    return type_info.kl.name.suffix

  def render_param_pass_type(self, type_info):
    return "in"

  def render_param_pre(self, ti, vn):
    return ""

  def param_cxx_value_name(self, ti, kl_vn):
    return kl_vn

  def render_param_post(self, ti, vn):
    return ""

  def render_param_copy_back(self, ti, vn):
    return ""

  def result_kl_type_name(self, ti):
    return ti.kl.name

  def result_cxx_value_name(self, ti, kl_vn):
    return kl_vn

  def render_result_decl_and_assign_cxx(self, ti, kl_vn):
    cxx_tn = ti.kl.name
    cxx_vn = self.result_cxx_value_name(ti, kl_vn)
    return cxx_tn.base + " " + cxx_vn + cxx_tn.suffix + " = "

  def render_result_cxx_to_kl(self, ti, kl_vn):
    return ""

  def render_result_return_kl(self, ti, kl_vn):
    return "return " + kl_vn + ";"

class NullTypeSimplifier(TypeSimplifier):

  def __init__(self):
    TypeSimplifier.__init__(self)

  @property
  def will_promote(self):
    return False
