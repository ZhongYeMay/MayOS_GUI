import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import os,json

#language choice, hell, sleepy
# 18th.May,2025 01:21
# finished
while True:
    if os.path.exists("system/lang/default_lang.txt"):
        with open("system/lang/default_lang.txt", "r", encoding = "utf-8") as lang:
            lang = lang.read()
            messagebox.showinfo("Tip", message="The language is "+lang)
        break
    else:
        with open("system/info/ver", "r", encoding = "utf-8") as ver:
            ver = ver.read()
        print("[System]               Please choose display language:")
        print("[System]               1.English(USA)")
        print("[System]               2.Chinese Simplified")
        print("[System]               3.Traditional Chinese(Taiwan,HongKong,Macau)")
        print("[System]               The MayOS_GUI Version is "+ ver)
        lang_choice = input("[System]Your choice >>>")
        if lang_choice == "1":
            with open("system/lang/default_lang.txt", "w", encoding="utf-8") as lang:
                lang = lang.write("en_us")
        elif lang_choice == "2":
            with open("system/lang/default_lang.txt", "w", encoding="utf-8") as lang:
                lang = lang.write("zh_cn")
        elif lang_choice == "3":
            with open("system/lang/default_lang.txt", "w", encoding="utf-8") as lang:
                lang = lang.write("zh_thm")
# finished
# tested

def load_sytemsmsg(index):
    """从JSON文件中读取指定索引的提示信息"""
    global lang
    with open('system/lang/systems.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data['systems_'+lang][index-1]
def load_regmsg(index):
    """从JSON文件中读取指定索引的提示信息"""
    global lang
    with open('system/lang/regs.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data['regs_'+lang][index-1]

#command line oobe, not finished yet :)
#but with a little gui :(
while True:
    if os.path.exists("files/users/pswd.txt") & os.path.exists("files/users/name.txt"):
        messagebox.showinfo(load_sytemsmsg(1), message=load_regmsg(1))
        break
    else:
        username = str(input(load_regmsg(2)))
        usna_2nd = str(input(load_regmsg(3)))
        password = str(input(load_regmsg(4)))
        pswd_2nd = str(input(load_regmsg(5)))
        if password == pswd_2nd and username == usna_2nd:
            with open("files/users/pswd.txt", 'w', encoding = 'utf-8') as pswd:
                pswd.write(password)
            with open("files/users/name.txt", 'w', encoding = 'utf-8') as name:
                name.write(username)
            messagebox.showinfo(load_sytemsmsg(1), message=load_regmsg(6))
            break
        else:
            messagebox.showerror(load_sytemsmsg(2), message=load_regmsg(7))
            continue
    #username&password


MayOS_start = tk.Tk()
MayOS_start.geometry("300x100")#分辨率

MayOS_start.mainloop()