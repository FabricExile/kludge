def in_param(cls):

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

def io_param(cls):

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
    lambda self: self.type_name.edk + " _KLUDGE_CPP_RESERVED_result = "
    )

  setattr(
    cls,
    'gen_edk_store_result_post',
    lambda self: ""
    )

  setattr(
    cls,
    'gen_edk_return_dir_result',
    lambda self: "return _KLUDGE_CPP_RESERVED_result;"
    )

  return cls

def direct_result_by_deref(cls):

  cls = direct_result(cls)

  setattr(
    cls,
    'gen_edk_store_result_pre',
    lambda self: self.type_name.edk + " _KLUDGE_CPP_RESERVED_result = *"
    )

  return cls

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
