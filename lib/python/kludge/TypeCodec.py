from kludge import GenStr, GenLambda, GenTmpl, CPPTypeExpr, SimpleTypeSpec

class TypeCodec:

  protocols = {
    'conversion': [
      'edk_to_cpp',
      'cpp_arg',
      'cpp_to_edk',
      ],
    'result': [
      'kl_result_type',
      'direct_result_edk_type',
      'indirect_result_edk_param',
      'edk_store_result_pre',
      'edk_store_result_post',
      'edk_return_direct_result',
      ],
    'params': [
      'kl_param',
      'edk_param',
      ],
    }

  def __init__(
    self,
    jinjenv,
    ):
    self.jinjenv = jinjenv

    for protocol_name, hook_names in TypeCodec.protocols.iteritems():
      def impl(gd):
        raise Exception("unimplemented " + protocol_name + " protocol")
      for hook_name in hook_names:
        self.set_hook(hook_name, impl)

    # Special signature and no reflection
    def maybe_match_default(cpp_type_spec, type_mgr):
      raise Exception("unimplemented match protocol")
    self.set_hook('maybe_match', maybe_match_default)

  def set_hook(self, name, meth):
    setattr(self, name, meth)

  def make_gen(self, gen_spec):
    if isinstance(gen_spec, basestring):
      gen_spec = GenTmpl(gen_spec)
    return gen_spec.make_gen(self.jinjenv)

  def raise_missing_or_invalid(self, name):
    raise Exception("missing or invalid '" + name + "' (must be a string or an instance of GenXXX)")

  # Recipes: match

  def match(self, impl):
    self.set_hook('maybe_match', impl)
    return self

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

  # Recipes: result

  def no_result(self):
    def impl(gd):
      raise Exception(gd.type.cpp.name + ": unsupported as a result type")
    for hook_name in TypeCodec.protocols['result']:
      self.set_hook('gen_' + hook_name, impl)
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
      'gen_edk_return_direct_result',
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
      'gen_edk_return_direct_result',
      lambda gd: ""
      )
    return self
 
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
