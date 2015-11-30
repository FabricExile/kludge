//////////////////////////////////////////////////////////////////////////////
// KLUDGE class {{ t.type_name }}
//////////////////////////////////////////////////////////////////////////////
//

#include <{{ header }}>

namespace Fabric { namespace EDK { namespace KL {

struct {{ t.type_name }}
{% if t.parent %}
  : {{ t.parent }} {};
{% else %}
{
    friend struct Traits<{{ t.type_name }}>;

    Data handle;

protected:

    static void ConstructEmpty(
        {{ t.type_name }} *thisPtr
        )
    {
        thisPtr->handle = NULL;
    }

    static void ConstructCopy(
        {{ t.type_name }} *thisPtr,
        {{ t.type_name }} const *thatPtr
        )
    {
      if ( thatPtr->handle )
      {
        // [pzion 20151128] Using reinterpret_case here breaks gcc 4.8
        ::{{ t.codegen.cpp_base_type }} *handle =
          (::{{ t.codegen.cpp_base_type }} *)( thatPtr->handle );

        {{ enter }}
        ::{{ t.codegen.cpp_base_type }} *handle_copy = new ::{{ t.codegen.cpp_base_type }}();        
        *handle_copy = *handle;
        {{ leave }}
        thisPtr->handle = reinterpret_cast<Data>( handle_copy );
      }
      else thisPtr->handle = NULL;
    }

    static void AssignCopy(
        {{ t.type_name }} *thisPtr,
        {{ t.type_name }} const *thatPtr
        )
    {
      Destruct( thisPtr );
      ConstructCopy( thisPtr, thatPtr );
    }

    static void Destruct(
        {{ t.type_name }} *thisPtr
        )
    {
        // [pzion 20151128] Using reinterpret_case here breaks gcc 4.8
        ::{{ t.codegen.cpp_base_type }} *handle =
          (::{{ t.codegen.cpp_base_type }} *)( thisPtr->handle );

        {{ enter }}
        delete handle;
        {{ leave }}

        thisPtr->handle = NULL;
    }
};
{% endif %}

      
template<>
struct Traits<{{ t.type_name }}>
{
    FABRIC_EDK_COMPLEX_TYPE( {{ t.type_name }} )

    static void ConstructEmpty(
        {{ t.type_name }} &this_
        )
    {
      {{ t.type_name }}::ConstructEmpty( &this_ );
    }
    static void ConstructCopy(
        {{ t.type_name }} &this_,
        {{ t.type_name }} const &that_
        )
    {
      {{ t.type_name }}::ConstructCopy( &this_, &that_ );
    }
    static void AssignCopy(
        {{ t.type_name }} &this_,
        {{ t.type_name }} const &that_
        )
    {
      {{ t.type_name }}::AssignCopy( &this_, &that_ );
    }
    static void Destruct(
        {{ t.type_name }} &this_
        )
    {
      {{ t.type_name }}::Destruct( &this_ );
    }
};


{% if not t.codegen.is_abstract %}
    FABRIC_EXT_EXPORT void {{ t.type_name }}__basic_constructor(
      Traits<{{ t.type_name_cpp_full }}>::IOParam this_
      )
    {
      Traits<{{ t.type_name }}>::ConstructEmpty( this_ );
    }

    FABRIC_EXT_EXPORT void {{ t.type_name }}__copy_constructor(
      Traits<{{ t.type_name_cpp_full }}>::IOParam this_,
      Traits<{{ t.type_name_cpp_full }}>::INParam that_
      )
    {
      Traits<{{ t.type_name }}>::ConstructCopy( this_, that_ );
    }
     
    FABRIC_EXT_EXPORT void {{ t.type_name }}__destructor(
      Traits< {{ t.type_name_cpp_full }} >::IOParam this_
      )
    {
      Traits<{{ t.type_name }}>::Destruct( this_ );
    }
{% endif %}

{% for method in t.methods %}

    FABRIC_EXT_EXPORT
    {% set needs_comma = False %}
    {% if manager.uses_returnval(method.ret_type_name) %}
        {{ method.ret_type_name_cpp_full }}
    {% else %}
        void
    {% endif %}
    {{ method.symbol }}(
    {% if method.ret_type_name and not manager.uses_returnval(method.ret_type_name) %}
        Traits< {{ method.ret_type_name_cpp_full }} >::Result _result
        {% set needs_comma = True %}
    {% endif %}
    {% if not method.codegen.is_static %}
        {% if method.ret_type_name and not manager.uses_returnval(method.ret_type_name) -%}
            ,
        {% endif %}
        {% if method.codegen.is_constructor or method.codegen.is_destructor %}
            Traits<{{ t.type_name_cpp_full }}>::IOParam {{ "this_" -}}
        {% else %}
            Traits<{{ t.type_name_cpp_full }}>::{{ method.usage_cpp }} {{ "this_" -}}
        {% endif %}
        {% set needs_comma = True %}
    {% endif %}
    {% for param in method.params %}
        {% if needs_comma or not loop.first -%}
            ,
        {% endif %}
        Traits<{{ param.type_name_cpp_full }}>::{{ param.usage_cpp }} {{ param.name -}}
    {% endfor %}
    )
    {
    {% if method.codegen.is_constructor %}
        {{ t.type_name }}__basic_constructor(this_);

        {% for param in method.params %}
            {{ parser.output_param_conversion(param.type_name, param.name, param.type_name_cpp_full, param.codegen.cpp_base_type) }}
        {% endfor %}

        {{ enter }}

        ::{{ t.codegen.cpp_base_type }} *handle = new ::{{ t.codegen.cpp_base_type }}(
        {% for param in method.params %}
            {% if not loop.first %},{% endif %}
            {{ param.name }}_param
        {% endfor %}
        );
        this_.handle = reinterpret_cast<KL::Data>(handle);

        {{ leave }}

    {% else %}
        {% if not method.codegen.is_static %}
            if (!this_.handle)
                throwException("handle is null");

            ::{{ t.codegen.cpp_base_type }} &handle =
                *(::{{ t.codegen.cpp_base_type }} *)(this_.handle);
            {% if parser.is_pointer_repr(t.type_name) %}
                if (!handle)
                    throwException("{{ t.type_name }} underlying pointer is null");
            {% endif %}
        {% endif %}

        {% for param in method.params %}
            {{ parser.output_param_conversion(param.type_name, param.name, param.type_name_cpp_full, param.codegen.cpp_base_type) }}
        {% endfor %}

        {{ enter }}

        {% if method.ret_type_name %}
            ::{{ method.codegen.cpp_qual_ret_type }} _result_param =
        {% endif %}
        {% if not method.codegen.is_static %}
            handle{% if parser.is_pointer_repr(t.type_name) %}->{% else %}.{% endif %}
        {% endif %}
        {{ method.codegen.cpp_function }}(
        {% for param in method.params %}
            {% if not loop.first %},{% endif %}
            {{ param.name }}_param
        {% endfor %}
        );

        {{ leave }}

        {% for param in method.params %}
            {% if param.usage == 'io' %}
                {{ parser.output_param_reconversion(param.type_name, param.name, param.codegen.cpp_base_type) }}
            {% endif %}
        {% endfor %}

        {% if method.ret_type_name and not manager.uses_returnval(method.ret_type_name) %}
            {{ parser.output_param_reconversion(method.ret_type_name_base, '_result', method.codegen.cpp_base_ret_type) }}
        {% elif method.ret_type_name %}
            return _result_param;
        {% endif %}

    {% endif %}
    }

{% endfor %}

} } }

//
//////////////////////////////////////////////////////////////////////////////
