#ifndef _Namespaces_hpp
#define _Namespaces_hpp

#include <string>

namespace FooNS {

namespace BarNS {

struct BarType {
  std::string str;
};

} // namespace BarNS

inline BarNS::BarType ReturnBarType() {
  BarNS::BarType bt;
  bt.str = "foo";
  return bt;
}

} // namespace FooNS

#endif
