#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

from libkludge.cpp_type_expr_parser import dir_qual
from libkludge.dir_qual_type_codec import DirQualTypeCodec
from result_codec import ResultCodec
from param_codec import ParamCodec

class Member:

  def __init__(
    self,
    type_codec,
    name,
    is_public,
    ):
    dqtc = DirQualTypeCodec(dir_qual.direct, type_codec)
    self.type = type_codec
    self.result = ResultCodec(dqtc)
    self.param = ParamCodec(dqtc, name)
    self.name = name
    self.is_public = is_public

  @property
  def type_info(self):
      return self.type.type_info
