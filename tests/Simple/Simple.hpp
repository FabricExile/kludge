#ifndef _Simple_hpp
#define _Simple_hpp

#include <stdint.h>

inline void SimpleParams(
  bool boolValue,
  bool const &boolConstRef,
  bool &boolMutableRef,
  int8_t int8Value,
  int8_t const &int8ConstRef,
  int8_t &int8MutableRef,
  uint8_t uint8Value,
  uint8_t const &uint8ConstRef,
  uint8_t &uint8MutableRef,
  int16_t int16Value,
  int16_t const &int16ConstRef,
  int16_t &int16MutableRef,
  uint16_t uint16Value,
  uint16_t const &uint16ConstRef,
  uint16_t &uint16MutableRef,
  int32_t int32Value,
  int32_t const &int32ConstRef,
  int32_t &int32MutableRef,
  uint32_t uint32Value,
  uint32_t const &uint32ConstRef,
  uint32_t &uint32MutableRef,
  int64_t int64Value,
  int64_t const &int64ConstRef,
  int64_t &int64MutableRef,
  uint64_t uint64Value,
  uint64_t const &uint64ConstRef,
  uint64_t &uint64MutableRef,
  float floatValue,
  float const &floatConstRef,
  float &floatMutableRef,
  double doubleValue,
  double const &doubleConstRef,
  double &doubleMutableRef
  )
{
  boolMutableRef = !boolMutableRef;

  int8MutableRef += int8Value;
  int8MutableRef += int8ConstRef;

  uint8MutableRef += uint8Value;
  uint8MutableRef += uint8ConstRef;

  int16MutableRef += int16Value;
  int16MutableRef += int16ConstRef;

  uint16MutableRef += uint16Value;
  uint16MutableRef += uint16ConstRef;

  int32MutableRef += int32Value;
  int32MutableRef += int32ConstRef;

  uint32MutableRef += uint32Value;
  uint32MutableRef += uint32ConstRef;

  int64MutableRef += int64Value;
  int64MutableRef += int64ConstRef;

  uint64MutableRef += uint64Value;
  uint64MutableRef += uint64ConstRef;

  floatMutableRef += floatValue;
  floatMutableRef += floatConstRef;

  doubleMutableRef += doubleValue;
  doubleMutableRef += doubleConstRef;
}

inline int SimpleValueResult() { return 42; }
inline int const &SimpleConstRefResult() { static int const val = 42; return val; }
inline int &SimpleMutableRefResult() { static int val = 42; return val; }

inline long SimpleObscure(
  signed short signedShortVal,
  long longVal
  ) { return signedShortVal + longVal; }

#endif
