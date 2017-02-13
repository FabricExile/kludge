#
# Copyright (c) 2010-2017 Fabric Software Inc. All rights reserved.
#

class Test(object):

  def __init__(self, name_kl, jinjenv, kl, out, skip_epilog=False):
    self.name_kl = name_kl
    self.skip_epilog = skip_epilog
    self._templates = {
      'kl': jinjenv.from_string(kl),
      'out': jinjenv.from_string(out),
      }
  
  def render(self, lang):
    return self._templates[lang].render(test = self).lstrip()
