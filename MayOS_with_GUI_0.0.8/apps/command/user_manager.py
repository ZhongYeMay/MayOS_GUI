# 用户管理模块
import json
import os
from apps.command.aes_ecb_enc import AESCipher

class UserManager:
    USER_FILE = os.path.join(os.getcwd(), 'files', 'users', 'users.json')
    AES_KEY = b'MayOS2025AESKey!!'  # 16字节密钥

    @staticmethod
    def load_users():
        if not os.path.exists(UserManager.USER_FILE):
            os.makedirs(os.path.dirname(UserManager.USER_FILE), exist_ok=True)
            # 默认用户
            users = {'test': '123456'}
            enc_users = {}
            cipher = AESCipher(UserManager.AES_KEY)
            for u, p in users.items():
                enc_users[cipher.encrypt(u)] = cipher.encrypt(p)
            with open(UserManager.USER_FILE, 'w', encoding='utf-8') as f:
                json.dump(enc_users, f)
            return users
        with open(UserManager.USER_FILE, 'r', encoding='utf-8') as f:
            enc_users = json.load(f)
        cipher = AESCipher(UserManager.AES_KEY)
        users = {}
        for enc_u, enc_p in enc_users.items():
            try:
                u = cipher.decrypt(enc_u)
                p = cipher.decrypt(enc_p)
                users[u] = p
            except Exception:
                continue
        return users

    @staticmethod
    def verify_user(username, password):
        users = UserManager.load_users()
        return users.get(username) == password

    @staticmethod
    def add_user(username, password):
        users = UserManager.load_users()
        if username in users:
            return False
        users[username] = password
        cipher = AESCipher(UserManager.AES_KEY)
        enc_users = {cipher.encrypt(u): cipher.encrypt(p) for u, p in users.items()}
        with open(UserManager.USER_FILE, 'w', encoding='utf-8') as f:
            json.dump(enc_users, f)
        return True

    @staticmethod
    def get_all_users():
        return list(UserManager.load_users().keys())
