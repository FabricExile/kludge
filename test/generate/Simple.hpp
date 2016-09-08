//
// Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
//

#pragma once

#include <stdint.h>

inline void SimpleParams(
  bool boolValue,
  bool const *boolConstPtr,
  bool *boolMutablePtr,
  bool const &boolConstRef,
  bool &boolMutableRef,
  int8_t int8Value,
  int8_t const *int8ConstPtr,
  int8_t *int8MutablePtr,
  int8_t const &int8ConstRef,
  int8_t &int8MutableRef,
  uint8_t uint8Value,
  uint8_t const *uint8ConstPtr,
  uint8_t *uint8MutablePtr,
  uint8_t const &uint8ConstRef,
  uint8_t &uint8MutableRef,
  int16_t int16Value,
  int16_t const *int16ConstPtr,
  int16_t *int16MutablePtr,
  int16_t const &int16ConstRef,
  int16_t &int16MutableRef,
  uint16_t uint16Value,
  uint16_t const *uint16ConstPtr,
  uint16_t *uint16MutablePtr,
  uint16_t const &uint16ConstRef,
  uint16_t &uint16MutableRef,
  int32_t int32Value,
  int32_t const *int32ConstPtr,
  int32_t *int32MutablePtr,
  int32_t const &int32ConstRef,
  int32_t &int32MutableRef,
  uint32_t uint32Value,
  uint32_t const *uint32ConstPtr,
  uint32_t *uint32MutablePtr,
  uint32_t const &uint32ConstRef,
  uint32_t &uint32MutableRef,
  int64_t int64Value,
  int64_t const *int64ConstPtr,
  int64_t *int64MutablePtr,
  int64_t const &int64ConstRef,
  int64_t &int64MutableRef,
  uint64_t uint64Value,
  uint64_t const *uint64ConstPtr,
  uint64_t *uint64MutablePtr,
  uint64_t const &uint64ConstRef,
  uint64_t &uint64MutableRef,
  float floatValue,
  float const *floatConstPtr,
  float *floatMutablePtr,
  float const &floatConstRef,
  float &floatMutableRef,
  double doubleValue,
  double const *doubleConstPtr,
  double *doubleMutablePtr,
  double const &doubleConstRef,
  double &doubleMutableRef
  )
{
  boolMutableRef = !boolMutableRef;
  *boolMutablePtr = !*boolMutablePtr;

  int8MutableRef += int8Value;
  int8MutableRef += int8ConstRef;
  *int8MutablePtr += int8Value;
  *int8MutablePtr += *int8ConstPtr;

  uint8MutableRef += uint8Value;
  uint8MutableRef += uint8ConstRef;
  *uint8MutablePtr += uint8Value;
  *uint8MutablePtr += *uint8ConstPtr;

  int16MutableRef += int16Value;
  int16MutableRef += int16ConstRef;
  *int16MutablePtr += int16Value;
  *int16MutablePtr += *int16ConstPtr;

  uint16MutableRef += uint16Value;
  uint16MutableRef += uint16ConstRef;
  *uint16MutablePtr += uint16Value;
  *uint16MutablePtr += *uint16ConstPtr;

  int32MutableRef += int32Value;
  int32MutableRef += int32ConstRef;
  *int32MutablePtr += int32Value;
  *int32MutablePtr += *int32ConstPtr;

  uint32MutableRef += uint32Value;
  uint32MutableRef += uint32ConstRef;
  *uint32MutablePtr += uint32Value;
  *uint32MutablePtr += *uint32ConstPtr;

  int64MutableRef += int64Value;
  int64MutableRef += int64ConstRef;
  *int64MutablePtr += int64Value;
  *int64MutablePtr += *int64ConstPtr;

  uint64MutableRef += uint64Value;
  uint64MutableRef += uint64ConstRef;
  *uint64MutablePtr += uint64Value;
  *uint64MutablePtr += *uint64ConstPtr;

  floatMutableRef += floatValue;
  floatMutableRef += floatConstRef;
  *floatMutablePtr += floatValue;
  *floatMutablePtr += *floatConstPtr;

  doubleMutableRef += doubleValue;
  doubleMutableRef += doubleConstRef;
  *doubleMutablePtr += doubleValue;
  *doubleMutablePtr += *doubleConstPtr;
}

inline int SimpleValueResult() { return 42; }
inline int const *SimpleConstPtrResult() { static int const val = 42; return &val; }
inline int *SimpleMutablePtrResult() { static int val = 42; return &val; }
inline int const &SimpleConstRefResult() { static int const val = 42; return val; }
inline int &SimpleMutableRefResult() { static int val = 42; return val; }

inline long SimpleObscure(
  signed short signedShortVal,
  long longVal
  ) { return signedShortVal + longVal; }

inline long SimpleObscure(
  signed short signedShortVal,
  long longVal,
  long long longLongVal
  ) { return signedShortVal + longVal + longLongVal; }
