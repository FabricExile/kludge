import abc

class Type:

  __metaclass__ = abc.ABCMeta

  def __init__(self):
    self.is_const = False
    self.is_volatile = False

  @property
  def is_mutable(self):
    return not self.is_const

  def make_const(self):
    self.is_const = True
    return self

  def make_volatile(self):
    self.is_volatile = True
    return self

  @abc.abstractmethod
  def get_desc(self):
    pass

  @abc.abstractmethod
  def get_unqualified_desc(self):
    pass

  def __str__(self):
    return self.get_desc()

  def __eq__(self, other):
    return type(self) == type(other) \
      and self.is_const == other.is_const \
      and self.is_volatile == other.is_volatile

  def __ne__(self, other):
    return not self == other

class Direct(Type):

  def __init__(self):
    Type.__init__(self)

  def get_desc(self):
    result = ""
    if self.is_const:
      result += "const "
    if self.is_volatile:
      result += "volatile "
    return result + self.get_unqualified_desc()

class Void(Direct):

  def __init__(self):
    Direct.__init__(self)

  def get_unqualified_desc(self):
    return "void"

class Bool(Direct):

  def __init__(self):
    Direct.__init__(self)

  def get_unqualified_desc(self):
    return "bool"

class Numeric(Direct):

  def __init__(self):
    Direct.__init__(self)

class Integer(Numeric):

  def __init__(self):
    Numeric.__init__(self)
    self.is_signed = True

  def make_unsigned(self):
    self.is_signed = False
    return self

  def make_signed(self):
    self.is_signed = True
    return self

  def get_unqualified_desc(self):
    result = ""
    if not self.is_signed:
      result = "unsigned "
    result += self.get_signed_desc()
    return result

  @abc.abstractmethod
  def get_signed_desc(self):
    pass

  def __eq__(self, other):
    return Numeric.__eq__(self, other) \
      and self.is_signed == other.is_signed

class Char(Integer):

  def __init__(self):
    Integer.__init__(self)

  def get_signed_desc(self):
    return "char"

class Short(Integer):

  def __init__(self):
    Integer.__init__(self)

  def get_signed_desc(self):
    return "short"

class Int(Integer):

  def __init__(self):
    Integer.__init__(self)

  def get_signed_desc(self):
    return "int"

class Long(Integer):

  def __init__(self):
    Integer.__init__(self)

  def get_signed_desc(self):
    return "long"

class LongLong(Integer):

  def __init__(self):
    Integer.__init__(self)

  def get_signed_desc(self):
    return "long long"

class FloatingPoint(Numeric):

  def __init__(self):
    Numeric.__init__(self)

class Float(FloatingPoint):

  def __init__(self):
    FloatingPoint.__init__(self)

  def get_unqualified_desc(self):
    return "float"

class Double(FloatingPoint):

  def __init__(self):
    FloatingPoint.__init__(self)

  def get_unqualified_desc(self):
    return "double"

class Named(Direct):

  def __init__(self, name):
    Direct.__init__(self)
    self.name = name

  def get_unqualified_desc(self):
    return self.name

  def __eq__(self, other):
    return Direct.__eq__(self, other) \
      and self.name == other.name

class Template(Direct):

  def __init__(self, name, params):
    Direct.__init__(self)
    self.name = name
    self.params = params

  def get_unqualified_desc(self):
    return self.name + "< " + ", ".join(map(
      lambda param: param.get_desc(),
      self.params
      )) + " >"

  def __eq__(self, other):
    return Direct.__eq__(self, other) \
      and self.name == other.name \
      and self.params == other.params

class Indirect(Type):

  def __init__(self, pointee):
    Type.__init__(self)
    self.pointee = pointee

  def get_desc(self):
    result = self.get_unqualified_desc()
    if self.is_const:
      result += " const"
    if self.is_volatile:
      result += " volatile"
    return result

  def __eq__(self, other):
    return Type.__eq__(self, other) \
      and self.pointee == other.pointee

class PointerTo(Indirect):

  def __init__(self, pointee):
    Indirect.__init__(self, pointee)

  def get_unqualified_desc(self):
    return self.pointee.get_desc() + " *"

class ReferenceTo(Indirect):

  def __init__(self, pointee):
    Indirect.__init__(self, pointee)

  def get_unqualified_desc(self):
    return self.pointee.get_desc() + " &"

def Const(ty):
  return ty.make_const()
