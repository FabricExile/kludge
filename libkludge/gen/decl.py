#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

import abc

class Decl(object):
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
    return self

  @property
  def location(self):
    return None

  def add_test(self, kl, out):
    self.ext.add_test(self.get_test_name(), kl, out)

  @abc.abstractmethod
  def get_test_name(self):
    pass

  @abc.abstractmethod
  def get_template_basename(self):
    pass

  def render(self, context, lang):
    basename = self.get_template_basename()
    return self.ext.jinjenv.get_template(
      'gen/'+basename+'/'+basename+'.'+context+'.'+lang
      ).render({'decl': self, basename: self})
