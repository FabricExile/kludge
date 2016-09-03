#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

import abc

class Decl:
  def __init__(
    self,
    extname,
    include_filename,
    location,
    desc,
    ):
    self._extname = extname
    self._include_filename = include_filename
    self._location = location
    self._desc = desc

  @property
  def include_filename(self):
    return self._include_filename

  @property
  def location(self):
    return self._location

  @property
  def desc(self):
    return self._desc

  @abc.abstractmethod
  def jinja_stream_types(self, jinjenv, lang): pass

  @abc.abstractmethod
  def jinja_stream_aliases(self, jinjenv, lang): pass

  @abc.abstractmethod
  def jinja_stream_funcs(self, jinjenv, lang): pass
