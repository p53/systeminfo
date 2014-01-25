"""
Module: voidtemplate.py

Class: VoidTemplate

This class is just void template, returns empty string

@author: Pavol Ipoth
@license: GPL
@copyright: Copyright 2013 Pavol Ipoth
@contact: pavol.ipoth@gmail.com

"""

import string

class VoidTemplate:
    
        _template = ''
        
        _iteration = 0
        """
        @type: int
        @ivar: holds index for iterating over items
        """
        
        _maxInfo = {}
        """
        @type: dict
        @ivar: holds maximum length for each column
        """
        
        def __init__(self, tableRows, names, tplstring):
            """
            Method: __init__
            
            Method is just void method
            """
            pass
        
        def __str__(self):
            """
            Method: __str__
            
            This method is key method is not implemented as name of class suggests
            it is just void class
            
            @rtype: str
            @return: returns empty string
            """
            return ''
