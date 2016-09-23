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
    self._tail_selectors = []

    self._alias_new_cpp_type_name_to_old_cpp_type_expr = {}
    self._cpp_type_name_to_dqti = {}

    self.named_selectors = {
      'owned': OwnedSelector(ext),
      'wrapped': WrappedSelector(ext),
      'in_place': InPlaceSelector(ext),
      'mirror': MirrorSelector(ext),
      }
    
    # Order is very important here!
    self.add_selector(VoidSelector(ext))
    self.add_selector(VoidPtrSelector(ext))
    self.add_selector(self.named_selectors['in_place'])
    self.add_selector(self.named_selectors['owned'])
    self.add_selector(self.named_selectors['wrapped'])
    self.add_selector(self.named_selectors['mirror'])
    self.add_selector(FixedArraySelector(ext))
    self.add_selector(PtrRefSelector(ext))

    # Special: they only add new selectors, and therefore must come last
    self.add_tail_selector(StdStringSelector(ext))
    self.add_tail_selector(StdVectorSelector(ext))
    self.add_tail_selector(StdSetSelector(ext))
    self.add_tail_selector(OtherSelector(ext))

  def add_selector(self, codec):
    print "Registered conversion selector: %s" % codec.get_desc()
    self._selectors.append(codec)

  def add_tail_selector(self, codec):
    print "Registered tail selector: %s" % codec.get_desc()
    self._tail_selectors.append(codec)

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

    keep_looking = True
    while keep_looking:
      keep_looking = False
      for selector in self._selectors:
        dqti = selector.maybe_create_dqti(self, cpp_type_expr)
        if dqti:
          assert isinstance(dqti, DirQualTypeInfo)
          print "type_mgr: Adding conversion: %s -> %s" % (cpp_type_name, dqti)
          self._cpp_type_name_to_dqti[cpp_type_name] = dqti
          return dqti
      for tail_selector in self._tail_selectors:
        dqti = tail_selector.maybe_create_dqti(self, cpp_type_expr)
        if dqti:
          print "type_mgr: Defining %s" % cpp_type_name
          assert not isinstance(dqti, DirQualTypeInfo)
          keep_looking = True
          break

  def get_dqti(self, cpp_type_expr):
    dqti = self.maybe_get_dqti(cpp_type_expr)
    if dqti:
      return dqti

    raise Exception(str(cpp_type_expr) + ": no EDK type association found")
