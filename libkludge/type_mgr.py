#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

from types import *
import cpp_type_expr_parser
from value_name import ValueName
from type_info import TypeInfo
from dir_qual_type_info import DirQualTypeInfo
from param_codec import ParamCodec
from cpp_type_expr_parser import *

class TypeMgr:

  def __init__(self, ext):
    self._selectors = []

    self._alias_new_cpp_type_name_to_old_cpp_type_expr = {}
    self._cpp_type_name_to_dqti = {}

    self.selectors = {
      'owned': OwnedSelector(ext),
      'wrapped': WrappedSelector(ext),
      'in_place': InPlaceSelector(ext),
      }
    
    # Order is very important here!
    self.add_selector(VoidSelector(ext))
    self.add_selector(VoidPtrSelector(ext))
    self.add_selector(StdVectorSelector(ext))
    self.add_selector(self.selectors['in_place'])
    self.add_selector(self.selectors['owned'])
    self.add_selector(self.selectors['wrapped'])
    self.add_selector(StdStringSelector(ext))
    # self.add_selector(FixedArraySelector(ext))
    # self.add_selector(StdMapSelector(ext))
    self.add_selector(PtrRefSelector(ext))

  def add_selector(self, codec):
    print "Registered conversion selector: %s" % codec.get_desc()
    self._selectors.append(codec)

  def has_alias(self, new_cpp_type_expr):
    return self._alias_new_cpp_type_name_to_old_cpp_type_expr.has_key(str(new_cpp_type_expr))

  def add_alias(self, new_cpp_type_expr, old_cpp_type_expr):
    self._alias_new_cpp_type_name_to_old_cpp_type_expr[str(new_cpp_type_expr)] = old_cpp_type_expr

  def maybe_get_dqti(self, cpp_type_expr):
    undq_cpp_type_expr, dq = cpp_type_expr.get_undq()

    while True:
      undq_cpp_type_name = str(undq_cpp_type_expr)
      alias_cpp_type_expr = self._alias_new_cpp_type_name_to_old_cpp_type_expr.get(undq_cpp_type_name)
      if not alias_cpp_type_expr:
        break
      undq_cpp_type_expr = alias_cpp_type_expr

    cpp_type_expr = undq_cpp_type_expr.get_redq(dq)

    cpp_type_name = str(cpp_type_expr)

    # print "type_mgr: Checking cache for %s" % cpp_type_name
    dqti = self._cpp_type_name_to_dqti.get(cpp_type_name)
    if dqti:
      # print "type_mgr: Found cached conversion %s -> %s" % (cpp_type_name, dqti)
      return dqti

    for selector in self._selectors:
      dqti = selector.maybe_create_dqti(self, cpp_type_expr)
      if dqti:
        print "type_mgr: Adding conversion: %s -> %s" % (cpp_type_name, dqti)
        self._cpp_type_name_to_dqti[cpp_type_name] = dqti
        if selector.should_create_ptr_ref:
          self.maybe_get_dqti(PointerTo(cpp_type_expr))
        return dqti

  def get_dqti(self, cpp_type_expr):
    dqti = self.maybe_get_dqti(cpp_type_expr)
    if dqti:
      return dqti

    raise Exception(str(cpp_type_expr) + ": no EDK type association found")
