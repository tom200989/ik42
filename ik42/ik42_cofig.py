import sys, os
sys.path.append("..")
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
import platform
import locale

# imei_dir = 'C:/ik42'
# imei_path = imei_dir + '/ik42.txt'

IMEI_ROOT_DIR_WIN = 'C:\\'
IMEI_ROOT_DIR_XNIX = '\\Applications'

imei_file_dir = 'ik41'
imei_file_name = 'ik41.txt'

def getpath():
    """
    获取imei文件的绝对路径
    :return: imei文件的绝对路径
    """
    if 'Windows' in platform.system():
        return os.path.join(IMEI_ROOT_DIR_WIN, imei_file_dir, imei_file_name)

    if 'Linux' in platform.system() or 'Unix' in platform.system():
        return os.path.join(IMEI_ROOT_DIR_XNIX, imei_file_dir, imei_file_name)

def getDir():
    """
    获取imei目录的绝对路径
    :return: imei目录的绝对路径
    """
    if 'Windows' in platform.system():
        return os.path.join(IMEI_ROOT_DIR_WIN, imei_file_dir)

    if 'Linux' in platform.system() or 'Unix' in platform.system():
        return os.path.join(IMEI_ROOT_DIR_XNIX, imei_file_dir)

def getLanguage():
    """
    获取系统语言
    :return: 系统语言
    """
    if 'Windows' in platform.system():
        return locale.getdefaultlocale()[0]

    if 'Linux' in platform.system() or 'Unix' in platform.system():
        return os.getenv('LANG')

'''
本软件可视化部分采用Qt引擎, 需要遵守以下规则:

0- python平台使用3.7

1- 打包文件采用pyinstaller进行打包 (需cd到ik42文件夹)
pyinstaller -F -w -i 你的ico图标的绝对路径.ico ik42_main.py
如: pyinstaller -F -w -i C:\project\python\ik42\ik42\ik42.ico ik42_main.py
如: pyinstaller -D -w -i C:\project\python\ik42\ik42\ik42.ico ik42_main2.py

采用 -F 即可打出绿色版(无压缩, 无DLL)的包, 缺点是启动较慢, 优点是安全
采用 -D 即可打出执行版(有压缩, 有DLL)的包, 缺点是不安全, 优点是启动快

2- Unix/Linux系统请按照对应平台更改[imei_dir][imei_path]路径

3- 需要安装的库包如下: (安装路径需要是当前工程的venv目录下, 必须!!)
    模块名                                 版本
    PyQt5	                            5.15.2
    PyQt5-Qt	                        5.15.2
    PyQt5-sip	                        12.8.1
    altgraph	                        0.17
    certifi	                            2020.12.5
    chardet	                            4.0.0
    click	                            7.1.2
    future	                            0.18.2
    idna	                            2.10
    importlib-metadata	                3.7.0
    pefile	                            2019.4.18
    pip	                                21.0.1
    pycryptodome	                    3.10.1
    pyinstaller	                        4.2
    pyinstaller-hooks-contrib	        2020.11
    pyqt5-plugins	                    5.15.2.2.0.1
    pyqt5-tools	                        5.15.2.3.0.2
    python-dotenv	                    0.15.0
    pywin32-ctypes	                    0.2.0
    qt5-applications	                5.15.2.2.1
    qt5-tools	                        5.15.2.1.0.1
    requests	                        2.25.1
    setuptools	                        54.0.0
    typing-extensions	                3.7.4.3
    urllib3	                            1.26.3
    zipp	                            3.4.1
    
4- ik42_http.py 可单独调试端口, 如有问题请自行debug

5- 切勿改动ik42_main.py 和 ik42_aes.py 以及res文件夹的任何代码或者文件命名
'''
