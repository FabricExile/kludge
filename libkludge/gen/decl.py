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
    self.tests = []

  def add_cpp_local_include(self, cpp_local_include):
    self.cpp_local_includes.append(cpp_local_include)
    return self

  @property
  def location(self):
    return None

  class Test(object):

    def __init__(self, name_kl, jinjenv, kl, out):
      self.name_kl = name_kl
      self._templates = {
        'kl': jinjenv.from_string(kl),
        'out': jinjenv.from_string(out),
        }
    
    def render(self, lang):
      return self._templates[lang].render(test = self).strip()

  def add_test(self, kl, out):
    self.tests.append(self.Test(self.name_kl, self.ext.jinjenv, kl, out))

  @abc.abstractmethod
  def get_kl_name(self):
    pass

  @property
  def name_kl(self):
    return self.get_kl_name()

  @abc.abstractmethod
  def get_template_basename(self):
    pass

  def render(self, context, lang):
    basename = self.get_template_basename()
    return self.ext.jinjenv.get_template(
      'gen/'+basename+'/'+basename+'.'+context+'.'+lang
      ).render({'decl': self, basename: self})
