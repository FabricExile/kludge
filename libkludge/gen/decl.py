#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

import abc

class Decl:
  def __init__(
    self,
    ext,
    desc,
    ):
    self.ext = ext
    self.desc = desc
    self.cpp_local_includes = []

  def add_cpp_local_include(self, cpp_local_include):
    self.cpp_local_includes.append(cpp_local_include)

  @property
  def location(self):
    return None
  
  @abc.abstractmethod
  def jinja_stream_types(self, jinjenv, lang): pass

  @abc.abstractmethod
  def jinja_stream_aliases(self, jinjenv, lang): pass

  @abc.abstractmethod
  def jinja_stream_funcs(self, jinjenv, lang): pass
