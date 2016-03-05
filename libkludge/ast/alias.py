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
    new_type_spec,
    old_type_spec,
    ):
    Decl.__init__(
        self,
        extname,
        include_filename,
        location,
        "Type alias '%s'" % desc
        )
    self.new_type = new_type_spec
    self.old_type = old_type_spec

  def jinja_stream(self, jinjenv, lang):
    return jinjenv.get_template('alias.template.' + lang).stream(alias = self)
