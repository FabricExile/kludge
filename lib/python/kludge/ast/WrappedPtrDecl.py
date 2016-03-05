from kludge.ast import Decl

class WrappedPtrDecl(Decl):
  def __init__(
    self,
    extname,
    include_filename,
    location,
    desc,
    name,
    self_type_codec,
    members,
    ):
    Decl.__init__(self, extname, include_filename, location, desc)
    self.name = name
    self.self = self_type_codec
    self.members = members

  def jinja_stream(self, jinjenv, lang):
    return jinjenv.get_template('wrapped_ptr.template.' + lang).stream(wrapped_ptr = self)
