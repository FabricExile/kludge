class GenSpec: pass

class GenStr:
  def __init__(self, value):
    self._value = value
  def make_gen(self, jinjenv):
    return lambda gd: self._value

class GenLambda:
  def __init__(self, value):
    self._value = value
  def make_gen(self, jinjenv):
    return self._value

class GenTmpl:
  def __init__(self, value):
    self._value = value
  def make_gen(self, jinjenv):
    # IMPORTANT: bake the template so it is not regenerated on each invocation
    template = jinjenv.from_string(self._value)
    return lambda gd: template.render(gd.__dict__)

class GenFile:
  def __init__(self, value):
    self._value = value
  def make_gen(self, jinjenv):
    # IMPORTANT: bake the template so it is not regenerated on each invocation
    template = jinjenv.get_template(self._value)
    return lambda gd: template.render(gd.__dict__)

class TypeCodec:

  def __init__(
    self,
    jinjenv,
    ):
    self.jinjenv = jinjenv

  def set_hook(self, name, meth):
    if meth != None:
      setattr(self, name, meth)

  def make_gen(self, gen_spec):
    if gen_spec != None:
      if isinstance(gen_spec, basestring):
        gen_spec = GenTmpl(gen_spec)
      return gen_spec.make_gen(self.jinjenv)

  # Protocol: match

  def maybe_match(self, cpp_type_spec, type_mgr):
    raise Exception(cpp_type_spec.name + ": unimplemented match protocol")

  # Recipes: match

  def match_cpp_expr_types(self, cpp_expr_types_to_match, type_spec_builder):
    def impl(cpp_type_spec, type_mgr):
      for cpp_expr_type_to_match in cpp_expr_types_to_match:
        if cpp_type_spec.expr == cpp_expr_type_to_match:
          return type_spec_builder(cpp_type_spec)
    self.set_hook('maybe_match', impl)
    return self

  def match_cpp_expr_type(self, cpp_expr_type_to_match, type_spec_builder):
    return self.match_cpp_expr_types([cpp_expr_type_to_match], type_spec_builder)

  def match_value_by_dict(self, lookup):
    def impl(self, cpp_type_spec, type_mgr):
      if isinstance(cpp_type_spec.expr, CPPTypeExpr.Direct):
        kl_type_name = lookup.get(cpp_type_spec.expr.get_unqualified_desc())
        if kl_type_name:
          return SimpleTypeInfo(kl_type_name, cpp_type_spec)
    self.set_hook('maybe_match', impl)
    return self

  def match_const_ref_by_dict(self, lookup):
    def impl(self, cpp_type_spec, type_mgr):
      if isinstance(cpp_type_spec.expr, CPPTypeExpr.ReferenceTo) \
        and cpp_type_spec.expr.pointee.is_const \
        and isinstance(cpp_type_spec.expr.pointee, CPPTypeExpr.Direct):
        kl_type_name = lookup.get(cpp_type_spec.expr.pointee.get_unqualified_desc())
        if kl_type_name:
          return SimpleTypeInfo(kl_type_name, cpp_type_spec)
    self.set_hook('maybe_match', impl)
    return self

  def match_const_ptr_by_dict(self, lookup):
    def impl(self, cpp_type_spec, type_mgr):
      if isinstance(cpp_type_spec.expr, CPPTypeExpr.PointerTo) \
        and cpp_type_spec.expr.pointee.is_const \
        and isinstance(cpp_type_spec.expr.pointee, CPPTypeExpr.Direct):
        kl_type_name = lookup.get(cpp_type_spec.expr.pointee.get_unqualified_desc())
        if kl_type_name:
          return SimpleTypeInfo(kl_type_name, cpp_type_spec)
    self.set_hook('maybe_match', impl)
    return self

  def match_mutable_ref_by_dict(self, lookup):
    def impl(self, cpp_type_spec, type_mgr):
      if isinstance(cpp_type_spec.expr, CPPTypeExpr.ReferenceTo) \
        and cpp_type_spec.expr.pointee.is_mutable \
        and isinstance(cpp_type_spec.expr.pointee, CPPTypeExpr.Direct):
        kl_type_name = lookup.get(cpp_type_spec.expr.pointee.get_unqualified_desc())
        if kl_type_name:
          return SimpleTypeInfo(kl_type_name, cpp_type_spec)
    self.set_hook('maybe_match', impl)
    return self

  def match_mutable_ptr_by_dict(self, lookup):
    def impl(self, cpp_type_spec, type_mgr):
      if isinstance(cpp_type_spec.expr, CPPTypeExpr.PointerTo) \
        and cpp_type_spec.expr.pointee.is_mutable \
        and isinstance(cpp_type_spec.expr.pointee, CPPTypeExpr.Direct):
        kl_type_name = lookup.get(cpp_type_spec.expr.pointee.get_unqualified_desc())
        if kl_type_name:
          return SimpleTypeInfo(kl_type_name, cpp_type_spec)
    self.set_hook('maybe_match', impl)
    return self

  # Protocol: conversion

  def raise_unimplemented_conversion(self, gd):
    raise Exception(gd.type_spec.cpp.name + ": unimplmeneted conversion protocol")

  def gen_edk_to_cpp(self, gd):
    self.raise_unimplemented_conversion(gd)

  def gen_cpp_arg(self, gd):
    self.raise_unimplemented_conversion(gd)

  def gen_cpp_to_edk(self, gd):
    self.raise_unimplemented_conversion(gd)

  # Recipes: conversion

  def conv(
    self,
    edk_to_cpp = GenStr(""),
    cpp_arg = None,
    cpp_to_edk = GenStr(""),
    ):
    self.set_hook('gen_edk_to_cpp', self.make_gen(edk_to_cpp))
    self.set_hook('gen_cpp_arg', self.make_gen(cpp_arg))
    self.set_hook('gen_cpp_to_edk', self.make_gen(cpp_to_edk))
    return self

  # Protocol: result

  def raise_unsupported_as_result(self, gd):
    raise Exception(gd.type_spec.cpp.name + ": unsupported as result")

  def gen_kl_result_type(self, gd):
    return gd.type.kl.compound

  def gen_direct_result_edk_type(self, gd):
    self.raise_unsupported_as_result(gd)

  def gen_indirect_result_edk_param(self, gd):
    self.raise_unsupported_as_result(gd)

  def gen_edk_store_result_pre(self, gd):
    self.raise_unsupported_as_result(gd)

  def gen_edk_store_result_post(self, gd):
    self.raise_unsupported_as_result(gd)

  def gen_edk_return_dir_result(self, gd):
    self.raise_unsupported_as_result(gd)

  # Recipes: result

  def direct_result(
    self,
    pre = GenLambda(lambda gd: gd.type.edk.name + " " + gd.name.edk),
    post = GenStr(""),
    ):
    self.set_hook(
      'gen_direct_result_edk_type',
      lambda gd: gd.type.edk.name
      )
    self.set_hook(
      'gen_indirect_result_edk_param',
      lambda gd: ""
      )
    self.set_hook('gen_edk_store_result_pre', self.make_gen(pre))
    self.set_hook('gen_edk_store_result_post', self.make_gen(post))
    self.set_hook(
      'gen_edk_return_dir_result',
      lambda gd: "return " + gd.name.edk + ";"
      )
    return self

  def indirect_result(
    self,
    pre = GenLambda(lambda gd: gd.name.edk + " = "),
    post = GenStr(""),
    ):
    self.set_hook(
      'gen_direct_result_edk_type',
      lambda gd: "void"
      )
    self.set_hook(
      'gen_indirect_result_edk_param',
      lambda gd: "Traits< " + gd.type.edk.name + " >::Result " + gd.name.edk
      )
    self.set_hook('gen_edk_store_result_pre', self.make_gen(pre))
    self.set_hook('gen_edk_store_result_post', self.make_gen(post))
    self.set_hook(
      'gen_edk_return_dir_result',
      lambda gd: ""
      )
    return self
 
  # Protocol: params

  def raise_unsupported_as_param(self, gd):
    raise Exception(gd.type_spec.cpp.name + ": unsupported as params")

  def gen_kl_param(self, gd):
    self.raise_unsupported_as_param(gd)

  def gen_edk_param(self, gd):
    self.raise_unsupported_as_param(gd)
 
  # Recipes: params

  def in_param(self):
    self.set_hook(
      'gen_kl_param',
      lambda gd:
        gd.type.kl.base + " " + gd.name.kl + gd.type.kl.suffix
      )
    self.set_hook(
      'gen_edk_param',
      lambda gd:
        "Traits< " + gd.type.edk.name + " >::INParam " + gd.name.edk
      )
    return self

  def io_param(self):
    self.set_hook(
      'gen_kl_param',
      lambda gd:
        "io " + gd.type.kl.base + " " + gd.name.kl + gd.type.kl.suffix
      )
    self.set_hook(
      'gen_edk_param',
      lambda gd:
        "Traits< " + gd.type.edk.name + " >::IOParam " + gd.name.edk
      )
    return self
