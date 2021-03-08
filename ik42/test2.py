import base64
from Crypto.Cipher import AES
import hashlib

# 密钥（key）, 密斯偏移量（iv） CBC模式加密

def AES_Encrypt(key, data, iv):
    pad = lambda s: s + (16 - len(s) % 16) * chr(16 - len(s) % 16)
    data = pad(data)
    # 字符串补位
    cipher = AES.new(key.encode('utf8'), AES.MODE_CBC, iv.encode('utf8'))
    encryptedbytes = cipher.encrypt(data.encode('utf8'))
    # 加密后得到的是bytes类型的数据
    encodestrs = base64.b64encode(encryptedbytes)
    # 使用Base64进行编码,返回byte字符串
    enctext = encodestrs.decode('utf8')
    # 对byte字符串按utf-8进行解码
    return enctext

def AES_Decrypt(key, data, iv):
    data = data.encode('utf8')
    encodebytes = base64.decodebytes(data)
    # 将加密数据转换位bytes类型数据
    cipher = AES.new(key.encode('utf8'), AES.MODE_CBC, iv.encode('utf8'))
    text_decrypted = cipher.decrypt(encodebytes)
    unpad = lambda s: s[0:-s[-1]]
    text_decrypted = unpad(text_decrypted)
    # 去补位
    text_decrypted = text_decrypted.decode('utf8')
    return text_decrypted

key = 'ABCDhij123abefgf'
data = '015693000001169'
iv = '0000000000000000'
AES_Encrypt(key, data, iv)
enctext = AES_Encrypt(key, data, iv)
print(enctext)

text_decrypted = AES_Decrypt(key, enctext,iv)
print(text_decrypted)

# MD5
md5_ecn_imei = hashlib.md5(enctext.encode("utf8")).hexdigest()
print(md5_ecn_imei)
