#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

from libkludge.type_codec import TypeCodec
from libkludge.type_info import TypeInfo
from libkludge.selector import Selector
from libkludge.dir_qual_type_codec import DirQualTypeCodec
from libkludge.cpp_type_expr_parser import *

const_cpp_type_expr = PointerTo(Const(Void()))
mutable_cpp_type_expr = PointerTo(Void())

class ConstVoidPtrTypeCodec(TypeCodec):

  is_in_place = True

  def __init__(self, jinjenv):
    TypeCodec.__init__(
      self,
      jinjenv,
      TypeInfo(
        name = "Data",
        lib_expr = const_cpp_type_expr,
        )
      )

  def build_type_dir_spec(self):
    tds = TypeCodec.build_type_dir_spec(self)
    tds["conv"]["*"] = "protocols/conv/builtin/none_cast_away_const"
    tds["result"]["*"] = "protocols/result/builtin/direct"
    return tds

class MutableVoidPtrTypeCodec(TypeCodec):

  is_in_place = True

  def __init__(self, jinjenv):
    TypeCodec.__init__(
      self,
      jinjenv,
      TypeName(
        kl_base = "Data",
        kl_suffix = "",
        edk = "::Fabric::EDK::KL::Data",
        lib_expr = mutable_cpp_type_expr,
        )
      )

  def build_type_dir_spec(self):
    tds = TypeCodec.build_type_dir_spec(self)
    tds["conv"]["*"] = "protocols/conv/builtin/none"
    tds["result"]["*"] = "protocols/result/builtin/direct"
    return tds

class VoidPtrSelector(Selector):

  def __init__(self, jinjenv):
    Selector.__init__(self, jinjenv)

  def maybe_create_dqtc(self, type_mgr, cpp_type_expr):
    if cpp_type_expr == const_cpp_type_expr:
      return DirQualTypeCodec(
        dir_qual.direct,
        ConstVoidPtrTypeCodec(self.jinjenv)
        )
    if cpp_type_expr == mutable_cpp_type_expr:
      return DirQualTypeCodec(
        dir_qual.direct,
        MutableVoidPtrTypeCodec(self.jinjenv)
        )
