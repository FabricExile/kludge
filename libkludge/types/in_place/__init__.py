from libkludge.type_info import TypeInfo
from libkludge.selector import Selector
from libkludge.dir_qual_type_info import DirQualTypeInfo
from libkludge.cpp_type_expr_parser import *

class InPlaceTypeInfo(TypeInfo):

  can_in_place = True

  def __init__(
    self,
    jinjenv,
    kl_type_name,
    nested_name,
    undq_cpp_type_expr,
    ):
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
    tds["result"]["decl_and_assign_lib_begin"] = "types/builtin/in_place/result"
    tds["result"]["indirect_lib_to_edk"] = "types/builtin/in_place/result"
    return tds    

class InPlaceSelector(Selector):

  def __init__(
    self,
    jinjenv,
    kl_type_name,
    nested_name,
    cpp_type_expr,
    ):
    Selector.__init__(self, jinjenv)
    self.kl_type_name = kl_type_name
    self.nested_name = nested_name
    self.cpp_type_expr = cpp_type_expr

  def get_desc(self):
    return "InPlace:%s" % str(self.nested_name)
    
  def maybe_create_dqti(self, type_mgr, cpp_type_expr):
    if cpp_type_expr == self.cpp_type_expr:
      return DirQualTypeInfo(
        dir_qual.direct,
        InPlaceTypeInfo(
          self.jinjenv,
          self.kl_type_name,
          self.nested_name,
          cpp_type_expr.make_unqualified()
          )
        )

    if isinstance(cpp_type_expr, PointerTo) \
      and cpp_type_expr.pointee.make_unqualified() == self.cpp_type_expr:
      if cpp_type_expr.pointee.is_const:
        dq = dir_qual.const_pointer
      else:
        dq = dir_qual.mutable_pointer
      return DirQualTypeInfo(
        dq,
        InPlaceTypeInfo(
          self.jinjenv,
          self.kl_type_name,
          self.nested_name,
          cpp_type_expr.pointee.make_unqualified()
          )
        )

    if isinstance(cpp_type_expr, ReferenceTo) \
      and cpp_type_expr.pointee.make_unqualified() == self.cpp_type_expr:
      if cpp_type_expr.pointee.is_const:
        dq = dir_qual.const_reference
      else:
        dq = dir_qual.mutable_reference
      return DirQualTypeInfo(
        dq,
        InPlaceTypeInfo(
          self.jinjenv,
          self.kl_type_name,
          self.nested_name,
          cpp_type_expr.pointee.make_unqualified()
          )
        )
