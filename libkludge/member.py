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
    dqti,
    name,
    is_public,
    ):
    self.dqti = dqti
    self.name = name
    self.is_public = is_public

    self.result = ResultCodec(dqti)
    self.param = ParamCodec(dqti, name)

  @property
  def type_info(self):
    return self.dqti.type_info

  @property
  def can_in_place(self):
    return self.dqti.can_in_place

  @property
  def is_settable(self):
    return self.dqti.type_info.lib.expr.is_mutable \
      and ( self.dqti.dir_qual.is_direct \
        or self.dqti.dir_qual.is_mutable_indirect )
