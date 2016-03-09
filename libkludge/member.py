#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

from libkludge.cpp_type_expr_parser import dir_qual
from libkludge.dir_qual_type_info import DirQualTypeInfo
from result_codec import ResultCodec
from param_codec import ParamCodec

class Member:

  def __init__(
    self,
    type_info,
    name,
    is_public,
    ):
    self.type_info = type_info
    self.name = name
    self.is_public = is_public

    dqti = DirQualTypeInfo(dir_qual.direct, type_info)
    self.result = ResultCodec(dqti)
    self.param = ParamCodec(dqti, name)
