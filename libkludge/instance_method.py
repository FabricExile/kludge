import clang
from clang.cindex import CursorKind, TypeKind
from value_name import ValueName
from result_codec import ResultCodec
from this_codec import ThisCodec
from param_codec import ParamCodec

class InstanceMethod:

  def __init__(
    self,
    type_mgr,
    namespace_mgr,
    current_namespace_path,
    this_type_info,
    clang_instance_method,
    ):
    self.name = clang_instance_method.spelling

    nested_result_type_name = namespace_mgr.get_nested_type_name(current_namespace_path, clang_instance_method.result_type.spelling)
    self.result = ResultCodec(
      type_mgr.get_dqti(nested_result_type_name)
      )

    is_mutable = not clang_instance_method.type.spelling.endswith('const')
    self.this = ThisCodec(this_type_info, is_mutable)

    self.params = []
    for child in clang_instance_method.get_children():
        if child.kind == CursorKind.PARM_DECL:
            nested_param_type_name = namespace_mgr.get_nested_type_name(current_namespace_path, child.type.spelling)
            self.params.append(ParamCodec(
              type_mgr.get_dqti(nested_param_type_name),
              child.spelling
              ))
