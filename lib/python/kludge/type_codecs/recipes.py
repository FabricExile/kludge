from kludge import CPPTypeExpr
from kludge import SimpleTypeName

def match_cpp_expr_types(cpp_expr_types_to_match, type_name):
  def deco(cls):
    def impl(cls, cpp_type_expr, type_mgr):
      for cpp_expr_type_to_match in cpp_expr_types_to_match:
        if cpp_type_expr == cpp_expr_type_to_match:
          return cls(type_name)          
    setattr(cls, 'maybe_get_type_codec', classmethod(impl))
    return cls
  return deco

def match_cpp_expr_type(cpp_expr_type_to_match, type_name):
  return match_cpp_expr_types([cpp_expr_type_to_match], type_name)

def match_value_by_dict(lookup):
  def deco(cls):
    def impl(cls, cpp_type_expr, type_mgr):
      if isinstance(cpp_type_expr, CPPTypeExpr.Direct):
        kl_type_name = lookup.get(cpp_type_expr.get_unqualified_desc())
        if kl_type_name:
          return cls(SimpleTypeName(kl_type_name, str(cpp_type_expr)))
    setattr(cls, 'maybe_get_type_codec', classmethod(impl))
    return cls
  return deco

def match_const_ref_by_dict(lookup):
  def deco(cls):
    def impl(cls, cpp_type_expr, type_mgr):
      if isinstance(cpp_type_expr, CPPTypeExpr.ReferenceTo) \
        and cpp_type_expr.pointee.is_const \
        and isinstance(cpp_type_expr.pointee, CPPTypeExpr.Direct):
        kl_type_name = lookup.get(cpp_type_expr.pointee.get_unqualified_desc())
        if kl_type_name:
          return cls(SimpleTypeName(kl_type_name, str(cpp_type_expr)))
    setattr(cls, 'maybe_get_type_codec', classmethod(impl))
    return cls
  return deco

def match_const_ptr_by_dict(lookup):
  def deco(cls):
    def impl(cls, cpp_type_expr, type_mgr):
      if isinstance(cpp_type_expr, CPPTypeExpr.PointerTo) \
        and cpp_type_expr.pointee.is_const \
        and isinstance(cpp_type_expr.pointee, CPPTypeExpr.Direct):
        kl_type_name = lookup.get(cpp_type_expr.pointee.get_unqualified_desc())
        if kl_type_name:
          return cls(SimpleTypeName(kl_type_name, str(cpp_type_expr)))
    setattr(cls, 'maybe_get_type_codec', classmethod(impl))
    return cls
  return deco

def match_mutable_ref_by_dict(lookup):
  def deco(cls):
    def impl(cls, cpp_type_expr, type_mgr):
      if isinstance(cpp_type_expr, CPPTypeExpr.ReferenceTo) \
        and cpp_type_expr.pointee.is_mutable \
        and isinstance(cpp_type_expr.pointee, CPPTypeExpr.Direct):
        kl_type_name = lookup.get(cpp_type_expr.pointee.get_unqualified_desc())
        if kl_type_name:
          return cls(SimpleTypeName(kl_type_name, str(cpp_type_expr)))

    setattr(cls, 'maybe_get_type_codec', classmethod(impl))
    return cls
  return deco

def match_mutable_ptr_by_dict(lookup):
  def deco(cls):
    def impl(cls, cpp_type_expr, type_mgr):
      if isinstance(cpp_type_expr, CPPTypeExpr.PointerTo) \
        and cpp_type_expr.pointee.is_mutable \
        and isinstance(cpp_type_expr.pointee, CPPTypeExpr.Direct):
        kl_type_name = lookup.get(cpp_type_expr.pointee.get_unqualified_desc())
        if kl_type_name:
          return cls(SimpleTypeName(kl_type_name, str(cpp_type_expr)))
    setattr(cls, 'maybe_get_type_codec', classmethod(impl))
    return cls
  return deco

def in_param():
  def deco(cls):
    setattr(
      cls,
      'gen_kl_param',
      lambda self, kl_name: self.gen_kl_in_param(kl_name)
      )
    setattr(
      cls,
      'gen_edk_param',
      lambda self, edk_name: self.gen_edk_in_param(edk_name)
      )
    return cls
  return deco

def io_param():
  def deco(cls):
    setattr(
      cls,
      'gen_kl_param',
      lambda self, kl_name: self.gen_kl_io_param(kl_name)
      )
    setattr(
      cls,
      'gen_edk_param',
      lambda self, edk_name: self.gen_edk_io_param(edk_name)
      )
    return cls
  return deco

def direct_result(cls):

  setattr(
    cls,
    'gen_direct_result_edk_type',
    lambda self: self.type_name.kl.compound
    )

  setattr(
    cls,
    'gen_indirect_result_edk_param',
    lambda self: ""
    )

  setattr(
    cls,
    'gen_edk_store_result_pre',
    lambda self: self.type_name.edk + " _KLUDGE_EDK_RESERVED_result = "
    )

  setattr(
    cls,
    'gen_edk_store_result_post',
    lambda self: ""
    )

  setattr(
    cls,
    'gen_edk_return_dir_result',
    lambda self: "return _KLUDGE_EDK_RESERVED_result;"
    )

  return cls

def direct_result_by_deref(cls):

  cls = direct_result(cls)

  setattr(
    cls,
    'gen_edk_store_result_pre',
    lambda self: self.type_name.edk + " _KLUDGE_EDK_RESERVED_result = *"
    )

  return cls

indirect_result_edk_name = "_KLUDGE_EDK_RESERVED_result"

def indirect_result(
  pre = lambda edk_name: edk_name + " = ",
  post = lambda edk_name: "",
  ):
  def deco(cls):
    setattr(
      cls,
      'gen_direct_result_edk_type',
      lambda self: "void"
      )
    setattr(
      cls,
      'gen_indirect_result_edk_param',
      lambda self: "Traits< " + self.type_name.edk + " >::Result _KLUDGE_EDK_RESERVED_result"
      )
    setattr(
      cls,
      'gen_edk_store_result_pre',
      lambda self: pre(indirect_result_edk_name)
      )
    setattr(
      cls,
      'gen_edk_store_result_post',
      lambda self: post(indirect_result_edk_name)
      )
    setattr(
      cls,
      'gen_edk_return_dir_result',
      lambda self: ""
      )
    return cls
  return deco

def cpp_arg_is_edk_param(filter):
  def deco(cls):
    setattr(
      cls,
      'gen_edk_param_to_cpp_arg',
      lambda self, param_name: ""
      )
    setattr(
      cls,
      'gen_cpp_arg',
      lambda self, param_name: filter(param_name.edk)
      )
    setattr(
      cls,
      'gen_cpp_arg_to_edk_param',
      lambda self, param_name: ""
      )
    return cls
  return deco

def cpp_arg_is_edk_param_ref(cls):

  setattr(
    cls,
    'gen_edk_param_to_cpp_arg',
    lambda self, param_name: ""
    )

  setattr(
    cls,
    'gen_cpp_arg',
    lambda self, param_name: param_name.edk
    )

  setattr(
    cls,
    'gen_cpp_arg_to_edk_param',
    lambda self, param_name: ""
    )

  return cls

def cpp_arg_is_edk_param_ptr(cls):
  setattr(
    cls,
    'gen_edk_param_to_cpp_arg',
    lambda self, param_name: ""
    )
  setattr(
    cls,
    'gen_cpp_arg',
    lambda self, param_name: "&" + param_name.edk
    )
  setattr(
    cls,
    'gen_cpp_arg_to_edk_param',
    lambda self, param_name: ""
    )
  return cls
