class DeclSet:

  def __init__(self):
    self._decls = []

  def add(self, decl):
    self._decls.append(decl)

  def jinjify(self, target, jinjenv, ext_name):
    return lambda: jinjenv.get_template('edk_ext.template.' + target).render(
      ext_name = ext_name,
      decl_gens = map(
        lambda decl: decl.jinjify(target, jinjenv),
        self._decls
        )
      )
