{############################################################################}
{# Copyright (c) 2010-2017 Fabric Software Inc. All rights reserved.        #}
{############################################################################}
::Fabric::EDK::KL::Traits< {{param.type_info.edk.name}} >::{{ "IOParam" if param.is_mutable_indirect else "INParam" }} {{param.value_name.edk}}
