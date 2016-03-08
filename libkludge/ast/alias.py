from decl import Decl
from libkludge.value_name import ValueName
from libkludge.cpp_type_expr_parser import *

class Alias(Decl):
  def __init__(
    self,
    extname,
    include_filename,
    location,
    desc,
    new_type_info,
    old_type_info,
    ):
    Decl.__init__(
        self,
        extname,
        include_filename,
        location,
        "Type alias '%s'" % desc
        )
    self.new_type_info = new_type_info
    self.old_type_info = old_type_info

  def jinja_stream(self, jinjenv, lang):
    return jinjenv.get_template('ast/builtin/alias.template.' + lang).stream(decl = self)
