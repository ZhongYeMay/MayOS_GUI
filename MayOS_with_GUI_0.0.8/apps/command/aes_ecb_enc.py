class AESCipher:
    def __init__(self, key):
        self.key = key if isinstance(key, str) else key.decode('utf-8', errors='ignore')

    def encrypt(self, raw):
        # 简单可逆加密：异或+base64
        raw = str(raw)
        enc = ''.join(chr(ord(c) ^ ord(self.key[i % len(self.key)])) for i, c in enumerate(raw))
        return enc.encode('utf-8').hex()

    def decrypt(self, enc):
        try:
            enc_str = bytes.fromhex(enc).decode('utf-8')
            dec = ''.join(chr(ord(c) ^ ord(self.key[i % len(self.key)])) for i, c in enumerate(enc_str))
            return dec
        except Exception:
            return ''