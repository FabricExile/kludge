.. _KludgeTutorialWhichTypeToChoose:

Tutorial: Which type method to choose?
==========================================

As discussed in the :ref:`KludgeADLTypes` section you can wrap types in a variety of ways. This tutorial tries to describe which one works best in which scenario.

add_owned_type
-------------------

Use this method for types which are owned by the extension and not by the C++ library. Owned here refers to memory ownership. Upon construction of a type like this the memory will be stored in an opaque pointer of wrapped struct. The KL struct will perform reference counting on the owned memory, and once the last referee is destroyed the memory will be freed. Owned KL types call delete on the owned memory so you need to make to only use add_owned_type in situations where this is legal.

.. note:: add_owned_type is the default method used in Kludge, so please adapt and change the resulting kludge files if this is not the right method in your particular case.

add_opaque_type
----------------------

This method should be used for types which are not managed by the KL struct - but are completely opaque to KL in terms of memory ownership. This is usually the case for C APIs where you need to use global functions to construct and destruct pointers. The KL structs simply wrap these pointers but don't call any memory relevant functions on them. An example of the add_opaque_type usage is the sqlite3 extension. The sqlite3 C API uses pointers like this. To make things a bit easier for users we have added a higher level extension in pure KL called Sqlite3Wrapper, which uses KL objects to call the low level sqlite3 functions when constructing or destructing these pointers.

add_in_place_type
----------------------

Use this methods for types which map precisely in their memory layout to a type in KL. You might have a type in C++ like

.. code-block:: c++

    struct MyType {
      double d;
      bool b;
    };

and a KL structure like this

.. code-block:: kl

    struct MyType {
      Float64 d;
      Boolean b;
    };

In situations like this you can use the add_in_place_type method. The type's memory won't be touched - it will merely be translated directly between C++ and KL using the same memory layout. This is very efficient and makes things quite simple on the KL side too, since you can access all members of the type as well. Make sure to use this type where it applies in your project.

add_mirror
--------------

The add_mirror method is a specialized version of the add_in_place_type. The KL type passed to add_mirror is not provided by the extension you are currently authoring, but by an existing one that KL already supports. In Kludge speak there's a mirror of the type in C++ already in KL. A good example for this is any of the Math types - for example the Vec3. If the API you are wrapping has a float vector 3 you might as well add it as a mirror for the KL Vec3. That way all methods and functions of the wrapped library will work with the standard KL Vec3 type.

add_wrapped_type
-------------------

The add_wrapped_type method can be used to wrap a type to KL which already is making use a templated wrapper class in C++. The template wrapper class has to provide the two C++ operators ``operator->()``, to access the value the template owns, and ``bool operator !``, to assess if the template points to a NULL value. If these two exist Kludge can wrap the type with the add_wrapped_type method. The memory management is then left to the templated wrapper class and KL simply invokes the given operators.

