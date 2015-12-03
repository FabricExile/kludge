from kludge import TypeCodec
from kludge.type_codecs.recipes import *

cpp_base_type_to_kl_base_type = {
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

@match_value_by_dict(cpp_base_type_to_kl_base_type)
@direct_result
@in_param
@cpp_arg_is_edk_param_ref
class SimpleValue(TypeCodec): pass

@match_const_ref_by_dict(cpp_base_type_to_kl_base_type)
@direct_result
@in_param
@cpp_arg_is_edk_param_ref
class SimpleConstRef(TypeCodec): pass

@match_const_ptr_by_dict(cpp_base_type_to_kl_base_type)
@direct_result_by_deref
@in_param
@cpp_arg_is_edk_param_ptr
class SimpleConstPtr(TypeCodec): pass

@match_mutable_ref_by_dict(cpp_base_type_to_kl_base_type)
@direct_result
@io_param
@cpp_arg_is_edk_param_ref
class SimpleMutableRef(TypeCodec): pass

@match_mutable_ptr_by_dict(cpp_base_type_to_kl_base_type)
@direct_result_by_deref
@io_param
@cpp_arg_is_edk_param_ptr
class SimpleMutablePtr(TypeCodec): pass
