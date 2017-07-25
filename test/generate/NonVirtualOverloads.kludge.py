#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

ext.add_cpp_quoted_include('NonVirtualOverloads.hpp')

baseClassType = ext.add_owned_type('BaseClass')
baseClassType.add_ctor(['int'])
baseClassType.add_const_method('Reverse', 'bool')
baseClassType.add_mutable_method('SetFrom', 'void', ['const BaseClass &'])

classType = ext.add_owned_type('Class', extends='BaseClass')
classType.add_ctor(['int'])
classType.add_const_method('Reverse', 'bool')
classType.add_mutable_method('SetFrom', 'void', ['const Class &'])
