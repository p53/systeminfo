
__docformat__ = "javadoc"

"""
Module: propertytemplate.py

Class: PropertyTableTemplate

Copyright 2013 Pavol Ipoth <pavol.ipoth@gmail.com>

This class processes template string
It is used for generating string as key value pairs of properties

@author: Pavol Ipoth
"""

import string

class PropertyTemplate:
        _template = ''
        
        """
            Variable holds maximum length for key column
            
            @var _maxInfo dict
        """
        _maxInfo = {'propname': 0, 'propval': 0 }
        
        """
            Variable holds names for each property
            
            @var _property_names dict
        """
        _property_names = {}
        
        """
            Method: __init__
            
            Method initializies object
            
            @param tableRows list
            @param names list
            @param tplstring str
            @return void
        """
        def __init__(self, tableRows, names, tplstring):
                self._property_names = names
                self.tableData = tableRows[0]
                self._template = tplstring

        """
            Method: __str__
            
            This method is key method in generating output string, in format of key value pairs,
            it calls __getitem__ for each item
            
            @return output str
        """
        def __str__(self):
                length = 0
                output = "\n"

                # if there is no value in data, fill with N/A
                for key, data in self._property_names.iteritems():
                        current_key = self._property_names[key]
                        
                        if key not in self.tableData.keys():
                            self.tableData[key] = 'N/A'
                            
                        if self.tableData[key] is None or self.tableData[key] == '':
                                self.tableData[key] = 'N/A'

                        if self._maxInfo['propname'] < len(current_key):
                                self._maxInfo['propname'] = len(current_key)

                        if self._maxInfo['propval'] < len(self.tableData[key]):
                                self._maxInfo['propval'] = len(self.tableData[key])

                if len(self.tableData.keys()) > 0:
                     output = output + self._template % self + "\n"

                return output
                
        """
            Method: __getitem__
            
            Method formats and generates string for item
            
            @param key string
            @return string
        """
        def __getitem__(self, key):
                el = key.split("|")
                current_key = ''
                
                if el[0] in self._property_names.keys():
                    current_key = self._property_names[el[0]]
                else:
                    current_key = el[0]
                   
                # value column is not formated
                if len(el) == 1:
                        valformated = self.tableData[key]
                        keyformated = current_key
                        return keyformated + ':' + valformated
                else:
                        valformated = self.tableData[el[0]]
                        keyformated = getattr(string, el[1])(current_key, self._maxInfo['propname'])
                        return keyformated + ':' + valformated


