from libkludge.type_info import TypeInfo
from libkludge.selector import Selector
from libkludge.dir_qual_type_info import DirQualTypeInfo
from libkludge.cpp_type_expr_parser import *

class InPlaceStructTypeInfo(TypeInfo):

  is_in_place = True

  def __init__(self, jinjenv, name, undq_cpp_type_expr):
    TypeInfo.__init__(
      self,
      jinjenv,
      name = name,
      lib_expr = undq_cpp_type_expr,
      )

  def build_codec_lookup_rules(self):
    tds = TypeInfo.build_codec_lookup_rules(self)
    tds["conv"]["*"] = "protocols/conv/builtin/none"
    tds["result"]["decl_and_assign_lib"] = "types/builtin/in_place_struct/result"
    tds["result"]["indirect_lib_to_edk"] = "types/builtin/in_place_struct/result"
    return tds    

class InPlaceStructSelector(Selector):

  def __init__(self, jinjenv, cpp_type_name):
    Selector.__init__(self, jinjenv)
    self.cpp_type_name = cpp_type_name

  def maybe_create_dqti(self, type_mgr, cpp_type_expr):
    if isinstance(cpp_type_expr, Named) \
      and cpp_type_expr.name == self.cpp_type_name:
      return DirQualTypeInfo(
        dir_qual.direct,
        InPlaceStructTypeInfo(
          self.jinjenv,
          self.cpp_type_name,
          cpp_type_expr.make_unqualified()
          )
        )
    if isinstance(cpp_type_expr, PointerTo) \
      and isinstance(cpp_type_expr.pointee, Named) \
      and cpp_type_expr.pointee.name == self.cpp_type_name:
      if cpp_type_expr.pointee.is_const:
        dq = dir_qual.const_pointer
      else:
        dq = dir_qual.mutable_pointer
      return DirQualTypeInfo(
        dq,
        InPlaceStructTypeInfo(
          self.jinjenv,
          self.cpp_type_name,
          cpp_type_expr.pointee.make_unqualified()
          )
        )
    if isinstance(cpp_type_expr, ReferenceTo) \
      and isinstance(cpp_type_expr.pointee, Named) \
      and cpp_type_expr.pointee.name == self.cpp_type_name:
      if cpp_type_expr.pointee.is_const:
        dq = dir_qual.const_reference
      else:
        dq = dir_qual.mutable_reference
      return DirQualTypeInfo(
        dq,
        InPlaceStructTypeInfo(
          self.jinjenv,
          self.cpp_type_name,
          cpp_type_expr.pointee.make_unqualified()
          )
        )
