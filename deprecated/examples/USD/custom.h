#ifndef __KLUDGE_USD_CUSTOM_H__
#define __KLUDGE_USD_CUSTOM_H__

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

#include <pxr/base/vt/array.h>
#include <pxr/usd/usd/timeCode.h>
#include <pxr/usd/usd/attribute.h>

#define KLUDGE_USDATTRIBUTE_GETTER_SETTER(type)                                \
                                                                               \
  typedef VtArray<type> type##Array;                                           \
                                                                               \
  static bool UsdAttribute_Get##type(UsdAttribute const &attr, type &param,    \
                                     UsdTimeCode time =                        \
                                         UsdTimeCode::Default()) {             \
    return attr.Get<type>(&param, time);                                       \
  }                                                                            \
                                                                               \
  static bool UsdAttribute_Set##type(                                          \
      UsdAttribute const &attr, type const &param,                             \
      UsdTimeCode time = UsdTimeCode::Default()) {                             \
    return attr.Set<type>(param, time);                                        \
  }                                                                            \
  static bool UsdAttribute_Get##type##Array(                                   \
      UsdAttribute const &attr, type##Array &param,                            \
      UsdTimeCode time = UsdTimeCode::Default()) {                             \
    return attr.Get<type##Array>(&param, time);                                \
  }                                                                            \
                                                                               \
  static bool UsdAttribute_Set##type##Array(                                   \
      UsdAttribute const &attr, type##Array const &param,                      \
      UsdTimeCode time = UsdTimeCode::Default()) {                             \
    return attr.Set<type##Array>(param, time);                                 \
  }

// add all other relevant types

KLUDGE_USDATTRIBUTE_GETTER_SETTER(GfVec3f);
KLUDGE_USDATTRIBUTE_GETTER_SETTER(TfToken);

#endif // __KLUDGE_USD_CUSTOM_H__
