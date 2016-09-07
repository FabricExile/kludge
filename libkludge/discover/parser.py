#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

import os, sys, optparse, re, traceback
import clang
from clang.cindex import AccessSpecifier, CursorKind, TypeKind
from libkludge import util

class Parser(object):

  def __init__(self, name, opts):
    self.name = name
    self.opts = opts
  
  def error(self, string):
    util.error(self.opts, string)

  def warning(self, string):
    util.warning(self.opts, string)

  def info(self, string):
    util.info(self.opts, string)

  def debug(self, string):
    util.debug(self.opts, string)

  class Logger(object):

    def __init__(self, parser, indent=""):
      self.parser = parser
      self.indent = indent

    def error(self, string):
      self.parser.error(self.indent + string)

    def warning(self, string):
      self.parser.warning(self.indent + string)

    def info(self, string):
      self.parser.info(self.indent + string)

    def debug(self, string):
      self.parser.debug(self.indent + string)

    def indent(self):
      return Logger(self.parser, self.indent + " ")

  envvar_re = re.compile("\\${[A-Za-z_]+}")

  @classmethod
  def expand_envvars(cls, string_value):
    while True:
        match_object = cls.envvar_re.match(string_value)
        if not match_object:
            break
        try:
            envvar_name = string_value[match_object.start(0)+2:match_object.end(0)-1]
            envvar_value = os.environ[envvar_name]
        except Exception, e:
            raise Exception("Missing environment variable " + envvar_name)
        string_value = \
              string_value[:match_object.start(0)] \
            + envvar_value \
            + string_value[match_object.end(0):]
    return string_value

  @classmethod
  def escape_cxxflag(cls, string_value):
      return string_value.replace('"', '\\\\"')

  def process(self, filename):
    self.parse(self.expand_envvars(filename))

  @staticmethod
  def print_diag(diag):
      msg = 'compile '
      if diag.severity >= clang.cindex.Diagnostic.Fatal:
          msg += 'FATAL ERROR'
      elif diag.severity >= clang.cindex.Diagnostic.Error:
          msg += 'error'
      elif diag.severity >= clang.cindex.Diagnostic.Warning:
          msg += 'warning'
      elif diag.severity >= clang.cindex.Diagnostic.Note:
          msg += 'note'
      else:
          msg += 'diag'

      print msg + ': ' + diag.spelling + ' : ' + str(diag.location)
      for fix in diag.fixits:
          print '    ' + str(fix)

      if diag.severity >= clang.cindex.Diagnostic.Fatal:
          return False
      return True

  @staticmethod
  def get_location(clang_location):
      return "%s:%u" % (clang_location.file.name, clang_location.line)

    # @staticmethod
    # def get_nested_name(cursor):
    #     semantic_parent = cursor.semantic_parent
    #     if semantic_parent and semantic_parent.kind in [
    #         CursorKind.NAMESPACE,
    #         CursorKind.CLASS_DECL,
    #         CursorKind.CLASS_TEMPLATE,
    #         CursorKind.STRUCT_DECL,
    #         ]:
    #         result = Parser.get_nested_name(semantic_parent)
    #         result.append(cursor.spelling)
    #     else:
    #         result = [cursor.spelling]
    #     return result

    # @staticmethod
    # def get_nested_type_name(clang_type):
    #     return Parser.get_nested_name(clang_type.get_declaration())

    # @staticmethod
    # def get_qualified_spelling(cursor, separator):
    #     semantic_parent = cursor.semantic_parent
    #     if semantic_parent:
    #         if semantic_parent.kind in [
    #             CursorKind.NAMESPACE,
    #             CursorKind.CLASS_DECL,
    #             CursorKind.CLASS_TEMPLATE,
    #             CursorKind.STRUCT_DECL,
    #             ]:
    #             return Parser.get_qualified_spelling(semantic_parent, separator) + separator + cursor.spelling
    #     return cursor.spelling

  def dump_cursor(self, indent, cursor):
      print indent + str(cursor.kind) + " " + cursor.displayname
      print indent + "  " + str(cursor.location)
      if cursor.kind == CursorKind.TYPEDEF_DECL:
          print indent + "  underlying type: " + cursor.underlying_typedef_type.spelling
          declaration = cursor.underlying_typedef_type.get_declaration()
          if declaration:
              print indent + "    [declaration]"
              self.dump_cursor(indent + "    ", declaration)
      if cursor.kind == CursorKind.TYPE_REF \
          or cursor.kind == CursorKind.TEMPLATE_REF:
          referenced = cursor.referenced
          if referenced:
              print indent + "  [referenced]"
              self.dump_cursor(indent + "  ", referenced)
      childIndent = indent + "."
      for childCursor in cursor.get_children():
          self.dump_cursor(childIndent, childCursor)

    # def maybe_parse_dependent_record_decl(self, indent, decl, template_param_types = []):
    #     if decl.kind == TypeKind.LVALUEREFERENCE or decl.kind == TypeKind.POINTER:
    #         underlying_decl = decl.get_pointee()
    #     else:
    #         underlying_decl = decl
    #     underlying_decl_cursor = underlying_decl.get_declaration()

    #     if not self.should_parse_file(underlying_decl_cursor.location.file):
    #         return

    #     decl_namespace = self.get_cursor_namespace_path(underlying_decl_cursor)

    #     if underlying_decl_cursor.kind == CursorKind.CLASS_DECL or underlying_decl_cursor.kind == CursorKind.STRUCT_DECL:
    #         # FIXME [andrew 20160811] see tests/Templates/Template::takesTemplType() for an example of this
    #         if underlying_decl.spelling.count('<') > underlying_decl_cursor.spelling.count('<'):
    #             print 'WARNING: skipping templated type "'+str(underlying_decl.spelling)+ \
    #                 '" as "'+str(underlying_decl_cursor.spelling)+'"'
    #             return

    #         self.parse_record_decl(underlying_decl_cursor.location.file.name, indent, decl_namespace, underlying_decl_cursor, template_param_types)
    #     elif underlying_decl_cursor.kind == CursorKind.TYPEDEF_DECL:
    #         self.parse_TYPEDEF_DECL(underlying_decl_cursor.location.file.name, indent, decl_namespace, underlying_decl_cursor)

    # def get_cursor_namespace_path(self, cursor):
    #     namespace_path = []
    #     if cursor:
    #         current = cursor.semantic_parent
    #         while current and current.kind != CursorKind.TRANSLATION_UNIT:
    #             namespace_path = [current.spelling] + namespace_path
    #             current = current.semantic_parent
    #     return namespace_path

    # def resolve_maybe_templated_clang_type(self, current_namespace_path, type_name, template_param_type_map):
        # cpp_type_expr = self.namespace_mgr.resolve_cpp_type_expr(
        #         current_namespace_path, type_name)
        # undq_cpp_type_expr, _ = cpp_type_expr.get_undq_type_expr_and_dq()
        # resolved_type = template_param_type_map.get(
        #         str(undq_cpp_type_expr), None)
        # return resolved_type

    # def resolve_maybe_templated_cpp_expr(
    #     self,
    #     indent,
    #     current_namespace_path,
    #     clang_type,
    #     template_param_type_map,
    #     ): 
        # print "resolve_maybe_templated_cpp_expr clang_type=%s template_param_type_map=%s" % (clang_type, template_param_type_map)

        # result_type = clang_type

        # cpp_type_expr = self.namespace_mgr.resolve_cpp_type_expr(current_namespace_path, clang_type.spelling)
        # orig_cpp_type_expr = cpp_type_expr.__copy__()
        # undq_cpp_type_expr, _ = orig_cpp_type_expr.get_undq_type_expr_and_dq()
        # resolved_type = template_param_type_map.get(
        #         str(undq_cpp_type_expr), None)
        # if resolved_type:
        #     result_type = resolved_type
        #     cpp_type_expr = self.namespace_mgr.resolve_cpp_type_expr(
        #             current_namespace_path, result_type.spelling)
        #     cpp_type_expr = cpp_type_expr.get_as_dirqual(orig_cpp_type_expr)

        # self.maybe_parse_dependent_record_decl(indent, result_type, template_param_type_map)

        # return cpp_type_expr

    # def collect_params(self, indent, cursor, current_namespace_path, template_param_type_map):
        # params = []
        # param_configs = []
        # try:
        #     param_num = 0
        #     for child in cursor.get_children():
        #         if child.kind == CursorKind.PARM_DECL:
        #             has_default_value = False
        #             if child.type.kind != TypeKind.CONSTANTARRAY:
        #                 for pc in child.get_children():
        #                     if pc.kind in [
        #                         CursorKind.UNEXPOSED_EXPR,
        #                         CursorKind.INTEGER_LITERAL,
        #                         CursorKind.FLOATING_LITERAL,
        #                         CursorKind.STRING_LITERAL,
        #                         CursorKind.CXX_BOOL_LITERAL_EXPR,
        #                         CursorKind.CXX_NULL_PTR_LITERAL_EXPR,
        #                         CursorKind.DECL_REF_EXPR,
        #                         # bit of a hack but this could be e.g. "=1.0/6.0"
        #                         CursorKind.BINARY_OPERATOR
        #                         ]:
        #                         has_default_value = True
        #                         break

        #             param_cpp_type_expr = self.resolve_maybe_templated_cpp_expr(
        #                     indent, current_namespace_path, child.type,
        #                     template_param_type_map)

        #             param_name = child.spelling
        #             illegal_names = ['in', 'out', 'io']
        #             if not param_name or param_name in illegal_names:
        #                 param_name = 'arg'+str(param_num)
        #             param_num += 1

        #             if has_default_value:
        #                 param_configs.append(list(params))

        #             params.append(ParamCodec(
        #               self.type_mgr.get_dqti(param_cpp_type_expr),
        #               param_name
        #               ))
        #     param_configs.append(params)
        # except Exception as e:
        #     print "Warning: ignored one constructor for '%s' at %s:%d" % (
        #             cursor.spelling, cursor.location.file, cursor.location.line)
        #     print "  Reason: %s" % e

        # return param_configs

    # def collect_instance_methods(self, indent, clang_instance_methods, existing_method_edk_symbol_names,
    #         current_namespace_path, record_namespace_path, template_param_type_map, this_type_info, is_operator_arrow):
    #     pass
    #     # instance_methods = []
        # for clang_instance_method in clang_instance_methods:
        #     self.methods_seen += 1

        #     if clang_instance_method.spelling in self.config.get('ignore_methods', []):
        #         print "Ignoring method '%s' at %s:%d by user request" % (
        #                 clang_instance_method.spelling,
        #                 clang_instance_method.location.file,
        #                 clang_instance_method.location.line)
        #         continue
        #     try:
        #         param_configs = self.collect_params(indent+'  ', clang_instance_method,
        #                 current_namespace_path, template_param_type_map)

        #         result_type = clang_instance_method.result_type
        #         result_cpp_type_expr = self.resolve_maybe_templated_cpp_expr(
        #                 indent, record_namespace_path, result_type,
        #                 template_param_type_map)

        #         result_codec = ResultCodec(
        #           self.type_mgr.get_dqti(result_cpp_type_expr)
        #           )

        #         if clang_instance_method.spelling == "operator->":
        #             print "%s  FOUND operator->" % (indent)
        #             op_arrow_instance_methods = []
        #             result_cursor = self.resolve_maybe_templated_clang_type(current_namespace_path,
        #                     result_type.spelling, template_param_type_map)
        #             for c in result_cursor.get_declaration().get_children():
        #                 if c.kind == CursorKind.CXX_METHOD:
        #                     print "%s    operator->: CXX_METHOD %s" % (indent, c.displayname)
        #                     if c.access_specifier != AccessSpecifier.PUBLIC:
        #                         print "%s    %s ->is private" % (indent, c.displayname)
        #                         continue
        #                     elif c.is_static_method():
        #                         print "%s    %s ->is static" % (indent, c.displayname)
        #                         continue
        #                     else:
        #                         if clang.cindex.conf.lib.clang_CXXMethod_isPureVirtual(c):
        #                             print "%s    %s ->is pure virtual" % (indent, c.displayname)
        #                         op_arrow_instance_methods.append(c)

        #             instance_methods += self.collect_instance_methods(indent, op_arrow_instance_methods,
        #                     existing_method_edk_symbol_names, current_namespace_path,
        #                     record_namespace_path, template_param_type_map, this_type_info, True)
        #         elif clang_instance_method.spelling.startswith("operator"):
        #             # FIXME [andrew 20160812] add operator support
        #             print "%s    ->is operator" % (indent)
        #             continue
        #         else:
        #             for param_config in param_configs:
        #                 instance_method = InstanceMethod(
        #                     self.type_mgr,
        #                     self.namespace_mgr,
        #                     record_namespace_path,
        #                     this_type_info,
        #                     clang_instance_method,
        #                     result_codec,
        #                     param_config,
        #                     is_operator_arrow,
        #                     )
        #                 if instance_method.edk_symbol_name in existing_method_edk_symbol_names:
        #                     raise Exception("instance method with name EDK symbol name already exists")
        #                 existing_method_edk_symbol_names.add(instance_method.edk_symbol_name)
        #                 instance_methods.append(instance_method)

        #         self.methods_mapped += 1

        #     except Exception as e:
        #         print "Warning: ignored method '%s' at %s:%d" % (
        #                 clang_instance_method.spelling,
        #                 clang_instance_method.location.file,
        #                 clang_instance_method.location.line)
        #         print "  Reason: %s" % e

        # return instance_methods

  # def parse_record_decl(
      # self,
      # include_filename,
      # indent,
      # current_namespace_path,
      # cursor,
      # template_param_types = [],
      # cpp_specialized_type_name = None
      # ):
      # pass
    #     # print "---------------------------------------------------------------------"
    #     # traceback.print_stack(file=sys.stdout)
    #     # print "---------------------------------------------------------------------"
    #     # self.dump_cursor(indent + "  ", cursor)

    #     # if the ignore type is a template ignore anything derived from it
    #     if cursor.displayname.split('<')[0] in self.config.get('ignore_types', []):
    #         print "Ignoring RECORD_DECL '%s' at %s:%d by user request" % (
    #             cursor.displayname, cursor.location.file, cursor.location.line)
    #         return

    #     if len(list(cursor.get_children())) < 1:
    #         print "%s%s-> forward declaration" % (indent, cursor.displayname)
    #         return

    #     if not cpp_specialized_type_name:
    #         cpp_specialized_type_name = cursor.displayname
    #     print "parse_record_decl cpp_specialized_type_name=%s" % cpp_specialized_type_name

    #     record_namespace_path = current_namespace_path + [cpp_specialized_type_name]
    #     try:
    #         cpp_type_expr = self.namespace_mgr.cpp_type_expr_parser.parse(cpp_specialized_type_name)
    #         print "%sRECORD_DECL %s" % (indent, str(cpp_type_expr))

    #         self.namespace_mgr.add_type(current_namespace_path, str(cpp_type_expr), cpp_type_expr)
    #         cpp_type_expr = self.namespace_mgr.resolve_cpp_type_expr(current_namespace_path, str(cpp_type_expr))

    #         undq_cpp_type_expr, _ = cpp_type_expr.get_undq_type_expr_and_dq()
    #         if str(undq_cpp_type_expr) in self.parsed_cpp_types: 
    #             print "%s  -> skipping because type already exists" % indent
    #             return
    #         self.parsed_cpp_types[str(undq_cpp_type_expr)] = False

    #         self.records_seen += 1

    #         self.namespace_mgr.add_nested_namespace(current_namespace_path, cpp_specialized_type_name)

    #         clang_members = []
    #         clang_instance_methods = []
    #         clang_constructors = []
    #         has_default_constructor = False
    #         has_private_default_constructor = False
    #         block_empty_kl_constructor = False
    #         clang_base_classes = []
    #         clang_nested_types = []
    #         clang_static_functions = []
    #         is_abstract = cursor.is_abstract_type()
    #         if is_abstract:
    #             print "%s  -> is abstract" % (indent)
    #         no_copy_constructor = False
    #         has_vtable = False
    #         template_parameters = []

    #         for child in cursor.get_children():
    #             if child.kind == CursorKind.CONSTRUCTOR and \
    #                   child.access_specifier != AccessSpecifier.PUBLIC:
    #                 print "%s  private CONSTRUCTOR %s" % (indent, child.displayname)
    #                 has_private_default_constructor = True
    #                 if child.is_copy_constructor():
    #                     no_copy_constructor = True

    #             if child.access_specifier != AccessSpecifier.PUBLIC:
    #                 continue

    #             if child.kind == CursorKind.TYPEDEF_DECL:
    #                 self.parse_TYPEDEF_DECL(
    #                     include_filename,
    #                     indent+"  ",
    #                     record_namespace_path,
    #                     child,
    #                     )
    #                 continue
    #             elif child.kind == CursorKind.TEMPLATE_TYPE_PARAMETER:
    #                 print "%s  TEMPLATE_TYPE_PARAMETER %s" % (indent, child.displayname)
    #                 template_parameters.append(child)
    #                 continue
    #             elif child.kind == CursorKind.FIELD_DECL:
    #                 print "%s  FIELD_DECL %s" % (indent, child.displayname)
    #                 clang_members.append(child)
    #                 continue
    #             elif child.kind == CursorKind.CXX_BASE_SPECIFIER:
    #                 print "%s  CXX_BASE_SPECIFIER %s" % (indent, child.displayname)
    #                 clang_base_classes.append(child)
    #             elif child.kind == CursorKind.CXX_METHOD:
    #                 print "%s  CXX_METHOD %s" % (indent, child.displayname)
    #                 if clang.cindex.conf.lib.clang_CXXMethod_isVirtual(child):
    #                     has_vtable = True

    #                 if child.is_static_method():
    #                     print "%s    ->is static" % (indent)
    #                     clang_static_functions.append(child)
    #                 else:
    #                     if clang.cindex.conf.lib.clang_CXXMethod_isPureVirtual(child):
    #                         print "%s    ->is pure virtual" % (indent)
    #                     clang_instance_methods.append(child)
    #                 continue
    #             elif child.kind == CursorKind.CONSTRUCTOR:
    #                 print "%s  CONSTRUCTOR %s" % (indent, child.displayname)
    #                 clang_constructors.append(child)
    #                 continue
    #             elif child.kind == CursorKind.CLASS_DECL or child.kind == CursorKind.STRUCT_DECL:
    #                 print "%s  nested RECORD_DECL %s" % (indent, child.displayname)
    #                 clang_nested_types.append(child)
    #                 continue

    #         if len(template_parameters) > len(template_param_types):
    #             raise Exception("number of template parameters doesn't match expected number")

    #         template_param_type_map = {}
    #         for i in range(len(template_parameters)):
    #             template_param = template_parameters[i].type
    #             param_type = template_param_types[i]
    #             template_param_type_map[template_param.spelling] = param_type

    #         can_in_place = True
    #         members = []
    #         for clang_member in clang_members:
    #             try:
    #                 member_type = clang_member.type
    #                 for child in clang_member.get_children():
    #                     if child.kind == CursorKind.TYPE_REF:
    #                         child_def = child.get_definition()
    #                         if child_def and child_def.kind == CursorKind.TEMPLATE_TYPE_PARAMETER:
    #                             member_type = template_param_type_map[child.displayname]
    #                     elif child.kind == CursorKind.TEMPLATE_REF:
    #                         underlying_type = clang_member.type
    #                         num_template_args = underlying_type.get_num_template_arguments()
    #                         if num_template_args > 0:
    #                             self.resolve_template_specialization(indent, include_filename,
    #                                     current_namespace_path, underlying_type, clang_member)
    #                     elif child.kind == CursorKind.NAMESPACE_REF:
    #                         pass
    #                     else:
    #                         raise Exception("unexpected member child kind: "+str(child.kind))

    #                 member_cpp_type_expr = self.namespace_mgr.resolve_cpp_type_expr(record_namespace_path, member_type)
    #                 member = Member(
    #                     self.type_mgr.get_dqti(member_cpp_type_expr),
    #                     clang_member.displayname,
    #                     clang_member.access_specifier == AccessSpecifier.PUBLIC,
    #                     )
    #                 if not member.can_in_place:
    #                     can_in_place = False
    #                 members.append(member)
    #             except Exception as e:
    #                 can_in_place = False
    #                 print "Warning: member '%s' at %s:%d" % (
    #                         clang_member.displayname,
    #                         clang_member.location.file,
    #                         clang_member.location.line)
    #                 print "  Reason: %s" % e

    #         # [andrew 20160517] FIXME disabling in-place until we can handle the vtable
    #         can_in_place = False

    #         if str(cpp_type_expr) in self.config.get('no_copy_types', []):
    #             no_copy_constructor = True

    #         base_classes = []
    #         for clang_base_class in clang_base_classes:
    #             try:
    #                 underlying_type = clang_base_class.type
    #                 num_template_args = underlying_type.get_num_template_arguments()
    #                 if num_template_args > 0:
    #                     base_class_cpp_type_expr = self.resolve_template_specialization(indent, include_filename,
    #                             current_namespace_path, underlying_type, clang_base_class)
    #                 else:
    #                     type_def = clang_base_class.type
    #                     self.maybe_parse_dependent_record_decl(indent, type_def, template_param_type_map)
    #                     base_class_cpp_type_expr = self.namespace_mgr.resolve_cpp_type_expr(
    #                             current_namespace_path, type_def)
    #                 base_class_dqti = self.type_mgr.get_dqti(base_class_cpp_type_expr)
    #                 base_classes.append(base_class_dqti)
    #             except Exception as e:
    #                 print "Warning: ignoring base class '%s' at %s:%d" % (
    #                         clang_base_class.displayname,
    #                         clang_base_class.location.file,
    #                         clang_base_class.location.line)
    #                 print "  Reason: %s" % e

    #         # [andrew 20160517] FIXME this would be fine with objects + interfaces but not structs
    #         if len(base_classes) > 1:
    #             print 'WARNING: ignoring all but the first base class: "'+str(base_classes[0].type_info.get_desc())+'"'
    #             base_classes = [base_classes[0]]

    #         if can_in_place:
    #             self.type_mgr.add_selector(
    #                 InPlaceStructSelector(
    #                     self.jinjenv,
    #                     record_namespace_path,
    #                     cpp_type_expr,
    #                     )
    #                 )
    #         else:
    #             self.type_mgr.add_selector(
    #                 WrappedPtrSelector(
    #                     self.jinjenv,
    #                     std(cpp_type_expr),
    #                     record_namespace_path,
    #                     cpp_type_expr,
    #                     is_abstract,
    #                     no_copy_constructor,
    #                     )
    #                 )

    #         this_type_info = self.type_mgr.get_dqti(cpp_type_expr).type_info

    #         for nested_type in clang_nested_types:
    #             self.parse_record_decl(include_filename, indent+"  ", record_namespace_path,
    #                     nested_type)

    #         existing_method_edk_symbol_names = set()
    #         instance_methods = self.collect_instance_methods(indent, clang_instance_methods,
    #                 existing_method_edk_symbol_names, current_namespace_path,
    #                 record_namespace_path, template_param_type_map, this_type_info, False)

    #         if cursor.displayname.split('<')[0] in self.config.get('force_op_arrow', []):
    #             print "%s  -> forcing addition of templated type methods" % (indent)
    #             sub_type = template_param_types[0]
    #             op_arrow_instance_methods = []
    #             for c in sub_type.get_declaration().get_children():
    #                 if c.kind == CursorKind.CXX_METHOD:
    #                     print "%s    operator->: CXX_METHOD %s" % (indent, c.displayname)
    #                     if c.access_specifier != AccessSpecifier.PUBLIC:
    #                         print "%s    %s ->is private" % (indent, c.displayname)
    #                         continue
    #                     elif c.is_static_method():
    #                         print "%s    %s ->is static" % (indent, c.displayname)
    #                         continue
    #                     else:
    #                         if clang.cindex.conf.lib.clang_CXXMethod_isPureVirtual(c):
    #                             print "%s    %s ->is pure virtual" % (indent, c.displayname)
    #                         op_arrow_instance_methods.append(c)

    #             instance_methods += self.collect_instance_methods(indent, op_arrow_instance_methods,
    #                     existing_method_edk_symbol_names, current_namespace_path,
    #                     record_namespace_path, template_param_type_map, this_type_info, True)

    #         constructors = []
    #         if not is_abstract:
    #             for clang_constructor in clang_constructors:
    #                 try:
    #                     self.methods_seen += 1

    #                     param_configs = self.collect_params(indent+'  ', clang_constructor, current_namespace_path, template_param_type_map)

    #                     for param_config in param_configs:
    #                         constructor = Constructor(
    #                             self.type_mgr,
    #                             self.namespace_mgr,
    #                             record_namespace_path,
    #                             this_type_info,
    #                             clang_constructor.location,
    #                             cpp_specialized_type_name,
    #                             param_config,
    #                             )

    #                         if len(param_config) == 0:
    #                             has_default_constructor = True

    #                         if constructor.edk_symbol_name in existing_method_edk_symbol_names:
    #                             raise Exception("instance method with name EDK symbol name already exists")
    #                         existing_method_edk_symbol_names.add(constructor.edk_symbol_name)
    #                         constructors.append(constructor)

    #                     self.methods_mapped += 1

    #                 except Exception as e:
    #                     print "Warning: ignored constructor for '%s' at %s:%d" % (
    #                             cpp_specialized_type_name, clang_constructor.location.file,
    #                             clang_constructor.location.line)
    #                     print "  Reason: %s" % e

    #             if not has_default_constructor and len(clang_constructors) == 0 and not has_private_default_constructor:
    #                 print "%s  -> adding default constructor" % (indent)

    #                 try:
    #                     constructor = Constructor(
    #                         self.type_mgr,
    #                         self.namespace_mgr,
    #                         record_namespace_path,
    #                         this_type_info,
    #                         None,
    #                         cpp_specialized_type_name,
    #                         [],
    #                         )
    #                     if constructor.edk_symbol_name in existing_method_edk_symbol_names:
    #                         raise Exception("instance method with name EDK symbol name already exists")
    #                     existing_method_edk_symbol_names.add(constructor.edk_symbol_name)
    #                     constructors.append(constructor)
    #                 except Exception as e:
    #                     print "Warning: ignored manual default constructor"
    #                     print "  Reason: %s" % e

    #         # this type cannot be instantiated without parameters (or at all)
    #         if is_abstract or (not has_default_constructor and len(clang_constructors) > 0):
    #             print "%s  -> blocking default construction of type" % (indent)
    #             block_empty_kl_constructor = True

    #         if can_in_place:
    #             self.edk_decls.add(
    #                 ast.Wrapping(
    #                     self.config['extname'],
    #                     include_filename,
    #                     self.get_location(cursor.location),
    #                     cpp_specialized_type_name,
    #                     this_type_info,
    #                     members,
    #                     instance_methods,
    #                     constructors,
    #                     base_classes,
    #                     block_empty_kl_constructor,
    #                     "ast/builtin/in_place_struct_decl",
    #                     )
    #                 )
    #         else:
    #             self.edk_decls.add(
    #                 ast.Wrapping(
    #                     self.config['extname'],
    #                     include_filename,
    #                     self.get_location(cursor.location),
    #                     cpp_specialized_type_name,
    #                     this_type_info,
    #                     members,
    #                     instance_methods,
    #                     constructors,
    #                     base_classes,
    #                     block_empty_kl_constructor,
    #                     "ast/builtin/wrapped_ptr_type_decl",
    #                     "ast/builtin/wrapped_ptr_decl",
    #                     )
    #                 )

    #         for static_function in clang_static_functions:
    #             self.parse_FUNCTION_DECL(include_filename, indent,
    #                     record_namespace_path, static_function)

    #         self.records_mapped += 1
    #         self.parsed_cpp_types[str(undq_cpp_type_expr)] = True

    #     except Exception as e:
    #         print "Warning: ignored type '%s' at %s:%d" % (
    #                 cpp_specialized_type_name, cursor.location.file, cursor.location.line)
    #         print "  Reason: %s" % e

    # def parse_MACRO_INSTANTIATION(self, include_filename, indent, current_namespace_path, cursor):
    #     print dir(cursor)
    #     self.dump_cursor(indent, cursor)
    #     print indent + ".get_definition() ->"
    #     self.dump_cursor(indent + ' ', cursor.get_definition())

  def resolve_template_specialization(self, indent, include_filename, current_namespace_path, underlying_type, cursor):
      pass
        # template_class = None
        # template_args = []
        # for i in range(underlying_type.get_num_template_arguments()):
        #     template_args += [underlying_type.get_template_argument_as_type(i)]
        # for child in cursor.get_children():
        #     if child.kind == CursorKind.TEMPLATE_REF:
        #         if template_class:
        #             raise Exception("more than one TEMPLATE_REF found: "+str(child.displayname))
        #         template_class = child.get_definition()
        #     elif child.kind == CursorKind.TYPE_REF:
        #         pass
        #     elif child.kind == CursorKind.NAMESPACE_REF:
        #         pass
        #     else:
        #         raise Exception("unexpected child kind: "+str(child.kind))

        # if not template_class:
        #     raise Exception('template class not found')

        # specialized_name = underlying_type.spelling.split('<', 1)[0]
        # specialized_name += '<'
        # first = True
        # for arg in template_args:
        #     if not first:
        #         specialized_name += ', '
        #     first = False
        #     resolved_type = self.namespace_mgr.resolve_cpp_type_expr(current_namespace_path, arg.spelling)
        #     #if arg.kind == TypeKind.RECORD:
        #     #    specialized_name += '::'
        #     specialized_name += str(resolved_type)
        # specialized_name += '>'
        # template_namespace = self.get_cursor_namespace_path(template_class)
        # self.parse_record_decl(include_filename, indent, template_namespace, template_class, template_args, specialized_name)
        # return self.namespace_mgr.resolve_cpp_type_expr(current_namespace_path, specialized_name)

  def parse_TYPEDEF_DECL(self, include_filename, indent, current_namespace_path, cursor):
      pass
        # underlying_type = cursor.underlying_typedef_type
        # new_cpp_type_name = cursor.type.spelling
        # new_nested_name = current_namespace_path + [new_cpp_type_name]
        # new_cpp_type_expr = cpp_type_expr_parser.Named(new_nested_name)

        # if self.type_mgr.has_alias(new_cpp_type_expr):
        #     return

        # old_cpp_type_name = underlying_type.spelling
        # old_cpp_type_name = old_cpp_type_name.replace("struct ", "")
        # old_cpp_type_name = old_cpp_type_name.replace("class ", "")
        # try:
        #     old_cpp_type_expr = self.namespace_mgr.resolve_cpp_type_expr(current_namespace_path, old_cpp_type_name)
        #     print "%sTYPEDEF_DECL %s -> %s" % (indent, str(new_cpp_type_expr), str(old_cpp_type_expr))

        #     # check if we handle this type specially, like std::vector<>
        #     old_type_info = self.type_mgr.maybe_get_dqti(old_cpp_type_expr)
        #     if not old_type_info:
        #         num_template_args = underlying_type.get_num_template_arguments()
        #         if num_template_args > 0:
        #             old_cpp_type_expr = self.resolve_template_specialization(indent, include_filename,
        #                     current_namespace_path, underlying_type, cursor)
        #         else:
        #             self.maybe_parse_dependent_record_decl(indent, underlying_type)

        #     old_type_info = self.type_mgr.get_dqti(old_cpp_type_expr).type_info

        #     self.namespace_mgr.add_type(current_namespace_path, new_cpp_type_name, new_cpp_type_expr)
        #     self.type_mgr.add_alias(new_cpp_type_expr, old_cpp_type_expr)
        #     new_kl_type_name = "_".join(new_nested_name)
        #     new_kl_type_name = replace_invalid_chars(new_kl_type_name)
        #     self.edk_decls.add(
        #         ast.Alias(
        #             self.config['extname'],
        #             include_filename,
        #             self.get_location(cursor.location),
        #             cursor.displayname,
        #             new_kl_type_name,
        #             old_type_info,
        #             )
        #         )
        # except Exception as e:
        #     print "Warning: ignored typedef '%s' at %s:%d" % (
        #             new_cpp_type_name, cursor.location.file, cursor.location.line)
        #     print "  Reason: %s" % e
        #     print "  Traceback:"
        #     print "---------------------------------------------------------------------"
        #     traceback.print_exc(file=sys.stdout)
        #     print "---------------------------------------------------------------------"

  def parse_FUNCTION_DECL(self, include_filename, indent, current_namespace_path, cursor):
      pass
        # if self.queue_functions:
        #     self.queued_functions.append({
        #         'inc': include_filename,
        #         'ns': current_namespace_path,
        #         'cur': cursor
        #         })
        #     return

        # nested_name = current_namespace_path + [cursor.spelling]
        # cpp_function_name = "::".join(nested_name)
        # print "%sFUNCTION_DECL %s" % (indent, cpp_function_name)

        # func_name_and_loc = ':'.join([cursor.spelling, str(cursor.location.file), str(cursor.location.line)])
        # if func_name_and_loc in self.parsed_cpp_functions: 
        #     print "%s  -> skipping because function already exists" % indent
        #     return
        # self.parsed_cpp_functions[func_name_and_loc] = False

        # self.functions_seen += 1

        # if cursor.spelling in self.config.get('ignore_functions', []):
        #     print "Ignoring function '%s' at %s:%d by user request" % (
        #             cursor.spelling,
        #             cursor.location.file,
        #             cursor.location.line)
        #     return

        # try:
        #     if cursor.spelling.startswith("operator"):
        #         # FIXME [andrew 20160812] add operator support
        #         raise Exception("function is operator")

        #     param_configs = self.collect_params(indent+'  ', cursor,
        #             current_namespace_path, {})

        #     result_cpp_type_expr = self.namespace_mgr.resolve_cpp_type_expr(current_namespace_path, cursor.result_type)

        #     for param_config in param_configs:
        #         func = ast.Func(
        #             self.config['extname'],
        #             include_filename,
        #             self.get_location(cursor.location),
        #             cursor.displayname,
        #             nested_name,
        #             self.type_mgr.get_dqti(result_cpp_type_expr),
        #             param_config,
        #             )
        #         if func.edk_symbol_name in self.existing_edk_symbol_names:
        #             raise Exception("identical EDK symbol already exists")
        #         self.existing_edk_symbol_names.add(func.edk_symbol_name)
        #         self.edk_decls.add(func)

        #     self.functions_mapped += 1
        #     self.parsed_cpp_functions[func_name_and_loc] = True

        # except Exception as e:
        #     print "Warning: ignored function '%s' at %s:%d" % (
        #             cursor.spelling, cursor.location.file, cursor.location.line)
        #     print "  Reason: %s" % e

  ignored_cursor_kinds = [
      CursorKind.MACRO_DEFINITION,
      CursorKind.INCLUSION_DIRECTIVE,
      ]

  def parse_cursor(self, logger, cursor):
      cursor_kind = cursor.kind
      logger.debug("AST: %s %s %s" % (str(cursor_kind), cursor.displayname, str(cursor.location)))
      if cursor_kind in Parser.ignored_cursor_kinds:
          pass
      # elif cursor_kind == CursorKind.NAMESPACE:
      #     nested_namespace_name = cursor.spelling
      #     nested_namespace_path = self.namespace_mgr.add_nested_namespace(
      #         current_namespace_path,
      #         nested_namespace_name,
      #         )
      #     print "%sNAMESPACE %s" % (indent, "::".join(nested_namespace_path))
      #     self.parse_children(include_filename, indent + "  ", nested_namespace_path, cursor)
      # elif cursor_kind == CursorKind.NAMESPACE_ALIAS:
      #     ns_alias_path = current_namespace_path + [cursor.displayname]
      #     ns_path = []
      #     for path in cursor.get_children():
      #         ns_path += [path.displayname]
      #     self.namespace_mgr.add_namespace_alias(ns_alias_path, ns_path)
      # elif cursor_kind == CursorKind.UNEXPOSED_DECL:
      #     self.parse_children(include_filename, indent, current_namespace_path, cursor)
      # elif cursor_kind == CursorKind.MACRO_INSTANTIATION:
      #     self.parse_MACRO_INSTANTIATION(include_filename, indent, current_namespace_path, cursor)
      # elif cursor_kind == CursorKind.TYPEDEF_DECL:
      #     self.parse_TYPEDEF_DECL(include_filename, indent, current_namespace_path, cursor)
      # elif cursor_kind == CursorKind.CLASS_DECL or cursor_kind == CursorKind.STRUCT_DECL:
      #     self.parse_record_decl(include_filename, indent, current_namespace_path, cursor)
      # elif cursor_kind == CursorKind.CLASS_TEMPLATE:
      #     # [andrew 20160519] ignore the template itself, only deal with specializations
      #     pass
      # elif cursor_kind == CursorKind.FUNCTION_DECL:
      #     self.parse_FUNCTION_DECL(include_filename, indent, current_namespace_path, cursor)
      # elif cursor_kind == CursorKind.USING_DIRECTIVE:
      #     for child in cursor.get_children():
      #         if child.kind == CursorKind.NAMESPACE_REF:
      #             self.namespace_mgr.add_using_namespace(current_namespace_path, child.spelling.split("::"))
      # else:
      #     print "%sUnhandled %s at %s:%d" % (indent, cursor_kind, cursor.location.file, cursor.location.line)

  def parse_children(self, include_filename, childIndent, current_namespace_path, cursor):
      for childCursor in cursor.get_children():
          self.parse_cursor(include_filename, childIndent, current_namespace_path, childCursor)

  def parse(self, filename):
    logger = self.Logger(self)

    logger.info("Parsing '%s'" % filename)

    clang_opts = ['-x', 'c++']
    if self.opts.clang_opts:
      clang_opts.extend(self.opts.clang_opts)
    if self.opts.cpppath:
      for cppdir in self.opts.cpppath:
          clang_opts.extend(["-I", self.expand_envvars(cppdir)])
    if self.opts.cppdefines:
      for cppdefine in self.opts.cppdefines:
          clang_opts.extend(["-D", self.expand_envvars(cppdefine)])
    logger.info("  using Clang opts: %s" % " ".join(clang_opts))

    clang_index = clang.cindex.Index.create()
    unit = clang_index.parse(
        filename,
        [
            "-isystem", self.expand_envvars('${KLUDGE_LLVM_ROOT}/include/c++/v1'),
            "-isystem", self.expand_envvars('${KLUDGE_LLVM_ROOT}/lib/clang/3.9.0/include'),
            ] + clang_opts,
        None,
        clang.cindex.TranslationUnit.PARSE_SKIP_FUNCTION_BODIES,
        # clang.cindex.TranslationUnit.PARSE_DETAILED_PROCESSING_RECORD
        )

    skip = False
    for d in unit.diagnostics:
        skip = skip or not self.print_diag(d)

    if skip:
        logger.error("Fatal errors encountered; aborting")
        return 0

    for cursor in unit.cursor.get_children():
        if hasattr(cursor.location.file, 'name') \
          and cursor.location.file.name != filename:
          continue
        self.parse_cursor(logger, cursor)
