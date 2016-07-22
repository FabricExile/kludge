#ifndef _Namespaces_hpp
#define _Namespaces_hpp

#include <string>

namespace FooNS {

namespace BarNS {

template <typename T>
struct MyTempl
{
  T t;
};

struct BarType {
  typedef size_t size;
  std::string str;
  size getSize() const { return str.size(); }

  struct SubType
  {
    SubType() {}

    int a;
    enum Enum
    {
      FOO,
      BAR
    };
  };

  typedef MyTempl<SubType::Enum> MySubTypeEnum;

  void addSubType(SubType s) {}
};

} // namespace BarNS

inline BarNS::BarType ReturnBarType() {
  BarNS::BarType bt;
  bt.str = "foo";
  return bt;
}

} // namespace FooNS

#endif
