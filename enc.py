import hashlib
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# 用密码派生出固定 key 和 nonce
def get_key_nonce(password: str):
    password_bytes = password.encode()
    key = hashlib.sha256(password_bytes).digest()        # 32字节 key
    nonce = hashlib.md5(password_bytes).digest()[:12]     # 12字节 nonce
    return key, nonce

# 获取密码并初始化加密器
password = input("请输入用于加密的密码：")
key, nonce = get_key_nonce(password)
aesgcm = AESGCM(key)

# 循环读取并加密字符串
while True:
    try:
        plaintext = input("请输入要加密的字符串（Ctrl+C 退出）：").encode()
        ciphertext = aesgcm.encrypt(nonce, plaintext, None)
        encoded = base64.b64encode(ciphertext).decode()
        print("加密结果：", encoded)
    except KeyboardInterrupt:
        print("\n程序已退出。")
        break
    except Exception as e:
        print("加密失败：", e)
