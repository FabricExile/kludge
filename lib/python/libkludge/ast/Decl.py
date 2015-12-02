import abc

class Decl:
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
