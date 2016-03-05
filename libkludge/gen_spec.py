class GenSpec: pass

class GenStr:
  def __init__(self, value):
    self._value = value
  def make_gen(self):
    return lambda gd: self._value

class GenLambda:
  def __init__(self, value):
    self._value = value
  def make_gen(self):
    return self._value

class GenTmpl:
  def __init__(self, value):
    self._value = value
  def make_gen(self):
    # IMPORTANT: bake the template so it is not regenerated on each invocation
    template = GenSpec.jinjenv.from_string(self._value.strip())
    return lambda gd: template.render(gd.__dict__)

class GenFile:
  def __init__(self, value):
    self._value = value
  def make_gen(self):
    # IMPORTANT: bake the template so it is not regenerated on each invocation
    template = GenSpec.jinjenv.get_template(self._value)
    return lambda gd: template.render(gd.__dict__)
