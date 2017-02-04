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
  Make_Boolean_CxxConstPtr(boolean),
  Make_Boolean_CxxPtr(boolean),
  Make_Boolean_CxxConstRef(boolean),
  Make_Boolean_CxxRef(boolean),
  sint8,
  Make_SInt8_CxxConstPtr(sint8),
  Make_SInt8_CxxPtr(sint8),
  Make_SInt8_CxxConstRef(sint8),
  Make_SInt8_CxxRef(sint8),
  uint8,
  Make_UInt8_CxxConstPtr(uint8),
  Make_UInt8_CxxPtr(uint8),
  Make_UInt8_CxxConstRef(uint8),
  Make_UInt8_CxxRef(uint8),
  sint16,
  Make_SInt16_CxxConstPtr(sint16),
  Make_SInt16_CxxPtr(sint16),
  Make_SInt16_CxxConstRef(sint16),
  Make_SInt16_CxxRef(sint16),
  uint16,
  Make_UInt16_CxxConstPtr(uint16),
  Make_UInt16_CxxPtr(uint16),
  Make_UInt16_CxxConstRef(uint16),
  Make_UInt16_CxxRef(uint16),
  sint32,
  Make_SInt32_CxxConstPtr(sint32),
  Make_SInt32_CxxPtr(sint32),
  Make_SInt32_CxxConstRef(sint32),
  Make_SInt32_CxxRef(sint32),
  uint32,
  Make_UInt32_CxxConstPtr(uint32),
  Make_UInt32_CxxPtr(uint32),
  Make_UInt32_CxxConstRef(uint32),
  Make_UInt32_CxxRef(uint32),
  sint64,
  Make_SInt64_CxxConstPtr(sint64),
  Make_SInt64_CxxPtr(sint64),
  Make_SInt64_CxxConstRef(sint64),
  Make_SInt64_CxxRef(sint64),
  uint64,
  Make_UInt64_CxxConstPtr(uint64),
  Make_UInt64_CxxPtr(uint64),
  Make_UInt64_CxxConstRef(uint64),
  Make_UInt64_CxxRef(uint64),
  float32,
  Make_Float32_CxxConstPtr(float32),
  Make_Float32_CxxPtr(float32),
  Make_Float32_CxxConstRef(float32),
  Make_Float32_CxxRef(float32),
  float64,
  Make_Float64_CxxConstPtr(float64),
  Make_Float64_CxxPtr(float64),
  Make_Float64_CxxConstRef(float64),
  Make_Float64_CxxRef(float64),
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
After: sint8 = -110
After: uint8 = 110
After: sint16 = -11110
After: uint16 = 11110
After: sint32 = -111111110
After: uint32 = 111111110
After: sint64 = -11111111111111110
After: uint64 = 11111111111111110
After: float32 = +31.4159
After: float64 = +31.4159265358979
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
report("SimpleConstPtrResult(): ptr.cxxIsValid() = " + ptr.cxxIsValid());
report("SimpleConstPtrResult(): Boolean(ptr) = " + Boolean(ptr));
report("SimpleConstPtrResult(): ptr.cxx_deref() = " + ptr.cxx_deref());
report("SimpleConstPtrResult(): ptr.cxx_getAt(0) = " + ptr.cxx_getAt(0));
""", """
SimpleConstPtrResult(): ptr = <Opaque>
SimpleConstPtrResult(): ptr.cxxIsValid() = true
SimpleConstPtrResult(): Boolean(ptr) = true
SimpleConstPtrResult(): ptr.cxx_deref() = 42
SimpleConstPtrResult(): ptr.cxx_getAt(0) = 42
""")

ext.add_func('SimpleMutablePtrResult', 'int *')\
  .add_test("""
SInt32_CxxPtr ptr = SimpleMutablePtrResult();
report("SimplePtrResult(): before: ptr = " + ptr);
report("SimplePtrResult(): before: ptr.cxxIsValid() = " + ptr.cxxIsValid());
report("SimplePtrResult(): before: Boolean(ptr) = " + Boolean(ptr));
report("SimplePtrResult(): before: ptr.cxx_deref() = " + ptr.cxx_deref());
report("SimplePtrResult(): before: ptr.cxx_getAt(0) = " + ptr.cxx_getAt(0));
report("SimplePtrResult(): ptr.cxx_deref().cxx_set(-7)");
ptr.cxx_deref().cxx_set(-7);
report("SimplePtrResult(): before: ptr.cxx_deref() = " + ptr.cxx_deref());
report("SimplePtrResult(): before: ptr.cxx_getAt(0) = " + ptr.cxx_getAt(0));
""", """
SimplePtrResult(): before: ptr = {ptr:<Opaque>}
SimplePtrResult(): before: ptr.cxxIsValid() = true
SimplePtrResult(): before: Boolean(ptr) = true
SimplePtrResult(): before: ptr.cxx_deref() = 42
SimplePtrResult(): before: ptr.cxx_getAt(0) = 42
SimplePtrResult(): ptr.cxx_deref().cxx_set(-7)
SimplePtrResult(): before: ptr.cxx_deref() = -7
SimplePtrResult(): before: ptr.cxx_getAt(0) = -7
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
result.cxx_set(-7);
result = SimpleMutableRefResult();
report("SimpleMutableRefResult(): after: result = " + result);
""", """
SimpleMutableRefResult(): before: result = 42
SimpleMutableRefResult(): after: result = -7
""")

ext.add_func('GetCString', 'char const *')\
  .add_test("""
CxxCharConstPtr ptr = GetCString();
report("GetCString: ptr = " + ptr);
""", """
GetCString: ptr = Hello, world!
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
