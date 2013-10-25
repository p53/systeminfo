def readFile(file):
        f = open(file, 'r')
        lines = f.readlines()
        f.close()
        return lines
