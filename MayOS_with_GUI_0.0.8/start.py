import tkinter as tk
from tkinter import messagebox
import os
import sys
from apps.command.user_manager import UserManager
from apps.command.register_manager import RegisterManager

def startup_register_and_login():
    user_file = os.path.join(os.getcwd(), 'files', 'users', 'users.json')
    root = tk.Tk()
    root.withdraw()
    if not os.path.exists(user_file):
        messagebox.showinfo("首次使用", "未检测到用户文件，请先注册用户！")
        reg_window = tk.Toplevel()
        reg_window.title("用户注册")
        reg_window.geometry("300x180")
        reg_window.resizable(False, False)
        reg_success = {'flag': False}
        tk.Label(reg_window, text="用户名:").pack(pady=5)
        username_entry = tk.Entry(reg_window)
        username_entry.pack(pady=5)
        tk.Label(reg_window, text="密码:").pack(pady=5)
        password_entry = tk.Entry(reg_window, show="*")
        password_entry.pack(pady=5)
        def do_register():
            username = username_entry.get()
            password = password_entry.get()
            success, msg = RegisterManager.register_user(username, password)
            if success:
                messagebox.showinfo("注册成功", msg)
                reg_success['flag'] = True
                reg_window.destroy()
            else:
                messagebox.showerror("注册失败", msg)
        reg_btn = tk.Button(reg_window, text="注册", command=do_register)
        reg_btn.pack(pady=10)
        reg_window.protocol("WM_DELETE_WINDOW", lambda: (root.destroy(), sys.exit(0)))
        root.wait_window(reg_window)
        if not reg_success['flag']:
            root.destroy()
            sys.exit(0)
    # 注册后或已存在用户文件，弹出登录
    login_window = tk.Toplevel()
    login_window.title("用户登录")
    login_window.geometry("300x220")
    login_window.resizable(False, False)
    login_success = {'flag': False}
    tk.Label(login_window, text="用户名:").pack(pady=5)
    # 获取所有用户名
    user_list = UserManager.get_all_users()
    username_var = tk.StringVar()
    if user_list:
        username_var.set(user_list[0])
    username_menu = tk.OptionMenu(login_window, username_var, *user_list)
    username_menu.pack(pady=5)
    tk.Label(login_window, text="密码:").pack(pady=5)
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack(pady=5)
    def do_login():
        username = username_var.get()
        password = password_entry.get()
        if UserManager.verify_user(username, password):
            login_success['flag'] = True
            login_window.destroy()
            root.destroy()
        else:
            messagebox.showerror("登录失败", "用户名或密码错误！")
            root.destroy()
            sys.exit(0)
    login_btn = tk.Button(login_window, text="登录", command=do_login)
    login_btn.pack(pady=10)
    login_window.protocol("WM_DELETE_WINDOW", lambda: (root.destroy(), sys.exit(0)))
    root.mainloop()
    return login_success['flag']

if __name__ == "__main__":
    if startup_register_and_login():
        # 授权后启动主程序
        os.environ['MAYOS_AUTHORIZED'] = '1'
        os.system(f'python main.py')
    else:
        print("未经授权的启动，强制退出！")
        sys.exit(0)
