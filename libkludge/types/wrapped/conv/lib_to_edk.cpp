{############################################################################}
{# Copyright (c) 2010-2017 Fabric Software Inc. All rights reserved.        #}
{############################################################################}
delete {{conv.value_name.edk}}.cpp_ptr;
{{conv.value_name.edk}}.cpp_ptr = new {{conv.type_info.lib.name.compound}}( {{conv.value_name.lib}} );
