#
# Copyright (c) 2010-2017 Fabric Software Inc. All rights reserved.
#

class CPPValueName:

  def __init__(self, name, edk=None, lib=None):
    if edk:
      self.edk = edk
    else:
      self.edk = "_KLUDGE_EDK_"+name
    if lib:
      self.lib = lib
    else:
      self.lib = "_KLUDGE_LIB_"+name

  def child(self, index):
    return CPPValueName(
      name = None,
      edk = "%s__%d" % (self.edk, index),
      lib = "%s__%d" % (self.lib, index),
      )

class ValueName:

  def __init__(self, name):
    self.kl = name
    self.cpp = CPPValueName(name)

  @property
  def edk(self):
      return self.cpp.edk

  @property
  def lib(self):
      return self.cpp.lib
  
result_cpp_value_name = CPPValueName("RESERVED_result")
this_cpp_value_name = CPPValueName("RESERVED_this")
