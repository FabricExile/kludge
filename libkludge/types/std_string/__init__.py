#
# Copyright (c) 2010-2017 Fabric Software Inc. All rights reserved.
#

from libkludge.type_info import TypeInfo, KLTypeName
from libkludge.type_simplifier import TypeSimplifier
from libkludge.selector import Selector
from libkludge.generate.record import Record
from libkludge.dir_qual_type_info import DirQualTypeInfo
from libkludge.cpp_type_expr_parser import *

class StdStringTypeSimplifier(TypeSimplifier):

  def __init__(self):
    TypeSimplifier.__init__(self)

  def param_cost(self, type_info):
    return 100

  def param_type_name(self, ti):
    return KLTypeName("String", "")

  def render_param_pre(self, ti, vn):
    return "CxxStdString __" + vn + "(" + vn + ");"

  def param_cxx_value_name(self, ti, kl_vn):
    return "__" + kl_vn

  def render_param_post(self, ti, vn):
    return ""

  def render_param_copy_back(self, ti, vn):
    return vn + " = String(" + self.param_cxx_value_name(ti, vn) + ");"

  def result_kl_type_name(self, ti):
    return KLTypeName("String", "")

class StdStringSelector(Selector):

  def __init__(self, ext):
    Selector.__init__(self, ext)
    self.cpp_type_expr = Named([Simple('std'), Simple('string')])

  def get_desc(self):
    return 'CxxStdString'

  def maybe_create_dqti(self, type_mgr, cpp_type_expr):
    undq_cpp_type_expr, dq = cpp_type_expr.get_undq()
    if dq.is_direct and undq_cpp_type_expr == self.cpp_type_expr:
      kl_type_name = 'CxxStdString'
      record = Record(
        self.ext.root_namespace,
        child_namespace_component=undq_cpp_type_expr.components[0],
        child_namespace_kl_name=kl_type_name,
        )
      record.add_ctor([])
      record.add_ctor(['char const *'], dont_promote=True)
      record.add_ctor(['char const *', 'size_t'])
      record.add_ctor(['char const *', 'char const *'])
      record.add_const_method('c_str', 'char const *')
      record.add_const_method('data', 'char const *', kl_name='cxxData')
      record.add_const_method('size', 'size_t')
      record.add_mutable_method('clear')
      record.add_mutable_method('append', None, ['char const *', 'char const *'])
      record.add_get_ind_op('char')
      record.add_set_ind_op('char')
      record.add_mutable_method('push_back', None, ['char'])
      record.add_kl("""
/// \dfgPresetOmit
inline {{type_name}}(String string) {
  CxxChar array<>(string.data(), string.length());
  this = {{type_name}}(CxxCharConstPtr(array, 0), CxxCharConstPtr(array, string.length()));
}

/// \dfgPresetOmit
inline {{type_name}} Make_{{type_name}}(String string) {
  return {{type_name}}(string);
}

/// Convert to a string
/// \dfgPresetOmit
{{type_name}}.appendDesc(io String string) {
  CxxCharConstPtr ptr = this.cxx_c_str();
  string += String(ptr);
}
""")
      type_mgr.named_selectors['owned'].register(
        kl_type_name=kl_type_name,
        kl_type_name_for_derivatives=kl_type_name,
        cpp_type_expr=undq_cpp_type_expr,
        extends=None,
        record=record,
        simplifier=StdStringTypeSimplifier(),
        )
      return True # restart
