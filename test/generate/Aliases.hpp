//
// Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
//

#pragma once

typedef unsigned AliasType;

inline AliasType ReturnAliasValue() { return 63; }
void TakeAliasType(AliasType a) {}
void TakeAliasTypeRef(AliasType &a) {}
void TakeAliasTypeConstRef(AliasType const &a) {}
