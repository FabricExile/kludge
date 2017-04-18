from libkludge.type_info import TypeInfo
from libkludge.selector import Selector
from libkludge.cpp_type_expr_parser import dir_qual
from libkludge.dir_qual_type_info import DirQualTypeInfo
from libkludge.cpp_type_expr_parser import *

class EnumTypeInfo(TypeInfo):

  def __init__(self, jinjenv, kl_type_name, undq_cpp_type_expr):
    TypeInfo.__init__(
      self,
      jinjenv,
      kl_name_base=kl_type_name,
      lib_expr=undq_cpp_type_expr,
      is_simple=True,
      )

  def build_codec_lookup_rules(self):
    tds = TypeInfo.build_codec_lookup_rules(self)
    tds["conv"]["*"] = "protocols/conv/builtin/none"
    tds["conv"]["edk_to_lib_decl"] = "types/builtin/enum/conv"
    tds["conv"]["lib_to_edk_decl"] = "types/builtin/enum/conv"
    tds["result"]["*"] = "protocols/result/builtin/direct"
    tds["repr"]["new_begin"] = "types/builtin/enum/repr"
    tds["repr"]["new_end"] = "types/builtin/enum/repr"
    return tds

class EnumSelector(Selector):

  def __init__(
    self,
    ext,
    cpp_type_expr,
    kl_type_name,
    ):
    Selector.__init__(self, ext)
    self.cpp_type_expr = cpp_type_expr
    self.kl_type_name = kl_type_name

  def get_desc(self):
    return "Enum"
  
  def maybe_create_dqti(self, type_mgr, cpp_type_expr):
    undq_cpp_type_expr, dq = cpp_type_expr.get_undq()
    if undq_cpp_type_expr == self.cpp_type_expr:
      return DirQualTypeInfo(
        dq,
        EnumTypeInfo(
          self.jinjenv,
          self.kl_type_name,
          undq_cpp_type_expr,
          )
        )
