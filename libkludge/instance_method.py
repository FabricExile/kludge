#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

import clang
from clang.cindex import CursorKind, TypeKind
from value_name import ValueName
from result_codec import ResultCodec
from this_codec import ThisCodec
from param_codec import ParamCodec
from symbol_helpers import replace_invalid_chars
import hashlib

class InstanceMethod:

  def __init__(
    self,
    type_mgr,
    namespace_mgr,
    current_namespace_path,
    this_type_info,
    clang_instance_method,
    result,
    params,
    ):
    self.name = clang_instance_method.spelling
    self.desc = "Instance method '%s'" % clang_instance_method.displayname
    self.location = "%s:%s" % (clang_instance_method.location.file, clang_instance_method.location.line)

    is_mutable = not clang_instance_method.type.spelling.endswith('const')
    self.this = ThisCodec(this_type_info, is_mutable)

    self.result = result
    self.params = params

    h = hashlib.md5()
    for param in self.params:
      h.update(param.type_info.edk.name.toplevel)

    self.edk_symbol_name = "_".join([this_type_info.kl.name.compound, self.name, h.hexdigest()])
    self.edk_symbol_name = replace_invalid_chars(self.edk_symbol_name)
