import hashlib
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def decrypt(ciphertext_b64: str, password: str) -> str:
    try:
        # 派生 key 和 nonce（和加密时保持一致）
        key = hashlib.sha256(password.encode()).digest()
        nonce = hashlib.md5(password.encode()).digest()[:12]

        # 解码密文
        ciphertext = base64.b64decode(ciphertext_b64)

        # 解密
        aesgcm = AESGCM(key)
        plaintext = aesgcm.decrypt(nonce, ciphertext, None)

        return plaintext.decode()

    except Exception as e:
        return f"❌ 解密失败：{str(e)}"
if __name__ == "__main__":
    enc_text = input("请输入加密后的密文（base64）：")
    pwd = input("请输入密码：")
    result = decrypt(enc_text, pwd)
    print("解密结果：", result)
