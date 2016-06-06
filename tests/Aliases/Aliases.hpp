#ifndef _Aliases_hpp
#define _Aliases_hpp

typedef unsigned AliasType;

inline AliasType ReturnAliasValue() { return 63; }
void TakeAliasType(AliasType a) {}
void TakeAliasTypeRef(AliasType &a) {}
void TakeAliasTypeConstRef(AliasType const &a) {}

#endif
