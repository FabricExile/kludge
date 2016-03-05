from kludge import TypeCodec, GenLambda

def build_simple_type_codecs():
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

  class SimpleTypeCodecBase(TypeCodec): pass
  SimpleTypeCodecBase.conv_none()
  SimpleTypeCodecBase.result_direct()

  class SimpleValueTypeCodec(SimpleTypeCodecBase): pass
  SimpleValueTypeCodec.match_value_by_dict(cpp_base_type_to_kl_base_type)
  SimpleValueTypeCodec.traits_value()
  SimpleValueTypeCodec.prop_in_place()

  class SimpleConstRefTypeCodec(SimpleTypeCodecBase): pass
  SimpleConstRefTypeCodec.match_const_ref_by_dict(cpp_base_type_to_kl_base_type)
  SimpleConstRefTypeCodec.traits_const_ref()

  class SimpleConstPtrTypeCodec(SimpleTypeCodecBase): pass
  SimpleConstPtrTypeCodec.match_const_ptr_by_dict(cpp_base_type_to_kl_base_type)
  SimpleConstPtrTypeCodec.traits_const_ptr()

  class SimpleMutableRefType(SimpleTypeCodecBase): pass
  SimpleMutableRefType.match_mutable_ref_by_dict(cpp_base_type_to_kl_base_type)
  SimpleMutableRefType.traits_mutable_ref()
  SimpleMutableRefType.param_io()

  class SimpleMutablePtrType(SimpleTypeCodecBase): pass
  SimpleMutablePtrType.match_mutable_ptr_by_dict(cpp_base_type_to_kl_base_type)
  SimpleMutablePtrType.traits_mutable_ptr()
  SimpleMutablePtrType.param_io()

  return [
    SimpleValueTypeCodec,
    SimpleConstRefTypeCodec,
    SimpleConstPtrTypeCodec,
    SimpleMutableRefType,
    SimpleMutablePtrType,
    ]
