#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

class DirQualTypeInfo:

  def __init__(self, dir_qual, type_info):
    self.dir_qual = dir_qual
    self.type_info = type_info

  def get_desc(self):
    return "%s:%s" % (self.dir_qual.get_desc(), self.type_info.get_desc())
