from decl import Decl
from libkludge.value_name import ValueName
from libkludge.cpp_type_expr_parser import *

class Alias(Decl):
  def __init__(
    self,
    ext,
    new_kl_type_name,
    old_type_info,
    ):
    Decl.__init__(
      self,
      ext,
      "Type alias %s -> %s" % (new_kl_type_name, old_type_info.lib.name)
      )
    self.new_kl_type_name = new_kl_type_name
    self.old_type_info = old_type_info

  def render(self, lang):
    return self.ext.jinjenv.get_template("gen/alias/alias." + lang).render(decl=self, alias=self)
