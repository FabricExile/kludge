#
# Copyright (c) 2010-2017 Fabric Software Inc. All rights reserved.
#

from libkludge.type_info import TypeInfo, KLTypeName
from libkludge.type_simplifier import TypeSimplifier
from libkludge.selector import Selector
from libkludge.generate.record import Record
from libkludge.dir_qual_type_info import DirQualTypeInfo
from libkludge.cpp_type_expr_parser import *

def build_derived_name(kl_type_name, suffix):
  if kl_type_name.startswith('Cxx'):
    return kl_type_name + suffix
  else:
    return 'Cxx' + kl_type_name + suffix

class StdVectorTypeSimplifier(TypeSimplifier):

  def __init__(self, eti):
    TypeSimplifier.__init__(self)
    self.eti = eti

  def param_cost(self, type_info):
    return 100

  def param_type_name(self, type_info):
    ele_tn = self.eti.simplifier.param_type_name(self.eti)
    return KLTypeName(ele_tn.base, ele_tn.suffix + "[]")

  def render_param_pre(self, ti, kl_vn):
    cxx_vn = self.param_cxx_value_name(ti, kl_vn)
    return '\n'.join([
      ti.kl.name.base + " " + cxx_vn + ti.kl.name.suffix + ";",
      cxx_vn + ".reserve(" + kl_vn + ".size());",
      "for (Index i=0; i<" + kl_vn + ".size(); ++i)",
      "  " + cxx_vn + ".push_back(" + kl_vn + "[i]);",
      ])

  def param_cxx_value_name(self, ti, kl_vn):
    return kl_vn + "__cxx"

  def render_param_post(self, ti, vn):
    return ""

  def render_param_copy_back(self, ti, kl_vn):
    cxx_vn = self.param_cxx_value_name(ti, kl_vn)
    cxx_tn = ti.kl.name
    return '\n'.join([
      "if (Fabric_Guarded && " + cxx_vn + ".size() >= 2147483648u64)",
      "  report('Resulting value of " + cxx_tn.compound + " " + cxx_vn + " is too large for KL variable array');",
      kl_vn + ".resize(UInt32(" + cxx_vn + ".size()));",
      "for (Index i=0; i<" + cxx_vn + ".size(); ++i)",
      "  " + kl_vn + "[i] = " + cxx_vn + ".cxx_getAtIndex(i).cxx_get();",
      ])

  def result_kl_type_name(self, ti):
    etn = self.eti.simplifier.result_kl_type_name(self.eti)
    return KLTypeName(etn.base, etn.suffix + '[]')

  def result_cxx_value_name(self, ti, kl_vn):
    return kl_vn + "__cxx"

  def render_result_decl_cxx_to_kl(self, ti, kl_vn):
    kl_tn = self.result_kl_type_name(ti);
    cxx_vn = self.result_cxx_value_name(ti, kl_vn)
    cxx_tn = ti.kl.name
    ind_vn = cxx_vn + '__ind'
    ele_kl_vn = cxx_vn + '__ele'
    return '\n'.join([
      kl_tn.base + " " + kl_vn + kl_tn.suffix + ";",
      "if (Fabric_Guarded && " + cxx_vn + ".size() >= 2147483648u64)",
      "  report('Resulting value of " + cxx_tn.compound + " is too large for KL variable array');",
      kl_vn + ".reserve(UInt32(" + cxx_vn + ".size()));",
      "for (Index " + ind_vn + "=0; " + ind_vn + " < " + cxx_vn + ".size(); ++" + ind_vn + ") {",
      "  " + self.eti.simplifier.render_result_decl_and_assign_cxx(self.eti, ele_kl_vn),
      "    " + cxx_vn + ".cxx_getAtIndex(" + ind_vn + ").cxx_get();",
      "  " + self.eti.simplifier.render_result_decl_cxx_to_kl(self.eti, ele_kl_vn),
      "  " + kl_vn + ".push(" + ele_kl_vn + ");",
      "}",
      ])

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
      element_type_info_for_derivatives = element_type_info.for_derivatives()
      element_cpp_type_name_for_derivatives = element_type_info_for_derivatives.lib.name.compound
      element_kl_type_name_for_derivatives = element_type_info_for_derivatives.kl.name.compound
      if element_kl_type_name.startswith('Cxx'):
        kl_type_name = element_kl_type_name + 'StdVector'
      else:
        kl_type_name = 'Cxx' + element_kl_type_name + 'StdVector'
      is_kludge_ext = self.is_kludge_ext_cpp_type_expr(undq_cpp_type_expr)
      record = Record(
        self.ext.root_namespace,
        child_namespace_component=undq_cpp_type_expr.components[0],
        child_namespace_kl_name=kl_type_name,
        is_kludge_ext=is_kludge_ext,
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
/// \dfgPresetOmit
/// \internal
{{type_name}}({{element_type_name}} array<>) {
  this = {{type_name}}(
    {{element_type_name_const_ptr}}(array, 0),
    {{element_type_name_const_ptr}}(array, array.size())
    );
}

/// \dfgPresetOmit
/// \internal
{{type_name}} Make_{{type_name}}({{element_type_name}} array<>) {
  return {{type_name}}(array);
}

/// \dfgPresetOmit
/// \internal
inline {{element_type_name}}[] Make_{{element_type_name}}VariableArray({{type_name}} vec) {
  UInt32 size = UInt32(vec.cxx_size());
  {{element_type_name}} result[];
  result.reserve(size);
  for (Index i = 0; i < size; ++i)  {
    {{element_type_name_const_ref}} ref = vec.cxx_getAtIndex(i);
    result.push(ref.cxx_get());
  }
  return result;
}

/// \dfgPresetOmit
/// \internal
{{type_name}}.appendDesc(io String string) {
  string += "{{type_name}}:[";
  UInt64 count = this.cxx_size();
  for (UInt64 index = 0; index < count; ++index) {
    if (index > 0 )
      string += ",";
    if (index == 32) {
      string += "...";
      break;
    }
    string += this.cxx_getAtIndex(index);
  }
  string += "]";
}
""",
  element_type_name=element_kl_type_name,
  element_type_name_const_ptr=build_derived_name(element_kl_type_name_for_derivatives, 'ConstPtr'),
  element_type_name_const_ref=build_derived_name(element_kl_type_name_for_derivatives, 'ConstRef'),
  )
      type_mgr.named_selectors['owned'].register(
        kl_type_name=kl_type_name,
        kl_type_name_for_derivatives=kl_type_name,
        cpp_type_expr=undq_cpp_type_expr,
        extends=None,
        record=record,
        simplifier=StdVectorTypeSimplifier(element_type_info),
        is_kludge_ext=is_kludge_ext,
        )
      return True # restart
