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

    result_cpp_type_expr = namespace_mgr.resolve_cpp_type_expr(current_namespace_path, clang_instance_method.result_type.spelling)
    print "result_cpp_type_expr = %s" % str(result_cpp_type_expr)
    self.result = ResultCodec(
      type_mgr.get_dqti(result_cpp_type_expr)
      )

    is_mutable = not clang_instance_method.type.spelling.endswith('const')
    self.this = ThisCodec(this_type_info, is_mutable)

    self.params = []
    for child in clang_instance_method.get_children():
        if child.kind == CursorKind.PARM_DECL:
            param_cpp_type_expr = namespace_mgr.resolve_cpp_type_expr(current_namespace_path, child.type.spelling)
            self.params.append(ParamCodec(
              type_mgr.get_dqti(param_cpp_type_expr),
              child.spelling
              ))
