from Crypto.Cipher import AES
import base64
import hashlib

imei = "015693000001169"
aes_key = "ABCDhij123abefgf"
aes_iv = "0000000000000000"

# 先切割
clip_imei = lambda data: data + (16 - len(data.encode('utf8')) % 16) * chr(16 - len(data.encode('utf8')) % 16)
imei = clip_imei(imei)
print(imei)
# 创建AES对象
cipher = AES.new(aes_key.encode('utf8'), AES.MODE_CBC, aes_iv.encode('utf8'))
# 加密
encrypt_imei = cipher.encrypt(imei.encode('utf8'))
# Base64
b64_imei = base64.b64encode(encrypt_imei)
# enc_imei = b64_imei.decode('utf8')

# 最终结果
md5_ecn_imei = hashlib.md5(b64_imei).hexdigest()

print("python加密结果 = " + md5_ecn_imei, "; len = ", len(md5_ecn_imei))
