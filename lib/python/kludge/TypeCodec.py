from kludge import GenStr, GenLambda, GenTmpl, CPPTypeExpr, SimpleTypeSpec

class TypeCodec:

  protocols = {
    'conversion': [
      'conv_edk_to_cpp',
      'conv_edk_to_cpp_decl',
      'conv_cpp_to_edk',
      'conv_cpp_to_edk_decl',
      ],
    'result': [
      'result_direct_type_edk',
      'result_indirect_param_edk',
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
    jinjenv,
    ):
    self.jinjenv = jinjenv

    for protocol_name, hook_names in TypeCodec.protocols.iteritems():
      def impl(gd):
        raise Exception("unimplemented " + protocol_name + " protocol")
      for hook_name in hook_names:
        self.set_hook(hook_name, impl)

    # Special signature and no reflection
    def maybe_match_default(cpp_type_name, cpp_type_spec, type_mgr):
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

  def match_cpp_expr_types(self, cpp_expr_types_to_match, type_spec):
    def impl(cpp_type_expr, type_mgr):
      for cpp_expr_type_to_match in cpp_expr_types_to_match:
        if cpp_type_expr == cpp_expr_type_to_match:
          return type_spec
    self.set_hook('maybe_match', impl)
    return self

  def match_cpp_expr_type(self, cpp_expr_type_to_match, type_spec):
    return self.match_cpp_expr_types([cpp_expr_type_to_match], type_spec)

  def match_value_by_dict(self, lookup):
    def impl(cpp_type_expr, type_mgr):
      if isinstance(cpp_type_expr, CPPTypeExpr.Direct):
        unqual_cpp_type_name = cpp_type_expr.get_unqualified_desc()
        kl_type_name = lookup.get(unqual_cpp_type_name)
        if kl_type_name:
          return SimpleTypeSpec(kl_type_name, unqual_cpp_type_name)
    self.set_hook('maybe_match', impl)
    return self

  def match_const_ref_by_dict(self, lookup):
    def impl(cpp_type_expr, type_mgr):
      if isinstance(cpp_type_expr, CPPTypeExpr.ReferenceTo) \
        and cpp_type_expr.pointee.is_const \
        and isinstance(cpp_type_expr.pointee, CPPTypeExpr.Direct):
        unqual_cpp_type_name = cpp_type_expr.pointee.get_unqualified_desc()
        kl_type_name = lookup.get(unqual_cpp_type_name)
        if kl_type_name:
          return SimpleTypeSpec(kl_type_name, unqual_cpp_type_name)
    self.set_hook('maybe_match', impl)
    return self

  def match_const_ptr_by_dict(self, lookup):
    def impl(cpp_type_expr, type_mgr):
      if isinstance(cpp_type_expr, CPPTypeExpr.PointerTo) \
        and cpp_type_expr.pointee.is_const \
        and isinstance(cpp_type_expr.pointee, CPPTypeExpr.Direct):
        unqual_cpp_type_name = cpp_type_expr.pointee.get_unqualified_desc()
        kl_type_name = lookup.get(unqual_cpp_type_name)
        if kl_type_name:
          return SimpleTypeSpec(kl_type_name, unqual_cpp_type_name)
    self.set_hook('maybe_match', impl)
    return self

  def match_mutable_ref_by_dict(self, lookup):
    def impl(cpp_type_expr, type_mgr):
      if isinstance(cpp_type_expr, CPPTypeExpr.ReferenceTo) \
        and cpp_type_expr.pointee.is_mutable \
        and isinstance(cpp_type_expr.pointee, CPPTypeExpr.Direct):
        unqual_cpp_type_name = cpp_type_expr.pointee.get_unqualified_desc()
        kl_type_name = lookup.get(unqual_cpp_type_name)
        if kl_type_name:
          return SimpleTypeSpec(kl_type_name, unqual_cpp_type_name)
    self.set_hook('maybe_match', impl)
    return self

  def match_mutable_ptr_by_dict(self, lookup):
    def impl(cpp_type_expr, type_mgr):
      if isinstance(cpp_type_expr, CPPTypeExpr.PointerTo) \
        and cpp_type_expr.pointee.is_mutable \
        and isinstance(cpp_type_expr.pointee, CPPTypeExpr.Direct):
        unqual_cpp_type_name = cpp_type_expr.pointee.get_unqualified_desc()
        kl_type_name = lookup.get(unqual_cpp_type_name)
        if kl_type_name:
          return SimpleTypeSpec(kl_type_name, unqual_cpp_type_name)
    self.set_hook('maybe_match', impl)
    return self

  # Recipes: conversion

  def conv(
    self,
    edk_to_cpp = None,
    edk_to_cpp_decl = GenLambda(
      lambda gd: gd.type.cpp.name + " " + gd.conv_edk_to_cpp()
      ),
    cpp_to_edk = None,
    cpp_to_edk_decl = GenLambda(
      lambda gd: gd.type.edk.name + " " + gd.conv_cpp_to_edk()
      ),
    ):
    try:
      self.set_hook('gen_conv_edk_to_cpp', self.make_gen(edk_to_cpp))
    except:
      self.raise_missing_or_invalid('edk_to_cpp')
    try:
      self.set_hook('gen_conv_edk_to_cpp_decl', self.make_gen(edk_to_cpp_decl))
    except:
      self.raise_missing_or_invalid('edk_to_cpp_decl')
    try:
      self.set_hook('gen_conv_cpp_to_edk', self.make_gen(cpp_to_edk))
    except:
      self.raise_missing_or_invalid('cpp_to_edk')
    try:
      self.set_hook('gen_conv_cpp_to_edk_decl', self.make_gen(cpp_to_edk_decl))
    except:
      self.raise_missing_or_invalid('cpp_to_edk_decl')
    return self

  def no_conv(self):
    return self.conv(
      edk_to_cpp = GenLambda(
        lambda gd: gd.name.cpp + " = " + gd.name.edk + ";"
        ),
      cpp_to_edk = GenLambda(
        lambda gd: gd.name.edk + " = " + gd.name.cpp + ";"
        ),
      )

  # Recipes: result

  def no_result(self):
    def impl(gd):
      raise Exception(gd.type.cpp.name + ": unsupported as a result type")
    for hook_name in TypeCodec.protocols['result']:
      self.set_hook('gen_' + hook_name, impl)
    return self

  def result(
    self,
    direct_type_edk = None,
    indirect_param_edk = None,
    decl_and_assign_cpp = None,
    indirect_assign_to_edk = None,
    direct_return_edk = None,
    ):
    try:
      self.set_hook('gen_result_direct_type_edk', self.make_gen(direct_type_edk))
    except:
      self.raise_missing_or_invalid('direct_type_edk')
    try:
      self.set_hook('gen_result_indirect_param_edk', self.make_gen(indirect_param_edk))
    except:
      self.raise_missing_or_invalid('indirect_param_edk')
    try:
      self.set_hook('gen_result_decl_and_assign_cpp', self.make_gen(decl_and_assign_cpp))
    except:
      self.raise_missing_or_invalid('decl_and_assign_cpp')
    try:
      self.set_hook('gen_result_indirect_assign_to_edk', self.make_gen(indirect_assign_to_edk))
    except:
      self.raise_missing_or_invalid('indirect_assign_to_edk')
    try:
      self.set_hook('gen_result_direct_return_edk', self.make_gen(direct_return_edk))
    except:
      self.raise_missing_or_invalid('direct_return_edk')
    return self

  def result_direct(
    self,
    decl_and_assign_cpp = GenLambda(
      lambda gd: gd.type.cpp.name + " " + gd.name.cpp + " = "
      ),
    ):
    return self.result(
      direct_type_edk = GenLambda(
        lambda gd: gd.type.edk.name
        ),
      indirect_param_edk = GenStr(""),
      decl_and_assign_cpp = decl_and_assign_cpp,
      indirect_assign_to_edk = GenStr(""),
      direct_return_edk = GenLambda(
        lambda gd: gd.conv_cpp_to_edk_decl() + "\n  return " + gd.name.edk + ";"
        ),
      )

  def result_direct_from_ptr(self):
    return self.result_direct(
      decl_and_assign_cpp = GenLambda(
        lambda gd: gd.type.cpp.name + " " + gd.name.cpp + " = *"
        )
      )

  def result_indirect(
    self,
    decl_and_assign_cpp = GenLambda(
      lambda gd: gd.type.cpp.name + " " + gd.name.cpp + " = "
      ),
    ):
    return self.result(
      direct_type_edk = GenStr("void"),
      indirect_param_edk = GenLambda(
        lambda gd: "Traits< " + gd.type.edk.name + " >::Result " + gd.name.edk
        ),
      decl_and_assign_cpp = decl_and_assign_cpp,
      indirect_assign_to_edk = GenLambda(
        lambda gd: gd.conv_cpp_to_edk()
        ),
      direct_return_edk = GenStr(""),
      )
 
  def result_indirect_from_ptr(self):
    return self.result_indirect(
      decl_and_assign_cpp = GenLambda(
        lambda gd: gd.type.cpp.name + " " + gd.name.cpp + " = *"
        )
      )

  # Recipes: param

  def param(
    self,
    kl = None,
    edk = None,
    edk_to_cpp_decl = GenLambda(
      lambda gd: gd.conv_edk_to_cpp_decl()
      ),
    cpp = None,
    cpp_to_edk = None,
    ):
    try:
      self.set_hook('gen_param_edk', self.make_gen(edk))
    except:
      self.raise_missing_or_invalid('edk')
    try:
      self.set_hook('gen_param_kl', self.make_gen(kl))
    except:
      self.raise_missing_or_invalid('kl')
    try:
      self.set_hook('gen_param_edk_to_cpp_decl', self.make_gen(edk_to_cpp_decl))
    except:
      self.raise_missing_or_invalid('edk_to_cpp_decl')
    try:
      self.set_hook('gen_param_cpp', self.make_gen(cpp))
    except:
      self.raise_missing_or_invalid('cpp')
    try:
      self.set_hook('gen_param_cpp_to_edk', self.make_gen(cpp_to_edk))
    except:
      self.raise_missing_or_invalid('cpp_to_edk')
    return self

  def param_in(
    self,
    cpp = GenLambda(
      lambda gd: gd.name.cpp
      )
    ):
    return self.param(
      kl = GenLambda(
        lambda gd: gd.type.kl.base + " " + gd.name.kl + gd.type.kl.suffix
        ),
      edk = GenLambda(
        lambda gd: "Traits< " + gd.type.edk.name + " >::INParam " + gd.name.edk
        ),
      cpp = cpp,
      cpp_to_edk = GenStr(""),
      )

  def param_in_to_ptr(self):
    return self.param_in(
      cpp = GenLambda(
        lambda gd: "&" + gd.name.cpp
        )
      )      

  def param_io(
    self,
    cpp = GenLambda(
      lambda gd: gd.name.cpp
      )
    ):
    return self.param(
      kl = GenLambda(
        lambda gd: "io " + gd.type.kl.base + " " + gd.name.kl + gd.type.kl.suffix
        ),
      edk = GenLambda(
        lambda gd: "Traits< " + gd.type.edk.name + " >::IOParam " + gd.name.edk
        ),
      cpp = cpp,
      cpp_to_edk = GenLambda(
        lambda gd: gd.conv_cpp_to_edk()
        ),
      )

  def param_io_to_ptr(self):
    return self.param_io(
      cpp = GenLambda(
        lambda gd: "&" + gd.name.cpp
        )
      )      
