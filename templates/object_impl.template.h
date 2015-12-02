#ifndef __KL2EDK_AUTOGEN_{{ t.type_name }}_impl__
#define __KL2EDK_AUTOGEN_{{ t.type_name }}_impl__

#ifdef KL2EDK_INCLUDE_MESSAGES
  #pragma message ( "Including '{{ t.type_name }}_impl.h'" )
#endif

////////////////////////////////////////////////////////////////
// THIS FILE IS AUTOMATICALLY GENERATED -- DO NOT MODIFY!!
////////////////////////////////////////////////////////////////
// Generated by kl2edk version {{ version_full }}
////////////////////////////////////////////////////////////////

#include <FabricEDK.h>
#if FABRIC_EDK_VERSION_MAJ != {{ version_maj }} || FABRIC_EDK_VERSION_MIN != {{ version_min }}
# error "This file needs to be rebuilt for the current EDK version!"
#endif

#include "global.h"
{% for d in t.depends %}
#include "{{ d }}.h"
{% endfor %}
#include "{{ t.type_name }}.h"
{% for i in t.interfaces %}
#include "{{ i.type_name }}_impl.h"
{% endfor %}
{% if t.parent %}
#include "{{ t.parent.type_name }}_impl.h"
{% endif %}

namespace Fabric { namespace EDK { namespace KL {

{% if t.parent %}
  struct {{ t.type_name }}::Bits : public {{ t.parent.type_name }}::Bits
{% else %}
  struct {{ t.type_name }}::Bits
{% endif %}
  {
{% if not t.parent %}
    ObjectCore __objectCore;
{% endif %}
{% for member in t.members %}
    {{ member.type_name_cpp }} {{ member.name }};
{% endfor %}
{% if not t.parent %}
    Object::Bits __interfaceObjectBits;
{% endif %}
{% for interface in t.interfaces %}
    {{ interface.type_name }}::Bits __interface{{ interface.type_name }}Bits;
{% endfor %}
  };
  
  inline void {{ t.type_name }}::ConstructEmpty( {{ t.type_name }} *self )
  {
    self->m_bits = 0;
  }
  
  inline void {{ t.type_name }}::ConstructCopy( {{ t.type_name }} *self, {{ t.type_name }} const *other )
  {
    if ( (self->m_bits = other->m_bits) )
      AtomicUInt32Increment( &self->m_bits->__objectCore.refCount );
  }
  
  inline void {{ t.type_name }}::AssignCopy( {{ t.type_name }} *self, {{ t.type_name }} const *other )
  {
    if ( self->m_bits != other->m_bits )
    {
      Destruct( self );
      ConstructCopy( self, other );
    }
  }
  
  inline void {{ t.type_name }}::Destruct( {{ t.type_name }} *self )
  {
    if ( self->m_bits
      && AtomicUInt32DecrementAndGetValue( &self->m_bits->__objectCore.refCount ) == 0 )
    {
      ObjectCore *objectCorePtr = &self->m_bits->__objectCore;
      self->m_bits->__objectCore.lTableSwapPtrPtr->get()->lifecycleDestroy(
        &objectCorePtr
        );
    }
  }
  
  inline {{ t.type_name }}::{{ t.type_name }}()
  {
    ConstructEmpty( this );
  }
  
  inline {{ t.type_name }} {{ t.type_name }}::Create()
  {
    static KL::SwapPtr<void> const *sp = 0;
    if ( !sp )
    {
      sp = static_cast<KL::SwapPtr<void> const *>(
        s_callbacks.m_lookupGlobalSymbol(
          "sp.function.kl.OO_{{ t.type_name }}.createEmpty.L.OO_{{ t.type_name }}",
          {{ "sp.function.kl.OO_"|length + t.type_name|length + ".createEmpty.L.OO_"|length + t.type_name|length }}
          )
        );
      if ( !sp )
        throwException(
          "EDK internal error: failed to look up '%s'",
          "sp.function.kl.OO_{{ t.type_name }}.createEmpty.L.OO_{{ t.type_name }}"
          );
    }
    void (*createFuncPtr)(void *) = ((void (*)(void *))sp->get());
    if ( !createFuncPtr )
      throwException(
        "EDK internal error: target of '%s' is NULL",
        "sp.function.kl.OO_{{ t.type_name }}.createEmpty.L.OO_{{ t.type_name }}"
        );
    {{ t.type_name }} result;
    createFuncPtr( &result );
    return result;
  }
  
  inline {{ t.type_name }}::{{ t.type_name }}( {{ t.type_name }} const &that )
  {
    ConstructCopy( this, &that );
  }
  
  inline {{ t.type_name }} &{{ t.type_name }}::operator =( {{ t.type_name }} const &that )
  {
    AssignCopy( this, &that );
    return *this;
  }
  
  inline {{ t.type_name }}::~{{ t.type_name }}()
  {
{% if not t.parent %}
    Destruct( this );
{% endif %}
  }
  
  inline void {{ t.type_name }}::appendDesc( String::IOParam string ) const
  {
    if ( m_bits )
    {
      ObjectCore *objectCorePtr = &m_bits->__objectCore;
      objectCorePtr->lTableSwapPtrPtr->get()->appendDesc(
        &objectCorePtr, string
        );
    }
    else string.append( "null", 4 );
  }
  inline uint32_t {{ t.type_name }}::getRefCount() const
  {
    if ( m_bits )
    {
      ObjectCore *objectCorePtr = &m_bits->__objectCore;
      return objectCorePtr->refCount;
    }
    else return 0;
  }
  inline Type {{ t.type_name }}::getType() const
  {
    if ( m_bits )
    {
      return Type( m_bits->__objectCore.typeInfoSwapPtrPtr->get() );
    }
    else return Type();
  }
  
  inline bool {{ t.type_name }}::isValid() const
  {
    return !!m_bits;
  }
  
  inline {{ t.type_name }}::operator bool() const
  {
    return isValid();
  }
  
  inline bool {{ t.type_name }}::operator !() const
  {
    return !isValid();
  }
  
  inline {{ t.type_name }}::Bits *{{ t.type_name }}::operator ->()
  {
    return static_cast<{{ t.type_name }}::Bits *>( m_bits );
  }
  
  inline {{ t.type_name }}::Bits const *{{ t.type_name }}::operator ->() const
  {
    return static_cast<{{ t.type_name }}::Bits const *>( m_bits );
  }
  
  inline bool {{ t.type_name }}::operator ==( INParam that )
  {
    return m_bits == that.m_bits;
  }
  
  inline bool {{ t.type_name }}::operator !=( INParam that )
  {
    return m_bits != that.m_bits;
  }

{% for method in t.interface_methods %}
  // method from '{{ method.interface.type_name }}'
  inline
  {% if method.ret_type_name %}
  {{ method.ret_type_name_cpp }}
  {% else %}
  void
  {% endif %}
  {{ t.type_name }}::{{ method.name }}(
  {% for param in method.params %}
    {% if not loop.first %}
,
    {% endif %}
    Traits< {{ param.type_name_cpp }} >::{{ param.usage_cpp }} {{ param.name -}}
    {% if loop.last %}

    {% endif %}
  {% endfor %}
    ){% if method.usage == "in" %} const{% endif %}

  {
{% if method.ret_type_name %}
    {{ method.ret_type_name_cpp }} _result;
{% endif %}
    ObjectCore const *objectCorePtr = &static_cast<{{ t.type_name }}::Bits *>( m_bits )->__objectCore;
  {% if manager.uses_returnval(method.ret_type_name) %}    _result ={% endif %}
    static_cast<{{ t.type_name }}::Bits *>( m_bits )->__interface{{ method.interface.type_name }}Bits.vTableSwapPtrPtr->get()->{{ method.name }}_{{ method.hash() }}(
  {% if method.ret_type_name and not manager.uses_returnval(method.ret_type_name) %}      _result,
  {% endif %}
      {{ "&objectCorePtr" -}}
  {% for param in method.params %}
,
      {{ param.name -}}
  {% endfor %}
 );
{% if method.ret_type_name %}
    return _result;
{% endif %}
  }

{% endfor %}
}}}

#endif // __KL2EDK_AUTOGEN_{{ t.type_name }}_impl__