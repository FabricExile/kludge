#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

from libkludge.type_codec import TypeCodec
from libkludge.type_info import TypeInfo
from libkludge.selector import Selector
from libkludge.cpp_type_expr_parser import dir_qual
from libkludge.dir_qual_type_codec import DirQualTypeCodec
from libkludge.cpp_type_expr_parser import Void

class VoidTypeCodec(TypeCodec):

  def __init__(self, jinjenv):
    TypeCodec.__init__(
      self,
      jinjenv,
      TypeInfo(
        name = "",
        lib_expr = Void(),
        )
      )

  def build_codec_lookup_rules(self):
    tds = TypeCodec.build_codec_lookup_rules(self)
    tds["result"]["*"] = "types/builtin/void/result"
    return tds

class VoidSelector(Selector):

  def __init__(self, jinjenv):
    Selector.__init__(self, jinjenv)

  def maybe_create_dqtc(self, type_mgr, cpp_type_expr):
    if isinstance(cpp_type_expr, Void):
      return DirQualTypeCodec(
        dir_qual.direct,
        VoidTypeCodec(self.jinjenv)
        )
