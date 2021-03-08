import sys, os
sys.path.append("..")
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']

from ik42.ik42_cofig import *

class ik42_file:

    def __init__(self):
        super().__init__()

    def write_imei(self, path, imei):
        file2 = open(path, "a+")
        file2.write(imei + '\n')
        file2.close()

    def read_imei(self, path):
        imeis = []
        try:
            file = open(path, 'r')
            with file as f:
                for content in f:
                    imeis.append(content.replace('\n', ''))
            file.close()
        except Exception as error:
            err = error.__str__()
            if 'No such file or directory' in err:
                self.create_imei(path)
        return imeis

    def create_imei(self, path):
        os.mkdir(imei_dir)
        file2 = open(path, "a+")
        file2.write('')
        file2.close()

if __name__ == '__main__':
    ikf = ik42_file()
    ikf.read_imei(imei_path)
    pass
