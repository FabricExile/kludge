from kludge import GenStr, GenLambda, GenTmpl, CPPTypeExpr, ValueName, SimpleTypeSpec

class TypeCodec:

  protocols = {
    'traits': [
      'traits_kl',
      'traits_edk',
      'traits_cpp',
      'traits_pointer_make',
      'traits_pointer_undo',
      'traits_reference',
      ],
    'conversion': [
      'conv_edk_to_cpp',
      'conv_edk_to_cpp_decl',
      'conv_cpp_to_edk',
      'conv_cpp_to_edk_decl',
      ],
    'result': [
      'result_direct_type_edk',
      'result_indirect_param_edk',
      'result_indirect_init_edk',
      'result_decl_and_assign_cpp',
      'result_indirect_assign_to_edk',
      'result_direct_return_edk',
      ],
    'param': [
      'param_kl',
      'param_edk',
      'param_edk_to_cpp_decl',
      'param_cpp',
      'param_cpp_to_edk',
      ],
    }

  def __init__(
    self,
    value_name,
    type_spec,
    ):
    self.name = value_name
    self.type = type_spec
    self.children = []
    child_index = 1
    for child_type_info in type_spec.child_type_infos:
      self.children.append(
        child_type_info.make_codec(
          ValueName(value_name.kl + "_RESERVED_child_%u" % child_index),
          )
        )
      child_index += 1
    if self.children:
      setattr(
        self,
        'element',
        self.children[0]
        )

  @classmethod
  def set_class_hook(cls, name, meth):
    setattr(cls, name, classmethod(meth))

  @classmethod
  def set_hook(cls, name, meth):
    setattr(cls, name, meth)

  @staticmethod
  def make_gen(gen_spec):
    if isinstance(gen_spec, basestring):
      gen_spec = GenTmpl(gen_spec)
    return gen_spec.make_gen()

  @classmethod
  def raise_unimplemented_protocol(cls, protocol_name):
    raise Exception("unimplemented " + protocol_name + " protocol on " + cls.__name__)

  @staticmethod
  def raise_missing_or_invalid(name):
    raise Exception("missing or invalid '" + name + "' (must be a string or an instance of GenXXX)")

  # Recipes: match

  @classmethod
  def maybe_match(cls, cpp_type_expr, type_mgr):
    cls.raise_unimplemented_protocol('match')

  @classmethod
  def match(cls, impl):
    cls.set_class_hook('maybe_match', impl)
    return cls

  @classmethod
  def match_cpp_type_exprs(cls, cpp_expr_types_to_match, type_spec_builder):
    def impl(cls, cpp_type_expr, type_mgr):
      for cpp_expr_type_to_match in cpp_expr_types_to_match:
        if cpp_type_expr == cpp_expr_type_to_match:
          unqual_cpp_type_name = str(cpp_type_expr)
          return type_spec_builder(cpp_type_expr)
    cls.set_class_hook('maybe_match', impl)
    return cls

  @classmethod
  def match_cpp_type_expr(cls, cpp_expr_type_to_match, type_spec_builder):
    return cls.match_cpp_type_exprs([cpp_expr_type_to_match], type_spec_builder)

  @classmethod
  def match_value_by_dict(cls, lookup):
    def impl(cls, cpp_type_expr, type_mgr):
      if isinstance(cpp_type_expr, CPPTypeExpr.Direct):
        unqual_cpp_type_name = cpp_type_expr.get_unqualified_desc()
        kl_type_name = lookup.get(unqual_cpp_type_name)
        if kl_type_name:
          return SimpleTypeSpec(kl_type_name, unqual_cpp_type_name, cpp_type_expr)
    cls.set_class_hook('maybe_match', impl)
    return cls

  @classmethod
  def match_const_ref_by_dict(cls, lookup):
    def impl(cls, cpp_type_expr, type_mgr):
      if isinstance(cpp_type_expr, CPPTypeExpr.ReferenceTo) \
        and cpp_type_expr.pointee.is_const \
        and isinstance(cpp_type_expr.pointee, CPPTypeExpr.Direct):
        unqual_cpp_type_name = cpp_type_expr.pointee.get_unqualified_desc()
        kl_type_name = lookup.get(unqual_cpp_type_name)
        if kl_type_name:
          return SimpleTypeSpec(kl_type_name, unqual_cpp_type_name, cpp_type_expr)
    cls.set_class_hook('maybe_match', impl)
    return cls

  @classmethod
  def match_const_ptr_by_dict(cls, lookup):
    def impl(cls, cpp_type_expr, type_mgr):
      if isinstance(cpp_type_expr, CPPTypeExpr.PointerTo) \
        and cpp_type_expr.pointee.is_const \
        and isinstance(cpp_type_expr.pointee, CPPTypeExpr.Direct):
        unqual_cpp_type_name = cpp_type_expr.pointee.get_unqualified_desc()
        kl_type_name = lookup.get(unqual_cpp_type_name)
        if kl_type_name:
          return SimpleTypeSpec(kl_type_name, unqual_cpp_type_name, cpp_type_expr)
    cls.set_class_hook('maybe_match', impl)
    return cls

  @classmethod
  def match_mutable_ref_by_dict(cls, lookup):
    def impl(cls, cpp_type_expr, type_mgr):
      if isinstance(cpp_type_expr, CPPTypeExpr.ReferenceTo) \
        and cpp_type_expr.pointee.is_mutable \
        and isinstance(cpp_type_expr.pointee, CPPTypeExpr.Direct):
        unqual_cpp_type_name = cpp_type_expr.pointee.get_unqualified_desc()
        kl_type_name = lookup.get(unqual_cpp_type_name)
        if kl_type_name:
          return SimpleTypeSpec(kl_type_name, unqual_cpp_type_name, cpp_type_expr)
    cls.set_class_hook('maybe_match', impl)
    return cls

  @classmethod
  def match_mutable_ptr_by_dict(cls, lookup):
    def impl(cls, cpp_type_expr, type_mgr):
      if isinstance(cpp_type_expr, CPPTypeExpr.PointerTo) \
        and cpp_type_expr.pointee.is_mutable \
        and isinstance(cpp_type_expr.pointee, CPPTypeExpr.Direct):
        unqual_cpp_type_name = cpp_type_expr.pointee.get_unqualified_desc()
        kl_type_name = lookup.get(unqual_cpp_type_name)
        if kl_type_name:
          return SimpleTypeSpec(kl_type_name, unqual_cpp_type_name, cpp_type_expr)
    cls.set_class_hook('maybe_match', impl)
    return cls

  # Recipes: traits

  @classmethod
  def traits(
    cls,
    kl = None,
    edk = None,
    cpp = None,
    pointer_make = None,
    pointer_undo = None,
    reference = None,
    ):
    try:
      cls.set_hook('traits_kl', cls.make_gen(kl))
    except:
      cls.raise_missing_or_invalid('kl')
    try:
      cls.set_hook('traits_edk', cls.make_gen(edk))
    except:
      cls.raise_missing_or_invalid('edk')
    try:
      cls.set_hook('traits_cpp', cls.make_gen(cpp))
    except:
      cls.raise_missing_or_invalid('cpp')
    try:
      cls.set_hook('traits_pointer_make', cls.make_gen(pointer_make))
    except:
      cls.raise_missing_or_invalid('pointer_make')
    try:
      cls.set_hook('traits_pointer_undo', cls.make_gen(pointer_undo))
    except:
      cls.raise_missing_or_invalid('pointer_undo')
    try:
      cls.set_hook('traits_reference', cls.make_gen(reference))
    except:
      cls.raise_missing_or_invalid('reference')
    return cls

  @classmethod
  def traits_value(cls):
    return cls.traits(
      kl = GenStr(""),
      edk = GenStr("INParam"),
      cpp = GenStr(""),
      pointer_make = GenStr(""),
      pointer_undo = GenStr(""),
      reference = GenStr("const &"),
      )

  @classmethod
  def traits_const_ref(cls):
    return cls.traits(
      kl = GenStr(""),
      edk = GenStr("INParam"),
      cpp = GenStr("const &"),
      pointer_make = GenStr(""),
      pointer_undo = GenStr(""),
      reference = GenStr("const &"),
      )

  @classmethod
  def traits_const_ptr(cls):
    return cls.traits(
      kl = GenStr(""),
      edk = GenStr("INParam"),
      cpp = GenStr("const *"),
      pointer_make = GenStr("&"),
      pointer_undo = GenStr("*"),
      reference = GenStr("const &"),
      )

  @classmethod
  def traits_mutable_ref(cls):
    return cls.traits(
      kl = GenStr("io"),
      edk = GenStr("IOParam"),
      cpp = GenStr("&"),
      pointer_make = GenStr(""),
      pointer_undo = GenStr(""),
      reference = GenStr("&"),
      )

  @classmethod
  def traits_mutable_ptr(cls):
    return cls.traits(
      kl = GenStr("io"),
      edk = GenStr("IOParam"),
      cpp = GenStr("*"),
      pointer_make = GenStr("&"),
      pointer_undo = GenStr("*"),
      reference = GenStr("&"),
      )

  # Recipes: conversion

  @classmethod
  def conv(
    cls,
    edk_to_cpp = GenLambda(
      lambda self: self.name.cpp + " = " + self.name.edk + ";"
      ),
    edk_to_cpp_decl = GenLambda(
      lambda self: self.type.cpp.name + " " + self.conv_edk_to_cpp()
      ),
    cpp_to_edk = GenLambda(
      lambda self: self.name.edk + " = " + self.name.cpp + ";"
      ),
    cpp_to_edk_decl = GenLambda(
      lambda self: self.type.edk.name + " " + self.conv_cpp_to_edk()
      ),
    ):
    try:
      cls.set_hook('conv_edk_to_cpp', cls.make_gen(edk_to_cpp))
    except Exception as e:
      print str(e)
      cls.raise_missing_or_invalid('edk_to_cpp')
    try:
      cls.set_hook('conv_edk_to_cpp_decl', cls.make_gen(edk_to_cpp_decl))
    except:
      cls.raise_missing_or_invalid('edk_to_cpp_decl')
    try:
      cls.set_hook('conv_cpp_to_edk', cls.make_gen(cpp_to_edk))
    except:
      cls.raise_missing_or_invalid('cpp_to_edk')
    try:
      cls.set_hook('conv_cpp_to_edk_decl', cls.make_gen(cpp_to_edk_decl))
    except:
      cls.raise_missing_or_invalid('cpp_to_edk_decl')
    return cls

  @classmethod
  def conv_none(cls):
    return cls.conv(
      edk_to_cpp = GenStr(""),
      edk_to_cpp_decl = GenLambda(
        lambda self: self.type.cpp.name + " " + self.traits_reference() + self.name.cpp + " = " + self.name.edk + ";"
        ),
      cpp_to_edk = GenStr(""),
      cpp_to_edk_decl = GenLambda(
        lambda self: self.type.edk.name + " const &" + self.name.edk + " = " + self.name.cpp + ";"
        ),
      )

  @classmethod
  def conv_none_cast_away_const(cls):
    return cls.conv(
      edk_to_cpp = GenStr(""),
      edk_to_cpp_decl = GenLambda(
        lambda self: self.type.cpp.name + " " + self.traits_reference() + self.name.cpp + " = const_cast< " + self.type.cpp.name+ " " + self.traits_reference() + " >( " + self.name.edk + ");"
        ),
      cpp_to_edk = GenStr(""),
      cpp_to_edk_decl = GenLambda(
        lambda self: self.type.edk.name + " const &" + self.name.edk + " = const_cast< " + self.type.edk.name + " const & >( " + self.name.cpp + ");"
        ),
      )

  # Recipes: result

  @classmethod
  def result_forbidden(cls):
    def impl(self):
      raise Exception(self.type.cpp.name + ": unsupported as a result type")
    for hook_name in TypeCodec.protocols['result']:
      cls.set_hook(hook_name, impl)
    return cls

  @classmethod
  def result(
    cls,
    direct_type_edk = GenStr("void"),
    indirect_param_edk = GenLambda(
      lambda self: "::Fabric::EDK::KL::Traits< " + self.type.edk.name + " >::Result " + self.name.edk
      ),
    indirect_init_edk = GenStr(""),
    decl_and_assign_cpp = GenLambda(
      lambda self: self.type.cpp.name + " " + self.name.cpp + " = " + self.traits_pointer_undo()
      ),
    indirect_assign_to_edk = GenLambda(
      lambda self: self.conv_cpp_to_edk()
      ),
    direct_return_edk = GenStr(""),
    ):
    try:
      cls.set_hook('result_direct_type_edk', cls.make_gen(direct_type_edk))
    except:
      cls.raise_missing_or_invalid('direct_type_edk')
    try:
      cls.set_hook('result_indirect_param_edk', cls.make_gen(indirect_param_edk))
    except:
      cls.raise_missing_or_invalid('indirect_param_edk')
    try:
      cls.set_hook('result_indirect_init_edk', cls.make_gen(indirect_init_edk))
    except:
      cls.raise_missing_or_invalid('indirect_init_edk')
    try:
      cls.set_hook('result_decl_and_assign_cpp', cls.make_gen(decl_and_assign_cpp))
    except:
      cls.raise_missing_or_invalid('decl_and_assign_cpp')
    try:
      cls.set_hook('result_indirect_assign_to_edk', cls.make_gen(indirect_assign_to_edk))
    except:
      cls.raise_missing_or_invalid('indirect_assign_to_edk')
    try:
      cls.set_hook('result_direct_return_edk', cls.make_gen(direct_return_edk))
    except:
      cls.raise_missing_or_invalid('direct_return_edk')
    return cls

  @classmethod
  def result_direct(
    cls,
    decl_and_assign_cpp = GenLambda(
      lambda self: self.type.cpp.name + " " + self.name.cpp + " = " + self.traits_pointer_undo()
      ),
    ):
    return cls.result(
      direct_type_edk = GenLambda(
        lambda self: self.type.edk.name
        ),
      indirect_param_edk = GenStr(""),
      decl_and_assign_cpp = decl_and_assign_cpp,
      indirect_assign_to_edk = GenStr(""),
      direct_return_edk = GenLambda(
        lambda self: self.conv_cpp_to_edk_decl() + "\nreturn " + self.name.edk + ";"
        ),
      )

  # Recipes: param

  @classmethod
  def param(
    cls,
    kl = GenLambda(
      lambda self: self.traits_kl() + " " + self.type.kl.base + " " + self.name.kl + self.type.kl.suffix
      ),
    edk = GenLambda(
      lambda self: "::Fabric::EDK::KL::Traits< " + self.type.edk.name + " >::" + self.traits_edk() + " " + self.name.edk
      ),
    edk_to_cpp_decl = GenLambda(
      lambda self: self.conv_edk_to_cpp_decl()
      ),
    cpp = GenLambda(
      lambda self: self.traits_pointer_make() + self.name.cpp
      ),
    cpp_to_edk = GenStr(""),
    ):
    try:
      cls.set_hook('param_edk', cls.make_gen(edk))
    except:
      cls.raise_missing_or_invalid('edk')
    try:
      cls.set_hook('param_kl', cls.make_gen(kl))
    except:
      cls.raise_missing_or_invalid('kl')
    try:
      cls.set_hook('param_edk_to_cpp_decl', cls.make_gen(edk_to_cpp_decl))
    except:
      cls.raise_missing_or_invalid('edk_to_cpp_decl')
    try:
      cls.set_hook('param_cpp', cls.make_gen(cpp))
    except:
      cls.raise_missing_or_invalid('cpp')
    try:
      cls.set_hook('param_cpp_to_edk', cls.make_gen(cpp_to_edk))
    except:
      cls.raise_missing_or_invalid('cpp_to_edk')
    return cls

  @classmethod
  def param_in(cls):
    return cls.param()

  @classmethod
  def param_io(cls):
    return cls.param(
      cpp_to_edk = GenLambda(
        lambda self: self.conv_cpp_to_edk()
        ),
      )

for protocol_name, hook_names in TypeCodec.protocols.iteritems():
  def impl(self, protocol_name=protocol_name):
    self.__class__.raise_unimplemented_protocol(protocol_name)
  for hook_name in hook_names:
    TypeCodec.set_hook(hook_name, impl)

# param() and result() are optional
TypeCodec.param()
TypeCodec.result()
