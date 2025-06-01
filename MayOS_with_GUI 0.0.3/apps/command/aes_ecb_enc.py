import random,os,json
from Crypto.Cipher import AES

def load_error(index):
    """从JSON文件中读取指定索引的提示信息"""
    with open('system/lang/error.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data['error'][index-1], data['numbers'][index-1]


#随机生成密钥
while True:
    if os.path.exists("files/users/enc_key.txt"):
        with open("files/users/enc_key.txt", "r", encoding = "utf-8") as enc_key:
            enc_key = enc_key.read()
            break
    else:
        rand_key = random.randint(16,128)
        with open("files/users/enc_key.txt", "w", encoding = "utf-8") as rand_key:
            rand_key = rand_key.write()
        continue

    #读取源文件
while True:
    if os.path.exists("files/users/pswd.txt") and os.path.exists("files/users/name.txt"):
        with open("files/users/pswd.txt", "r", encoding = "utf-8") as enc_pswd:
            enc_pswd = enc_pswd.read()
        with open("files/users/name.txt", "r", encoding = "utf-8") as enc_name:
            enc_name = enc_name.read()
        break
    else:
        print(load_error(1) + "当且系统未注册，请重新启动[start.py]以修复该问题。")
        print(load_error(1) + "1. 重新运行[start.py]")
        print(load_error(1) + "2. 退出MayOS_GUI")