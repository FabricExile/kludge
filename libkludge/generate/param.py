#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

from libkludge.param_codec import ParamCodec

class Param(object):

  def __init__(self, name, cpp_type_name):
    self.name = name
    self.cpp_type_name = cpp_type_name

  def gen_codec(self, index, dqti_resolver):
    return ParamCodec(
      dqti_resolver(self.cpp_type_name),
      "_arg%d" % index if not self.name else self.name
      )
