#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

from param import Param

def massage_returns(returns):
  if not returns:
    returns = 'void'
  assert isinstance(returns, basestring)
  return returns

def massage_param(param):
  if isinstance(param, basestring):
    param = Param('', param)
  assert isinstance(param, Param)
  return param

def massage_params(params):
  assert isinstance(params, list)
  return [massage_param(param) for param in params]
