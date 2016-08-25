//
// Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
//

#include <iostream>
#include <sstream>
#include <string>
#include <vector>

std::vector<std::string> hello( int count )
{
  std::cout << "Called hello(" << count << ")\n" << std::flush;
  std::vector<std::string> result;
  for ( int i = 0; i < count; ++i )
  {
    std::ostringstream os;
    os << "foo" << i;
    result.push_back( os.str() );
  }
  return result;
}
