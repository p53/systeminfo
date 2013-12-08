
__docformat__ = "javadoc"

"""
Module: tabletemplate.py

Class: TableTemplate

Copyright 2013 Pavol Ipoth <pavol.ipoth@gmail.com>

This class processes template string
It is used for generating body of table output

@author: Pavol Ipoth
"""

import string

class TableTemplate:
        
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
            
            Initializies object, finds maximum width for each table columns
            
            @param tableRows list this is list of asset items
            @param names list this is list of column names
            @param tplstring str this is template string
            @return void
        """
        def __init__(self, tableRows, names, tplstring):
                self.header = names
                tableRows.insert(0, names)
                self.tableData = tableRows
                self._template = tplstring
                for key, value in self.header.iteritems():
                        self._maxInfo[key] = [len(value)]
                        self._maxInfo[key+'Max'] = len(value)

                for cpunum, info in enumerate(self.tableData):
                        if len(info.keys()) > 0:
                                for key, value in self.header.iteritems():
                                    if key not in self.tableData[cpunum]:
                                        self.tableData[cpunum][key] = 'N/A'

                                    if self.tableData[cpunum][key] is None or self.tableData[cpunum][key] == '':
                                        self.tableData[cpunum][key] = 'N/A'

                                    if max(self._maxInfo[key]) < len(self.tableData[cpunum][key]):
                                        self._maxInfo[key+'Max'] = len(self.tableData[cpunum][key])

                                    self._maxInfo[key].append(len(str(self.tableData[cpunum][key])))
                
                # we are popping out header fields, we need just data for body
                self.tableData.pop(0)
        
        """
            Method: __str__
            
            This method is key method in generating output string, just for header items,
            for each items is calling __getitem__ method
            
            @return output str
        """
        def __str__(self):
                length = 0
                output = ""
                for i, v in enumerate(self.tableData):
                        if len(v.keys()) > 0:
                                output = output + self._template % self
                                self._iteration = self._iteration + 1

                self._iteration = 0
                return output

        """
            Method: __getitem__
            
            Method formats and generates string for item
            
            @param key string
            @return string
        """
        def __getitem__(self, key):
                el = key.split("|")
                if len(el) == 1:
                        return self.tableData[self._iteration][key]
                else:
                        return getattr(string, el[1])(self.tableData[self._iteration][el[0]], self._maxInfo[el[0]+'Max'])

            
            

