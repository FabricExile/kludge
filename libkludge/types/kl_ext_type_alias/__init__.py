from libkludge.type_info import TypeInfo
from libkludge.selector import Selector
from libkludge.dir_qual_type_info import DirQualTypeInfo
from libkludge.cpp_type_expr_parser import *

class KLExtTypeAliasTypeInfo(TypeInfo):

  can_in_place = True

  def __init__(self, jinjenv, undq_cpp_type_expr, kl_type_name):
    TypeInfo.__init__(
      self,
      jinjenv,
      kl_name_base = kl_type_name,
      lib_expr = undq_cpp_type_expr,
      )

  def build_codec_lookup_rules(self):
    tds = TypeInfo.build_codec_lookup_rules(self)
    tds["conv"]["*"] = "protocols/conv/builtin/none"
    tds["result"]["decl_and_assign_lib_begin"] = "types/builtin/kl_ext_type_alias/result"
    tds["result"]["decl_and_assign_lib_end"] = "types/builtin/kl_ext_type_alias/result"
    tds["result"]["indirect_lib_to_edk"] = "types/builtin/kl_ext_type_alias/result"
    tds["repr"]["defn_kl"] = "types/builtin/kl_ext_type_alias/repr"
    return tds    

class KLExtTypeAliasSelector(Selector):

  def __init__(self, jinjenv, cpp_type_expr, kl_type_name):
    Selector.__init__(self, jinjenv)
    self.cpp_type_expr = cpp_type_expr
    self.kl_type_name = kl_type_name

  def get_desc(self):
    return "KLExtTypeAlias:%s" % str(self.cpp_type_expr)
    
  def maybe_create_dqti(self, type_mgr, cpp_type_expr):
    undq_cpp_type_expr, dq = cpp_type_expr.get_undq()
    if undq_cpp_type_expr == self.cpp_type_expr:
      return DirQualTypeInfo(
        dq,
        KLExtTypeAliasTypeInfo(
          self.jinjenv,
          self.cpp_type_expr,
          self.kl_type_name,
          )
        )
