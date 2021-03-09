import sys, os
sys.path.append("..")
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']

from PyQt5 import QtGui
from PyQt5.Qt import *
from ik42.res._strings import *
from ik42.res._qss import *
from ik42.res._image_rcc import *
from ik42.ik42_utils import *
import requests
import json
import hashlib
from ik42.ik42_aes import *

responceCodeField = "responceCode"
imeiCode = "imeiCode"
testApi = False  # 测试

class ik42_http(QThread):
    httpSignal = pyqtSignal(dict)
    def __init__(self, parent, imei):
        super().__init__(parent)
        self.imei = imei
        self.responceCodeField = "responceCode"
        self.imeiCode = "imeiCode"
        self.timeout_tick = 2
        self.STATU_CODE_TIMEOUT = 707
        self.STATU_CODE_OK = 200
        self.host = "192.168.2.1"
        self.aes_key = "ABCDhij123abefgf"
        self.aes_iv = "0000000000000000"

        if testApi is True:
            self.host = '192.168.2.1'
            self.apiImpl = "GetLoginState"
        else:
            self.host = '192.168.1.1'
            self.apiImpl = "ToolCertification"

    # 重写run
    def run(self) -> None:
        self.post(self.imei)

    # 刷新IMEI号
    def refresh(self, new_imei):
        self.imei = new_imei

    # AES MD5 加密
    def encryByAesMd5(self, imei):
        # 先进行AES加密
        aes_imei = AES_Tool().encrypt_ECB(self.aes_key, imei)
        # 在MD5加密
        md5_ecn_imei = hashlib.md5(aes_imei.encode('utf8')).hexdigest()
        return md5_ecn_imei

    def post(self, imei):
        # 指定连接
        url = "http://" + self.host + "/jrd/webapi"
        # 指定头
        header = {  #
            "_TclRequestVerificationKey": "KSDHSDFOGQ5WERYTUIQWERTYUISDFG1HJZXCVCXBN2GDSMNDHKVKFsVBNf",  #
            "_TclRequestVerificationToken": "",  #
            "Host": self.host,  #
            "Origin": "http://" + self.host,  #
            "Referer": "http://" + self.host + "/",  #
            "Content-Type": "text/plain"  #
        }
        # 对IMEI号进行加密
        imei = self.encryByAesMd5(imei)
        print(imei)
        # 指定请求参数
        paramStr = '{"jsonrpc":"2.0","method":"' + self.apiImpl + '","params":{"imei":"' + imei + '"},"id":"5.4"}'
        # 转换成json
        paramJson = json.loads(paramStr)
        # 发起请求
        textDict = {}
        try:
            responce = requests.post(url, headers=header, json=paramJson, timeout=self.timeout_tick)
            if responce.status_code == self.STATU_CODE_OK:
                # 响应
                textstr = responce.text
                # 转换Json->Dict {"jsonrpc":"2.0","result":{"WebAddress":"192.168.1.1","ResultCode":0},"id":"5.4"}
                textDict = json.loads(textstr)
            # 填充响应码
            textDict[self.responceCodeField] = responce.status_code
            textDict[self.imeiCode] = self.imei

        except Exception as error:
            print(error)
            textDict[self.responceCodeField] = self.STATU_CODE_TIMEOUT  # 超时返回707
            textDict[self.imeiCode] = self.imei

        self.httpSignal.emit(textDict)  # 发送信号

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = QWidget()
    widget.resize(500, 300)
    widget.setWindowTitle("Hello, PyQt5!")

    httpThread = ik42_http(widget, "015693000001169")
    httpThread.httpSignal.connect(lambda dic: print(dic))
    httpThread.start()

    widget.show()
    sys.exit(app.exec())
