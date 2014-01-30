#!/usr/bin/env python

from distutils.core import setup

setup(name='systeminfo',
      version='1.2',
      description='Python Utilities for getting HW info on Linux',
      author='Pavol Ipoth',
      author_email='pavol.ipoth@gmail.com',
      packages=['systeminfo', 
		'systeminfo.io', 
		'systeminfo.misc',
		'systeminfo.proc',
		'systeminfo.template',
		'systeminfo.view'
		],
     )

