from kludge.ast import Decl

class InPlaceStructDecl(Decl):
  def __init__(
    self,
    extname,
    include_filename,
    location,
    desc,
    name,
    members,
    ):
    Decl.__init__(self, extname, include_filename, location, desc)
    self.name = name
    self.members = members

  def jinja_stream(self, jinjenv, lang):
    return jinjenv.get_template('in_place_struct.template.' + lang).stream(in_place_struct = self)