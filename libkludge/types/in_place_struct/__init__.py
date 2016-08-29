from libkludge.type_info import TypeInfo
from libkludge.selector import Selector
from libkludge.dir_qual_type_info import DirQualTypeInfo
from libkludge.cpp_type_expr_parser import *

class InPlaceStructTypeInfo(TypeInfo):

  can_in_place = True

  def __init__(self, jinjenv, nested_name, undq_cpp_type_expr):
    TypeInfo.__init__(
      self,
      jinjenv,
      nested_name = nested_name,
      lib_expr = undq_cpp_type_expr,
      )

  def build_codec_lookup_rules(self):
    tds = TypeInfo.build_codec_lookup_rules(self)
    tds["conv"]["*"] = "protocols/conv/builtin/none"
    tds["result"]["decl_and_assign_lib"] = "types/builtin/in_place_struct/result"
    tds["result"]["indirect_lib_to_edk"] = "types/builtin/in_place_struct/result"
    tds["repr"]["*"] = "protocols/repr/builtin/inplace"
    return tds    

class InPlaceStructSelector(Selector):

  def __init__(self, jinjenv, nested_name, cpp_type_expr):
    Selector.__init__(self, jinjenv)
    self.nested_name = nested_name
    self.cpp_type_name = str(cpp_type_expr)

  def get_desc(self):
    return "InPlaceStruct:%s" % str(self.nested_name)
    
  def maybe_create_dqti(self, type_mgr, cpp_type_expr):
    if isinstance(cpp_type_expr, Named) \
      and str(cpp_type_expr) == self.cpp_type_name:
      print "%s == %s" % (str(cpp_type_expr), self.cpp_type_name)
      return DirQualTypeInfo(
        dir_qual.direct,
        InPlaceStructTypeInfo(
          self.jinjenv,
          self.nested_name,
          cpp_type_expr.make_unqualified()
          )
        )

    if isinstance(cpp_type_expr, PointerTo) \
      and isinstance(cpp_type_expr.pointee, Named) \
      and str(cpp_type_expr.pointee) == self.cpp_type_name:
      if cpp_type_expr.pointee.is_const:
        dq = dir_qual.const_pointer
      else:
        dq = dir_qual.mutable_pointer
      return DirQualTypeInfo(
        dq,
        InPlaceStructTypeInfo(
          self.jinjenv,
          self.nested_name,
          cpp_type_expr.pointee.make_unqualified()
          )
        )

    if isinstance(cpp_type_expr, ReferenceTo) \
      and isinstance(cpp_type_expr.pointee, Named) \
      and str(cpp_type_expr.pointee) == self.cpp_type_name:
      if cpp_type_expr.pointee.is_const:
        dq = dir_qual.const_reference
      else:
        dq = dir_qual.mutable_reference
      return DirQualTypeInfo(
        dq,
        InPlaceStructTypeInfo(
          self.jinjenv,
          self.nested_name,
          cpp_type_expr.pointee.make_unqualified()
          )
        )
