from expr import *
from pyparsing import *
import sys, traceback

class Parser:

  def __init__(self):
    self.tok_ast = Literal("*").suppress()
    self.tok_amp = Literal("&").suppress()
    self.tok_colon_colon = Literal("::").suppress()
    self.tok_langle = Literal("<").suppress()
    self.tok_rangle = Literal(">").suppress()
    self.tok_comma = Literal(",").suppress()
    self.tok_lparen = Literal("[").suppress()
    self.tok_rparen = Literal("]").suppress()

    self.key_void = Keyword("void")
    self.key_bool = Keyword("bool")
    self.key_char = Keyword("char")
    self.key_short = Keyword("short")
    self.key_int = Keyword("int")
    self.key_long = Keyword("long")
    self.key_float = Keyword("float")
    self.key_double = Keyword("double")
    self.key_signed = Keyword("signed")
    self.key_unsigned = Keyword("unsigned")
    self.key_const = Keyword("const")
    self.key_volatile = Keyword("volatile")
    self.key_struct = Keyword("struct").suppress()
    self.key_class = Keyword("class").suppress()

    self.ident = And([
      NotAny(self.key_const),
      NotAny(self.key_volatile),
      NotAny(self.key_struct),
      NotAny(self.key_class),
      Word(alphas+"_", alphanums+"_"),
      ])
    self.number = Word(nums).setParseAction(lambda s,l,t: int(t[0]))

    self.ty_void = self.key_void.setParseAction(lambda s,l,t: Void())
    self.ty_bool = self.key_bool.setParseAction(lambda s,l,t: Bool())
    self.ty_char = self.key_char.setParseAction(lambda s,l,t: Char())
    self.ty_short = self.key_short.setParseAction(lambda s,l,t: Short())
    self.ty_int = self.key_int.setParseAction(lambda s,l,t: Int())
    self.ty_long = self.key_long.setParseAction(lambda s,l,t: Long())
    self.ty_long_long = (self.key_long + self.key_long).setParseAction(lambda s,l,t: LongLong())
    self.ty_unqualified_integer = self.ty_char | self.ty_short | self.ty_int | self.ty_long_long | self.ty_long
    self.ty_integer = Forward()
    self.ty_integer << MatchFirst([
      ( self.key_signed + self.ty_integer ).setParseAction(lambda s,l,t: t[1].make_signed()),
      ( self.key_unsigned + self.ty_integer ).setParseAction(lambda s,l,t: t[1].make_unsigned()),
      self.ty_unqualified_integer,
      self.key_signed.setParseAction(lambda s,l,t: Int()),
      self.key_unsigned.setParseAction(lambda s,l,t: Int().make_unsigned()),
      ])
    self.ty_float = self.key_float.setParseAction(lambda s,l,t: Float())
    self.ty_double = self.key_double.setParseAction(lambda s,l,t: Double())
    self.ty_floating_point = self.ty_float | self.ty_double

    self.ty_post_qualified = Forward()

    def make_simple(s,l,t):
      # print "make_simple t=%s" % t
      return Simple(t[0])
    self.ty_simple = MatchFirst([
      self.ident,
      self.key_struct + self.ident,
      self.key_class + self.ident,
      ]).setParseAction(make_simple)

    self.ty_template_params = Forward()
    self.ty_template_params << (
        (self.ty_post_qualified + self.tok_comma + self.ty_template_params)
      | self.ty_post_qualified
      | Empty()
      )

    def make_template(s,l,t):
      # print "make_template t[0]=%s t[1:]=%s" % (t[0].__class__, t[1:].__class__)
      return Template(t[0], t[1:])
    self.ty_template = (
        self.ident
      + self.tok_langle
      + self.ty_template_params
      + self.tok_rangle
      ).setParseAction(make_template)

    def make_component(s,l,t):
      # print "make_component t=%s" % t
      return t[0]
    self.ty_component = (
        self.ty_template
      | self.ty_simple
      ).setParseAction(make_component)

    self.ty_components = Forward()
    self.ty_components << (
        (self.ty_component + self.tok_colon_colon + self.ty_components)
      | self.ty_component
      )

    def make_named(s,l,t):
      # print "make_named t=%s" % t
      return Named(t[:])
    self.ty_named = MatchFirst([
      self.ty_components,
      self.tok_colon_colon + self.ty_components,
      ]).setParseAction(make_named)

    self.ty_unqualified = MatchFirst([
      self.ty_void,
      self.ty_bool,
      self.ty_integer,
      self.ty_floating_point,
      self.ty_named,
      ])

    self.ty_pre_qualified = Forward()
    self.ty_pre_qualified << MatchFirst([
        self.ty_unqualified,
        (self.key_const + self.ty_pre_qualified).setParseAction(lambda s,l,t: t[1].make_const()),
        (self.key_volatile + self.ty_pre_qualified).setParseAction(lambda s,l,t: t[1].make_volatile()),
        ])

    self.ty_post_qualified_NO_LEFT_REC = Forward()
    def make_const(te):
      return te.make_const()
    def make_volatile(te):
      return te.make_volatile()
    def make_pointer(te):
      return PointerTo(te)
    def make_reference(te):
      return ReferenceTo(te)
    def make_fixed_array_of(num):
      return lambda te: FixedArrayOf(te, num)
    self.ty_post_qualified_NO_LEFT_REC << MatchFirst([
      (self.key_const.setParseAction(lambda s,l,t: make_const) + self.ty_post_qualified_NO_LEFT_REC),
      (self.key_volatile.setParseAction(lambda s,l,t: make_volatile) + self.ty_post_qualified_NO_LEFT_REC),
      (self.tok_ast.setParseAction(lambda s,l,t: make_pointer) + self.ty_post_qualified_NO_LEFT_REC),
      (self.tok_amp.setParseAction(lambda s,l,t: make_reference) + self.ty_post_qualified_NO_LEFT_REC),
      ((self.tok_lparen + self.number + self.tok_rparen).setParseAction(lambda s,l,t: make_fixed_array_of(t[0])) + self.ty_post_qualified_NO_LEFT_REC),
      Empty(),
      ])
    def make_post_qualified(s, l, t):
      result = t[0]
      for i in range(1, len(t)):
        result = t[i](result)
      return result
    self.ty_post_qualified << \
      (self.ty_pre_qualified + self.ty_post_qualified_NO_LEFT_REC).setParseAction(make_post_qualified)

    self.grammar = self.ty_post_qualified + StringEnd()
    self.grammar.validate()

  def parse(self, cpp_type_name):
    try:
      return self.grammar.parseString(cpp_type_name)[0]
    except Exception as e:
      raise Exception(cpp_type_name + ": unhandled C++ type expression (details: %s)" % str(e))

if __name__ == "__main__":
  p = Parser()
  for e in [
    "void",
    "const void",
    "int *",
    "signed",
    "unsigned",
    "bool",
    "const bool",
    "volatile const signed unsigned",
    "const uint64_t & const ** volatile &",
    "foo<>",
    "foo<bar>",
    "foo<bar, baz>",
    "std::string const &",
    "std::vector<std::string>",
    "some::nested<template::expr<int, another>, yet::another<const volatile void *>>",
    "const std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > &",
    "int[2]",
    "float[4][4]",
    "std::vector<std::string[2]>[5]",
    "SdfHandleTo<SdfLayer>::Handle",
    # error cases
    "const",
    "volatile",
    "int int",
    "int * void & const",
    ]:
    try:
      r = str(p.parse(e))
    except Exception as ex:
      r = "ERROR (%s)" % ex
      # r += str(ex)
    print "%s -> %s" % (e, r)
