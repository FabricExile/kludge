//
// Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
//

#pragma once

#include <iostream>
#include <stdio.h>
#include <string>
#include <vector>

class Entry
{
  public:
    Entry(){}
    ~Entry(){}
};

class Book : public Entry
{
public:
  Book(const char * title)
  : Entry()
  , m_title(title)
  {
    std::cout << "Book::Book(" << m_title << ")\n" << std::flush;
  }

  Book(const Book & other)
  {
    m_title = other.m_title;
  }

  ~Book()
  {
    std::cout << "Book::~Book(" << m_title << ")\n" << std::flush;
  }

  const char * getTitle() const
  {
    return m_title.c_str();
  }

private:
  std::string m_title;
};

class Library
{
public:
  Library()
  {
    std::cout << "Library::Library()\n" << std::flush;
  }

  ~Library()
  {
    for(size_t i=0;i<m_books.size();i++)
    {
      delete(m_books[i]);
    }
    m_books.clear();

    std::cout << "Library::~Library()\n" << std::flush;
  }

  void addBook(Book * book)
  {
    m_books.push_back(book);
  }

  void addBook2(Book book)
  {
    m_books.push_back(new Book(book));
  }

  bool hasBook(Book & book) const
  {
    std::string title = book.getTitle();
    for(size_t i=0;i<m_books.size();i++)
    {
      if(title == m_books[i]->getTitle())
        return true;
    }
    return false;
  }

  size_t getNumBooks() const
  {
    return m_books.size();
  }

  const Book * getBook(size_t index) const
  {
    return (const Book *)m_books[index];
  }

  const Book & getBookRef(size_t index) const
  {
    return *m_books[index];
  }

private:

  std::vector<Book*> m_books;
};
