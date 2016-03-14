#ifndef _Namespaces_hpp
#define _Namespaces_hpp

#include <string>

namespace FooNS {

namespace BarNS {

struct BarType {
  typedef size_t size;
  std::string str;
  size getSize() const { return str.size(); }
};

} // namespace BarNS

inline BarNS::BarType ReturnBarType() {
  BarNS::BarType bt;
  bt.str = "foo";
  return bt;
}

} // namespace FooNS

#endif
