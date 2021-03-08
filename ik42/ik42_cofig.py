import sys, os
sys.path.append("..")
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']

imei_dir = 'C:/ik42'
imei_path = imei_dir + '/ik42.txt'
