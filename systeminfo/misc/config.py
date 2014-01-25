"""
Module: config.py

This module sets some basic properties for script and is making package
building more straightforward

@author: Pavol Ipoth
@license: GPL
@copyright: Copyright 2013 Pavol Ipoth
@contact: pavol.ipoth@gmail.com

"""

import os
import sys

cacheDir = os.path.dirname(sys.argv[0]) + '/cache/'
confDir = os.path.dirname(sys.argv[0]) + '/settings/'
