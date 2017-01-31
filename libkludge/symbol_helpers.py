#
# Copyright (c) 2010-2017 Fabric Software Inc. All rights reserved.
#

import re

def replace_invalid_chars(symbol):
    return re.sub('[^0-9a-zA-Z_]+', '__', symbol)

