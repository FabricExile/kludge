#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

ext.add_cpp_quoted_include('Simple.hpp')

ext.add_func('SimpleParams', None, [
  'bool',
  'bool const *',
  'bool *',
  'bool const &',
  'bool &',
  'int8_t',
  'int8_t const *',
  'int8_t *',
  'int8_t const &',
  'int8_t &',
  'uint8_t',
  'uint8_t const *',
  'uint8_t *',
  'uint8_t const &',
  'uint8_t &',
  'int16_t',
  'int16_t const *',
  'int16_t *',
  'int16_t const &',
  'int16_t &',
  'uint16_t',
  'uint16_t const *',
  'uint16_t *',
  'uint16_t const &',
  'uint16_t &',
  'int32_t',
  'int32_t const *',
  'int32_t *',
  'int32_t const &',
  'int32_t &',
  'uint32_t',
  'uint32_t const *',
  'uint32_t *',
  'uint32_t const &',
  'uint32_t &',
  'int64_t',
  'int64_t const *',
  'int64_t *',
  'int64_t const &',
  'int64_t &',
  'uint64_t',
  'uint64_t const *',
  'uint64_t *',
  'uint64_t const &',
  'uint64_t &',
  'float',
  'float const *',
  'float *',
  'float const &',
  'float &',
  'double',
  'double const *',
  'double *',
  'double const &',
  'double &',
  ])\
  .add_test("""
Boolean boolean;
SInt8 sint8 = -11s8;
UInt8 uint8 = 11u8;
SInt16 sint16 = -1111s16;
UInt16 uint16 = 1111u16;
SInt32 sint32 = -11111111s32;
UInt32 uint32 = 11111111u32;
SInt64 sint64 = -1111111111111111s64;
UInt64 uint64 = 1111111111111111u64;
Float32 float32 = 3.14159;
Float64 float64 = 3.14159265358979;
report("Before: boolean = " + boolean);
report("Before: sint8 = " + sint8);
report("Before: uint8 = " + uint8);
report("Before: sint16 = " + sint16);
report("Before: uint16 = " + uint16);
report("Before: sint32 = " + sint32);
report("Before: uint32 = " + uint32);
report("Before: sint64 = " + sint64);
report("Before: uint64 = " + uint64);
report("Before: float32 = " + float32);
report("Before: float64 = " + float64);
SimpleParams(
  boolean,
  BooleanConstPtr(boolean),
  BooleanPtr(boolean),
  boolean,
  BooleanRef(boolean),
  sint8,
  SInt8ConstPtr(sint8),
  SInt8Ptr(sint8),
  sint8,
  SInt8Ref(sint8),
  uint8,
  UInt8ConstPtr(uint8),
  UInt8Ptr(uint8),
  uint8,
  UInt8Ref(uint8),
  sint16,
  SInt16ConstPtr(sint16),
  SInt16Ptr(sint16),
  sint16,
  SInt16Ref(sint16),
  uint16,
  UInt16ConstPtr(uint16),
  UInt16Ptr(uint16),
  uint16,
  UInt16Ref(uint16),
  sint32,
  SInt32ConstPtr(sint32),
  SInt32Ptr(sint32),
  sint32,
  SInt32Ref(sint32),
  uint32,
  UInt32ConstPtr(uint32),
  UInt32Ptr(uint32),
  uint32,
  UInt32Ref(uint32),
  sint64,
  SInt64ConstPtr(sint64),
  SInt64Ptr(sint64),
  sint64,
  SInt64Ref(sint64),
  uint64,
  UInt64ConstPtr(uint64),
  UInt64Ptr(uint64),
  uint64,
  UInt64Ref(uint64),
  float32,
  Float32ConstPtr(float32),
  Float32Ptr(float32),
  float32,
  Float32Ref(float32),
  float64,
  Float64ConstPtr(float64),
  Float64Ptr(float64),
  float64,
  Float64Ref(float64),
  );
report("After: boolean = " + boolean);
report("After: sint8 = " + sint8);
report("After: uint8 = " + uint8);
report("After: sint16 = " + sint16);
report("After: uint16 = " + uint16);
report("After: sint32 = " + sint32);
report("After: uint32 = " + uint32);
report("After: sint64 = " + sint64);
report("After: uint64 = " + uint64);
report("After: float32 = " + float32);
report("After: float64 = " + float64);
""", """
Before: boolean = false
Before: sint8 = -11
Before: uint8 = 11
Before: sint16 = -1111
Before: uint16 = 1111
Before: sint32 = -11111111
Before: uint32 = 11111111
Before: sint64 = -1111111111111111
Before: uint64 = 1111111111111111
Before: float32 = +3.14159
Before: float64 = +3.14159265358979
After: boolean = false
After: sint8 = -88
After: uint8 = 88
After: sint16 = -8888
After: uint16 = 8888
After: sint32 = -88888888
After: uint32 = 88888888
After: sint64 = -8888888888888888
After: uint64 = 8888888888888888
After: float32 = +25.13272
After: float64 = +25.13274122871832
""")


ext.add_func('SimpleValueResult', 'int')\
  .add_test("""
report("SimpleValueResult() = " + SimpleValueResult());
""", """
SimpleValueResult() = 42
""")

ext.add_func('SimpleConstRefResult', 'int const &')\
  .add_test("""
report("SimpleConstRefResult() = " + SimpleConstRefResult());
""", """
SimpleConstRefResult() = 42
""")

ext.add_func('SimpleMutableRefResult', 'int &')\
  .add_test("""
report("SimpleMutableRefResult() = " + SimpleMutableRefResult());
""", """
SimpleMutableRefResult() = 42
""")

ext.add_func("SimpleObscure", 'long', ['signed short', 'long'])\
  .add_test("""
report("SimpleObscure(56, 89) = " + SimpleObscure(56, 89));
""", """
SimpleObscure(56, 89) = 145
""")

ext.add_func("SimpleObscure", 'long', ['signed short', 'long', 'long long'])\
  .add_test("""
report("SimpleObscure(56, 89, 1) = " + SimpleObscure(56, 89, 1));
""", """
SimpleObscure(56, 89, 1) = 146
""")
