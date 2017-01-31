#
# Copyright (c) 2010-2017 Fabric Software Inc. All rights reserved.
#

import abc

class Selector(object):

  __metaclass__ = abc.ABCMeta

  def __init__(self, ext):
    self.ext = ext

  @property
  def jinjenv(self):
    return self.ext.jinjenv

  @abc.abstractmethod
  def maybe_create_dqti(self, type_mgr, cpp_type_expr):
    pass
