/*
 *  Copyright 2010-2015 Fabric Software Inc. All rights reserved.
 */

#include "extension.h"
#include "FabricEDK.h"
#include "UsdAttribute_functions.h"

#include <amber/usd/attribute.h>
#include <amber/usd/stage.h>
#include <amber/vt/array.h>

#include <bedrock/gf/ostreamMethods.h>
#include <bedrock/gf/matrix2d.h>
#include <bedrock/gf/matrix3d.h>
#include <bedrock/gf/matrix4d.h>
#include <bedrock/gf/matrix4f.h>
#include <bedrock/gf/quatd.h>
#include <bedrock/gf/quatf.h>
#include <bedrock/gf/vec2d.h>
#include <bedrock/gf/vec2f.h>
#include <bedrock/gf/vec2i.h>
#include <bedrock/gf/vec3d.h>
#include <bedrock/gf/vec3f.h>
#include <bedrock/gf/vec3i.h>
#include <bedrock/gf/vec4d.h>
#include <bedrock/gf/vec4f.h>
#include <bedrock/gf/vec4i.h>

#include <bedrock/tf/errorMark.h>

using namespace Fabric::EDK;

{% for t in types %}

{% if not t.simple %}
#include "{{ t.kl_type }}.h"
{% endif %}

FABRIC_EXT_EXPORT
KL::Boolean USD_UsdAttribute_GetAs{{ t.kl_type }}(
  KL::Traits<KL::UsdAttribute>::INParam this_,
  KL::Traits< KL::{{ t.kl_type }} >::IOParam value,
  KL::Traits<KL::UsdTime>::INParam time )
{
  if ( !this_.handle )
    throwException( "handle is null" );

  UsdAttribute &handle = *reinterpret_cast<UsdAttribute *>( this_.handle );

  if (!time.handle)
    throwException( "time parameter is null" );
  UsdTime &time_param = *reinterpret_cast<UsdTime *>( time.handle );

  TfErrorMark __mark;

  {{ t.usd_type }} usd_value;
  bool _cpp_result = handle.Get< {{ t.usd_type }} >( &usd_value, time_param );

  if ( _cpp_result )
{% if t.simple %}
    value = usd_value;
{% else %}
    memcpy( &value, &usd_value, sizeof( {{ t.usd_type }} ) );
{% endif %}

  klThrowOnError( __mark );

  return _cpp_result;
}

FABRIC_EXT_EXPORT
KL::Boolean USD_UsdAttribute_GetAs{{ t.kl_type }}VA(
  KL::Traits<KL::UsdAttribute>::INParam this_,
  KL::Traits< KL::VariableArray< KL::{{ t.kl_type }} > >::IOParam value,
  KL::Traits<KL::UsdTime>::INParam time )
{
  if ( !this_.handle )
    throwException( "handle is null" );

  UsdAttribute &handle = *reinterpret_cast<UsdAttribute *>( this_.handle );

  if (!time.handle)
    throwException( "time parameter is null" );
  UsdTime &time_param = *reinterpret_cast<UsdTime *>( time.handle );

  TfErrorMark __mark;

  VtArray< {{ t.usd_type }} > usd_value;
  bool _cpp_result = handle.Get< VtArray< {{ t.usd_type }} > >( &usd_value, time_param );

  if ( _cpp_result )
  {
    size_t size = usd_value.size();
    value.resize( size );
    memcpy( &value[0], usd_value.data(), sizeof( {{ t.usd_type }} ) * size );
  }

  klThrowOnError( __mark );

  return _cpp_result;
}

FABRIC_EXT_EXPORT
KL::Boolean USD_UsdAttribute_SetAs{{ t.kl_type }}(
  KL::Traits<KL::UsdAttribute>::INParam this_,
  KL::Traits< KL::{{ t.kl_type }} >::INParam value,
  KL::Traits<KL::UsdTime>::INParam time )
{
  if ( !this_.handle )
    throwException( "handle is null" );

  UsdAttribute &handle = *reinterpret_cast<UsdAttribute *>( this_.handle );

  if (!time.handle)
    throwException( "time parameter is null" );
  UsdTime &time_param = *reinterpret_cast<UsdTime *>( time.handle );

  TfErrorMark __mark;

  {{ t.usd_type }} usd_value;
{% if t.simple %}
  usd_value = value;
{% else %}
  memcpy( &usd_value, &value, sizeof( {{ t.usd_type }} ) );
{% endif %}

  bool _cpp_result = handle.Set< {{ t.usd_type }} >( usd_value, time_param );

  klThrowOnError( __mark );

  return _cpp_result;
}

FABRIC_EXT_EXPORT
KL::Boolean USD_UsdAttribute_SetAs{{ t.kl_type }}VA(
  KL::Traits<KL::UsdAttribute>::INParam this_,
  KL::Traits< KL::VariableArray< KL::{{ t.kl_type }} > >::INParam value,
  KL::Traits<KL::UsdTime>::INParam time )
{
  if ( !this_.handle )
    throwException( "handle is null" );

  UsdAttribute &handle = *reinterpret_cast<UsdAttribute *>( this_.handle );

  if (!time.handle)
    throwException( "time parameter is null" );
  UsdTime &time_param = *reinterpret_cast<UsdTime *>( time.handle );

  TfErrorMark __mark;

  VtArray< {{ t.usd_type }} > usd_value;
  usd_value.resize( value.size() );
  memcpy( usd_value.data(), &value[0], sizeof( {{ t.usd_type }} ) * value.size() );

  bool _cpp_result = handle.Set< VtArray< {{ t.usd_type }} > >( usd_value, time_param );

  klThrowOnError( __mark );

  return _cpp_result;
}

{% endfor %}

