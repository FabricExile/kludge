from libkludge.type_info import TypeInfo
from libkludge.selector import Selector
from libkludge.dir_qual_type_info import DirQualTypeInfo
from libkludge.cpp_type_expr_parser import *

class KLExtTypeAliasTypeInfo(TypeInfo):

  can_in_place = True

  def __init__(self, jinjenv, nested_name, undq_cpp_type_expr, kl_type_name):
    TypeInfo.__init__(
      self,
      jinjenv,
      nested_name = nested_name,
      lib_expr = undq_cpp_type_expr,
      kl_name_base = kl_type_name,
      kl_name_suffix = '',
      )

  def build_codec_lookup_rules(self):
    tds = TypeInfo.build_codec_lookup_rules(self)
    tds["conv"]["*"] = "protocols/conv/builtin/none"
    tds["result"]["decl_and_assign_lib"] = "types/builtin/kl_ext_type_alias/result"
    tds["result"]["indirect_lib_to_edk"] = "types/builtin/kl_ext_type_alias/result"
    tds["repr"]["*"] = "protocols/repr/builtin/inplace"
    tds["repr"]["defn_kl"] = "types/builtin/kl_ext_type_alias/repr"
    return tds    

class KLExtTypeAliasSelector(Selector):

  def __init__(self, jinjenv, nested_name, cpp_type_expr, kl_type_name):
    Selector.__init__(self, jinjenv)
    self.nested_name = nested_name
    self.cpp_type_name = str(cpp_type_expr)
    self.kl_type_name = kl_type_name

  def get_desc(self):
    return "KLExtTypeAlias:%s" % str(self.nested_name)
    
  def maybe_create_dqti(self, type_mgr, cpp_type_expr):
    if isinstance(cpp_type_expr, Named) \
      and cpp_type_expr.nested_name == [self.cpp_type_name]:
      return DirQualTypeInfo(
        dir_qual.direct,
        KLExtTypeAliasTypeInfo(
          self.jinjenv,
          self.nested_name,
          cpp_type_expr.make_unqualified(),
          self.kl_type_name,
          )
        )

    if isinstance(cpp_type_expr, PointerTo) \
      and isinstance(cpp_type_expr.pointee, Named) \
      and cpp_type_expr.pointee.nested_name == [self.cpp_type_name]:
      if cpp_type_expr.pointee.is_const:
        dq = dir_qual.const_pointer
      else:
        dq = dir_qual.mutable_pointer
      return DirQualTypeInfo(
        dq,
        KLExtTypeAliasTypeInfo(
          self.jinjenv,
          self.nested_name,
          cpp_type_expr.pointee.make_unqualified(),
          self.kl_type_name,
          )
        )

    if isinstance(cpp_type_expr, ReferenceTo) \
      and isinstance(cpp_type_expr.pointee, Named) \
      and cpp_type_expr.pointee.nested_name == [self.cpp_type_name]:
      if cpp_type_expr.pointee.is_const:
        dq = dir_qual.const_reference
      else:
        dq = dir_qual.mutable_reference
      return DirQualTypeInfo(
        dq,
        KLExtTypeAliasTypeInfo(
          self.jinjenv,
          self.nested_name,
          cpp_type_expr.pointee.make_unqualified(),
          self.kl_type_name,
          )
        )
