class DeclSet:

  def __init__(self):
    self._decls = []

  def add(self, decl):
    self._decls.append(decl)

  def jinja_streams(self, jinjenv, lang):
    types = []
    funcs = []
    for decl in self._decls:
      t = decl.jinja_stream_types(jinjenv, lang)
      if t:
        types.append(t)
      f = decl.jinja_stream_funcs(jinjenv, lang)
      if f:
        funcs.append(f)
    return types + funcs
