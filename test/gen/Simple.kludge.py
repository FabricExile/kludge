ext.add_cpp_quoted_include('Simple.hpp')

ext.add_func('SimpleParams')\
  .add_param('bool')\
  .add_param('bool const &')\
  .add_param('bool &')\
  .add_param('int8_t')\
  .add_param('int8_t const &')\
  .add_param('int8_t &')\
  .add_param('uint8_t')\
  .add_param('uint8_t const &')\
  .add_param('uint8_t &')\
  .add_param('int16_t')\
  .add_param('int16_t const &')\
  .add_param('int16_t &')\
  .add_param('uint16_t')\
  .add_param('uint16_t const &')\
  .add_param('uint16_t &')\
  .add_param('int32_t')\
  .add_param('int32_t const &')\
  .add_param('int32_t &')\
  .add_param('uint32_t')\
  .add_param('uint32_t const &')\
  .add_param('uint32_t &')\
  .add_param('int64_t')\
  .add_param('int64_t const &')\
  .add_param('int64_t &')\
  .add_param('uint64_t')\
  .add_param('uint64_t const &')\
  .add_param('uint64_t &')\
  .add_param('float')\
  .add_param('float const &')\
  .add_param('float &')\
  .add_param('double')\
  .add_param('double const &')\
  .add_param('double &')\
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
  sint8,
  sint8,
  sint8,
  uint8,
  uint8,
  uint8,
  sint16,
  sint16,
  sint16,
  uint16,
  uint16,
  uint16,
  sint32,
  sint32,
  sint32,
  uint32,
  uint32,
  uint32,
  sint64,
  sint64,
  sint64,
  uint64,
  uint64,
  uint64,
  float32,
  float32,
  float32,
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
After: boolean = true
After: sint8 = -33
After: uint8 = 33
After: sint16 = -3333
After: uint16 = 3333
After: sint32 = -33333333
After: uint32 = 33333333
After: sint64 = -3333333333333333
After: uint64 = 3333333333333333
After: float32 = +9.42477
After: float64 = +9.424777960769371
""")


ext.add_func('SimpleValueResult')\
  .returns('int')\
  .add_test("""
report("SimpleValueResult() = " + SimpleValueResult());
""", """
SimpleValueResult() = 42
""")

ext.add_func('SimpleConstRefResult')\
  .returns('int const &')\
  .add_test("""
report("SimpleConstRefResult() = " + SimpleConstRefResult());
""", """
SimpleConstRefResult() = 42
""")

ext.add_func('SimpleMutableRefResult')\
  .returns('int &')\
  .add_test("""
report("SimpleMutableRefResult() = " + SimpleMutableRefResult());
""", """
SimpleMutableRefResult() = 42
""")

ext.add_func("SimpleObscure")\
  .returns('long')\
  .add_param('signed short')\
  .add_param('long')\
  .add_test("""
report("SimpleObscure(56, 89) = " + SimpleObscure(56, 89));
""", """
SimpleObscure(56, 89) = 145
""")

ext.add_func("SimpleObscure")\
  .returns('long')\
  .add_param('signed short')\
  .add_param('long')\
  .add_param('long long')\
  .add_test("""
report("SimpleObscure(56, 89, 1) = " + SimpleObscure(56, 89, 1));
""", """
SimpleObscure(56, 89, 1) = 146
""")
