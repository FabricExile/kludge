#
# Copyright (c) 2010-2017 Fabric Software Inc. All rights reserved.
#

class DirQualTypeInfo:

  def __init__(self, dir_qual, type_info):
    self.dir_qual = dir_qual
    self.type_info = type_info

  @property
  def dq(self):
    return self.dir_qual

  @property
  def ti(self):
    return self.type_info
  
  def get_desc(self):
    return "%s:%s" % (self.dir_qual.get_desc(), self.type_info.get_desc())

  def __str__(self):
    return self.get_desc()
