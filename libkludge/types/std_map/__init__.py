from libkludge.type_info import TypeInfo
from libkludge.selector import Selector
from libkludge.dir_qual_type_info import DirQualTypeInfo
from libkludge.cpp_type_expr_parser import *

class StdMapTypeInfo(TypeInfo):

  def __init__(self, jinjenv, undq_cpp_type_expr, key_dqti, value_dqti):
    TypeInfo.__init__(
      self,
      jinjenv,
      kl_name_base = value_dqti.type_info.kl.name.base,
      kl_name_suffix = "[" + key_dqti.type_info.kl.name.compound + "]" + value_dqti.type_info.kl.name.suffix,
      edk_name_toplevel = "::Fabric::EDK::KL::Dict< " + key_dqti.type_info.edk.name.toplevel + ", " + value_dqti.type_info.edk.name.toplevel + " >",
      lib_expr = undq_cpp_type_expr,
      child_dqtis = [key_dqti, value_dqti]
      )

  def build_codec_lookup_rules(self):
    tds = TypeInfo.build_codec_lookup_rules(self)
    tds["conv"]["*"] = "types/builtin/std_map/conv"
    return tds

class StdMapSelector(Selector):

  def __init__(self, jinjenv):
    Selector.__init__(self, jinjenv)

  def get_desc(self):
    return "StdMap"
  
  def maybe_create_dqti(self, type_mgr, cpp_type_expr):
    if isinstance(cpp_type_expr, Template) \
      and len(cpp_type_expr.nested_name) == 2 \
      and cpp_type_expr.nested_name[0] == "std" \
      and cpp_type_expr.nested_name[1] == "map" \
      and len(cpp_type_expr.params) == 2:
      key_dqti = type_mgr.get_dqti(cpp_type_expr.params[0])
      value_dqti = type_mgr.get_dqti(cpp_type_expr.params[1])
      return DirQualTypeInfo(
        dir_qual.direct,
        StdMapTypeInfo(
          self.jinjenv,
          cpp_type_expr.make_unqualified(),
          key_dqti,
          value_dqti,
          )
        )
    if isinstance(cpp_type_expr, ReferenceTo) \
      and isinstance(cpp_type_expr.pointee, Template) \
      and cpp_type_expr.pointee.is_const \
      and len(cpp_type_expr.pointee.nested_name) == 2 \
      and cpp_type_expr.pointee.nested_name[0] == "std" \
      and cpp_type_expr.pointee.nested_name[1] == "map" \
      and len(cpp_type_expr.pointee.params) == 2:
      key_dqti = type_mgr.get_dqti(cpp_type_expr.pointee.params[0])
      value_dqti = type_mgr.get_dqti(cpp_type_expr.pointee.params[1])
      return DirQualTypeInfo(
        dir_qual.const_reference,
        StdMapTypeInfo(
          self.jinjenv,
          cpp_type_expr.pointee.make_unqualified(),
          key_dqti,
          value_dqti,
          )
        )
