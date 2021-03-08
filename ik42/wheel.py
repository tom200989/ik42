import sys, os
sys.path.append("..")
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
from PyQt5 import QtGui
from PyQt5.Qt import *
from ik42.res._image_rcc import *

class Wheel(QLabel):
    wheelSignal = pyqtSignal(int)

    def __init__(self, speed=10, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 1.初始化角度和图片
        self.speed = speed
        self.cnt = 0
        self.loop_tick = 0  # 转过的圈数
        # 2.新建定时器对象
        self.timer = QTimer()
        self.timer.setInterval(self.speed)
        # self.timer.start()
        # 3.信号连接到槽
        self.timer.timeout.connect(self.onTimerOut)
        self.mouseReleaseEvent = lambda event: self.mouse_control()

    '''提供一个方法用于鼠标点击控制(用于测试)'''
    def mouse_control(self):
        if self.timer.isActive():
            self.timer.stop()
        else:
            self.timer.start()

    '''启动转动'''
    def startWheel(self):
        self.loop_tick = 0
        if self.timer.isActive() is False:
            self.timer.start()
            print("wheel start")

    '''停止转动'''
    def stopWheel(self):
        self.loop_tick = 0
        if self.timer.isActive() is True:
            self.timer.stop()
            print("wheel stop")

    # 4.定义槽
    def onTimerOut(self):
        self.update()  # 调用update会触发paintEvent()

    # 1.重写方法
    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        # 2.创建画家
        painter = QPainter(self)
        # 3.设置抗锯齿
        painter.setRenderHint(QPainter.Antialiasing)
        # 4.设置旋转角度和旋转轴
        painter.translate(self.width() / 2, self.height() / 2)  # 这里设置画家绘制原点便宜
        painter.rotate(self.cnt)  # 旋转画家角度
        painter.translate(-self.width() / 2, -self.height() / 2)  # 此处需要恢复画家为原点
        # 5.设定图片
        pixmap = QPixmap(":/ik42/ik42_loading.png")
        # 6.绘制图片
        painter.drawPixmap(QRect(0, 0, self.width(), self.height()), pixmap)
        # 7.旋转角度大于一圈, 恢复0度
        if self.cnt >= 360:
            self.cnt = 0
            self.loop_tick += 1
            self.wheelSignal.emit(self.loop_tick)
        else:
            self.cnt += 1

if __name__ == '__main__':
    app = QApplication(sys.argv)
    wheel = Wheel()
    wheel.resize(150, 150)
    wheel.show()
    # 开启应用程序, 开启消息循环
    sys.exit(app.exec_())
