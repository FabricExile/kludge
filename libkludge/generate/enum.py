#
# Copyright (c) 2010-2017 Fabric Software Inc. All rights reserved.
#

from decl import Decl
from test import Test
from this_access import ThisAccess
from libkludge.cpp_type_expr_parser import Void, Named, DirQual, directions, qualifiers
from libkludge.value_name import this_cpp_value_name
from libkludge.this_codec import ThisCodec
from libkludge.result_codec import ResultCodec
from libkludge.param_codec import ParamCodec
from libkludge.dir_qual_type_info import DirQualTypeInfo
from libkludge import util
import hashlib

class Enum(Decl):

  def __init__(
    self,
    parent_namespace,
    kl_local_name,
    type_info,
    values,
    child_namespace_component = None,
    ):
    Decl.__init__(self, parent_namespace)
    self.type_info = type_info
    self.values = values
    if child_namespace_component:
      self.namespace = parent_namespace.create_child(child_namespace_component, kl_local_name)
    else:
      self.namespace = parent_namespace
    self.comments = []

  def get_desc(self):
    return "Enum[%s]: %s" % (
      ", ".join(["%s=%d"%(val[0], val[1]) for val in self.values]),
      self.type_info or "(anonymous)",
      )
  
  def get_test_name(self):
    if not self.type_info:
      return "Anonymous"
    return self.type_info.kl.name.compound

  def get_kl_name(self):
    if not self.type_info:
      return None
    return self.type_info.kl.name.compound

  def get_template_path(self):
    return 'generate/enum/enum'

  def get_template_aliases(self):
    return ['enum']

  def add_comment(self, comment):
    self.comments.append(util.clean_comment(comment))
    return self
