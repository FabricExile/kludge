#ifndef _Functions_hpp
#define _Functions_hpp

#include <string>
#include <stdint.h>

namespace SomeNameSpace { namespace SomeNestedNameSpace {

inline void TestSimpleTypes(
  bool,
  bool const &,
  bool &,
  bool const *,
  bool *,
  int8_t,
  int8_t const &,
  int8_t &,
  // int8_t const *,
  // int8_t *,
  uint8_t,
  uint8_t const &,
  uint8_t &,
  uint8_t const *,
  uint8_t *,
  int16_t,
  int16_t const &,
  int16_t &,
  int16_t const *,
  int16_t *,
  uint16_t,
  uint16_t const &,
  uint16_t &,
  uint16_t const *,
  uint16_t *,
  int32_t,
  int32_t const &,
  int32_t &,
  int32_t const *,
  int32_t *,
  uint32_t,
  uint32_t const &,
  uint32_t &,
  uint32_t const *,
  uint32_t *,
  int64_t,
  int64_t const &,
  int64_t &,
  int64_t const *,
  int64_t *,
  uint64_t,
  uint64_t const &,
  uint64_t &,
  uint64_t const *,
  uint64_t *,
  float,
  float const &,
  float &,
  float const *,
  float *,
  double,
  double const &,
  double &,
  double const *,
  double *
  ) {}

inline void TestObscureIntegers(
  signed short signedShortVal,
  long longVal
  ) {}

inline void TestStdString(
  std::string strVal,
  std::string const &strConstRef,
  std::string &strMutableRef,
  std::string const *strConstPtr,
  std::string *strMutablePtr
  ) {}

inline void TestCString(
  char const *cStringVal,
  char const * const &CStringConstRef
  ) {}

inline int TestSimpleValueReturn() { return 42; }
inline int const &TestSimpleConstRefReturn() { static int foo = 42; return foo; }
inline int &TestSimpleMutableRefReturn() { static int foo = 42; return foo; }

inline std::string TestStdStringValueReturn() { return "hello"; }
inline std::string const &TestStdStringConstRefReturn() { static std::string foo = "hello"; return foo; }
inline std::string &TestStdStringMutableRefReturn() { static std::string foo = "hello"; return foo; }

inline char const * TestCStringValueReturn() { return "hello"; }
inline char const * const &TestCStringConstRefReturn() { static char const *foo = "hello"; return foo; }

} }

#endif
