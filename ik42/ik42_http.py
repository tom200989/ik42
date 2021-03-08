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
from Crypto.Cipher import AES
import base64
import hashlib

responceCodeField = "responceCode"
testApi = False  # 测试

class ik42_http(QThread):
    httpSignal = pyqtSignal(dict)
    def __init__(self, parent, imei):
        super().__init__(parent)
        self.imei = imei
        self.responceCodeField = "responceCode"
        self.timeout_tick = 15
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

    # AES MD5 加密
    def encryByAesMd5(self, imei):
        # 先进行AES加密
        cipher  = AES.new(self.aes_key.encode('utf8'), AES.MODE_CBC, self.aes_iv.encode('utf8'))
        encrypt_imei = cipher.encrypt(imei.encode('utf8'))
        b64_imei = base64.b64encode(encrypt_imei)
        enc_imei = b64_imei.decode('utf8')
        # 在MD5加密
        md5_ecn_imei = hashlib.md5(enc_imei).hexdigest()
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

        except Exception as error:
            print(error)
            textDict[self.responceCodeField] = self.STATU_CODE_TIMEOUT  # 超时返回707

        self.httpSignal.emit(textDict)  # 发送信号

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = QWidget()
    widget.resize(640, 480)
    widget.setWindowTitle("Hello, PyQt5!")

    httpThread = ik42_http(widget, "015693000001169")
    httpThread.httpSignal.connect(lambda dic: print(dic))
    httpThread.start()

    widget.show()
    sys.exit(app.exec())
