from kludge import GenStr, GenLambda, CPPTypeExpr, SimpleTypeSpec

class TypeCodec:

  def __init__(
    self,
    jinjenv,
    ):
    self.jinjenv = jinjenv

    self._init_result_protocol()

  def set_hook(self, name, meth):
    setattr(self, name, meth)

  def make_gen(self, gen_spec):
    if isinstance(gen_spec, basestring):
      gen_spec = GenTmpl(gen_spec)
    return gen_spec.make_gen(self.jinjenv)

  def raise_missing_or_invalid(self, name):
    raise Exception("missing or invalid '" + name + "' (must be a string or an instance of GenXXX)")

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
    def impl(cpp_type_spec, type_mgr):
      if isinstance(cpp_type_spec.expr, CPPTypeExpr.Direct):
        kl_type_name = lookup.get(cpp_type_spec.expr.get_unqualified_desc())
        if kl_type_name:
          return SimpleTypeSpec(kl_type_name, cpp_type_spec)
    self.set_hook('maybe_match', impl)
    return self

  def match_const_ref_by_dict(self, lookup):
    def impl(cpp_type_spec, type_mgr):
      if isinstance(cpp_type_spec.expr, CPPTypeExpr.ReferenceTo) \
        and cpp_type_spec.expr.pointee.is_const \
        and isinstance(cpp_type_spec.expr.pointee, CPPTypeExpr.Direct):
        kl_type_name = lookup.get(cpp_type_spec.expr.pointee.get_unqualified_desc())
        if kl_type_name:
          return SimpleTypeSpec(kl_type_name, cpp_type_spec)
    self.set_hook('maybe_match', impl)
    return self

  def match_const_ptr_by_dict(self, lookup):
    def impl(cpp_type_spec, type_mgr):
      if isinstance(cpp_type_spec.expr, CPPTypeExpr.PointerTo) \
        and cpp_type_spec.expr.pointee.is_const \
        and isinstance(cpp_type_spec.expr.pointee, CPPTypeExpr.Direct):
        kl_type_name = lookup.get(cpp_type_spec.expr.pointee.get_unqualified_desc())
        if kl_type_name:
          return SimpleTypeSpec(kl_type_name, cpp_type_spec)
    self.set_hook('maybe_match', impl)
    return self

  def match_mutable_ref_by_dict(self, lookup):
    def impl(cpp_type_spec, type_mgr):
      if isinstance(cpp_type_spec.expr, CPPTypeExpr.ReferenceTo) \
        and cpp_type_spec.expr.pointee.is_mutable \
        and isinstance(cpp_type_spec.expr.pointee, CPPTypeExpr.Direct):
        kl_type_name = lookup.get(cpp_type_spec.expr.pointee.get_unqualified_desc())
        if kl_type_name:
          return SimpleTypeSpec(kl_type_name, cpp_type_spec)
    self.set_hook('maybe_match', impl)
    return self

  def match_mutable_ptr_by_dict(self, lookup):
    def impl(cpp_type_spec, type_mgr):
      if isinstance(cpp_type_spec.expr, CPPTypeExpr.PointerTo) \
        and cpp_type_spec.expr.pointee.is_mutable \
        and isinstance(cpp_type_spec.expr.pointee, CPPTypeExpr.Direct):
        kl_type_name = lookup.get(cpp_type_spec.expr.pointee.get_unqualified_desc())
        if kl_type_name:
          return SimpleTypeSpec(kl_type_name, cpp_type_spec)
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
    edk_to_cpp = None,
    cpp_arg = None,
    cpp_to_edk = None,
    ):
    try:
      self.set_hook('gen_edk_to_cpp', self.make_gen(edk_to_cpp))
    except:
      self.raise_missing_or_invalid("edk_to_cpp")
    try:
      self.set_hook('gen_cpp_arg', self.make_gen(cpp_arg))
    except:
      self.raise_missing_or_invalid("cpp_arg")
    try:
      self.set_hook('gen_cpp_to_edk', self.make_gen(cpp_to_edk))
    except:
      self.raise_missing_or_invalid("cpp_to_edk")
    return self

  def no_conv(
    self,
    cpp_arg = None,
    ):
    return self.conv(
      edk_to_cpp = GenStr(""),
      cpp_arg = cpp_arg,
      cpp_to_edk = GenStr(""),
      )

  def no_conv_by_ref(self):
    return self.no_conv(
      cpp_arg = GenLambda(lambda gd: gd.name.edk),
      )

  def no_conv_by_ptr(self):
    return self.no_conv(
      cpp_arg = GenLambda(lambda gd: "&" + gd.name.edk),
      )

  # Protocol: result

  result_protocol_gen_names = [
    'gen_kl_result_type',
    'gen_direct_result_edk_type',
    'gen_indirect_result_edk_param',
    'gen_edk_store_result_pre',
    'gen_edk_store_result_post',
    'gen_edk_return_dir_result',
    ]

  def _init_result_protocol(self):
    def impl(gd):
      raise Exception("unimplemented result protocol")
    for gen_name in TypeCodec.result_protocol_gen_names:
      self.set_hook(gen_name, impl)

  # Recipes: result

  def no_result(self):
    def impl(gd):
      raise Exception(gd.type.cpp.name + ": unsupported as a result type")
    for gen_name in TypeCodec.result_protocol_gen_names:
      self.set_hook(gen_name, impl)
    return self

  def direct_result(
    self,
    pre = GenLambda(lambda gd: gd.type.edk.name + " " + gd.name.edk + " = "),
    post = GenStr(""),
    ):
    self.set_hook(
      'gen_kl_result_type',
      lambda gd: gd.type.kl.compound
      )
    self.set_hook(
      'gen_direct_result_edk_type',
      lambda gd: gd.type.edk.name
      )
    self.set_hook(
      'gen_indirect_result_edk_param',
      lambda gd: ""
      )
    try:
      self.set_hook('gen_edk_store_result_pre', self.make_gen(pre))
    except:
      self.raise_missing_or_invalid("pre")
    try:
      self.set_hook('gen_edk_store_result_post', self.make_gen(post))
    except:
      self.raise_missing_or_invalid("post")
    self.set_hook(
      'gen_edk_return_dir_result',
      lambda gd: "return " + gd.name.edk + ";"
      )
    return self

  def direct_result_deref_ptr(self):
    return self.direct_result(
      pre = GenLambda(lambda gd: gd.type.edk.name + " " + gd.name.edk + " = *")
      )

  def indirect_result(
    self,
    pre = GenLambda(lambda gd: gd.name.edk + " = "),
    post = GenStr(""),
    ):
    self.set_hook(
      'gen_kl_result_type',
      lambda gd: gd.type.kl.compound
      )
    self.set_hook(
      'gen_direct_result_edk_type',
      lambda gd: "void"
      )
    self.set_hook(
      'gen_indirect_result_edk_param',
      lambda gd: "Traits< " + gd.type.edk.name + " >::Result " + gd.name.edk
      )
    try:
      self.set_hook('gen_edk_store_result_pre', self.make_gen(pre))
    except:
      self.raise_missing_or_invalid("pre")
    try:
      self.set_hook('gen_edk_store_result_post', self.make_gen(post))
    except:
      self.raise_missing_or_invalid("post")
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
