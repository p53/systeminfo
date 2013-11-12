import string

class PropertyTemplate:
        _template = ''
        _maxInfo = {'propname': 0, 'propval': 0 }

        def __init__(self, tableRows, tplstring):
                self.tableData = tableRows
                self._template = tplstring

        def __str__(self):
                length = 0
                output = "\n"

                for key, data in self.tableData.iteritems():
                        if self.tableData[key] is None or self.tableData[key] == '':
                                self.tableData[key] = 'N/A'

                        if self._maxInfo['propname'] < len(self.tableData[key]['propname']):
                                self._maxInfo['propname'] = len(self.tableData[key]['propname'])

                        if self._maxInfo['propval'] < len(self.tableData[key]['propval']):
                                self._maxInfo['propval'] = len(self.tableData[key]['propval'])

                if len(self.tableData.keys()) > 0:
                     output = output + self._template % self + "\n"

                return output

        def __getitem__(self, key):
                el = key.split("|")
                if len(el) == 1:
                        valformated = self.tableData[key]['propval']
                        keyformated = self.tableData[key]['propname']
                        return keyformated + ':' + valformated
                else:
                        valformated = getattr(string, el[1])(self.tableData[el[0]]['propval'], self._maxInfo['propval'])
                        keyformated = getattr(string, el[1])(self.tableData[el[0]]['propname'], self._maxInfo['propname'])
                        return keyformated + ':' + valformated


