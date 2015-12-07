from kludge.ast import Decl

class WrappedPtrDecl(Decl):
  def __init__(
    self,
    extname,
    include_filename,
    location,
    desc,
    name,
    ):
    Decl.__init__(self, extname, include_filename, location, desc)
    self.name = name

  def jinja_stream(self, jinjenv, lang):
    return jinjenv.get_template('wrapped_ptr.template.' + lang).stream(wrapped_ptr = self)
