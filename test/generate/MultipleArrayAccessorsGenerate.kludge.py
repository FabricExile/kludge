#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

ext.add_cpp_quoted_include('MultipleArrayAccessorsGenerate.hpp')

classType = ext.add_managed_type('Class')
classType.add_ctor(['int'])
classType.add_get_ind_op('int', 'unsigned int')
