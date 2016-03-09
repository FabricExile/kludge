#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

class DirQualTypeInfo:

  def __init__(self, dir_qual, type_info):
    self.dir_qual = dir_qual
    self.type_info = type_info

  @property
  def can_in_place(self):
      return self.dir_qual.is_direct and self.type_info.can_in_place
