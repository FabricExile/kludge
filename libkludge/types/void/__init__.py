#
# Copyright (c) 2010-2017 Fabric Software Inc. All rights reserved.
#

from libkludge.type_info import TypeInfo
from libkludge.selector import Selector
from libkludge.cpp_type_expr_parser import dir_qual
from libkludge.dir_qual_type_info import DirQualTypeInfo
from libkludge.cpp_type_expr_parser import Void

class VoidTypeInfo(TypeInfo):

  def __init__(self, jinjenv):
    TypeInfo.__init__(
      self,
      jinjenv,
      lib_expr = Void(),
      kl_name_base = '',
      )

  def build_codec_lookup_rules(self):
    tds = TypeInfo.build_codec_lookup_rules(self)
    tds["result"]["*"] = "types/builtin/void/result"
    return tds

class VoidSelector(Selector):

  def __init__(self, ext):
    Selector.__init__(self, ext)

  def get_desc(self):
    return "Void"

  def maybe_create_dqti(self, type_mgr, cpp_type_expr):
    if isinstance(cpp_type_expr, Void):
      return DirQualTypeInfo(
        dir_qual.direct,
        VoidTypeInfo(self.jinjenv)
        )
