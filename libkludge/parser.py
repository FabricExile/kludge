#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

import jinja2, os, sys, optparse, json, re

import clang
from clang.cindex import AccessSpecifier, CursorKind, TypeKind

from kl2edk import KLStruct, Method, KLParam, TypesManager

import ast
from type_mgr import TypeMgr
from value_name import ValueName
from member import Member
from constructor import Constructor
from instance_method import InstanceMethod
from types import InPlaceStructSelector, WrappedPtrSelector
from param_codec import ParamCodec
from config import *
import clang_helpers
from namespace_mgr import NamespaceMgr
import cpp_type_expr_parser

class CPPType:
    def __init__(self, type_name, is_pointer, is_const):
        self.type_name = type_name
        self.is_pointer = is_pointer
        self.is_const = is_const


class CustomMapping:
    def __init__(self, cpp_type_name, is_pointer, kl_type_name):
        self.cpp_type_name = cpp_type_name
        self.is_pointer = is_pointer
        self.kl_type_name = kl_type_name


import abc


class KLTypeMapping:
    def __init__(self, kl_type_name, cpp_type_name):
        self.kl_type_name = kl_type_name
        self.cpp_type_name = cpp_type_name

class Parser:
    __metaclass__ = abc.ABCMeta

    basic_type_map = {
        TypeKind.INVALID: None,
        TypeKind.UNEXPOSED: None,
        TypeKind.VOID: None,
        TypeKind.BOOL: "Boolean",
        TypeKind.CHAR_U: "Byte",
        TypeKind.UCHAR: "Byte",
        TypeKind.CHAR16: "UInt16",
        TypeKind.CHAR32: "SInt32",
        TypeKind.USHORT: "UInt16",
        TypeKind.UINT: "UInt32",
        TypeKind.ULONG: "UInt32",
        TypeKind.ULONGLONG: "UInt64",
        TypeKind.UINT128: "UInt64",
        TypeKind.CHAR_S: "SInt8",
        TypeKind.SCHAR: "SInt8",
        TypeKind.WCHAR: "UInt16",
        TypeKind.SHORT: "SInt16",
        TypeKind.INT: "SInt32",
        TypeKind.LONG: "SInt32",
        TypeKind.LONGLONG: "SInt64",
        TypeKind.INT128: "SInt64",
        TypeKind.FLOAT: "Float32",
        TypeKind.DOUBLE: "Float64",
        TypeKind.LONGDOUBLE: "Float64",
        TypeKind.NULLPTR: None,
        TypeKind.OVERLOAD: None,
        TypeKind.DEPENDENT: None,
        TypeKind.OBJCID: None,
        TypeKind.OBJCCLASS: None,
        TypeKind.OBJCSEL: None,
        TypeKind.COMPLEX: None,
        TypeKind.POINTER: None,
        TypeKind.BLOCKPOINTER: None,
        TypeKind.LVALUEREFERENCE: None,
        TypeKind.RVALUEREFERENCE: None,
        TypeKind.RECORD: None,
        TypeKind.ENUM: None,
        TypeKind.TYPEDEF: None,
        TypeKind.OBJCINTERFACE: None,
        TypeKind.OBJCOBJECTPOINTER: None,
        TypeKind.FUNCTIONNOPROTO: None,
        TypeKind.FUNCTIONPROTO: None,
        TypeKind.CONSTANTARRAY: None,
        TypeKind.VECTOR: None,
        TypeKind.MEMBERPOINTER: None,
        TypeKind.INCOMPLETEARRAY: None,
    }

    def __init__(self):
        self.edk_decls = ast.DeclSet()
        self.existing_edk_symbol_names = set()

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

    def main(self):
        self.config = create_default_config()

        try:
            opt_parser = optparse.OptionParser(
                usage="""
%prog [options] <EXTNAME> [<input1.h> <input2.h> ...]
OR %prog -c <config file>""",
                description="KLUDGE: C++-to-KL wrap-o-matic",
                )
            opt_parser.add_option(
                '-c', '--config',
                action='store',
                default='',
                dest='config',
                metavar='CONFIG.json',
                help="load options from CONFIG.json in JSON format",
                )
            opt_parser.add_option(
                '-o', '--outdir',
                action='store',
                default=self.config['outdir'],
                dest='outdir',
                metavar='OUTDIR',
                help="output directory (defaults to %s)" % self.config['outdir'],
                )
            opt_parser.add_option(
                '-b', '--basename',
                action='store',
                default=self.config['basename'],
                dest='basename',
                metavar='BASENAME',
                help="output OUTDIR/BASENAME.{kl,cpp} (defaults to EXTNAME)",
                )
            opt_parser.add_option(
                '--clang_opt',
                action='append',
                dest='clang_opts',
                metavar='CLANGOPT',
                help="pass additional option to clang++ (can be used multiple times)",
                )
            (opts, args) = opt_parser.parse_args()
        except Exception as e:
            print "Error: %s" % str(e)
            print "Run '%s --help' for usage" % sys.argv[0]
            sys.exit(1)

        if opts.config:
            with open(opts.config) as fh:
                 self.config.update(json.load(fh))

        if len(args) > 0:
            self.config['extname'] = args[0]
            for i in range(1, len(args)):
                self.config['infiles'].append(args[i])

        if len(opts.basename) > 0:
            self.config['basename'] = opts.basename

        if opts.clang_opts:
            self.config["clang_opts"].extend(opts.clang_opts)

        if opts.outdir:
            self.config['outdir'] = opts.outdir

        if not self.config['extname']:
            print "Usage error: You must specify the extension name"
            print "Use --help for detailed usage information"
            return
        if not self.config['infiles']:
            print "Usage error: You must provide at least one input file"
            print "Use --help for detailed usage information"
            return
        if not self.config.get('basename'):
            self.config['basename'] = self.config['extname']

        print "Using configuration:"
        json.dump(
            self.config,
            sys.stdout,
            sort_keys=True,
            indent=2,
            separators=(',', ': '),
            )
        sys.stdout.write("\n")

        self.jinjenv = create_jinjenv(self.config)
        self.namespace_mgr = NamespaceMgr()
        self.type_mgr = TypeMgr(self.jinjenv)

        for infile in self.config['infiles']:
            self.parse(self.expand_envvars(infile))

        self.output(
            os.path.join(self.config['outdir'], self.config['basename'] + '.kl'),
            os.path.join(self.config['outdir'], self.config['basename'] + '.cpp'),
            )
        sconstruct_filename = os.path.join(self.config['outdir'], 'SConstruct')
        print "Writing %s" % sconstruct_filename
        with open(sconstruct_filename, "w") as fh:
            fh.write("""
#
# Copyright 2010-2015 Fabric Software Inc. All rights reserved.
#

import os, sys

extname = '%s'
basename = '%s'
cxxflags = ["-g", %s]
cpppath = [%s]
libpath = [%s]
libs = [%s]

try:
  fabricPath = os.environ['FABRIC_DIR']
except:
  print "You must set FABRIC_DIR in your environment."
  print "Refer to README.txt for more information."
  sys.exit(1)
SConscript(os.path.join(fabricPath, 'Samples', 'EDK', 'SConscript'))
Import('fabricBuildEnv')

fabricBuildEnv.Append(CPPPATH = ["../..", "."])
fabricBuildEnv.Append(CXXFLAGS = cxxflags)
fabricBuildEnv.Append(CPPPATH = cpppath)
fabricBuildEnv.Append(LIBPATH = libpath)
fabricBuildEnv.Append(LIBS = libs)

fabricBuildEnv.SharedLibrary(
  '-'.join([extname, fabricBuildEnv['FABRIC_BUILD_OS'], fabricBuildEnv['FABRIC_BUILD_ARCH']]),
  [basename + '.cpp']
  )
""" % (
    self.config['extname'],
    self.config['basename'],
    ", ".join(map(
        lambda opt: "'%s'" % self.expand_envvars(opt),
        self.config.get('clang_opts', [])
        )),
    ", ".join(map(
        lambda cppdir: "'%s'" % self.expand_envvars(cppdir),
        self.config.get('cpppath', [])
        )),
    ", ".join(map(
        lambda libdir: "'%s'" % self.expand_envvars(libdir),
        self.config.get('libpath', [])
        )),
    ", ".join(map(
        lambda libname: "'%s'" % libname,
        self.config.get('libs', [])
        )),
    ))
        fpmFilename = os.path.join(opts.outdir, self.config['extname']+'.fpm.json')
        print "Writing %s" % fpmFilename
        with open(fpmFilename, "w") as fh:
            fh.write("""
{
"libs": "%s",
"code": [
"actual.kl"
],
}
""" % self.config['extname'])

    # def get_kl_type(self, clang_type):
    #     canon_type = clang_type.get_canonical()
    #     base_name = canon_type.spelling
    #     if canon_type.is_const_qualified():
    #         base_name = base_name[len('const '):]
    #     kl_type = None
    #     is_array = False

    #     if canon_type.kind == TypeKind.LVALUEREFERENCE:
    #         kl_type = self.get_kl_type(canon_type.get_pointee())

    #     elif canon_type.kind == TypeKind.POINTER:
    #         if canon_type.get_pointee().kind == TypeKind.VOID:
    #             return "Data"
    #         if canon_type.get_pointee().kind in [TypeKind.CHAR_S,
    #                                              TypeKind.SCHAR]:
    #             return "String"
    #         kl_type = self.get_kl_type(canon_type.get_pointee())

    #     elif canon_type.kind == TypeKind.UNEXPOSED or canon_type.kind == TypeKind.RECORD:
    #         kl_type = base_name
    #         if kl_type.startswith('std::vector<'):
    #             is_array = True
    #             kl_type = kl_type[len('std::vector<'):kl_type.find(',')]
    #         if kl_type in self.cpp_type_to_kl_mappings:
    #             kl_type = self.cpp_type_to_kl_mappings[kl_type]

    #     elif canon_type.kind == TypeKind.TYPEDEF:
    #         kl_type = self.get_kl_type(canon_type.get_canonical())

    #     elif canon_type.kind == TypeKind.VOID:
    #         return None

    #     if not kl_type:
    #         kl_type = Parser.basic_type_map[canon_type.kind]

    #     if not kl_type:
    #         raise Exception('no KL type for ' + str(canon_type.spelling) + ' ('
    #                         + str(canon_type.kind) + ')')

    #     kl_type = self.get_kl_class_name(kl_type)

    #     if is_array:
    #         kl_type += '[]'

    #     return kl_type

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

    @staticmethod
    def get_nested_name(cursor):
        semantic_parent = cursor.semantic_parent
        if semantic_parent and semantic_parent.kind in [
            CursorKind.NAMESPACE,
            CursorKind.CLASS_DECL,
            CursorKind.STRUCT_DECL,
            ]:
            result = Parser.get_nested_name(semantic_parent)
            result.append(cursor.spelling)
        else:
            result = [cursor.spelling]
        return result

    @staticmethod
    def get_nested_type_name(clang_type):
        return Parser.get_nested_name(clang_type.get_declaration())

    @staticmethod
    def get_qualified_spelling(cursor, separator):
        semantic_parent = cursor.semantic_parent
        if semantic_parent:
            if semantic_parent.kind in [
                CursorKind.NAMESPACE,
                CursorKind.CLASS_DECL,
                CursorKind.STRUCT_DECL,
                ]:
                return Parser.get_qualified_spelling(semantic_parent, separator) + separator + cursor.spelling
        return cursor.spelling

    def dump_cursor(self, indent, cursor):
        print indent + str(cursor.kind) + " " + cursor.displayname
        print indent + str(cursor.location)
        childIndent = indent + "."
        for childCursor in cursor.get_children():
            self.dump_cursor(childIndent, childCursor)

    def parse_record_decl(
        self,
        include_filename,
        indent,
        current_namespace_path,
        cursor,
        ):
        # no children -> forward declaration
        if len(list(cursor.get_children())) < 1:
            print "%s-> no children" % indent
            return

        record_namespace_path = current_namespace_path + [cursor.displayname]
        try:
            cpp_type_expr = self.namespace_mgr.cpp_type_expr_parser.parse(cursor.displayname)
            print "%s%s %s" % (indent, str(cursor.kind), str(cpp_type_expr))

            self.namespace_mgr.add_type(current_namespace_path, cursor.displayname, cpp_type_expr)
            cpp_type_expr = self.namespace_mgr.resolve_cpp_type_expr(current_namespace_path, str(cpp_type_expr))
            self.namespace_mgr.add_nested_namespace(current_namespace_path, cursor.displayname)

            clang_members = []
            clang_instance_methods = []
            clang_constructors = []
            clang_base_classes = []
            type_is_pure_virtual = False
            type_has_vtable = False

            for child in cursor.get_children():
                if child.kind == CursorKind.TYPEDEF_DECL:
                    self.parse_TYPEDEF_DECL(
                        include_filename,
                        indent+"  ",
                        record_namespace_path,
                        child,
                        )
                    continue

                if child.kind == CursorKind.FIELD_DECL:
                    print "%s  FIELD_DECL %s" % (indent, child.displayname)
                    clang_members.append(child)
                    continue

                if child.access_specifier != AccessSpecifier.PUBLIC:
                    continue

                if child.kind == CursorKind.CXX_BASE_SPECIFIER:
                    clang_base_classes.append(child)
                elif child.kind == CursorKind.CXX_METHOD:
                    print "%s  CXX_METHOD %s" % (indent, child.displayname)
                    if clang.cindex.conf.lib.clang_CXXMethod_isVirtual(child):
                        type_has_vtable = True

                    if child.is_static_method():
                        print "%s    ->is static" % (indent)
                        self.parse_FUNCTION_DECL(include_filename, indent, record_namespace_path, child)
                    elif clang.cindex.conf.lib.clang_CXXMethod_isPureVirtual(child):
                        print "%s    ->is pure virtual" % (indent)
                        type_is_pure_virtual = True
                    elif child.spelling.startswith("operator"):
                        pass
                    else:
                        clang_instance_methods.append(child)
                    continue
                elif child.kind == CursorKind.CONSTRUCTOR:
                    print "%s  CONSTRUCTOR %s" % (indent, child.displayname)
                    clang_constructors.append(child)
                    continue

                    # result_type_info = self.type_mgr.get_type_info(child.result_type)
                    # print "result_type_info = " + str(result_type_info)

                    # is_const = child.type.spelling.endswith('const')
                    # print "this_cpp_type_name = " + child.type.spelling
                    # # this_type_info = self.type_mgr.get_type_info(

                    # if child.is_static_method():
                    #     continue

                    # if child.spelling in self.skip_methods:
                    #     self.print_skipping(
                    #         child.displayname,
                    #         "method is in skip list"
                    #         )
                    #     continue

                    # if self.abort_on_type(result_kl_type):
                    #     self.print_skipping(
                    #         child.displayname,
                    #         "result type '%s' is in abort list" % result_kl_type
                    #         )
                    #     continue

                    # this_usage = 'in'
                    # if not child.is_static_method():
                    #     if not child.kind == CursorKind.DESTRUCTOR and not child.kind == CursorKind.CONSTRUCTOR:
                    #         this_usage = 'in' if child.type.spelling.endswith(
                    #             'const') else 'io'
                    # method = Method(child.spelling, result_kl_type, this_usage,
                    #                 'public')
                    # method.codegen.cpp_qual_ret_type = self.get_cpp_qual_type_name(
                    #     child.result_type)
                    # method.codegen.cpp_base_ret_type = self.get_cpp_base_type_name(
                    #     child.result_type)

                    # if result_kl_type == 'Data':
                    #     continue

                    # operator = None
                    # if child.kind == CursorKind.DESTRUCTOR:
                    #     # destructor will be run by the KL destructor in C++
                    #     continue
                    # elif child.kind == CursorKind.CONSTRUCTOR:
                    #     if not include_constructors:
                    #         continue
                    #     method_name = child.spelling
                    #     method.codegen.is_constructor = True
                    #     num_params = 0
                    #     for p in child.get_children():
                    #         if p.kind == CursorKind.PARM_DECL:
                    #             num_params += 1
                    #     if num_params == 0:
                    #         kl_type.codegen.has_empty_constructor = True
                    # else:
                    #     if child.is_static_method():
                    #         method_name = kl_class_name + '_' + child.spelling
                    #         method.codegen.is_static = True
                    #         namespace = self.get_namespace(child)
                    #         if namespace:
                    #             namespace = '::'.join(namespace)
                    #         method.codegen.cpp_function = namespace
                    #     else:
                    #         if child.spelling.startswith('operator'):
                    #             operator = child.spelling[len('operator'):]
                    #             if operator not in ['<', '<=', '==', '!=', '>=',
                    #                                 '>']:
                    #                 self.print_skipping(
                    #                     child.displayname,
                    #                     "operator %s is unsupported" % operator
                    #                     )
                    #                 continue
                    #             method_name = operator
                    #             method.codegen.cpp_function = child.spelling
                    #         else:
                    #             method_name = kl_class_name + '.' + child.spelling
                    #             method.codegen.cpp_function = child.spelling

                    # method.codegen.kl_full_name = method_name

                    # i = 0
                    # skip = False
                    # for p in child.get_children():
                    #     if p.kind == CursorKind.PARM_DECL:
                    #         # has_default_value = False
                    #         # invalid_type = False
                    #         # try:
                    #         #     kl_type = self.get_kl_type(p.type)
                    #         # except Exception as _e:
                    #         #     invalid_type = True
                    #         # if invalid_type or self.abort_on_type(kl_type):
                    #         #     for pc in p.get_children():
                    #         #         # if it has a default value we'll try to go on from here
                    #         #         if pc.kind in [
                    #         #             CursorKind.UNEXPOSED_EXPR,
                    #         #             CursorKind.INTEGER_LITERAL,
                    #         #             CursorKind.FLOATING_LITERAL,
                    #         #             CursorKind.STRING_LITERAL,
                    #         #             CursorKind.CXX_BOOL_LITERAL_EXPR,
                    #         #             CursorKind.CXX_NULL_PTR_LITERAL_EXPR,
                    #         #             CursorKind.DECL_REF_EXPR
                    #         #         ]:
                    #         #             has_default_value = True
                    #         #             break
                    #         #     if has_default_value:
                    #         #         break
                    #         #     skip = True
                    #         #     break
                    #         name, kl_type, kl_usage = self.parse_clang_param(p)
                    #         param = KLParam(name, kl_type, kl_usage)
                    #         param.codegen.cpp_qual_type = kl_type.cpp_type_name
                    #         param.codegen.cpp_base_type = kl_type.cpp_type_name
                    #         method.params.append(param)
                    #         i += 1

                    # if skip:
                    #     self.print_skipping(
                    #         child.displayname,
                    #         "unsupported default value"
                    #         )
                    #     continue

                    # symbol_name = self.get_symbol_name(kl_class_name, method_name)
                    # method.symbol = symbol_name
                    # method.codegen.is_operator = operator

                    # kl_type.methods.append(method)

            can_in_place = True
            members = []
            for clang_member in clang_members:
                try:
                    member_cpp_type_expr = self.namespace_mgr.resolve_cpp_type_expr(record_namespace_path, clang_member.type)
                    member = Member(
                        self.type_mgr.get_dqti(member_cpp_type_expr),
                        clang_member.displayname,
                        clang_member.access_specifier == AccessSpecifier.PUBLIC,
                        )
                    if not member.can_in_place:
                        can_in_place = False
                    members.append(member)
                except Exception as e:
                    can_in_place = False
                    print "Warning: member at %s:%d" % (clang_member.location.file, clang_member.location.line)
                    print "  Reason: %s" % e

            # [andrew 20160517] FIXME disabling in-place until we can handle the vtable
            can_in_place = False

            if can_in_place:
                self.type_mgr.add_selector(
                    InPlaceStructSelector(
                        self.jinjenv,
                        record_namespace_path,
                        cpp_type_expr,
                        )
                    )
            else:
                self.type_mgr.add_selector(
                    WrappedPtrSelector(
                        self.jinjenv,
                        record_namespace_path,
                        cpp_type_expr,
                        )
                    )

            this_type_info = self.type_mgr.get_dqti(cpp_type_expr).type_info

            existing_method_edk_symbol_names = set()
            instance_methods = []
            for clang_instance_method in clang_instance_methods:
                try:
                    instance_method = InstanceMethod(
                        self.type_mgr,
                        self.namespace_mgr,
                        record_namespace_path,
                        this_type_info,
                        clang_instance_method,
                        )
                    if instance_method.edk_symbol_name in existing_method_edk_symbol_names:
                        raise Exception("instance method with name EDK symbol name already exists")
                    existing_method_edk_symbol_names.add(instance_method.edk_symbol_name)
                    instance_methods.append(instance_method)
                except Exception as e:
                    print "Warning: ignored method at %s:%d" % (clang_instance_method.location.file, clang_instance_method.location.line)
                    print "  Reason: %s" % e

            constructors = []
            if not type_is_pure_virtual:
                for clang_constructor in clang_constructors:
                    try:
                        constructor = Constructor(
                            self.type_mgr,
                            self.namespace_mgr,
                            record_namespace_path,
                            this_type_info,
                            clang_constructor,
                            )
                        if constructor.edk_symbol_name in existing_method_edk_symbol_names:
                            raise Exception("instance method with name EDK symbol name already exists")
                        existing_method_edk_symbol_names.add(constructor.edk_symbol_name)
                        constructors.append(constructor)
                    except Exception as e:
                        print "Warning: ignored constructor at %s:%d" % (clang_constructor.location.file, clang_constructor.location.line)
                        print "  Reason: %s" % e

            base_classes = []
            for clang_base_class in clang_base_classes:
                self.parse_record_decl(clang_base_class.location.file.name, indent,
                        current_namespace_path, clang_base_class)
                base_class_cpp_type_expr = self.namespace_mgr.resolve_cpp_type_expr(
                        current_namespace_path, clang_base_class.type)
                base_classes.append(self.type_mgr.get_dqti(base_class_cpp_type_expr))

            # [andrew 20160517] FIXME this would be fine with objects + interfaces but not structs
            if len(base_classes) > 1:
                raise Exception("type has more than one base class")

            if can_in_place:
                self.edk_decls.add(
                    ast.Wrapping(
                        self.config['extname'],
                        include_filename,
                        self.get_location(cursor.location),
                        cursor.displayname,
                        this_type_info,
                        members,
                        instance_methods,
                        constructors,
                        base_classes,
                        "ast/builtin/in_place_struct_decl",
                        )
                    )
            else:
                self.edk_decls.add(
                    ast.Wrapping(
                        self.config['extname'],
                        include_filename,
                        self.get_location(cursor.location),
                        cursor.displayname,
                        this_type_info,
                        members,
                        instance_methods,
                        constructors,
                        base_classes,
                        "ast/builtin/wrapped_ptr_decl",
                        )
                    )
        except Exception as e:
            print "Warning: ignored type at %s:%d" % (cursor.location.file, cursor.location.line)
            print "  Reason: %s" % e

    def parse_MACRO_INSTANTIATION(self, include_filename, indent, current_namespace_path, cursor):
        print dir(cursor)
        self.dump_cursor(indent, cursor)
        print indent + ".get_definition() ->"
        self.dump_cursor(indent + ' ', cursor.get_definition())

    def parse_TYPEDEF_DECL(self, include_filename, indent, current_namespace_path, cursor):
        new_cpp_type_name = cursor.type.spelling
        new_nested_name = current_namespace_path + [new_cpp_type_name]
        new_cpp_type_expr = cpp_type_expr_parser.Named("::".join(new_nested_name))
        old_cpp_type_name = cursor.underlying_typedef_type.spelling
        if old_cpp_type_name.startswith("struct "):
            old_cpp_type_name = old_cpp_type_name[7:]
        try:
            old_cpp_type_expr = self.namespace_mgr.resolve_cpp_type_expr(current_namespace_path, old_cpp_type_name)
            print "%sTYPEDEF_DECL %s -> %s" % (indent, str(new_cpp_type_expr), str(old_cpp_type_expr))
            self.namespace_mgr.add_type(current_namespace_path, new_cpp_type_name, new_cpp_type_expr)
            old_type_info = self.type_mgr.get_dqti(old_cpp_type_expr).type_info
            self.type_mgr.add_alias(new_cpp_type_expr, old_cpp_type_expr)
            self.edk_decls.add(
                ast.Alias(
                    self.config['extname'],
                    include_filename,
                    self.get_location(cursor.location),
                    cursor.displayname,
                    "_".join(new_nested_name),
                    old_type_info,
                    )
                )
        except Exception as e:
            print "Warning: ignored typedef at %s:%d" % (cursor.location.file, cursor.location.line)
            print "  Reason: %s" % e

    def parse_FUNCTION_DECL(self, include_filename, indent, current_namespace_path, cursor):
        nested_name = current_namespace_path + [cursor.spelling]
        print "%sFUNCTION_DECL %s" % (indent, "::".join(nested_name))

        try:
            param_index = 1
            params = []
            for param_cursor in cursor.get_children():
                if param_cursor.kind == CursorKind.PARM_DECL:
                    param_name = param_cursor.spelling
                    if len(param_name) == 0:
                        param_name = "_param_%u" % param_index
                    param_cpp_type_expr = self.namespace_mgr.resolve_cpp_type_expr(current_namespace_path, param_cursor.type)
                    params.append(ParamCodec(
                        self.type_mgr.get_dqti(param_cpp_type_expr),
                        param_name,
                        ))
                param_index += 1

            result_cpp_type_expr = self.namespace_mgr.resolve_cpp_type_expr(current_namespace_path, cursor.result_type)

            func = ast.Func(
                self.config['extname'],
                include_filename,
                self.get_location(cursor.location),
                cursor.displayname,
                nested_name,
                self.type_mgr.get_dqti(result_cpp_type_expr),
                params,
                )
            if func.edk_symbol_name in self.existing_edk_symbol_names:
                raise Exception("identical EDK symbol already exists")
            self.existing_edk_symbol_names.add(func.edk_symbol_name)
            self.edk_decls.add(func)
        except Exception as e:
            print "Warning: ignored function at %s:%d" % (cursor.location.file, cursor.location.line)
            print "  Reason: %s" % e

    ignored_cursor_kinds = [
        CursorKind.MACRO_DEFINITION,
        CursorKind.INCLUSION_DIRECTIVE,
        ]

    def parse_cursor(self, include_filename, indent, current_namespace_path, cursor):
        cursor_kind = cursor.kind
        if cursor_kind in Parser.ignored_cursor_kinds:
            pass
        elif cursor_kind == CursorKind.NAMESPACE:
            nested_namespace_name = cursor.spelling
            nested_namespace_path = self.namespace_mgr.add_nested_namespace(
                current_namespace_path,
                nested_namespace_name,
                )
            print "%sNAMESPACE %s" % (indent, "::".join(nested_namespace_path))
            self.parse_children(include_filename, indent + "  ", nested_namespace_path, cursor)
        elif cursor_kind == CursorKind.UNEXPOSED_DECL:
            self.parse_children(include_filename, indent, current_namespace_path, cursor)
        elif cursor_kind == CursorKind.MACRO_INSTANTIATION:
            self.parse_MACRO_INSTANTIATION(include_filename, indent, current_namespace_path, cursor)
        elif cursor_kind == CursorKind.TYPEDEF_DECL:
            self.parse_TYPEDEF_DECL(include_filename, indent, current_namespace_path, cursor)
        elif cursor_kind == CursorKind.CLASS_DECL or cursor_kind == CursorKind.STRUCT_DECL:
            self.parse_record_decl(include_filename, indent, current_namespace_path, cursor)
        elif cursor_kind == CursorKind.FUNCTION_DECL:
            self.parse_FUNCTION_DECL(include_filename, indent, current_namespace_path, cursor)
        elif cursor_kind == CursorKind.USING_DIRECTIVE:
            for child in cursor.get_children():
                if child.kind == CursorKind.NAMESPACE_REF:
                    self.namespace_mgr.add_using_namespace(current_namespace_path, child.spelling.split("::"))
        else:
            print "%sUnhandled %s at %s:%d" % (indent, cursor_kind, cursor.location.file, cursor.location.line)

    def parse_children(self, include_filename, childIndent, current_namespace_path, cursor):
        for childCursor in cursor.get_children():
            self.parse_cursor(include_filename, childIndent, current_namespace_path, childCursor)

    def parse(self, unit_filename):
        print "Parsing C++ source file: %s" % unit_filename

        clang_opts = self.config['clang_opts']
        cpppath = self.config.get('cpppath', [])
        for cppdir in cpppath:
            clang_opts.extend(["-I", self.expand_envvars(cppdir)])
        print "  using Clang opts: %s" % " ".join(clang_opts)

        clang_index = clang.cindex.Index.create()
        unit = clang_index.parse(
            unit_filename,
            # [andrew 20160517] FIXME this must be due to paths on my system
            clang_opts + ["-I", self.expand_envvars('${LLVM_PATH}/lib/clang/3.8.0/include')],
            None,
            clang.cindex.TranslationUnit.PARSE_SKIP_FUNCTION_BODIES,
            # clang.cindex.TranslationUnit.PARSE_DETAILED_PROCESSING_RECORD
            )

        skip = False
        for d in unit.diagnostics:
            skip = skip or not self.print_diag(d)

        if skip:
            print 'skipping unit: ' + unit.spelling
        else:
            for cursor in unit.cursor.get_children():
                if hasattr(cursor.location.file, 'name') and cursor.location.file.name != unit_filename:
                    continue
                self.parse_cursor(unit_filename, "", [], cursor)

    def jinja_stream(self, lang):
        return self.jinjenv.get_template("ast/builtin/template." + lang).stream(
            ext_name = self.config['extname'],
            gen_decl_streams = lambda: self.edk_decls.jinja_streams(self.jinjenv, lang),
            )
    
    def output(
        self,
        output_kl_filename,
        output_cpp_filename,
        ):
        # # prune types without full definitions
        # for kl_type_name in self.types_manager.types:
        #     kl_struct = self.types_manager.types[kl_type_name]
        #     methods = []
        #     for m in kl_struct.methods:
        #         remove = False
        #         for p in m.params:
        #             if not p.kl_type_name in self.known_types:
        #                 remove = True

        #         if m.ret_type_name and not m.ret_type_name.replace(
        #             '[]', '') in self.known_types:
        #             remove = True

        #         if not remove:
        #             methods.append(m)

        #     kl_struct.methods = methods

        print "Writing %s" % output_kl_filename
        self.jinja_stream('kl').dump(output_kl_filename)

        print "Writing %s" % output_cpp_filename
        self.jinja_stream('cpp').dump(output_cpp_filename)
