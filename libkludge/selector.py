#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

import abc

class Selector:

  __metaclass__ = abc.ABCMeta

  def __init__(self, jinjenv):
    self.jinjenv = jinjenv

  @abc.abstractmethod
  def maybe_create_dqti(self, type_mgr, cpp_type_expr):
    pass
