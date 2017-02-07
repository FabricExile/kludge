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

  @abc.abstractmethod
  def render_param_pre(self, type_info):
    return ""

  @abc.abstractmethod
  def render_param_post(self, type_info):
    return ""

  def result_type_name(self, type_info):
    return type_info.kl.name.compound

  @abc.abstractmethod
  def render_result_pre(self, type_info):
    return ""

  @abc.abstractmethod
  def render_result_post(self, type_info):
    return ""

class NullTypeSimplifier(TypeSimplifier):

  def __init__(self):
    TypeSimplifier.__init__(self)

  @property
  def will_promote(self):
    return False

  def render_param_pre(self, type_info):
    return ""

  def render_param_post(self, type_info):
    return ""

  def render_result_pre(self, type_info):
    return ""

  def render_result_post(self, type_info):
    return ""
