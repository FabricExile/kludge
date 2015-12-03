#ifndef _Simple_hpp
#define _Simple_hpp

#include <stdint.h>

inline void SimpleParams(
  bool boolValue,
  bool const &boolConstRef,
  bool const *boolConstPtr,
  bool &boolMutableRef,
  bool *boolMutablePtr,
  int8_t int8Value,
  int8_t const &int8ConstRef,
  // int8_t const *int8ConstPtr,
  int8_t &int8MutableRef,
  // int8_t *int8MutablePtr,
  uint8_t uint8Value,
  uint8_t const &uint8ConstRef,
  uint8_t const *uint8ConstPtr,
  uint8_t &uint8MutableRef,
  uint8_t *uint8MutablePtr,
  int16_t int16Value,
  int16_t const &int16ConstRef,
  int16_t const *int16ConstPtr,
  int16_t &int16MutableRef,
  int16_t *int16MutablePtr,
  uint16_t uint16Value,
  uint16_t const &uint16ConstRef,
  uint16_t const *uint16ConstPtr,
  uint16_t &uint16MutableRef,
  uint16_t *uint16MutablePtr,
  int32_t int32Value,
  int32_t const &int32ConstRef,
  int32_t const *int32ConstPtr,
  int32_t &int32MutableRef,
  int32_t *int32MutablePtr,
  uint32_t uint32Value,
  uint32_t const &uint32ConstRef,
  uint32_t const *uint32ConstPtr,
  uint32_t &uint32MutableRef,
  uint32_t *uint32MutablePtr,
  int64_t int64Value,
  int64_t const &int64ConstRef,
  int64_t const *int64ConstPtr,
  int64_t &int64MutableRef,
  int64_t *int64MutablePtr,
  uint64_t uint64Value,
  uint64_t const &uint64ConstRef,
  uint64_t const *uint64ConstPtr,
  uint64_t &uint64MutableRef,
  uint64_t *uint64MutablePtr,
  float floatValue,
  float const &floatConstRef,
  float const *floatConstPtr,
  float &floatMutableRef,
  float *floatMutablePtr,
  double doubleValue,
  double const &doubleConstRef,
  double const *doubleConstPtr,
  double &doubleMutableRef,
  double *doubleMutablePtr
  )
{
  boolMutableRef = !boolMutableRef;
  // *boolMutablePtr = !*boolMutablePtr;

  int8MutableRef += int8Value;
  int8MutableRef += int8ConstRef;
  // *int8MutablePtr += *int8ConstPtr;

  uint8MutableRef += uint8Value;
  uint8MutableRef += uint8ConstRef;
  *uint8MutablePtr += *uint8ConstPtr;

  int16MutableRef += int16Value;
  int16MutableRef += int16ConstRef;
  *int16MutablePtr += *int16ConstPtr;

  uint16MutableRef += uint16Value;
  uint16MutableRef += uint16ConstRef;
  *uint16MutablePtr += *uint16ConstPtr;

  int32MutableRef += int32Value;
  int32MutableRef += int32ConstRef;
  *int32MutablePtr += *int32ConstPtr;

  uint32MutableRef += uint32Value;
  uint32MutableRef += uint32ConstRef;
  *uint32MutablePtr += *uint32ConstPtr;

  int64MutableRef += int64Value;
  int64MutableRef += int64ConstRef;
  *int64MutablePtr += *int64ConstPtr;

  uint64MutableRef += uint64Value;
  uint64MutableRef += uint64ConstRef;
  *uint64MutablePtr += *uint64ConstPtr;

  floatMutableRef += floatValue;
  floatMutableRef += floatConstRef;
  *floatMutablePtr += *floatConstPtr;

  doubleMutableRef += doubleValue;
  doubleMutableRef += doubleConstRef;
  *doubleMutablePtr += *doubleConstPtr;
}

inline int SimpleValueResult() { return 42; }
inline int const &SimpleConstRefResult() { static int const val = 42; return val; }
inline int const *SimpleConstPtrResult() { static int const val = 42; return &val; }
inline int &SimpleMutableRefResult() { static int val = 42; return val; }
inline int *SimpleMutablePtrResult() { static int val = 42; return &val; }

inline long SimpleObscure(
  signed short signedShortVal,
  long longVal
  ) { return signedShortVal + longVal; }

#endif
