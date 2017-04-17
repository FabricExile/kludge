{############################################################################}
{# Copyright (c) 2010-2017 Fabric Software Inc. All rights reserved.        #}
{############################################################################}
{{result.value_name.edk}}.cpp_ptr =
  reinterpret_cast< ::{{result.base_type_info.lib.name.base}} >(
    const_cast< ::{{result.type_info.lib.name.base}} >(
