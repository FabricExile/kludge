from decl import Decl
from libkludge.value_name import ValueName
from libkludge.cpp_type_expr_parser import *

class Alias(Decl):
  def __init__(
    self,
    ext,
    new_kl_global_name,
    old_type_info,
    ):
    Decl.__init__(
      self,
      ext,
      )
    self.new_kl_global_name = new_kl_global_name
    self.old_type_info = old_type_info

  def get_desc(self):
    return "Alias KL[%s] -> %s" % (self.new_kl_global_name, self.old_type_info)

  def get_test_name(self):
    return self.new_kl_global_name

  def get_template_path(self):
    return 'generate/alias/alias'
