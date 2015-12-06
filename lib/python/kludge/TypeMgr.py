from kludge.type_codecs import *
from kludge import CPPTypeExpr, CPPTypeSpec, TypeSpec, ValueName, Value, TypeInfo
import clang.cindex

class TypeMgr:

  def __init__(self):
    self._type_codecs = []
    self._cpp_type_name_to_type_info = {}
    self._cpp_type_expr_parser = CPPTypeExpr.Parser()

    # First so we don't catch in Simple...
    self.add_type_codecs(
      build_c_string_type_codecs()
      )
    self.add_type_codecs(
      build_simple_type_codecs()
      )
    self.add_type_codecs(
      build_std_string_type_codecs()
      )
    self.add_type_codecs(
      build_std_vector_type_codecs()
      )
    self.add_type_codecs(
      build_std_map_type_codecs()
      )

  def add_type_codec(self, type_codec):
    self._type_codecs.append(type_codec)

  def add_type_codecs(self, type_codecs):
    for type_codec in type_codecs:
      self.add_type_codec(type_codec)

  @staticmethod
  def parse_value(value):
    if isinstance(value, CPPTypeExpr.Type):
      if isinstance(value, CPPTypeExpr.Void):
        return None, None
      cpp_type_expr = value
      cpp_type_name = str(cpp_type_expr)
    elif isinstance(value, basestring):
      if value == "void":
        return None, None
      cpp_type_expr = None
      cpp_type_name = void
    elif isinstance(value, clang.cindex.Type):
      cpp_type_name = value.spelling
      if cpp_type_name == "void":
        return None, None
      cpp_type_expr = None
    else:
      raise Exception("unexpected argument type")
    return cpp_type_name, cpp_type_expr

  def maybe_get_type_info(self, value):
    if hasattr(value, '__iter__'):
      result = []
      for v in value:
        r = self.maybe_get_type_info(v)
        if not r:
          return None
        result.append(r)
      return result
    else:
      cpp_type_name, cpp_type_expr = TypeMgr.parse_value(value)
      if not cpp_type_name:
        return TypeInfo.VOID

      type_info = self._cpp_type_name_to_type_info.get(cpp_type_name, None)
      if type_info:
        return type_info

      if not cpp_type_expr:
        try:
          cpp_type_expr = self._cpp_type_expr_parser.parse(cpp_type_name)
        except:
          raise Exception(cpp_type_name + ": malformed C++ type expression")

      for type_codec in self._type_codecs:
        type_spec = type_codec.maybe_match(cpp_type_expr, self)
        if type_spec:
          type_info = TypeInfo(type_codec, type_spec)
          self._cpp_type_name_to_type_info[cpp_type_name] = type_info
          return type_info

  def get_type_info(self, value):
    type_info = self.maybe_get_type_info(value)
    if type_info:
      if type_info == TypeInfo.VOID:
        return None
      else:
        return type_info

    cpp_type_name, cpp_type_expr = TypeMgr.parse_value(value)
    raise Exception(cpp_type_name + ": no EDK type association found")

  def convert_clang_params(self, clang_params):
    def mapper(clang_param):
      type_info = self.get_type_info(clang_param.clang_type)
      return type_info.make_codec(ValueName(clang_param.name))
    return map(mapper, clang_params)
