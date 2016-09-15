#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

from libkludge.type_info import TypeInfo
from libkludge.selector import Selector
from libkludge.generate.record import Record
from libkludge.dir_qual_type_info import DirQualTypeInfo
from libkludge.cpp_type_expr_parser import *

class StdVectorSelector(Selector):

  def __init__(self, ext):
    Selector.__init__(self, ext)

  def get_desc(self):
    return "StdVector"

  def maybe_create_dqti(self, type_mgr, cpp_type_expr):
    undq_cpp_type_expr, dq = cpp_type_expr.get_undq()
    if dq.is_direct \
      and isinstance(undq_cpp_type_expr, Named) \
      and len(undq_cpp_type_expr.components) == 2 \
      and undq_cpp_type_expr.components[0] == Simple("std") \
      and isinstance(undq_cpp_type_expr.components[1], Template) \
      and undq_cpp_type_expr.components[1].name == "vector" \
      and len(undq_cpp_type_expr.components[1].params) == 1:
      element_type_info = type_mgr.get_dqti(undq_cpp_type_expr.components[1].params[0]).type_info
      element_cpp_type_name = element_type_info.lib.name.compound
      element_kl_type_name = element_type_info.kl.name.compound
      kl_type_name = element_kl_type_name + '_StdVector'
      record = Record(
        self.ext.root_namespace,
        child_namespace_component=undq_cpp_type_expr.components[0],
        child_namespace_kl_name=kl_type_name,
        )
      record.add_ctor([])
      record.add_ctor(['size_t'])
      record.add_ctor([element_cpp_type_name + ' const *', element_cpp_type_name + ' const *'])
      record.add_const_method('size', 'size_t')
      record.add_mutable_method('reserve', None, ['size_t'])
      record.add_mutable_method('push_back', None, [element_cpp_type_name])
      record.add_get_ind_op(element_cpp_type_name + ' const &')
      record.add_set_ind_op(element_cpp_type_name + ' const &')
      record.add_mutable_method('pop_back')
      record.add_kl("""
inline {{type_name}} Make_{{type_name}}({{element_type_name}} array<>) {
  return {{type_name}}(
    {{element_type_name}}_CxxConstPtr(array, 0),
    {{element_type_name}}_CxxConstPtr(array, 2)
    );
}

inline {{element_type_name}}[] Make_{{element_type_name}}_VariableArray({{type_name}} vec) {
  UInt32 size = UInt32(vec.size());
  {{element_type_name}} result[];
  result.reserve(size);
  for (Index i = 0; i < size; ++i)  {
    {{element_type_name}}_CxxConstRef ptr = vec.getAt(i);
    result.push(ptr.cxxRefGet());
  }
  return result;
}
""", element_type_name=element_kl_type_name)
      type_mgr.selectors['owned'].register(
        kl_type_name=kl_type_name,
        kl_type_name_for_derivatives=kl_type_name,
        cpp_type_expr=undq_cpp_type_expr,
        extends=None,
        record=record,
        )
      return None
