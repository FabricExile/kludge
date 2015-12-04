class GenSpec: pass

class GenStr:
  def __init__(self, value):
    self._value = value
  def make_gen(self, jinjenv):
    return lambda gd: self._value

class GenLambda:
  def __init__(self, value):
    self._value = value
  def make_gen(self, jinjenv):
    return self._value

class GenTmpl:
  def __init__(self, value):
    self._value = value
  def make_gen(self, jinjenv):
    # IMPORTANT: bake the template so it is not regenerated on each invocation
    template = jinjenv.from_string(self._value)
    return lambda gd: template.render(gd.__dict__)

class GenFile:
  def __init__(self, value):
    self._value = value
  def make_gen(self, jinjenv):
    # IMPORTANT: bake the template so it is not regenerated on each invocation
    template = jinjenv.get_template(self._value)
    return lambda gd: template.render(gd.__dict__)
