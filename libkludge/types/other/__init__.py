#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

from libkludge.type_info import TypeInfo
from libkludge.selector import Selector
from libkludge.generate.record import Record
from libkludge.dir_qual_type_info import DirQualTypeInfo
from libkludge.cpp_type_expr_parser import *

class OtherSelector(Selector):

  def __init__(self, ext):
    Selector.__init__(self, ext)

  def get_desc(self):
    return "Other"

  def maybe_create_dqti(self, type_mgr, cpp_type_expr):
    undq_cpp_type_expr, dq = cpp_type_expr.get_undq()
    if dq.is_direct:
      kl_type_name = undq_cpp_type_expr.get_kl_desc()
      record = Record(
        self.ext.root_namespace,
        child_namespace_component=undq_cpp_type_expr.components[0],
        child_namespace_kl_name=kl_type_name,
        )
      type_mgr.named_selectors['owned'].register(
        kl_type_name=kl_type_name,
        kl_type_name_for_derivatives=kl_type_name,
        cpp_type_expr=undq_cpp_type_expr,
        extends=None,
        record=record,
        )
      return True # restart
