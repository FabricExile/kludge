#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

class DirQualTypeCodec:

  def __init__(self, dir_qual, type_codec):
    self.dir_qual = dir_qual
    self.type_codec = type_codec

  @property
  def type_info(self):
      return self.type_codec.type_info
