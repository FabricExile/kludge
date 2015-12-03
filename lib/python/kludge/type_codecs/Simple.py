from kludge import TypeCodec
from kludge.type_codecs.recipes import *
from kludge import CPPTypeExpr
from kludge import SimpleTypeName

class SimpleBase(TypeCodec):

  cpp_base_type_name_to_kl_type_name = {
    "bool": "Boolean",
    "char": "SInt8",
    "int8_t": "SInt8",
    "unsigned char": "UInt8",
    "uint8_t": "UInt8",
    "short": "SInt16",
    "int16_t": "SInt16",
    "unsigned short": "UInt16",
    "uint16_t": "UInt16",
    "int": "SInt32",
    "int32_t": "SInt32",
    "unsigned int": "UInt32",
    "uint32_t": "UInt32",
    "long": "SInt32",           # Warning: Linux + OS X ONLY
    "unsigned long": "UInt32",  # Warning: Linux + OS X ONLY
    "long long": "SInt64",
    "int64_t": "SInt64",
    "unsigned long long": "UInt64",
    "uint64_t": "UInt64",
    "float": "Float32",
    "double": "Float64",
    }

  def __init__(self, type_name):
    TypeCodec.__init__(self, type_name)

@direct_result
@in_param
@cpp_arg_is_edk_param_ref
class SimpleValue(SimpleBase):

  @classmethod
  def maybe_get_type_codec(cls, cpp_type_expr, type_mgr):
    if isinstance(cpp_type_expr, CPPTypeExpr.Direct):
      cpp_base_type_name = cpp_type_expr.get_unqualified_desc()
      kl_type_name = cls.cpp_base_type_name_to_kl_type_name.get(cpp_base_type_name)
      if kl_type_name:
        return SimpleValue(SimpleTypeName(kl_type_name, str(cpp_type_expr)))

  def __init__(self, type_name):
    SimpleBase.__init__(self, type_name)

@direct_result
@in_param
@cpp_arg_is_edk_param_ref
class SimpleConstRef(SimpleBase):

  @classmethod
  def maybe_get_type_codec(cls, cpp_type_expr, type_mgr):
    if isinstance(cpp_type_expr, CPPTypeExpr.Reference) \
      and cpp_type_expr.pointee.is_const \
      and isinstance(cpp_type_expr.pointee, CPPTypeExpr.Direct):
      cpp_base_type_name = cpp_type_expr.pointee.get_unqualified_desc()
      kl_type_name = cls.cpp_base_type_name_to_kl_type_name.get(cpp_base_type_name)
      if kl_type_name:
        return SimpleConstRef(SimpleTypeName(kl_type_name, str(cpp_type_expr)))

  def __init__(self, type_name):
    SimpleBase.__init__(self, type_name)

@direct_result_by_deref
@in_param
@cpp_arg_is_edk_param_ptr
class SimpleConstPtr(SimpleBase):

  @classmethod
  def maybe_get_type_codec(cls, cpp_type_expr, type_mgr):
    if isinstance(cpp_type_expr, CPPTypeExpr.Pointer) \
      and cpp_type_expr.pointee.is_const \
      and isinstance(cpp_type_expr.pointee, CPPTypeExpr.Direct):
      cpp_base_type_name = cpp_type_expr.pointee.get_unqualified_desc()
      kl_type_name = cls.cpp_base_type_name_to_kl_type_name.get(cpp_base_type_name)
      if kl_type_name:
        return SimpleConstPtr(SimpleTypeName(kl_type_name, str(cpp_type_expr)))

  def __init__(self, type_name):
    SimpleBase.__init__(self, type_name)

@direct_result
@io_param
@cpp_arg_is_edk_param_ref
class SimpleMutableRef(SimpleBase):

  @classmethod
  def maybe_get_type_codec(cls, cpp_type_expr, type_mgr):
    if isinstance(cpp_type_expr, CPPTypeExpr.Reference) \
      and cpp_type_expr.pointee.is_mutable \
      and isinstance(cpp_type_expr.pointee, CPPTypeExpr.Direct):
      cpp_base_type_name = cpp_type_expr.pointee.get_unqualified_desc()
      kl_type_name = cls.cpp_base_type_name_to_kl_type_name.get(cpp_base_type_name)
      if kl_type_name:
        return SimpleMutableRef(SimpleTypeName(kl_type_name, str(cpp_type_expr)))

  def __init__(self, type_name):
    SimpleBase.__init__(self, type_name)

@direct_result_by_deref
@io_param
@cpp_arg_is_edk_param_ptr
class SimpleMutablePtr(SimpleBase):

  @classmethod
  def maybe_get_type_codec(cls, cpp_type_expr, type_mgr):
    if isinstance(cpp_type_expr, CPPTypeExpr.Pointer) \
      and cpp_type_expr.pointee.is_mutable \
      and isinstance(cpp_type_expr.pointee, CPPTypeExpr.Direct):
      cpp_base_type_name = cpp_type_expr.pointee.get_unqualified_desc()
      kl_type_name = cls.cpp_base_type_name_to_kl_type_name.get(cpp_base_type_name)
      if kl_type_name:
        return SimpleMutablePtr(SimpleTypeName(kl_type_name, str(cpp_type_expr)))

  def __init__(self, type_name):
    SimpleBase.__init__(self, type_name)
