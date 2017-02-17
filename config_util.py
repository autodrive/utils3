import ConfigParser as cp


class FileReadLineStrip(__builtins__['file']):
    def readline(self, size=-1):
        # strip white spaces at the beginning and end of the text line
        txt = super(FileReadLineStrip, self).readline(size)
        if txt:
            result = txt.strip()
            del txt

            result += '\n'
        else:
            result = txt

        return result


class MyRawConfigParser(cp.RawConfigParser):
    def read(self, filename):
        with FileReadLineStrip(filename) as fp:
            result = cp.RawConfigParser.readfp(self, fp, filename)

        return result

    def readfp(self, file_object):
        result = self.read(str(file_object.name))

        return result
