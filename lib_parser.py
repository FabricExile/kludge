import jinja2, os, sys

import clang
from clang.cindex import AccessSpecifier, CursorKind, TypeKind

from kl2edk import Struct, Method, Param, Type, TypesManager


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


class LibParser:
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

    cpp_type_to_kl_mappings = {
        "float": "Float32",
        "double": "Float64",
        "std::basic_string<char>": "String",
    }

    def __init__(
        self,
        ext_name,
        ):
        self.clang_args = [
            '-x',
            'c++',
        ]

        self.classes = {}
        self.symbol_names = set()

        self.ext_name = ext_name
        self.types_manager = TypesManager(ext_name)

        self.wrapper_templates = {}
        self.cpp_type_to_kl_mappings = {}
        self.cpp_type_to_kl_mappings.update(LibParser.cpp_type_to_kl_mappings)
        self.kl_type_mappings = {}
        self.skip_methods = []
        self.cpp_ext_header_pre = ""
        self.cpp_ext_header_post = ""
	self.cpp_enter = ""
        self.cpp_leave = ""

        self.known_types = set(['Data', 'String'])
        for t in LibParser.basic_type_map:
            self.known_types.add(LibParser.basic_type_map[t])

        self.jinjenv = jinja2.Environment(
            trim_blocks=True,
            lstrip_blocks=True,
            loader=jinja2.PackageLoader('__main__', 'templates')
            )

    def get_kl_type(self, clang_type):
        canon_type = clang_type.get_canonical()
        base_name = canon_type.spelling
        if canon_type.is_const_qualified():
            base_name = base_name[len('const '):]
        kl_type = None
        is_array = False

        if canon_type.kind == TypeKind.LVALUEREFERENCE:
            kl_type = self.get_kl_type(canon_type.get_pointee())

        elif canon_type.kind == TypeKind.POINTER:
            if canon_type.get_pointee().kind == TypeKind.VOID:
                return "Data"
            if canon_type.get_pointee().kind in [TypeKind.CHAR_S,
                                                 TypeKind.SCHAR]:
                return "String"
            kl_type = self.get_kl_type(canon_type.get_pointee())

        elif canon_type.kind == TypeKind.UNEXPOSED or canon_type.kind == TypeKind.RECORD:
            kl_type = base_name
            if kl_type.startswith('std::vector<'):
                is_array = True
                kl_type = kl_type[len('std::vector<'):kl_type.find(',')]
            if kl_type in self.cpp_type_to_kl_mappings:
                kl_type = self.cpp_type_to_kl_mappings[kl_type]

        elif canon_type.kind == TypeKind.TYPEDEF:
            kl_type = self.get_kl_type(canon_type.get_canonical())

        elif canon_type.kind == TypeKind.VOID:
            return None

        if not kl_type:
            kl_type = LibParser.basic_type_map[canon_type.kind]

        if not kl_type:
            raise Exception('no KL type for ' + str(canon_type.spelling) + ' ('
                            + str(canon_type.kind) + ')')

        kl_type = self.get_kl_class_name(kl_type)

        if is_array:
            kl_type += '[]'

        return kl_type

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
            LibParser.debug_print(c, prefix + '  ')

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
    def get_namespace(cursor):
        namespace = [cursor.spelling]
        if cursor:
            parent = cursor.semantic_parent
            if parent:
                if parent.kind in [CursorKind.NAMESPACE, CursorKind.CLASS_DECL,
                                   CursorKind.STRUCT_DECL]:
                    namespace = LibParser.get_namespace(parent) + namespace
        return namespace

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

    def parse_class(self, cursor, header):

        # class with no children is a forward declaration
        if len(list(cursor.get_children())) < 1:
            return

        cpp_class_name = cursor.spelling
        kl_class_repr = self.get_kl_class_repr(cpp_class_name)
        kl_class_name = self.get_kl_class_name(cpp_class_name)

        self.known_types.add(kl_class_name)

        kl_struct = Struct(kl_class_name)
        kl_struct.codegen.cpp_base_type = kl_class_repr
        kl_struct.codegen.header = header

        self.parse_class_children(cursor, kl_struct, kl_class_name)

        self.types_manager.types[kl_class_name] = kl_struct

        return kl_class_name

    @staticmethod
    def print_skipping(function, reason):
        print 'skipping function: ' + function
        print '  since: %s' % reason

    def parse_class_children(self, cursor, kl_type, kl_class_name,
                             include_constructors=True):
        for child in cursor.get_children():
            if child.access_specifier != AccessSpecifier.PUBLIC:
                continue

            is_method = False

            if child.kind == CursorKind.CXX_BASE_SPECIFIER:
                cpp_class_name = self.parse_class(
                    child.get_definition(),
                    child.get_definition().location.file.name)
                parent_class_name = self.get_kl_class_name(cpp_class_name)
                kl_type.parent = parent_class_name

            elif child.kind in [CursorKind.CXX_METHOD, CursorKind.CONSTRUCTOR,
                                CursorKind.DESTRUCTOR,
                                CursorKind.FUNCTION_TEMPLATE]:
                is_method = True
                if clang.cindex.conf.lib.clang_CXXMethod_isPureVirtual(child):
                    kl_type.codegen.is_abstract = True

            if is_method:
                try:
                    kl_result_type = self.get_kl_type(child.result_type)
                except Exception as _e:
                    self.print_skipping(
                        child.displayname,
                        "child result type '%s' is not defined" % child.result_type
                        )
                    continue

                if child.spelling in self.skip_methods:
                    self.print_skipping(
                        child.displayname,
                        "method is in skip list"
                        )
                    continue
                if self.abort_on_type(kl_result_type):
                    self.print_skipping(
                        child.displayname,
                        "result type '%s' is in abort list" % kl_result_type
                        )
                    continue
                this_usage = 'in'
                if not child.is_static_method():
                    if not child.kind == CursorKind.DESTRUCTOR and not child.kind == CursorKind.CONSTRUCTOR:
                        this_usage = 'in' if child.type.spelling.endswith(
                            'const') else 'io'
                method = Method(child.spelling, kl_result_type, this_usage,
                                'public')
                method.codegen.cpp_qual_ret_type = self.get_cpp_qual_type_name(
                    child.result_type)
                method.codegen.cpp_base_ret_type = self.get_cpp_base_type_name(
                    child.result_type)

                if kl_result_type == 'Data':
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
                        has_default_value = False
                        invalid_type = False
                        try:
                            param_kl_type = self.get_kl_type(p.type)
                        except Exception as _e:
                            invalid_type = True
                        if invalid_type or self.abort_on_type(param_kl_type):
                            for pc in p.get_children():
                                # if it has a default value we'll try to go on from here
                                if pc.kind in [
                                    CursorKind.UNEXPOSED_EXPR,
                                    CursorKind.INTEGER_LITERAL,
                                    CursorKind.FLOATING_LITERAL,
                                    CursorKind.STRING_LITERAL,
                                    CursorKind.CXX_BOOL_LITERAL_EXPR,
                                    CursorKind.CXX_NULL_PTR_LITERAL_EXPR,
                                    CursorKind.DECL_REF_EXPR
                                ]:
                                    has_default_value = True
                                    break
                            if has_default_value:
                                break
                            skip = True
                            break
                        kl_name = p.spelling
                        if not kl_name:
                            kl_name = 'param' + str(i)
                        usage = 'io' if self.is_io_param(p.type) else 'in'
                        param = Param(kl_name, param_kl_type, usage)
                        param.codegen.cpp_qual_type = self.get_cpp_qual_type_name(
                            p.type)
                        param.codegen.cpp_base_type = self.get_cpp_base_type_name(
                            p.type)
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

    def parse_unit(self, cursor, header):
        for child in cursor.get_children():
            if hasattr(child.location.file,
                       'name') and child.location.file.name != header:
                continue

            if child.kind == CursorKind.CLASS_DECL:
                self.parse_class(child, header)
            elif child.kind == CursorKind.NAMESPACE:
                self.parse_unit(child, header)

    def parse(self, unit_filename):
        # print "arguments:"
        # for clang_arg in self.clang_args:
        #     print "  %s" % clang_arg

        print "parsing unit: %s" % unit_filename

        clang_index = clang.cindex.Index.create()
        unit = clang_index.parse(
            unit_filename,
            self.clang_args,
            None,
            clang.cindex.TranslationUnit.PARSE_DETAILED_PROCESSING_RECORD
            )

        skip = False
        for d in unit.diagnostics:
            skip = skip or not self.print_diag(d)

        if skip:
            print 'skipping unit: ' + unit.spelling
        else:
            self.parse_unit(unit.cursor, unit_filename)

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
                    if not p.type_name in self.known_types:
                        remove = True

                if m.ret_type_name and not m.ret_type_name.replace(
                    '[]', '') in self.known_types:
                    remove = True

                if not remove:
                    methods.append(m)

            kl_struct.methods = methods

        header = """//////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////
//
// Automatically generated by KLUDGE -- DO NOT EDIT
//
//////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////

"""
        snippets = {
          'kl': [],
          'cpp': []
        }
        with open(output_kl_filename, "w") as fh_kl:
            fh_kl.write(header)

            visited_kl_type_names = set()
            for kl_type_name in self.types_manager.types:
                self.output_kl_type(
                    kl_type_name,
                    visited_kl_type_names,
                    fh_kl,
                    snippets,
                    )

        with open(output_cpp_filename, "w") as fh:
            fh.write(self.jinjenv.get_template('ext.template.cpp').render({
                'header_pre': self.cpp_ext_header_pre,
                'header_post': self.cpp_ext_header_post,
                'body': ''.join(snippets['cpp']),
                }))
