#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

from types import *
import cpp_type_expr_parser
from value_name import ValueName
from type_info import TypeInfo
from dir_qual_type_codec import DirQualTypeCodec
from param_codec import ParamCodec
import clang.cindex
from cpp_type_expr_parser import Named

class TypeMgr:

  def __init__(self, jinjenv):
    self._selectors = []

    self._alias_name_to_expr = {}

    self._cpp_type_name_to_dqtc = {}
    self._cpp_type_expr_parser = cpp_type_expr_parser.Parser(self._alias_name_to_expr)

    # Order is very important here!
    self.add_selector(VoidSelector(jinjenv))
    self.add_selector(CStringSelector(jinjenv))  # must come before Simple so it matches char const *
    self.add_selector(VoidPtrSelector(jinjenv))
    self.add_selector(SimpleSelector(jinjenv))
    self.add_selector(StdStringSelector(jinjenv))
    self.add_selector(StdVectorSelector(jinjenv))
    self.add_selector(StdMapSelector(jinjenv))

  def add_selector(self, codec):
    self._selectors.append(codec)

  def add_dqtc(self, cpp_type_name, dqtc):
    self._cpp_type_name_to_dqtc[cpp_type_name] = dqtc

  def add_type_alias(self, new_cpp_type_name, old_cpp_type_name):
    old_dqtc = self.maybe_get_dqtc(old_cpp_type_name)
    if old_dqtc:
      old_type_info = old_dqtc.type_info
      new_type_info = TypeInfo(
        lib_expr = Named(new_cpp_type_name),
        name = new_cpp_type_name,
        )
      self._alias_name_to_expr[new_cpp_type_name] = old_type_info.lib.expr
      return new_type_info, old_type_info
    else:
      return None, None

  @staticmethod
  def parse_value(value):
    if isinstance(value, cpp_type_expr_parser.Type):
      cpp_type_expr = value
      cpp_type_name = str(cpp_type_expr)
    elif isinstance(value, basestring):
      cpp_type_expr = None
      cpp_type_name = value
    elif isinstance(value, clang.cindex.Type):
      cpp_type_name = value.spelling
      cpp_type_expr = None
    else:
      raise Exception("unexpected argument type")
    return cpp_type_name, cpp_type_expr

  def maybe_get_dqtc(self, value):
    cpp_type_name, cpp_type_expr = TypeMgr.parse_value(value)
    if not cpp_type_name:
      return None

    dqtc = self._cpp_type_name_to_dqtc.get(cpp_type_name)
    if dqtc:
      return dqtc

    if not cpp_type_expr:
      try:
        cpp_type_expr = self._cpp_type_expr_parser.parse(cpp_type_name)
      except Exception as e:
        raise Exception(cpp_type_name + ": malformed C++ type expression (%s)" % str(e))

    undq_cpp_type_expr, dq = cpp_type_expr.get_undq_type_expr_and_dq()

    for selector in self._selectors:
      dqtc = selector.maybe_create_dqtc(self, cpp_type_expr)
      if dqtc:
        self.add_dqtc(cpp_type_name, dqtc)
        return dqtc

  def get_dqtc(self, value):
    dqtc = self.maybe_get_dqtc(value)
    if dqtc:
      return dqtc

    cpp_type_name, cpp_type_expr = TypeMgr.parse_value(value)
    raise Exception(cpp_type_name + ": no EDK type association found")

  def convert_clang_params(self, clang_params):
    def mapper(clang_param):
      dqtc = self.get_dqtc(clang_param.clang_type)
      return ParamCodec(dqtc, clang_param.name)
    return map(mapper, clang_params)
