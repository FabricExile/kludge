import abc, edk_type

class EDKDecl:
  __metaclass__ = abc.ABCMeta

  def __init__(
    self,
    extname,
    include_filename,
    location,
    desc,
    ):
    self._extname = extname
    self._include_filename = include_filename
    self._location = location
    self._desc = desc

  def gen_include_filename(self):
    return self._include_filename

  def gen_location(self):
    return self._location

  def gen_desc(self):
    return self._desc

  @abc.abstractmethod
  def jinjify(self, target, jinjenv):
    """Return a lambda that generates code for the given target (kl, cpp)"""
    return

class EDKFunc(EDKDecl):
  def __init__(
    self,
    extname,
    include_filename,
    location,
    desc,
    nested_function_name,
    params,
    ):
    EDKDecl.__init__(self, extname, include_filename, location, desc)

    self._nested_function_name = nested_function_name
    self.params = params

  def gen_kl_name(self):
    return "_".join(self._nested_function_name)

  def gen_edk_name(self):
    return self._extname + "_" + "_".join(self._nested_function_name)

  def gen_cpp_name(self):
    return "::" + "::".join(self._nested_function_name)

  def jinjify(self, target, jinjenv):
    return lambda: jinjenv.get_template('edk_func.template.'+target).render(func = self)

class EDKDeclSet:
  def __init__(self):
    self._decls = []

  def add(self, decl):
    self._decls.append(decl)

  def jinjify(self, target, jinjenv):
    return lambda: jinjenv.get_template('edk_ext.template.' + target).render(
      decl_gens = map(
        lambda decl: decl.jinjify(target, jinjenv),
        self._decls
        )
      )