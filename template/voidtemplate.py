
__docformat__ = "javadoc"

"""
Module: voidtemplate.py

Class: VoidTemplate

Copyright 2013 Pavol Ipoth <pavol.ipoth@gmail.com>

This class is just void template, returns empty string

@author: Pavol Ipoth
"""

import string

class VoidTemplate:
    
        _template = ''
        
        """
            Variable holds index for iterating over items
            
            @var _iteration int
        """
        _iteration = 0
        
        """
            Variable holds maximum length for each column
            
            @var _maxInfo dict
        """
        _maxInfo = {}

        """
            Method: __init__
            
            Method is just void method
        """
        def __init__(self, tableRows, names, tplstring):
            pass
        
        """
            Method: __str__
            
            This method is key method is not implemented as name of class suggests
            it is just void class
            
            @return output str
        """
        def __str__(self):
            return ''
