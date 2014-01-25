"""
Module: config-prod.py

This module sets some basic properties for script and is making package
building more straightforward, used in building process as config.py,
we don't have to change paths to dirs in source code and because it is
module is automatically added to the path

@author: Pavol Ipoth
@license: GPL
@copyright: Copyright 2013 Pavol Ipoth
@contact: pavol.ipoth@gmail.com

"""

import os
import sys

cacheDir = '/var/cache/systeminfo/'
confDir = '/etc/systeminfo/settings/'
