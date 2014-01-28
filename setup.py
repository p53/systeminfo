#!/usr/bin/env python

from distutils.core import setup

setup(name='systeminfo',
      version='1.0',
      description='Python Utilities for getting HW info on Linux',
      author='Pavol Ipoth',
      author_email='pavol.ipoth@gmail.com',
      packages=['systeminfo', 
		'systeminfo.io',
		'systeminfo.proc',
		'systeminfo.misc',
		'systeminfo.view',
		'systeminfo.template',
		'systeminfo.view',
		]
     )
