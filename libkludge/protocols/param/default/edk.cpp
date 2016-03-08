{######################################################################}
{# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved. #}
{######################################################################}

::Fabric::EDK::KL::Traits< {{param.type_info.edk.name.toplevel}} >::{{ "IOParam" if param.is_mutable else "INParam" }} {{param.value_name.edk}}
