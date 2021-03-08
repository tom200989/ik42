import sys, os
sys.path.append("..")
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
from PyQt5.Qt import *

class ik42_utils:
    """获取屏幕宽高"""
    @staticmethod
    def getScreenSize():
        desktop = QApplication.desktop()
        screenWidth = desktop.width()
        screenHeight = desktop.height()
        return [screenWidth, screenHeight]

