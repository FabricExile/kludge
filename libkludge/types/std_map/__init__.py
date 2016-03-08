from libkludge.type_codec import TypeCodec
from libkludge.type_info import TypeInfo
from libkludge.selector import Selector
from libkludge.dir_qual_type_codec import DirQualTypeCodec
from libkludge.cpp_type_expr_parser import *

class StdMapTypeCodec(TypeCodec):

  def __init__(self, jinjenv, undq_cpp_type_expr, key_dqtc, value_dqtc):
    TypeCodec.__init__(
      self,
      jinjenv,
      TypeInfo(
        kl_name_base = value_dqtc.type_info.kl.name.base,
        kl_name_suffix = "[" + key_dqtc.type_info.kl.name.compound + "]" + value_dqtc.type_info.kl.name.suffix,
        edk_name_toplevel = "::Fabric::EDK::KL::Dict< " + key_dqtc.type_info.edk.name.toplevel + ", " + value_dqtc.type_info.edk.name.toplevel + " >",
        lib_expr = undq_cpp_type_expr,
        ),
      [key_dqtc, value_dqtc]
      )

  def build_codec_lookup_rules(self):
    tds = TypeCodec.build_codec_lookup_rules(self)
    tds["conv"]["*"] = "types/builtin/std_map/conv"
    return tds

class StdMapSelector(Selector):

  def __init__(self, jinjenv):
    Selector.__init__(self, jinjenv)

  def maybe_create_dqtc(self, type_mgr, cpp_type_expr):
    if isinstance(cpp_type_expr, Template) \
      and cpp_type_expr.name == "std::map" \
      and len(cpp_type_expr.params) == 2:
      key_dqtc = type_mgr.get_dqtc(cpp_type_expr.params[0])
      value_dqtc = type_mgr.get_dqtc(cpp_type_expr.params[1])
      return DirQualTypeCodec(
        dir_qual.direct,
        StdMapTypeCodec(
          self.jinjenv,
          cpp_type_expr.make_unqualified(),
          key_dqtc,
          value_dqtc,
          )
        )
    if isinstance(cpp_type_expr, ReferenceTo) \
      and isinstance(cpp_type_expr.pointee, Template) \
      and cpp_type_expr.pointee.is_const \
      and cpp_type_expr.pointee.name == "std::map" \
      and len(cpp_type_expr.pointee.params) == 2:
      key_dqtc = type_mgr.get_dqtc(cpp_type_expr.pointee.params[0])
      value_dqtc = type_mgr.get_dqtc(cpp_type_expr.pointee.params[1])
      return DirQualTypeCodec(
        dir_qual.const_reference,
        StdMapTypeCodec(
          self.jinjenv,
          cpp_type_expr.pointee.make_unqualified(),
          key_dqtc,
          value_dqtc,
          )
        )
