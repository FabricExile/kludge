#
# Copyright (c) 2010-2017 Fabric Software Inc. All rights reserved.
#

from libkludge.type_info import TypeInfo
from libkludge.selector import Selector
from libkludge.generate.record import Record
from libkludge.dir_qual_type_info import DirQualTypeInfo
from libkludge.cpp_type_expr_parser import *

class StdSetSelector(Selector):

  def __init__(self, ext):
    Selector.__init__(self, ext)

  def get_desc(self):
    return "StdSet"

  def maybe_create_dqti(self, type_mgr, cpp_type_expr):
    undq_cpp_type_expr, dq = cpp_type_expr.get_undq()
    if dq.is_direct \
      and isinstance(undq_cpp_type_expr, Named) \
      and len(undq_cpp_type_expr.components) == 2 \
      and undq_cpp_type_expr.components[0] == Simple("std") \
      and isinstance(undq_cpp_type_expr.components[1], Template) \
      and undq_cpp_type_expr.components[1].name == "set" \
      and len(undq_cpp_type_expr.components[1].params) == 1:
      element_type_info = type_mgr.get_dqti(undq_cpp_type_expr.components[1].params[0]).type_info
      element_cpp_type_name = element_type_info.lib.name.compound
      element_kl_type_name = element_type_info.kl.name.compound
      kl_type_name = element_kl_type_name + '_StdSet'
      record = Record(
        self.ext.root_namespace,
        child_namespace_component=undq_cpp_type_expr.components[0],
        child_namespace_kl_name=kl_type_name,
        )
      record.add_ctor([])
      record.add_const_method('count', 'size_t', [element_cpp_type_name + ' const &'])
      record.add_mutable_method('clear')
      record.add_mutable_method('insert', None, [element_cpp_type_name + ' const &'])
      record.add_mutable_method('erase', None, [element_cpp_type_name + ' const &'])
      type_mgr.named_selectors['owned'].register(
        kl_type_name=kl_type_name,
        kl_type_name_for_derivatives=kl_type_name,
        cpp_type_expr=undq_cpp_type_expr,
        extends=None,
        record=record,
        )
      return True # restart
