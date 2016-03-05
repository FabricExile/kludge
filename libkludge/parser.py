import jinja2, os, sys, optparse

import clang
from clang.cindex import AccessSpecifier, CursorKind, TypeKind

from kl2edk import KLStruct, Method, KLParam, TypesManager

import clang_wrapper
import ast
from gen_spec import GenSpec
from type_mgr import TypeMgr
from value_name import ValueName
from member import Member
from codecs import build_wrapped_ptr_codecs, build_in_place_struct_codecs

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
        self.clang_args = [
            '-x',
            'c++',
        ]

        self.classes = {}
        self.symbol_names = set()

        self.wrapper_templates = {}
        self.kl_type_mappings = {
            'float': KLTypeMapping('Float32', 'float'),
            }
        self.skip_methods = []
        self.cpp_ext_header_pre = ""
        self.cpp_ext_header_post = ""
    	self.cpp_enter = ""
        self.cpp_leave = ""

        self.known_types = set(['Data', 'String'])
        for t in Parser.basic_type_map:
            self.known_types.add(Parser.basic_type_map[t])

        self.jinjenv = jinja2.Environment(
            trim_blocks=True,
            lstrip_blocks=True,
            loader=jinja2.PackageLoader('__main__', 'templates'),
            undefined = jinja2.StrictUndefined,
            )
        GenSpec.jinjenv = self.jinjenv
        self.type_mgr = TypeMgr()
        self.edk_decls = ast.DeclSet()

    def init(self, ext_name, clang_opts):
        self.ext_name = ext_name
        self.types_manager = TypesManager(ext_name)
        self.clang_args.extend(clang_opts)

    def main(self):
        try:
            opt_parser = optparse.OptionParser(
                usage="%prog [options] <EXTNAME> <input.h> [<input2.h> ...]",
                description="KLUDGE: C++-to-KL wrap-o-matic",
                )
            opt_parser.add_option(
                '-o', '--outdir',
                action='store',
                default='.',
                dest='outdir',
                metavar='OUTDIR',
                help="output directory",
                )
            opt_parser.add_option(
                '-b', '--basename',
                action='store',
                default='',
                dest='basename',
                metavar='BASENAME',
                help="output OUTDIR/BASENAME.{kl,cpp} (defaults to EXTNAME)",
                )
            opt_parser.add_option(
                '-p', '--pass',
                action='append',
                dest='clang_opts',
                metavar='CLANGOPT',
                help="pass option to clang++ (can be used multiple times)",
                )
            (opts, args) = opt_parser.parse_args()
            if len(args) < 2:
                raise Exception("At least one input file is required")
        except Exception as e:
            print "Error: %s" % str(e)
            print "Run '%s --help' for usage" % sys.argv[0]
            sys.exit(1)

        extname = args[0]
        if len(opts.basename) > 0:
            basename = opts.basename
        else:
            basename = extname

        if not opts.clang_opts:
            opts.clang_opts = []

        self.init(extname, opts.clang_opts)
        for i in range(1, len(args)):
            self.parse(args[i])
        self.output(
            os.path.join(opts.outdir, basename + '.kl'),
            os.path.join(opts.outdir, basename + '.cpp'),
            )
        with open(os.path.join(opts.outdir, 'SConstruct'), "w") as fh:
            fh.write("""
#
# Copyright 2010-2015 Fabric Software Inc. All rights reserved.
#

import os, sys

extname = '%s'
basename = '%s'

try:
  fabricPath = os.environ['FABRIC_DIR']
except:
  print "You must set FABRIC_DIR in your environment."
  print "Refer to README.txt for more information."
  sys.exit(1)
SConscript(os.path.join(fabricPath, 'Samples', 'EDK', 'SConscript'))
Import('fabricBuildEnv')

fabricBuildEnv.Append(CPPPATH = ["../.."])
fabricBuildEnv.Append(CXXFLAGS = ["-g"])

fabricBuildEnv.SharedLibrary(
  '-'.join([extname, fabricBuildEnv['FABRIC_BUILD_OS'], fabricBuildEnv['FABRIC_BUILD_ARCH']]),
  [basename + '.cpp']
  )
""" % (extname, basename))
        with open(os.path.join(opts.outdir, extname+'.fpm.json'), "w") as fh:
            fh.write("""
{
"libs": "%s",
"code": [
"actual.kl"
],
}
""" % extname)

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

    def abort_on_type(self, kl_type):
        if not kl_type:
            return False
        if '<' in kl_type and kl_type.find('std::vector<') == -1:
            return True
        if '::' in kl_type:
            return True
        if 'const ' in kl_type:
            return True
        if 'type-parameter-' in kl_type:
            return True
        if kl_type.find('[]') != -1:
            return self.abort_on_type(kl_type.replace('[]', ''))
        return False

    @staticmethod
    def is_pointer_type(clang_type):
        canon_type = clang_type.get_canonical()
        if canon_type.kind in [TypeKind.LVALUEREFERENCE, TypeKind.POINTER]:
            return True
        return False

    @staticmethod
    def is_io_param(clang_type):
        canon_type = clang_type.get_canonical()
        #if canon_type.kind in [TypeKind.LVALUEREFERENCE, TypeKind.POINTER]:
        if canon_type.kind in [TypeKind.POINTER]:
            if canon_type.is_const_qualified():
                return False
            return True
        return False

    @staticmethod
    def get_cpp_qual_type_name(clang_type):
        return clang_type.get_canonical().spelling

    def get_cpp_base_type_name(self, clang_type):
        canon_type = clang_type.get_canonical()

        if canon_type.kind == TypeKind.LVALUEREFERENCE:
            return self.get_cpp_base_type_name(canon_type.get_pointee())

        base_name = canon_type.spelling
        if canon_type.is_const_qualified():
            base_name = base_name[len('const '):]
        return base_name

    @staticmethod
    def debug_print(cursor, prefix=''):
        print prefix + str(cursor.kind) + ': ' + str(cursor.spelling)
        for c in cursor.get_children():
            Parser.debug_print(c, prefix + '  ')

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
        return result;

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
            
    def output_class(self, class_name, parent_name, fh):
        fh.write('struct %s' % class_name)
        if parent_name:
            fh.write(' : ' + parent_name)
        fh.write('\n{\n')
        if not parent_name:
            fh.write('  private Data handle;\n')
        fh.write('};\n\n')

    def get_symbol_name(self, kl_class_name, method_name):
        if method_name == '<':
            method_name = kl_class_name + '__lt'
        elif method_name == '<=':
            method_name = kl_class_name + '__le'
        elif method_name == '==':
            method_name = kl_class_name + '__eq'
        elif method_name == '!=':
            method_name = kl_class_name + '__ne'
        elif method_name == '>=':
            method_name = kl_class_name + '__ge'
        elif method_name == '>':
            method_name = kl_class_name + '__gt'
        symbol_name = self.ext_name + '_' + method_name.replace('.', '_')
        if symbol_name in self.symbol_names:
            try_name = symbol_name
            i = 0
            while try_name in self.symbol_names:
                try_name = symbol_name + str(i)
                i += 1
            symbol_name = try_name
        self.symbol_names.add(symbol_name)
        return symbol_name

    def output_method(
        self, class_name, rval_type, method_name, params,
        symbol_name, this_usage,
        fh,
        ):
        if rval_type:
            fh.write(rval_type + ' ')
        fh.write(method_name)
        if this_usage == 'io':
            fh.write('!')
        fh.write('(')
        first = True
        for p in params:
            if not first:
                fh.write(', ')
            first = False
            fh.write(p)
        fh.write(') = "' + symbol_name + '";\n')

    def get_kl_class_name(self, cpp_class_name):
        if cpp_class_name in self.kl_type_mappings:
            return self.kl_type_mappings[cpp_class_name].kl_type_name
        return cpp_class_name

    def get_kl_class_repr(self, cpp_class_name):
        if cpp_class_name in self.kl_type_mappings:
            return self.kl_type_mappings[cpp_class_name].cpp_type_name
        return cpp_class_name

    def is_pointer_repr(self, cpp_class_name):
        if cpp_class_name in self.kl_type_mappings:
            return self.kl_type_mappings[cpp_class_name].is_pointer
        return False

    def output_param_conversion(self, type_name, name, kl_cpp_type,
                                param_cpp_type):
        output = []
        if param_cpp_type.find('std::vector<') != -1:
            param_cpp_type = param_cpp_type[len('std::vector<'):
                                            param_cpp_type.find(',')]
            output += ['std::vector< %s > %s_param;' % (param_cpp_type, name, )
                       ]
            output += ['%s_param.resize(%s.size());' % (name, name, )]
            output += ['for (uint32_t %s_i=0; %s_i < %s.size(); %s_i++)' %
                       (name, name, name, name, )]
            output += ['{']
            output += ['const %s &%s_param_array_item = %s[%s_i];' %
                       (Type.get_cpp_type_name(type_name, None, True), name,
                        name, name, )]
            output += [self.output_param_conversion(type_name,
                                                    name + '_param_array_item',
                                                    kl_cpp_type,
                                                    param_cpp_type)]
            output += ['%s_param[%s_i] = %s_param_array_item_param;' %
                       (name, name, name, )]
            output += ['}']
        elif self.types_manager.uses_returnval(type_name):
            output += ['::%s %s_param = %s;' % (param_cpp_type, name, name, )]
        elif type_name == 'String':
            output += ['::%s %s_param(%s.getCString());' %
                       (param_cpp_type, name, name, )]
        elif self.get_kl_class_repr(type_name) == param_cpp_type:
            output += [
                'if (!%s.handle) throwException("\'%s\' parameter is null");' %
                (name, name, )
            ]
            output += ['::%s &%s_param = *(::s *)( %s.handle );'
                       % (self.get_kl_class_name(type_name), name,
                          self.get_kl_class_repr(type_name), name, )]
            if self.is_pointer_repr(type_name):
                output += [
                    'if (!%s_param) throwException("\'%s\' parameter is null");'
                    % (name, name, )
                ]
        else:
            output += [
                'if (!%s.handle) throwException("\'%s\' parameter is null");' %
                (name, name, )
            ]
            output += [
                '::%s &%s_param_handle = *(::%s *)( %s.handle );'
                % (self.get_kl_class_repr(type_name), name,
                   self.get_kl_class_repr(type_name), name, )
            ]
            if self.is_pointer_repr(type_name):
                output += [
                    'if (!%s_param_handle) throwException("\'%s\' parameter is null");'
                    % (name, name, )
                ]
            output += ['::%s %s_param = %s_param_handle;' %
                       (param_cpp_type, name, name, )]
        return '\n'.join(output)

    def output_param_reconversion(self, type_name, name, param_cpp_type):
        output = []
        if param_cpp_type.find('std::vector<') != -1:
            param_cpp_type = param_cpp_type[len('std::vector<'):
                                            param_cpp_type.find(',')]
            output += ['%s.resize(%s_param.size());' % (name, name, )]
            output += ['for (uint32_t %s_i=0; %s_i < %s.size(); %s_i++)' %
                       (name, name, name, name, )]
            output += ['{']
            output += ['::%s %s_param_array_item;' %
                       (Type.get_cpp_type_name(type_name, None, True), name, )]
            output += ['::%s &%s_param_array_item_param = %s_param[%s_i];' %
                       (param_cpp_type, name, name, name, )]
            output += [self.output_param_reconversion(
                type_name, name + '_param_array_item', param_cpp_type)]
            output += ['%s[%s_i] = %s_param_array_item;' % (name, name, name, )
                       ]
            output += ['}']
        elif self.types_manager.uses_returnval(type_name):
            output += ['%s  = %s_param;' % (name, name, )]
        elif type_name == 'String':
            output += ['%s = %s_param;' % (name, name, )]
        else:
            output += ['::%s *%s_result = new ::%s();' %
                       (self.get_kl_class_repr(type_name), name,
                        self.get_kl_class_repr(type_name), )]
            output += ['*%s_result = %s_param;' % (name, name, )]
            output += ['%s.handle = reinterpret_cast<KL::Data>(%s_result);' %
                       (name, name, )]
        return '\n'.join(output)

    def parse_type_decl(self, header, indent, cursor, typemap):
        # no children -> forward declaration
        if len(list(cursor.get_children())) < 1:
            print "%s-> no children" % indent
            return

        cpp_desired_type_name = self.get_qualified_spelling(cursor, "::")
        if cpp_desired_type_name in self.kl_type_mappings:
            kl_type_mapping = self.kl_type_mappings[cpp_desired_type_name]
        else:
            kl_type_mapping = KLTypeMapping(
                self.get_qualified_spelling(cursor, "_"),
                "::" + cpp_desired_type_name,
                )
            self.kl_type_mappings[cpp_desired_type_name] = kl_type_mapping
            self.known_types.add(kl_type_mapping.kl_type_name)

        kl_type = KLStruct(
            kl_type_mapping.kl_type_name,
            kl_type_mapping.cpp_type_name,
            )
        kl_type.codegen.cpp_base_type = kl_type_mapping.cpp_type_name
        kl_type.codegen.header = header

        self.parse_type_decl_children(
            " "+indent,
            cursor,
            typemap,
            kl_type,
            kl_type_mapping.kl_type_name,
            )

        self.types_manager.types[kl_type_mapping.kl_type_name] = kl_type

    @staticmethod
    def print_skipping(function, reason):
        print 'skipping function: ' + function
        print '  since: %s' % reason

    def parse_clang_type(self, clang_type):
        clang_type_kind = clang_type.kind
        if clang_type_kind == TypeKind.VOID:
            return None
        elif clang_type_kind == TypeKind.FLOAT:
            return self.types_manager.Float32, 'in'
        # elif clang_type_kind == TypeKind.LVALUEREFERENCE:
        #     nested_kl_type, nested_kl_usage = self.parse_clang_type(clang_type.get_pointee())
        #     if nested_kl_usage == 'io':
        #         raise Exception('unparsable type')
        #     return nested_kl_type, 'io'
        # elif clang_type_kind == TypeKind.RECORD:
        #     cpp_type_name = clang_type.spelling
        #     kl_type_name = self.kl_type_mappings[cpp_type_name].kl_type_name
        #     kl_type = self.types_manager.types[kl_type_name]
        #     return kl_type, 'in'
        else:
            raise Exception("unhandled type: %s" % str(clang_type.spelling))

    def parse_clang_param(self, clang_param):
        param_name = clang_param.spelling
        if not param_name:
            param_name = 'param' + str(i)

        param_kl_type, param_kl_usage = self.parse_clang_type(clang_param.type)
        
        return param_name, param_kl_type, param_kl_usage

    def parse_type_decl_children(
        self,
        child_indent,
        cursor,
        typemap,
        kl_type,
        kl_class_name,
        include_constructors=True
        ):
        for child in cursor.get_children():
            print "%sparse_CLASS_DECL_children %s" % (child_indent, str(child.kind))

            if child.access_specifier != AccessSpecifier.PUBLIC:
                continue

            is_method = False

            if child.kind == CursorKind.CXX_BASE_SPECIFIER:
                cpp_class_name = self.parse_CLASS_DECL(
                    child_indent,
                    child.get_definition(),
                    child.get_definition().location.file.name
                    )
                parent_class_name = self.get_kl_class_name(cpp_class_name)
                kl_type.parent = parent_class_name

            elif child.kind in [
                CursorKind.CXX_METHOD,
                CursorKind.CONSTRUCTOR,
                CursorKind.DESTRUCTOR,
                CursorKind.FUNCTION_TEMPLATE,
                ]:
                is_method = True
                if clang.cindex.conf.lib.clang_CXXMethod_isPureVirtual(child):
                    kl_type.codegen.is_abstract = True

            if is_method:
                try:
                    result_kl_type = self.parse_clang_type(child.result_type)
                except Exception as e:
                    self.print_skipping(
                        child.displayname,
                        "child result type '%s' is not defined" % child.result_type.spelling
                        )
                    continue

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

                this_usage = 'in'
                if not child.is_static_method():
                    if not child.kind == CursorKind.DESTRUCTOR and not child.kind == CursorKind.CONSTRUCTOR:
                        this_usage = 'in' if child.type.spelling.endswith(
                            'const') else 'io'
                method = Method(child.spelling, result_kl_type, this_usage,
                                'public')
                method.codegen.cpp_qual_ret_type = self.get_cpp_qual_type_name(
                    child.result_type)
                method.codegen.cpp_base_ret_type = self.get_cpp_base_type_name(
                    child.result_type)

                if result_kl_type == 'Data':
                    continue

                operator = None
                if child.kind == CursorKind.DESTRUCTOR:
                    # destructor will be run by the KL destructor in C++
                    continue
                elif child.kind == CursorKind.CONSTRUCTOR:
                    if not include_constructors:
                        continue
                    method_name = child.spelling
                    method.codegen.is_constructor = True
                    num_params = 0
                    for p in child.get_children():
                        if p.kind == CursorKind.PARM_DECL:
                            num_params += 1
                    if num_params == 0:
                        kl_type.codegen.has_empty_constructor = True
                else:
                    if child.is_static_method():
                        method_name = kl_class_name + '_' + child.spelling
                        method.codegen.is_static = True
                        namespace = self.get_namespace(child)
                        if namespace:
                            namespace = '::'.join(namespace)
                        method.codegen.cpp_function = namespace
                    else:
                        if child.spelling.startswith('operator'):
                            operator = child.spelling[len('operator'):]
                            if operator not in ['<', '<=', '==', '!=', '>=',
                                                '>']:
                                self.print_skipping(
                                    child.displayname,
                                    "operator %s is unsupported" % operator
                                    )
                                continue
                            method_name = operator
                            method.codegen.cpp_function = child.spelling
                        else:
                            method_name = kl_class_name + '.' + child.spelling
                            method.codegen.cpp_function = child.spelling

                method.codegen.kl_full_name = method_name

                i = 0
                skip = False
                for p in child.get_children():
                    if p.kind == CursorKind.PARM_DECL:
                        # has_default_value = False
                        # invalid_type = False
                        # try:
                        #     kl_type = self.get_kl_type(p.type)
                        # except Exception as _e:
                        #     invalid_type = True
                        # if invalid_type or self.abort_on_type(kl_type):
                        #     for pc in p.get_children():
                        #         # if it has a default value we'll try to go on from here
                        #         if pc.kind in [
                        #             CursorKind.UNEXPOSED_EXPR,
                        #             CursorKind.INTEGER_LITERAL,
                        #             CursorKind.FLOATING_LITERAL,
                        #             CursorKind.STRING_LITERAL,
                        #             CursorKind.CXX_BOOL_LITERAL_EXPR,
                        #             CursorKind.CXX_NULL_PTR_LITERAL_EXPR,
                        #             CursorKind.DECL_REF_EXPR
                        #         ]:
                        #             has_default_value = True
                        #             break
                        #     if has_default_value:
                        #         break
                        #     skip = True
                        #     break
                        name, kl_type, kl_usage = self.parse_clang_param(p)
                        param = KLParam(name, kl_type, kl_usage)
                        param.codegen.cpp_qual_type = kl_type.cpp_type_name
                        param.codegen.cpp_base_type = kl_type.cpp_type_name
                        method.params.append(param)
                        i += 1

                if skip:
                    self.print_skipping(
                        child.displayname,
                        "unsupported default value"
                        )
                    continue

                symbol_name = self.get_symbol_name(kl_class_name, method_name)
                method.symbol = symbol_name
                method.codegen.is_operator = operator

                kl_type.methods.append(method)

    def output_cpp(
        self,
        kl_type,
        snippets,
        ):
        snippets.append(self.jinjenv.get_template('type.template.cpp').render({
            't': kl_type,
            'header': kl_type.codegen.header,
            'manager': self.types_manager,
            'parser': self,
            'enter': self.cpp_enter,
            'leave': self.cpp_leave,
            }))

    def dump_cursor(self, indent, cursor):
        print indent + str(cursor.kind) + " " + cursor.displayname
        print indent + str(cursor.location)
        childIndent = indent + "."
        for childCursor in cursor.get_children():
            self.dump_cursor(childIndent, childCursor)

    def parse_CLASS_DECL(self, include_filename, indent, cursor):
        print "%sCLASS_DECL %s" % (indent, cursor.displayname)

        class_name = cursor.spelling

        clang_members = []

        for child in cursor.get_children():
            if child.kind == CursorKind.FIELD_DECL:
                clang_members.append(child)
                continue

            if child.access_specifier != AccessSpecifier.PUBLIC:
                continue

            # if child.kind == CursorKind.CXX_BASE_SPECIFIER:
            #     cpp_class_name = self.parse_CLASS_DECL(
            #         child_indent,
            #         child.get_definition(),
            #         child.get_definition().location.file.name
            #         )
            #     parent_class_name = self.get_kl_class_name(cpp_class_name)
            #     kl_type.parent = parent_class_name

            # if child.kind == CursorKind.CXX_METHOD:
            #     print child.kind
            #     result_type_info = self.type_mgr.get_type_info(child.result_type)
            #     print "result_type_info = " + str(result_type_info)

            #     is_const = child.type.spelling.endswith('const')
            #     print "this_cpp_type_name = " + child.type.spelling
            #     # this_type_info = self.type_mgr.get_type_info(

            #     if child.is_static_method():
            #         pass
            #     else:
            #         pass
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

        members = [
            Member(
                self.type_mgr.get_type_info(clang_member.type).make_codec(ValueName(clang_member.displayname)),
                clang_member.access_specifier == AccessSpecifier.PUBLIC
                )
            for clang_member in clang_members
            ]

        can_in_place = all(member and member.codec.is_in_place for member in members)
        if can_in_place:
            self.type_mgr.add_codecs(
                build_in_place_struct_codecs(class_name)
                )
            self.edk_decls.add(
                ast.Wrapping(
                    self.ext_name,
                    include_filename,
                    self.get_location(cursor.location),
                    cursor.displayname,
                    class_name,
                    self.type_mgr.get_type_info(class_name).make_codec(ValueName("RESERVED_self")),
                    members,
                    "in_place_struct_decl",
                    )
                )
        else:
            self.type_mgr.add_codecs(
                build_wrapped_ptr_codecs(class_name)
                )
            self.edk_decls.add(
                ast.Wrapping(
                    self.ext_name,
                    include_filename,
                    self.get_location(cursor.location),
                    cursor.displayname,
                    class_name,
                    self.type_mgr.get_type_info(class_name).make_codec(ValueName("RESERVED_self")),
                    members,
                    "wrapped_ptr_decl",
                    )
                )

    def parse_MACRO_INSTANTIATION(self, include_filename, indent, cursor):
        print dir(cursor)
        self.dump_cursor(indent, cursor)
        print indent + ".get_definition() ->"
        self.dump_cursor(indent + ' ', cursor.get_definition())

    def parse_TYPEDEF_DECL(self, include_filename, indent, cursor):
        new_cpp_type_name = cursor.type.spelling
        old_cpp_type_name = cursor.underlying_typedef_type.spelling
        print "%sTYPEDEF_DECL %s -> %s" % (indent, new_cpp_type_name, old_cpp_type_name)
        new_type_spec, old_type_spec = self.type_mgr.add_type_alias(new_cpp_type_name, old_cpp_type_name)
        if new_type_spec and old_type_spec:
            self.edk_decls.add(
                ast.Alias(
                    self.ext_name,
                    include_filename,
                    self.get_location(cursor.location),
                    cursor.displayname,
                    new_type_spec,
                    old_type_spec,
                    )
                )

    def parse_FUNCTION_DECL(self, include_filename, indent, cursor):
        print "%sFUNCTION_DECL %s" % (indent, cursor.displayname)

        if True:
        # try:
            param_index = 1
            clang_params = []
            for param_cursor in cursor.get_children():
                if param_cursor.kind == CursorKind.PARM_DECL:
                    param_name = param_cursor.spelling
                    if len(param_name) == 0:
                        param_name = "_param_%u" % param_index
                    param_clang_type = param_cursor.type
                    clang_params.append(clang_wrapper.ClangParam(param_name, param_clang_type))
                param_index += 1

            self.edk_decls.add(
                ast.Func(
                    self.ext_name,
                    include_filename,
                    self.get_location(cursor.location),
                    cursor.displayname,
                    self.get_nested_name(cursor),
                    self.type_mgr.get_type_info(cursor.result_type),
                    self.type_mgr.convert_clang_params(clang_params),
                    )
                )
        # except Exception as e:
        #     print "%s Unable to wrap function: %s" % (indent, str(e))

    ignored_cursor_kinds = [
        CursorKind.MACRO_DEFINITION,
        CursorKind.INCLUSION_DIRECTIVE,
        ]

    def parse_cursor(self, include_filename, indent, cursor):
        cursor_kind = cursor.kind
        if cursor_kind in Parser.ignored_cursor_kinds:
            pass
        elif cursor_kind in [
            CursorKind.NAMESPACE,
            CursorKind.UNEXPOSED_DECL,
            ]:
            self.parse_children(include_filename, indent, cursor)
        elif cursor_kind == CursorKind.MACRO_INSTANTIATION:
            self.parse_MACRO_INSTANTIATION(include_filename, indent, cursor)
        elif cursor_kind == CursorKind.TYPEDEF_DECL:
            self.parse_TYPEDEF_DECL(include_filename, indent, cursor)
        elif cursor_kind == CursorKind.CLASS_DECL:
            self.parse_CLASS_DECL(include_filename, indent, cursor)
        elif cursor_kind == CursorKind.FUNCTION_DECL:
            self.parse_FUNCTION_DECL(include_filename, indent, cursor)
        else:
            print "%sUnhandled %s" % (indent, cursor_kind)

    def parse_children(self, include_filename, childIndent, cursor):
        for childCursor in cursor.get_children():
            self.parse_cursor(include_filename, childIndent, childCursor)

    def parse(self, unit_filename):
        print "parsing unit: %s" % unit_filename

        clang_index = clang.cindex.Index.create()
        unit = clang_index.parse(
            unit_filename,
            self.clang_args,
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
                self.parse_cursor(unit_filename, "", cursor)

    def output_kl_type(
        self,
        kl_type_name,
        visited_kl_type_names,
        fh_kl,
        snippets,
        ):
        print "output_kl_type %s" % kl_type_name
        if kl_type_name not in visited_kl_type_names:
            visited_kl_type_names.add(kl_type_name)
            kl_type = self.types_manager.types[kl_type_name]

            parent_kl_type_name = kl_type.parent
            if parent_kl_type_name:
                parent_kl_type = self.types_manager.types[parent_kl_type_name]

                self.output_kl_type(
                    parent_kl_type_name,
                    visited_kl_type_names,
                    fh_kl,
                    snippets,
        		    )
            
            self.output_class(kl_type_name, parent_kl_type_name, fh_kl)

            for m in kl_type.methods:
                params = []

                if m.codegen.is_operator:
                    params.append('in ' + kl_type_name + ' this_')

                for p in m.params:
                    param_type = p.type_name
                    if p.arraymod:
                        param_type += p.arraymod
                    params.append(p.usage + ' ' + param_type + ' ' + p.name)

                self.output_method(
                    kl_type_name,
                    m.ret_type_name,
                    m.codegen.kl_full_name,
                    params,
                    m.symbol,
                    m.usage,
                    fh_kl,
                    )

            if not kl_type.codegen.is_abstract:
                self.output_method(
                    kl_type_name,
                    None,
                    '~' + kl_type_name,
                    [],
                    kl_type_name + '__destructor',
                    'in',
                    fh_kl,
                    )
                self.output_method(
                    kl_type_name,
                    None,
                    kl_type_name,
                    ['in ' + kl_type_name + ' that'],
                    kl_type_name + '__copy_constructor',
                    'in',
                    fh_kl,
                    )
                self.output_method(
                    kl_type_name,
                    None,
                    kl_type_name + '.=',
                    ['in ' + kl_type_name + ' that'],
                    kl_type_name + '__copy_constructor',
                    'in',
                    fh_kl,
                    )

            self.output_cpp(kl_type, snippets['cpp'])

    def jinja_stream(self, lang):
        return self.jinjenv.get_template("template." + lang).stream(
            ext_name = self.ext_name,
            gen_decl_streams = lambda: self.edk_decls.jinja_streams(self.jinjenv, lang),
            )
    
    def output(
        self,
        output_kl_filename,
        output_cpp_filename,
        ):
        # prune types without full definitions
        for kl_type_name in self.types_manager.types:
            kl_struct = self.types_manager.types[kl_type_name]
            methods = []
            for m in kl_struct.methods:
                remove = False
                for p in m.params:
                    if not p.kl_type_name in self.known_types:
                        remove = True

                if m.ret_type_name and not m.ret_type_name.replace(
                    '[]', '') in self.known_types:
                    remove = True

                if not remove:
                    methods.append(m)

            kl_struct.methods = methods

        self.jinja_stream('kl').dump(output_kl_filename)
        self.jinja_stream('cpp').dump(output_cpp_filename)
