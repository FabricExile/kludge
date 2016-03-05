class DeclSet:

  def __init__(self):
    self._decls = []

  def add(self, decl):
    self._decls.append(decl)

  def jinja_streams(self, jinjenv, lang):
    return map(
      lambda decl: decl.jinja_stream(jinjenv, lang),
      self._decls
      )
