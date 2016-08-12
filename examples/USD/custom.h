#include <vector>

//
// these types are defined with SDF_DECLARE_HANDLES
//

#include <pxr/usd/sdf/layer.h>

typedef TfWeakPtr<SdfLayer> SdfLayerHandle;
//typedef TfWeakPtr<const SdfLayer> SdfLayerConstHandle;
typedef std::vector<SdfLayerHandle> SdfLayerVector;
//typedef std::vector<SdfLayerConstHandle> SdfLayerConstVector;

//
// these types are defined with TF_DECLARE_WEAK_AND_REF_PTRS
//

#include <pxr/usd/usd/stage.h>

typedef TfRefPtr<UsdStage> UsdStageRefPtr;
//typedef TfRefPtr<const UsdStage> UsdStageConstRefPtr;
typedef std::vector<UsdStageRefPtr> UsdStageRefPtrVector;
//typedef std::vector<UsdStageConstRefPtr> UsdStageConstRefPtrVector;

typedef TfWeakPtr<UsdStage> UsdStagePtr;
//typedef TfWeakPtr<const UsdStage> UsdStageConstPtr;
typedef std::vector<UsdStagePtr> PtrVector;
//typedef std::vector<UsdStageConstPtr> ConstPtrVector;

