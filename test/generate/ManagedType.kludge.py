#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

ext.add_cpp_quoted_include('ManagedType.hpp')

book = ext.add_managed_type('Book')
book.add_ctor(['const char *'])
book.add_ctor(['const Book &'])
book.add_const_method('getTitle', 'const char *', [])

library = ext.add_owned_type('Library')
library.add_ctor([])
library.add_mutable_method('addBook', None, ['Book *'])
library.add_mutable_method('addBook2', None, ['Book'])
library.add_const_method('hasBook', 'bool', ['Book &'])
library.add_const_method('getNumBooks', 'size_t', [])
library.add_const_method('getBook', 'const Book *', ['size_t'])
library.add_const_method('getBookRef', 'const Book &', ['size_t'])

ext.add_test("""
Book b1("Fabric");
b1.cxx_delete();
""", """
Book::Book(Fabric)
Book::~Book(Fabric)
""")

ext.add_test("""
Library lib;
lib.addBook(Book("Fabric"));
Book engine("Engine");
report(lib.hasBook(engine));
lib.addBook(engine);
report(lib.hasBook(engine));
lib.addBook(Book("Kludge"));
report(lib.getNumBooks());
report(lib.getBook(0));
Book b = lib.getBook(1);
report(b.getTitle());
report(lib.getBook(0).getTitle());
""", """
Library::Library()
Book::Book(Fabric)
Book::Book(Engine)
false
true
Book::Book(Kludge)
3
Book:MANAGED
Engine
Fabric
Book::~Book(Fabric)
Book::~Book(Engine)
Book::~Book(Kludge)
Library::~Library()
""")
