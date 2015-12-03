def pass_edk_param_by_ref(cls):
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

def pass_edk_param_by_ptr(cls):
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
