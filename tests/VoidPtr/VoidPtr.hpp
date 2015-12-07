#ifndef _VoidPtr_hpp
#define _VoidPtr_hpp

inline void const *ConstVoidPtrResult() {
  static int v;
  return &v;
}

#endif
