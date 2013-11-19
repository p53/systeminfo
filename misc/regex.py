import re

Class Regex:

    def filterArray(self, pattern, array):
        compre = re.compile(pattern)
        matches = []
        for item in array:
            match = compre.search(item)
            if match:
                matches.append(item)

        return matches
        
            
