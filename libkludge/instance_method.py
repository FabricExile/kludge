import clang
from clang.cindex import CursorKind, TypeKind
from value_name import ValueName

class InstanceMethod:

  def __init__(
    self,
    type_mgr,
    clang_instance_method,
    ):
    self.name = clang_instance_method.spelling

    clang_result_type = clang_instance_method.result_type
    if clang_result_type and clang_result_type.kind != TypeKind.VOID:
      self.result_codec = type_mgr.get_type_info(clang_result_type.spelling).make_codec(ValueName("RESERVED_result"))
    else:
      self.result_codec = None

    self.params = []
    for child in clang_instance_method.get_children():
        if child.kind == CursorKind.PARM_DECL:
            self.params.append(
              type_mgr.get_type_info(child.type.spelling).make_codec(ValueName(child.spelling))
              )
