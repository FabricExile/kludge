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
  Boolean_CxxConstPtr(boolean),
  Boolean_CxxPtr(boolean),
  boolean,
  Boolean_CxxRef(boolean),
  sint8,
  SInt8_CxxConstPtr(sint8),
  SInt8_CxxPtr(sint8),
  sint8,
  SInt8_CxxRef(sint8),
  uint8,
  UInt8_CxxConstPtr(uint8),
  UInt8_CxxPtr(uint8),
  uint8,
  UInt8_CxxRef(uint8),
  sint16,
  SInt16_CxxConstPtr(sint16),
  SInt16_CxxPtr(sint16),
  sint16,
  SInt16_CxxRef(sint16),
  uint16,
  UInt16_CxxConstPtr(uint16),
  UInt16_CxxPtr(uint16),
  uint16,
  UInt16_CxxRef(uint16),
  sint32,
  SInt32_CxxConstPtr(sint32),
  SInt32_CxxPtr(sint32),
  sint32,
  SInt32_CxxRef(sint32),
  uint32,
  UInt32_CxxConstPtr(uint32),
  UInt32_CxxPtr(uint32),
  uint32,
  UInt32_CxxRef(uint32),
  sint64,
  SInt64_CxxConstPtr(sint64),
  SInt64_CxxPtr(sint64),
  sint64,
  SInt64_CxxRef(sint64),
  uint64,
  UInt64_CxxConstPtr(uint64),
  UInt64_CxxPtr(uint64),
  uint64,
  UInt64_CxxRef(uint64),
  float32,
  Float32_CxxConstPtr(float32),
  Float32_CxxPtr(float32),
  float32,
  Float32_CxxRef(float32),
  float64,
  Float64_CxxConstPtr(float64),
  Float64_CxxPtr(float64),
  float64,
  Float64_CxxRef(float64),
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

ext.add_func('SimpleConstPtrResult', 'int const *')\
  .add_test("""
SInt32_CxxConstPtr ptr = SimpleConstPtrResult();
report("SimpleConstPtrResult(): ptr = " + ptr);
report("SimpleConstPtrResult(): ptr.cxxPtrIsValid() = " + ptr.cxxPtrIsValid());
report("SimpleConstPtrResult(): Boolean(ptr) = " + Boolean(ptr));
report("SimpleConstPtrResult(): ptr.cxxPtrDeref() = " + ptr.cxxPtrDeref());
report("SimpleConstPtrResult(): ptr.cxxPtrGetAt(0) = " + ptr.cxxPtrGetAt(0));
""", """
SimpleConstPtrResult(): ptr = <Opaque>
SimpleConstPtrResult(): ptr.cxxPtrIsValid() = true
SimpleConstPtrResult(): Boolean(ptr) = true
SimpleConstPtrResult(): ptr.cxxPtrDeref() = 42
SimpleConstPtrResult(): ptr.cxxPtrGetAt(0) = 42
""")

ext.add_func('SimpleMutablePtrResult', 'int *')\
  .add_test("""
SInt32_CxxPtr ptr = SimpleMutablePtrResult();
report("SimplePtrResult(): before: ptr = " + ptr);
report("SimplePtrResult(): before: ptr.cxxPtrIsValid() = " + ptr.cxxPtrIsValid());
report("SimplePtrResult(): before: Boolean(ptr) = " + Boolean(ptr));
report("SimplePtrResult(): before: ptr.cxxPtrDeref() = " + ptr.cxxPtrDeref());
report("SimplePtrResult(): before: ptr.cxxPtrGetAt(0) = " + ptr.cxxPtrGetAt(0));
report("SimplePtrResult(): ptr.cxxPtrDeref().cxxRefSet(-7)");
ptr.cxxPtrDeref().cxxRefSet(-7);
report("SimplePtrResult(): before: ptr.cxxPtrDeref() = " + ptr.cxxPtrDeref());
report("SimplePtrResult(): before: ptr.cxxPtrGetAt(0) = " + ptr.cxxPtrGetAt(0));
""", """
SimplePtrResult(): before: ptr = {ptr:<Opaque>}
SimplePtrResult(): before: ptr.cxxPtrIsValid() = true
SimplePtrResult(): before: Boolean(ptr) = true
SimplePtrResult(): before: ptr.cxxPtrDeref() = 42
SimplePtrResult(): before: ptr.cxxPtrGetAt(0) = 42
SimplePtrResult(): ptr.cxxPtrDeref().cxxRefSet(-7)
SimplePtrResult(): before: ptr.cxxPtrDeref() = -7
SimplePtrResult(): before: ptr.cxxPtrGetAt(0) = -7
""")

ext.add_func('SimpleConstRefResult', 'int const &')\
  .add_test("""
report("SimpleConstRefResult() = " + SimpleConstRefResult());
""", """
SimpleConstRefResult() = 42
""")

ext.add_func('SimpleMutableRefResult', 'int &')\
  .add_test("""
SInt32_CxxRef result = SimpleMutableRefResult();
report("SimpleMutableRefResult(): before: result = " + result);
result.cxxRefSet(-7);
result = SimpleMutableRefResult();
report("SimpleMutableRefResult(): after: result = " + result);
""", """
SimpleMutableRefResult(): before: result = 42
SimpleMutableRefResult(): after: result = -7
""")

# ext.add_func('GetCString', 'char const *')\
#   .add_test("""
# SInt8_CxxConstPtr ptr = GetCString();
# report("GetCString: ptr = " + ptr);
# """, """
# """)

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
