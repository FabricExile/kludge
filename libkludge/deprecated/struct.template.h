#ifndef __KL2EDK_AUTOGEN_{{ t.type_name }}__
#define __KL2EDK_AUTOGEN_{{ t.type_name }}__

#ifdef KL2EDK_INCLUDE_MESSAGES
  #pragma message ( "Including '{{ t.type_name }}.h'" )
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
{% if t.parent %}
#include "{{ t.parent.type_name }}.h"
{% endif %}

namespace Fabric { namespace EDK { namespace KL {

// KL struct '{{ t.type_name }}'
// Defined at {{ t.location }}

struct {{ t.type_name }}
{% if t.parent %}
    : public {{ t.parent.type_name }}
{% endif %}
{
  typedef {{ t.type_name }} &Result;
  typedef {{ t.type_name }} const &INParam;
  typedef {{ t.type_name }} &IOParam;
  typedef {{ t.type_name }} &OUTParam;

{% for member in t.members %}
  {{ member.type_name_cpp }} {{ member.name }};
{% endfor %}
};

inline void Traits<{{ t.type_name }}>::ConstructEmpty( {{ t.type_name }} &val )
{
{% for member in t.members %}
  Traits< {{ member.type_name_cpp }} >::ConstructEmpty( val.{{ member.name }} );
{% endfor %}
}
inline void Traits<{{ t.type_name }}>::ConstructCopy( {{ t.type_name }} &lhs, {{ t.type_name }} const &rhs )
{
{% for member in t.members %}
  Traits< {{ member.type_name_cpp }} >::ConstructCopy( lhs.{{ member.name }}, rhs.{{ member.name }} );
{% endfor %}
}
inline void Traits<{{ t.type_name }}>::AssignCopy( {{ t.type_name }} &lhs, {{ t.type_name }} const &rhs )
{
{% for member in t.members %}
  Traits< {{ member.type_name_cpp }} >::AssignCopy( lhs.{{ member.name }}, rhs.{{ member.name }} );
{% endfor %}
}
inline void Traits<{{ t.type_name }}>::Destruct( {{ t.type_name }} &val )
{
{% for member in t.members %}
  Traits< {{ member.type_name_cpp }} >::Destruct( val.{{ member.name }} );
{% endfor %}
}
}}}

#endif // __KL2EDK_AUTOGEN_{{ t.type_name }}__