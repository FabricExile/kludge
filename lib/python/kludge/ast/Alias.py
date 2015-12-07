from kludge.ast import Decl
from kludge import ValueName, Value, CPPTypeExpr

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
    Decl.__init__(self, extname, include_filename, location, desc)
    self.new_type = new_type_spec
    self.old_type = old_type_spec

  def jinja_stream(self, jinjenv, lang):
    return jinjenv.get_template('alias.template.' + lang).stream(alias = self)
