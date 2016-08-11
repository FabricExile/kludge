#include <FabricEDK.h>

#include <pxr/usd/usd/stage.h>

FABRIC_EXT_EXPORT
void
TfWeakPtr__UsdStage___FROM_TfRefPtr__UsdStage__(
    ::Fabric::EDK::KL::Traits< ::Fabric::EDK::KL::TfWeakPtr__UsdStage__ >::IOParam _this,
    ::Fabric::EDK::KL::Traits< ::Fabric::EDK::KL::TfRefPtr__UsdStage__ >::INParam _that
    )
{
  _this.cpp_ptr = new ::TfWeakPtr<::UsdStage>(*_that.cpp_ptr);
}

