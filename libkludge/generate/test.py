#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

class Test(object):

  def __init__(self, name_kl, jinjenv, kl, out):
    self.name_kl = name_kl
    self._templates = {
      'kl': jinjenv.from_string(kl),
      'out': jinjenv.from_string(out),
      }
  
  def render(self, lang):
    return self._templates[lang].render(test = self).lstrip()
