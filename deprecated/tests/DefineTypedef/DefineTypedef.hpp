#ifndef DEFINE_TYPEDEF_HPP
#define DEFINE_TYPEDEF_HPP

#define DECLARE_REF_PTR(type) typedef Ptr< class type > type##Ptr;

template<typename Ty>
class Ptr
{
public:

  Ptr() {}

  Ty get()
    { return m_type; }

private:

  Ty m_type;
};

class BaseType
{
public:
  BaseType() {}
};

DECLARE_REF_PTR(BaseType)

void GlobalFunction( BaseTypePtr tp )
{
}

#endif
