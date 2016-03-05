from decl import Decl

class Wrapping(Decl):
  def __init__(
    self,
    extname,
    include_filename,
    location,
    desc,
    type_name,
    self_codec,
    members,
    template_basename,
    ):
    Decl.__init__(
        self,
        extname,
        include_filename,
        location,
        desc,
        )
    self.type_name = type_name
    self.self = self_codec
    self.members = members
    self._template_basename = template_basename

  def jinja_stream(self, jinjenv, lang):
    return jinjenv.get_template(self._template_basename + '.template.' + lang).stream(decl = self)
