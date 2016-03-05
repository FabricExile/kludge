from decl import Decl

class WrappedPtrDecl(Decl):
  def __init__(
    self,
    extname,
    include_filename,
    location,
    desc,
    name,
    self_codec,
    members,
    ):
    Decl.__init__(
        self,
        extname,
        include_filename,
        location,
        "Wrapping of '%s' through WrappedPtr" % desc
        )
    self.name = name
    self.self = self_codec
    self.members = members

  def jinja_stream(self, jinjenv, lang):
    return jinjenv.get_template('wrapped_ptr_decl.template.' + lang).stream(decl = self)
