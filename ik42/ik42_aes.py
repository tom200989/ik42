import base64
from Crypto.Cipher import AES
import hashlib

class AES_Tool:

    def encrypt_ECB(self, key, data):
        """
        ECB 加密
        :param key: 密钥
        :param data: 需加密数据
        :return: 密文
        """
        # 非空判断
        if key is None or data is None or key is '' or data is '':
            print('请提供key和data')
            return
        # 16位整数倍判断
        if not len(key) == 16:
            print('key需要满足16位条件')
            return

        # 匿名内部类 - 填充['\0']到末尾
        pad = lambda s: s + '\0'
        # 填充data末尾
        data = pad(data)
        # 创建AES对象
        cipher = AES.new(key.encode('utf8'), AES.MODE_ECB)
        encrypt_byte = cipher.encrypt(data.encode('utf8'))
        # B64编码
        b64_encrypt_byte = base64.b64encode(encrypt_byte)
        # UTF8解码
        final_text = b64_encrypt_byte.decode('utf8')
        return final_text

    def decrypt_ECB(self, key, data):
        """
        ECB 解密
        :param key: 密钥
        :param data: 需解密内容
        :return: 明文
        """
        # 非空判断
        if key is None or data is None or key is '' or data is '':
            print('请提供key和data')
            return
        # 16位整数倍判断
        if not len(key) == 16:
            print('key需要满足16位条件')
            return

        # UTF8加码
        data = data.encode('utf8')
        # B64解码
        b64_decode_byte = base64.decodebytes(data)
        # 创建AES对象
        cipher = AES.new(key.encode('utf8'), AES.MODE_ECB)
        # 解密
        decrypt_byte = cipher.decrypt(b64_decode_byte)
        # 匿名内部类 - 倒叙取出末尾
        uppad = lambda s: s[0:-1]
        decrypt_text = uppad(decrypt_byte)
        # UTF8解码
        final_text = decrypt_text.decode('utf8')
        return final_text

    def encryt_CBC(self, key, data, iv):
        """
        CBC 加密
        :param key: 密钥
        :param data: 需加密数据
        :param iv: 偏移量
        :return: 密文
        """
        # 非空判断
        if key is None or data is None or key is '' or data is '':
            print('请提供key和data')
            return
        # 16位整数倍判断
        if not len(key) == 16:
            print('key需要满足16位条件')
            return

        # 匿名内部类 - 填充16整数倍长度
        pad = lambda s: s + (16 - len(s) % 16) * chr(16 - len(s) % 16)
        # 填充data末尾
        data = pad(data)
        # 创建AES对象
        cipher = AES.new(key.encode('utf8'), AES.MODE_CBC, iv.encode('utf8'))
        encrypt_byte = cipher.encrypt(data.encode('utf8'))
        # B64编码
        b64_encrypt_byte = base64.b64encode(encrypt_byte)
        # UTF8解码
        final_text = b64_encrypt_byte.decode('utf8')
        return final_text

    def decrypt_CBC(self, key, data, iv):
        """
        CBC 解密
        :param key: 密钥
        :param data: 需解密数据
        :param iv: 偏移量
        :return: 明文
        """
        # 非空判断
        if key is None or data is None or key is '' or data is '':
            print('请提供key和data')
            return  # 16位整数倍判断
        if not len(key) == 16:
            print('key需要满足16位条件')
            return

        # UTF8加码
        data = data.encode('utf8')
        # B64解码
        b64_decode_byte = base64.decodebytes(data)
        # 创建AES对象
        cipher = AES.new(key.encode('utf8'), AES.MODE_CBC, iv.encode('utf8'))
        # 解密
        decrypt_byte = cipher.decrypt(b64_decode_byte)
        # 匿名内部类 - 倒叙取出末尾
        uppad = lambda s: s[0:-s[-1]]
        decrypt_byte = uppad(decrypt_byte)
        # UTF8解码
        final_text = decrypt_byte.decode('utf8')
        return final_text

if __name__ == '__main__':
    key = 'ABCDhij123abefgf'
    data = '015693000001169'
    iv = '0000000000000000'

    encrypt_CBC = AES_Tool().encryt_CBC(key, data, iv)
    print("CBC加密结果: ", encrypt_CBC)

    decrypt_CBC = AES_Tool().decrypt_CBC(key, encrypt_CBC, iv)
    print("CBC解密结果: ", decrypt_CBC)

    encrypt_ECB = AES_Tool().encrypt_ECB(key, data)
    print("ECB加密结果: ", encrypt_ECB)

    decrypt_ECB = AES_Tool().decrypt_ECB(key, encrypt_ECB)
    print("ECB解密结果: ", decrypt_ECB)
