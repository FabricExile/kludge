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

  def param_value_name(self, ti, vn):
    return vn

  def render_param_post(self, ti, vn):
    return ""

  def result_type_name(self, ti):
    return ti.kl.name

  def result_value_name(self, ti):
    return "__result__"

  def render_result_pre(self, ti):
    tn = self.result_type_name(ti)
    vn = self.result_value_name(ti)
    return tn.base + " " + vn + tn.suffix + " ="

  def render_result_post(self, ti):
    return ""

  def render_result_return(self, ti):
    vn = self.result_value_name(ti)
    return "return " + vn + ";"

class NullTypeSimplifier(TypeSimplifier):

  def __init__(self):
    TypeSimplifier.__init__(self)

  @property
  def will_promote(self):
    return False
