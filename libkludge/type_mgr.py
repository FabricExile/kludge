#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

from types import *
import cpp_type_expr_parser
from value_name import ValueName
from type_info import TypeInfo
from dir_qual_type_info import DirQualTypeInfo
from param_codec import ParamCodec
import clang.cindex
import clang_helpers
from cpp_type_expr_parser import Named

class TypeMgr:

  def __init__(self, jinjenv):
    self._selectors = []

    self._alias_name_to_expr = {}

    self._cpp_type_name_to_dqti = {}

    # Order is very important here!
    self.add_selector(VoidSelector(jinjenv))
    self.add_selector(CStringSelector(jinjenv))  # must come before Simple so it matches char const *
    self.add_selector(VoidPtrSelector(jinjenv))
    self.add_selector(SimpleSelector(jinjenv))
    self.add_selector(StdStringSelector(jinjenv))
    self.add_selector(FixedArraySelector(jinjenv))
    self.add_selector(StdVectorSelector(jinjenv))
    self.add_selector(StdMapSelector(jinjenv))

  def create_cpp_type_expr_parser(self):
    return cpp_type_expr_parser.Parser(self._alias_name_to_expr)

  def add_selector(self, codec):
    print "Registered conversion selector: %s" % codec.get_desc()
    self._selectors.append(codec)

  def add_dqti(self, cpp_type_name, dqti):
    print "Adding type conversion: %s -> %s" % (cpp_type_name, dqti.get_desc())
    self._cpp_type_name_to_dqti[cpp_type_name] = dqti

  def add_type_alias(self, new_nested_name, new_cpp_type_expr, old_cpp_type_expr):
    old_dqti = self.maybe_get_dqti(old_cpp_type_expr)
    if old_dqti:
      old_type_info = old_dqti.type_info
      new_type_info = TypeInfo(
        old_type_info.jinjenv,
        lib_expr = new_cpp_type_expr,
        nested_name = new_nested_name,
        )
      self._alias_name_to_expr[str(new_cpp_type_expr)] = old_type_info.lib.expr
      return new_type_info, old_type_info
    else:
      return None, None

  def maybe_get_dqti(self, cpp_type_expr):
    cpp_type_name = str(cpp_type_expr)

    dqti = self._cpp_type_name_to_dqti.get(cpp_type_name)
    if dqti:
      return dqti

    for selector in self._selectors:
      dqti = selector.maybe_create_dqti(self, cpp_type_expr)
      if dqti:
        self.add_dqti(cpp_type_name, dqti)
        return dqti

  def get_dqti(self, cpp_type_expr):
    dqti = self.maybe_get_dqti(cpp_type_expr)
    if dqti:
      return dqti

    raise Exception(str(cpp_type_expr) + ": no EDK type association found")
