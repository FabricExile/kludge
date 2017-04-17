#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

ext.add_cpp_quoted_include('ManagedType.hpp')

book = ext.add_managed_type('Book')
book.add_ctor(['const char *'])
book.add_const_method('getTitle', 'const char *', [])

library = ext.add_owned_type('Library')
library.add_ctor([])
library.add_mutable_method('addBook', None, ['Book *'])
library.add_const_method('getNumBooks', 'size_t', [])
library.add_const_method('getBook', 'const Book *', ['size_t'])

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
lib.addBook(Book("Engine"));
lib.addBook(Book("Kludge"));
report(lib.getNumBooks());
report(lib.getBook(0));
Book b = lib.getBook(1);
report(b.getTitle());
""", """
Library::Library()
Book::Book(Fabric)
Book::Book(Engine)
Book::Book(Kludge)
3
Book:MANAGED
Engine
Book::~Book(Fabric)
Book::~Book(Engine)
Book::~Book(Kludge)
Library::~Library()
""")
