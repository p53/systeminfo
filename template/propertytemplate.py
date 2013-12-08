import string

class PropertyTemplate:
        _template = ''
        _maxInfo = {'propname': 0, 'propval': 0 }
        _property_names = {}
        
        def __init__(self, tableRows, names, tplstring):
                self._property_names = names
                self.tableData = tableRows[0]
                self._template = tplstring

        def __str__(self):
                length = 0
                output = "\n"

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

        def __getitem__(self, key):
                el = key.split("|")
                current_key = ''
                
                if el[0] in self._property_names.keys():
                    current_key = self._property_names[el[0]]
                else:
                    current_key = el[0]
                    
                if len(el) == 1:
                        valformated = self.tableData[key]
                        keyformated = current_key
                        return keyformated + ':' + valformated
                else:
                        valformated = self.tableData[el[0]]
                        keyformated = getattr(string, el[1])(current_key, self._maxInfo['propname'])
                        return keyformated + ':' + valformated


