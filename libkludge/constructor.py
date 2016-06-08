#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

from clang.cindex import CursorKind
from value_name import ValueName
from result_codec import ResultCodec
from this_codec import ThisCodec
from param_codec import ParamCodec
from symbol_helpers import replace_invalid_chars
import hashlib

class Constructor:

  def __init__(
    self,
    type_mgr,
    namespace_mgr,
    current_namespace_path,
    this_type_info,
    location,
    constructor_name,
    params,
    template_param_type_map,
    ):
    self.name = constructor_name
    self.desc = "Constructor '%s'" % constructor_name
    if location:
      self.location = "%s:%s" % (location.file, location.line)
    else:
      self.location = ""

    result_type_name = "void"
    result_cpp_type_expr = namespace_mgr.resolve_cpp_type_expr(current_namespace_path, result_type_name)
    self.result = ResultCodec(
      type_mgr.get_dqti(result_cpp_type_expr)
      )

    is_mutable = True
    self.this = ThisCodec(this_type_info, is_mutable)

    self.params = params

    h = hashlib.md5()
    for param in self.params:
      h.update(param.type_info.edk.name.toplevel)
    self.edk_symbol_name = "_".join([this_type_info.kl.name.compound, self.name, h.hexdigest()])
    self.edk_symbol_name = replace_invalid_chars(self.edk_symbol_name)
