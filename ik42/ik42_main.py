import sys, os
sys.path.append("..")
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']

from PyQt5.Qt import *
from ik42.res._strings import *
from ik42.res._qss import *
from ik42.res._image_rcc import *
from ik42.ik42_utils import *
from ik42.ik42_http import *
import requests
from ik42.wheel import *
from ik42.ik42_file import *
from ik42.ik42_cofig import *
import webbrowser
import time

class ik42_main(QWidget):

    def __init__(self):
        super().__init__()
        self.desktop = QApplication.desktop()  # 桌面对象
        self.sw = ik42_utils.getScreenSize()[0]  # 桌面宽
        self.sh = ik42_utils.getScreenSize()[1]  # 桌面高
        self.ww = 500
        self.wh = 300
        self.mw = int((self.sw - self.ww) * 0.5)  # 控件偏移量x
        self.mh = int((self.sh - self.wh) * 0.5)  # 控件偏移量y
        self.middleHorizotol = self.ww / 2

        self.bgw = QWidget(self)  # 背景
        # 设置点击背景时抢夺comboBox焦点
        self.bgw.mouseReleaseEvent = lambda event: self.bgw.setFocus()

        # 设置固定大小
        self.setFixedSize(self.ww, self.wh)
        self.bgw.setFixedSize(self.ww, self.wh)  # 大小与window一样
        # 移动到屏幕中间
        self.move(self.mw, self.mh)
        # 设置无边框
        self.setWindowFlag(Qt.FramelessWindowHint)
        # 设置样式
        self.bgw.setStyleSheet(QSS.background_all)
        # 被轮询的响应体
        self.responceDict = None

        # 页面
        self.NORMAL = 1
        self.STATE = 2
        self.LOADING = 3

        # 状态
        self.SUCCESS = 0
        self.FAILED = 1
        self.TIMEOUT = 2

        # 读取IMEI集合
        self.imeis = ik42_file().read_imei(getpath())
        self.imeis.reverse()

        # 建立元素
        self.tvIK42 = QLabel(self)
        self.ivIK42 = QLabel(self)
        self.cbIMEI = QComboBox(self)
        self.tvTip = QLabel(self)
        self.btVerify = QPushButton(self)
        self.tvCopr = QLabel(self)
        self.tvClose = QLabel(self)
        self.ivBack = QPushButton(self)

        self.ivState = QLabel(self)
        self.tvState = QLabel(self)
        self.btStateOk = QPushButton(self)

        self.wheel = Wheel(3, self)

        # 分组
        self.widgets = [  #
            {"idx": self.NORMAL, "elements": [self.tvIK42, self.ivIK42, self.cbIMEI, self.btVerify]},  # 首现元素
            {"idx": self.STATE, "elements": [self.ivState, self.tvState, self.btStateOk]},  # 状态元素
            {"idx": self.LOADING, "elements": [self.wheel, self.cbIMEI, self.btVerify]},  # 等待元素
        ]

        # 初始化线程
        self.ik42_http = None

        # 设置元素属性
        self.setAttr()
        # todo 初始显示元素组
        self.showOrHide(self.NORMAL)
        # todo 测试状态
        self.turnState(self.SUCCESS)
        # 设置移动初始值
        self.initMove()
        pass

    """设置移动初始值"""
    def initMove(self):
        # 1.加入一个标记位 -- 防止开启了鼠标追踪导致的崩溃, 因为鼠标追踪会先执行 mouseMoveEvent
        self.isMouseDown = False
        self.mouse_x = 0
        self.mouse_y = 0
        self.window_x = 0
        self.window_y = 0

    """设置鼠标按下监听"""
    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        # 判断鼠标按下的是否为左键
        if a0.button() == Qt.LeftButton:
            # 1.加入一个标记位 -- 防止开启了鼠标追踪导致的崩溃, 因为鼠标追踪会先执行 mouseMoveEvent
            self.isMouseDown = True
            # 2.记录鼠标按下的坐标
            self.mouse_x = a0.globalX()
            self.mouse_y = a0.globalY()
            # 3.记录当前窗口左上角点的坐标
            self.window_x = self.x()  # 注意这一句不能用globalX, 因为这里的self不是Event对象
            self.window_y = self.y()  # 注意这一句不能用globalY, 因为这里的self不是Event对象

    """设置鼠标移动监听"""
    def mouseMoveEvent(self, a0: QtGui.QMouseEvent) -> None:
        # 这里做出按下的判断 -- 只有按下时才去拖动
        if self.isMouseDown:
            # 4.获取新的鼠标点
            move_x = a0.globalX() - self.mouse_x
            move_y = a0.globalY() - self.mouse_y
            # 5.计算window需要移动的横纵距离
            window_new_x = self.window_x + move_x
            window_new_y = self.window_y + move_y
            # 6.开始move
            self.move(window_new_x, window_new_y)

    """设置鼠标释放监听"""
    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        # 7.当鼠标松开后 -- 恢复标记位
        self.isMouseDown = False

    '''设置指定元素组可见 @idx: 业务需要显示的索引组标号'''
    def showOrHide(self, idx):
        # 对回退键特殊处理
        if idx == self.STATE:
            self.ivBack.setVisible(True)
        else:
            self.ivBack.setHidden(True)
        # 先隐藏全部
        allWidgets = []
        for widict in self.widgets:
            allWidgets.extend(widict['elements'])
        for ele in allWidgets:
            ele.setHidden(True)
            if type(ele) == Wheel:
                ele.stopWheel()

        # 再显示指定的元素
        for widict in self.widgets:
            for element in widict['elements']:
                if widict['idx'] == idx:
                    element.setVisible(True)
                    if type(element) == Wheel:  # 当前是滚轮
                        if idx == self.LOADING:  # 且当前要求滚轮显示
                            element.startWheel()
                        else:
                            element.stopWheel()

    '''切换状态UI'''
    def turnState(self, state):
        if state == self.SUCCESS:  # 成功
            self.ivState.setStyleSheet(QSS.iv_ik42_success)
            self.tvState.setText(Strings.all_operation_are_success)
            self.btStateOk.setFixedSize(80, 30)
            self.btStateOk.setText(Strings.ok)
            self.ivBack.setHidden(True)
        elif state == self.FAILED:  # 失败
            self.ivState.setStyleSheet(QSS.iv_ik42_error)
            self.tvState.setText(Strings.unfortunately_the_verification)
            self.btStateOk.setFixedSize(100, 30)
            self.btStateOk.setText(Strings.try_again)
            self.ivBack.setVisible(True)
            self.cbIMEI.setEnabled(True)
            self.btVerify.setEnabled(True)
        elif state == self.TIMEOUT:  # 超时
            self.ivState.setStyleSheet(QSS.iv_ik42_timeout)
            self.tvState.setText(Strings.the_current_network)
            self.btStateOk.setFixedSize(100, 30)
            self.btStateOk.setText(Strings.try_again)
            self.ivBack.setVisible(True)
            self.cbIMEI.setEnabled(True)
            self.btVerify.setEnabled(True)

        self.btStateOk.move(self.middleHorizotol - self.btStateOk.width() / 2, self.tvState.geometry().y() + self.tvState.height() + 10)

    '''设置元素属性'''
    def setAttr(self):
        # 等待圈
        self.wheel.setFixedSize(60, 60)
        self.wheel.move(int(self.middleHorizotol - self.wheel.width() / 2), 50)

        # ivState : 状态
        self.ivState.setFixedSize(60, 60)
        self.ivState.setStyleSheet(QSS.iv_ik42_success)
        self.ivState.move(self.middleHorizotol - self.ivState.width() / 2, 50)

        # tvState : 状态提示
        self.tvState.setFixedSize(self.ww, 60)
        self.tvState.setAlignment(Qt.AlignCenter)
        self.tvState.setStyleSheet(QSS.tv_ik42_state)
        self.tvState.move(0, self.ivState.geometry().y() + self.tvState.height() + 10)
        self.tvState.setText(Strings.all_operation_are_success)

        # tvStateOK
        self.btStateOk.setFixedSize(80, 30)
        self.btStateOk.setStyleSheet(QSS.bt_ik42_ok_try_again)
        self.btStateOk.setText(Strings.ok)
        self.btStateOk.move(self.middleHorizotol - self.btStateOk.width() / 2, self.tvState.geometry().y() + self.tvState.height() + 10)
        self.btStateOk.clicked.connect(lambda: self.click_state(self.btStateOk.text()))

        # tvIk42 : LOGO
        self.tvIK42.setFixedSize(150, 32)
        self.tvIK42.setAlignment(Qt.AlignRight)
        self.tvIK42.setText("LINK KEY")
        self.tvIK42.setStyleSheet(QSS.tv_ik42_logo)
        self.tvIK42.move(self.middleHorizotol - self.tvIK42.width() / 2, 50)
        # ivIK42 : LOGO
        # self.ivIK42.setFixedSize(82, 47)
        # self.ivIK42.setStyleSheet(QSS.iv_ik42_u_pan)
        # self.ivIK42.move(self.middleHorizotol+50, 50 - (self.ivIK42.height() - self.tvIK42.height()) / 2)
        # cbIMEI : 输入框
        self.cbIMEI.setFixedSize(300, 32)
        self.cbIMEI.setEditable(True)
        self.cbIMEI.setStyleSheet(QSS.cb_ik42_imei)
        self.cbIMEI.move(self.getCenterX(self.cbIMEI), 130)
        self.cbIMEI.setMaxVisibleItems(5)
        self.cbIMEI.lineEdit().setMaxLength(15)
        self.cbIMEI.lineEdit().setAlignment(Qt.AlignCenter)
        self.cbIMEI.lineEdit().setPlaceholderText(Strings.please_input_your_15)
        self.cbIMEI.editTextChanged.connect(lambda text: self.cbChange(text))
        self.cbIMEI.setValidator(QRegExpValidator(QRegExp("[0-9]+$")))
        if len(self.imeis) == 0:
            self.cbIMEI.setCurrentIndex(-1)
            self.ivIK42.setFocus()  # 设置其他控件抢夺焦点
        else:
            self.cbIMEI.setCurrentIndex(1)
            self.cbIMEI.addItems(self.imeis)
        # tvTip : 提示
        self.tvTip.setFixedSize(300, 18)
        self.tvTip.setHidden(True)
        self.tvTip.setStyleSheet(QSS.tv_ik42_tip)
        self.tvTip.move(self.cbIMEI.geometry().x(), self.cbIMEI.geometry().y() + self.cbIMEI.height() + 5)
        self.tvTip.setAlignment(Qt.AlignCenter)
        self.tvTip.setText(Strings.you_must_provide)
        # btVerify : 认证按钮(点击)
        self.btVerify.setFixedSize(32, 32)
        btx = self.cbIMEI.geometry().x() + self.cbIMEI.width() + 10
        bty = self.cbIMEI.geometry().y()
        self.btVerify.move(btx, bty)
        self.btVerify.setStyleSheet(QSS.bt_ik42_verify)
        self.btVerify.clicked.connect(self.clickVerify)
        # tvCopr : 版权
        self.tvCopr.setFixedSize(self.ww, 18)
        self.tvCopr.move(0, self.wh - self.tvCopr.height())
        self.tvCopr.setAlignment(Qt.AlignCenter)
        self.tvCopr.setText(Strings.copr_tcl_all_rights)
        self.tvCopr.setStyleSheet(QSS.tv_ik42_copr)
        # tvClose : 关闭
        self.tvClose.setFixedSize(32, 32)
        self.tvClose.setText("x")
        self.tvClose.move(self.ww - self.tvClose.width(), 0)
        self.tvClose.setStyleSheet(QSS.tv_ik42_close)
        self.tvClose.mouseReleaseEvent = lambda event: self.exitSys()
        # ivBack : 回退
        self.ivBack.setFixedSize(20, 20)
        self.ivBack.move(8, 8)
        self.ivBack.setStyleSheet(QSS.iv_ik42_back)
        self.ivBack.setHidden(True)
        self.ivBack.clicked.connect(lambda: self.showOrHide(self.NORMAL))

    '''根据状态决定按钮的行为'''
    def click_state(self, btText):
        if btText == Strings.ok:
            self.exitSys()
        elif btText == Strings.try_again:
            # 再次指定请求逻辑
            self.clickVerify()

    '''输入框焦点发生改变'''
    def cbChange(self, text):
        if len(text) == 0:
            self.cbIMEI.clearEditText()
            self.ivIK42.setFocus()

    '''点击认证'''
    def clickVerify(self):
        cbText = self.cbIMEI.currentText()
        if cbText is None or cbText == "":
            self.tvTip.setVisible(True)
            self.tvTip.setText(Strings.you_must_provide)
        elif len(cbText) < 15:
            self.tvTip.setVisible(True)
            self.tvTip.setText(Strings.digit_imei_is_required)
        else:
            self.tvTip.setHidden(True)
            self.cbIMEI.setEnabled(False)
            self.btVerify.setEnabled(False)
            print("req imei = " + cbText)
            self.reqIK42(cbText)

    '''启动请求'''
    def reqIK42(self, imei):
        # 显示等待圈动画
        self.showOrHide(self.LOADING)
        # 此处用信号的目的是防止用time模块会导致线程卡死的问题
        self.wheel.wheelSignal.connect(lambda loop: self.send_req(loop, imei))

    '''发起请求'''
    def send_req(self, loop, imei):
        if loop > 1:
            # 此处一定要先释放
            if self.ik42_http is None:
                self.ik42_http = ik42_http(self, imei)
                self.ik42_http.httpSignal.connect(lambda resDict: self.anays_statu_code(resDict))
            else:
                self.ik42_http.refresh(imei)

            # 启动线程
            self.ik42_http.start()

    '''分析状态码'''
    def anays_statu_code(self, resDict):
        # 得到状态码
        statu_code = resDict[responceCodeField]
        imei = resDict[imeiCode]
        # 无响应
        if statu_code == 707:
            # 停止等待圈动画 + 连接超时UI
            self.showOrHide(self.STATE)
            self.turnState(self.TIMEOUT)
            # self.ik42_http.quit()  # 此处一定要退出子线程
            pass

        # 有响应
        elif statu_code == 200:
            if testApi is True:
                # 停止等待圈动画 + 显示成功UI + 缓存IMEI到本地
                self.showOrHide(self.STATE)
                self.turnState(self.SUCCESS)
                webbrowser.open("http://192.168.2.1")
                # 关闭软件
                self.btStateOk.setEnabled(False)
                time.sleep(2)
                self.exitSys()
            else:
                self.Ik42_responce(imei, resDict)

        else:
            # 停止等待圈动画 + 显示失败UI
            self.showOrHide(self.STATE)
            self.turnState(self.FAILED)

    '''响应码为200时 - 判断FW响应状态'''
    def Ik42_responce(self, imei, resDict):
        # 判断状态码
        result = resDict['result']
        if result is not None:  # 正常返回
            ResultCode = result['ResultCode']
            if ResultCode is not None:
                if ResultCode == self.SUCCESS:  # 成功
                    # 停止等待圈动画 + 显示成功UI + 缓存IMEI到本地
                    self.showOrHide(self.STATE)
                    self.turnState(self.SUCCESS)
                    # 保存IMEI到本地
                    if imei not in self.imeis:
                        ik42_file().write_imei(getpath(), imei)
                    # 打开网域
                    webAddress = result['WebAddress']
                    if not 'http' in webAddress:
                        url = 'http://' + webAddress
                    else:
                        url = webAddress
                    webbrowser.open(url)
                    self.ik42_http.quit()
                    # 关闭软件
                    self.btStateOk.setEnabled(False)
                    time.sleep(2)
                    self.exitSys()

                elif ResultCode == self.FAILED:  # 失败
                    # 停止等待圈动画 + 显示失败UI
                    self.showOrHide(self.STATE)
                    self.turnState(self.FAILED)
                    # self.ik42_http.quit()  # 此处一定要退出子线程
                    pass

                else:  # 超时
                    # 停止等待圈动画 + 连接超时UI
                    self.showOrHide(self.STATE)
                    self.turnState(self.TIMEOUT)
                    # self.ik42_http.quit()  # 此处一定要退出子线程
                    pass

        else:  # 接口错误
            # 停止等待圈动画 + 显示失败UI
            self.showOrHide(self.STATE)
            self.turnState(self.TIMEOUT)

    '''模拟comboBox数据'''
    def test(self):
        self.cbIMEI.addItem("012345678901232")
        self.cbIMEI.addItem("012345678901232")
        self.cbIMEI.addItem("012345678901233")
        self.cbIMEI.addItem("012345678901233")
        self.cbIMEI.addItem("012345678901233")
        self.cbIMEI.addItem("012345678901233")
        self.cbIMEI.addItem("012345678901233")
        self.cbIMEI.addItem("012345678901233")
        self.cbIMEI.addItem("012345678901233")

    '''控件居中的x坐标'''
    def getCenterX(self, childWidget):
        return (self.ww - childWidget.width()) / 2

    '''关闭退出'''
    def exitSys(self):
        # 关闭窗口
        self.close()
        sys.exit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    page_main = ik42_main()
    page_main.show()
    sys.exit(app.exec_())
