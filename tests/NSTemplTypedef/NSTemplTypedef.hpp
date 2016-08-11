#ifndef _NSTemplTypedef_hpp
#define _NSTemplTypedef_hpp

template<typename Ty>
class PtrRef
{
  Ty *m_ptr;
public:
  PtrRef(Ty t) : m_ptr(new Ty(t)) {}
  Ty getValue() { return *m_ptr; }
};

template<typename Ty>
struct TemplatePtrs
{
  typedef PtrRef<Ty> Ptr;
};

typedef TemplatePtrs<int>::Ptr IntPtr;

#endif
