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
CxxSimpleParams(
  boolean,
  Make_CxxBooleanConstPtr(boolean),
  Make_CxxBooleanPtr(boolean),
  Make_CxxBooleanConstRef(boolean),
  Make_CxxBooleanRef(boolean),
  sint8,
  Make_CxxSInt8ConstPtr(sint8),
  Make_CxxSInt8Ptr(sint8),
  Make_CxxSInt8ConstRef(sint8),
  Make_CxxSInt8Ref(sint8),
  uint8,
  Make_CxxUInt8ConstPtr(uint8),
  Make_CxxUInt8Ptr(uint8),
  Make_CxxUInt8ConstRef(uint8),
  Make_CxxUInt8Ref(uint8),
  sint16,
  Make_CxxSInt16ConstPtr(sint16),
  Make_CxxSInt16Ptr(sint16),
  Make_CxxSInt16ConstRef(sint16),
  Make_CxxSInt16Ref(sint16),
  uint16,
  Make_CxxUInt16ConstPtr(uint16),
  Make_CxxUInt16Ptr(uint16),
  Make_CxxUInt16ConstRef(uint16),
  Make_CxxUInt16Ref(uint16),
  sint32,
  Make_CxxSInt32ConstPtr(sint32),
  Make_CxxSInt32Ptr(sint32),
  Make_CxxSInt32ConstRef(sint32),
  Make_CxxSInt32Ref(sint32),
  uint32,
  Make_CxxUInt32ConstPtr(uint32),
  Make_CxxUInt32Ptr(uint32),
  Make_CxxUInt32ConstRef(uint32),
  Make_CxxUInt32Ref(uint32),
  sint64,
  Make_CxxSInt64ConstPtr(sint64),
  Make_CxxSInt64Ptr(sint64),
  Make_CxxSInt64ConstRef(sint64),
  Make_CxxSInt64Ref(sint64),
  uint64,
  Make_CxxUInt64ConstPtr(uint64),
  Make_CxxUInt64Ptr(uint64),
  Make_CxxUInt64ConstRef(uint64),
  Make_CxxUInt64Ref(uint64),
  float32,
  Make_CxxFloat32ConstPtr(float32),
  Make_CxxFloat32Ptr(float32),
  Make_CxxFloat32ConstRef(float32),
  Make_CxxFloat32Ref(float32),
  float64,
  Make_CxxFloat64ConstPtr(float64),
  Make_CxxFloat64Ptr(float64),
  Make_CxxFloat64ConstRef(float64),
  Make_CxxFloat64Ref(float64),
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
""")\
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
  boolean,
  boolean,
  boolean,
  boolean,
  sint8,
  sint8,
  sint8,
  sint8,
  sint8,
  uint8,
  uint8,
  uint8,
  uint8,
  uint8,
  sint16,
  sint16,
  sint16,
  sint16,
  sint16,
  uint16,
  uint16,
  uint16,
  uint16,
  uint16,
  sint32,
  sint32,
  sint32,
  sint32,
  sint32,
  uint32,
  uint32,
  uint32,
  uint32,
  uint32,
  sint64,
  sint64,
  sint64,
  sint64,
  sint64,
  uint64,
  uint64,
  uint64,
  uint64,
  uint64,
  float32,
  float32,
  float32,
  float32,
  float32,
  float64,
  float64,
  float64,
  float64,
  float64,
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
After: sint8 = -55
After: uint8 = 55
After: sint16 = -5555
After: uint16 = 5555
After: sint32 = -55555555
After: uint32 = 55555555
After: sint64 = -5555555555555555
After: uint64 = 5555555555555555
After: float32 = +15.70795
After: float64 = +15.70796326794895
""")


ext.add_func('SimpleValueResult', 'int')\
  .add_test("""
report("SimpleValueResult() = " + SimpleValueResult());
""", """
SimpleValueResult() = 42
""")

ext.add_func('SimpleConstPtrResult', 'int const *')\
  .add_test("""
CxxSInt32ConstPtr ptr = SimpleConstPtrResult();
report("SimpleConstPtrResult(): ptr = " + ptr);
report("SimpleConstPtrResult(): ptr.cxx_isValid() = " + ptr.cxx_isValid());
report("SimpleConstPtrResult(): Boolean(ptr) = " + Boolean(ptr));
report("SimpleConstPtrResult(): ptr.cxx_deref() = " + ptr.cxx_deref());
report("SimpleConstPtrResult(): ptr.cxx_getAt(0) = " + ptr.cxx_getAt(0));
""", """
SimpleConstPtrResult(): ptr = <Opaque>
SimpleConstPtrResult(): ptr.cxx_isValid() = true
SimpleConstPtrResult(): Boolean(ptr) = true
SimpleConstPtrResult(): ptr.cxx_deref() = 42
SimpleConstPtrResult(): ptr.cxx_getAt(0) = 42
""")

ext.add_func('SimpleMutablePtrResult', 'int *')\
  .add_test("""
CxxSInt32Ptr ptr = SimpleMutablePtrResult();
report("SimplePtrResult(): before: ptr = " + ptr);
report("SimplePtrResult(): before: ptr.cxx_isValid() = " + ptr.cxx_isValid());
report("SimplePtrResult(): before: Boolean(ptr) = " + Boolean(ptr));
report("SimplePtrResult(): before: ptr.cxx_deref() = " + ptr.cxx_deref());
report("SimplePtrResult(): before: ptr.cxx_getAt(0) = " + ptr.cxx_getAt(0));
report("SimplePtrResult(): ptr.cxx_deref().cxx_set(-7)");
ptr.cxx_deref().cxx_set(-7);
report("SimplePtrResult(): before: ptr.cxx_deref() = " + ptr.cxx_deref());
report("SimplePtrResult(): before: ptr.cxx_getAt(0) = " + ptr.cxx_getAt(0));
""", """
SimplePtrResult(): before: ptr = {ptr:<Opaque>}
SimplePtrResult(): before: ptr.cxx_isValid() = true
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
CxxSInt32Ref result = CxxSimpleMutableRefResult();
report("CxxSimpleMutableRefResult(): before: result = " + result);
result.cxx_set(-7);
result = CxxSimpleMutableRefResult();
report("CxxSimpleMutableRefResult(): after: result = " + result);
""", """
CxxSimpleMutableRefResult(): before: result = 42
CxxSimpleMutableRefResult(): after: result = -7
""")\
  .add_test("""
SInt32 result = SimpleMutableRefResult();
report("SimpleMutableRefResult(): result = " + result);
""", """
SimpleMutableRefResult(): result = -7
""")

ext.add_func('GetCString', 'char const *')\
  .add_test("""
CxxCharConstPtr ptr = CxxGetCString();
report("CxxGetCString: ptr = " + ptr);
""", """
CxxGetCString: ptr = Hello, world!
""")\
  .add_test("""
String string = GetCString();
report("GetCString: string = " + string);
""", """
GetCString: string = Hello, world!
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
