# main.py

import tkinter as tk
from tkinter import messagebox, Menu, Frame
from tkinter.ttk import Label, Button
from PIL import Image, ImageTk
import os
import datetime
import requests
from apps.command.version_manager import VersionManager
from apps.command.wallpaper_manager import WallpaperManager
from apps.command.update_manager import UpdateManager
from apps.command.ai_manager import AIManager
from apps.command.user_manager import UserManager
from apps.command.register_manager import RegisterManager
from tkhtmlview import HTMLLabel
import subprocess
import json
from tkinter import simpledialog
import sys
from tkinter import Canvas

if __name__ == "__main__":
    # 检查是否由 start.py 授权启动
    if not os.environ.get('MAYOS_AUTHORIZED'):  # 可用环境变量或其他方式
        tk.Tk().withdraw()
        messagebox.showerror("错误", "未经授权的启动，强制退出！")
        print("未经授权的启动，强制退出！")
        sys.exit(0)

def update_clock():
    """更新右下角时钟"""
    current_time = datetime.datetime.now().strftime("%H:%M:%S\n"f"%Y/%m/%d")
    clock_label.config(text=current_time)
    clock_label.after(1000, update_clock)  # 每秒更新一次

def launch_ai_web():
    """启动AI网页应用"""
    if AIManager.launch_ai_web():
        status_bar.config(text="已启动AI网页应用")
    else:
        messagebox.showerror("错误", "启动AI网页应用失败")

def download_info():
    """从GitHub下载版本信息"""
    try:
        url = "https://maydos-team.github.io/about/6.txt"
        work = os.getcwd()
        download_dir = os.path.join(work, "system", "info")

        # 确保目录存在
        os.makedirs(download_dir, exist_ok=True)

        # 下载文件
        filename = os.path.join(download_dir, "version_info.txt")
        response = requests.get(url, timeout=10)
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"\n文件已下载到: {filename}")
    except Exception as e:
        print(f"下载失败: {e}")

def check_for_updates():
    """检查是否有新版本"""
    current_version = VersionManager.get_current_version()
    latest_version = UpdateManager.check_for_updates(current_version)
    if latest_version:
        messagebox.showinfo("更新可用", f"发现新版本 {latest_version}，当前版本 {current_version}。\n请访问官方网站下载更新。")
        AIManager.open_official_website()
    else:
        messagebox.showinfo("检查更新", "当前已是最新版本。")

def show_changelog():
    """显示更新日志"""
    changelog_content = VersionManager.get_changelog()
    changelog_window = tk.Toplevel()
    changelog_window.title("更新日志")
    changelog_window.geometry("800x600")
    html_label = HTMLLabel(changelog_window, html=changelog_content)
    html_label.pack(fill=tk.BOTH, expand=True)

def startup_check_for_updates():
    """启动时检查更新"""
    check_for_updates()

def launch_calc():
    """启动计算器应用"""
    try:
        subprocess.Popen(['python', os.path.join('apps', 'gui_test', 'calc.py')])
        status_bar.config(text="已启动计算器")
    except Exception as e:
        messagebox.showerror("错误", f"启动计算器失败: {e}")

def launch_music():
    """启动音乐播放器应用"""
    try:
        subprocess.Popen(['python', os.path.join('apps', 'gui_test', 'music.py')])
        status_bar.config(text="已启动音乐播放器")
    except Exception as e:
        messagebox.showerror("错误", f"启动音乐播放器失败: {e}")

current_user = None  # 当前登录用户

def register():
    """用户注册弹窗"""
    reg_window = tk.Toplevel()
    reg_window.title("用户注册")
    reg_window.geometry("300x180")
    reg_window.resizable(False, False)

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
            reg_window.destroy()
        else:
            messagebox.showerror("注册失败", msg)

    reg_btn = tk.Button(reg_window, text="注册", command=do_register)
    reg_btn.pack(pady=10)

def login():
    """用户登录弹窗"""
    global current_user
    login_window = tk.Toplevel()
    login_window.title("用户登录")
    login_window.geometry("300x220")
    login_window.resizable(False, False)

    tk.Label(login_window, text="用户名:").pack(pady=5)
    username_entry = tk.Entry(login_window)
    username_entry.pack(pady=5)

    tk.Label(login_window, text="密码:").pack(pady=5)
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack(pady=5)

    def do_login():
        username = username_entry.get()
        password = password_entry.get()
        if UserManager.verify_user(username, password):
            global status_bar
            current_user = username
            status_bar.config(text=f"已登录用户: {username}")
            messagebox.showinfo("登录成功", f"欢迎 {username}！")
            login_window.destroy()
        else:
            messagebox.showerror("登录失败", "用户名或密码错误！")

    login_btn = tk.Button(login_window, text="登录", command=do_login)
    login_btn.pack(pady=10)
    reg_btn = tk.Button(login_window, text="注册新用户", command=register)
    reg_btn.pack(pady=5)

# 初始化版本系统
VersionManager.initialize_version_files()
current_version = VersionManager.get_current_version()
version_content = VersionManager.get_version_content(current_version)

# 创建主窗口
MayOSDesktop = tk.Tk()
MayOSDesktop.title(f"{current_version}")
MayOSDesktop.geometry("1280x740")

# 创建菜单栏
menubar = Menu(MayOSDesktop)

# 操作菜单
operation_menu = Menu(menubar, tearoff=0)
operation_menu.add_command(label="启动计算器", command=launch_calc)
operation_menu.add_command(label="启动音乐播放器", command=launch_music)
operation_menu.add_command(label="更新Bing壁纸", command=lambda: WallpaperManager.update_bing_wallpaper())
operation_menu.add_command(label="退出", command=MayOSDesktop.quit)
menubar.add_cascade(label="操作", menu=operation_menu)

# 帮助菜单
help_menu = Menu(menubar, tearoff=0)
help_menu.add_command(label="官方网址", command=lambda: AIManager.open_official_website())
help_menu.add_command(label="更新日志", command=show_changelog)
help_menu.add_command(label="检查更新", command=check_for_updates)
menubar.add_cascade(label="帮助", menu=help_menu)

# 关于菜单
about_menu = Menu(menubar, tearoff=0)
about_menu.add_command(label="版本信息", command=lambda: messagebox.showinfo("关于", f"当前版本: {current_version}"))
menubar.add_cascade(label="关于", menu=about_menu)

MayOSDesktop.config(menu=menubar)

test_label = None  # 保证全局有定义

# Canvas壁纸自适应
class CanvasWallpaper:
    def __init__(self, root, image_path):
        self.root = root
        self.image_path = image_path
        self.original_img = Image.open(image_path)
        self.canvas = Canvas(root, highlightthickness=0)
        self.canvas.place(x=0, y=0, relwidth=1, relheight=1)
        self.photo = None
        self.img_id = None
        self.draw_wallpaper()
        root.bind('<Configure>', self.on_resize)

    def draw_wallpaper(self):
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        if w < 100 or h < 100:
            w, h = 1280, 720
        img = self.original_img.resize((w, h), Image.LANCZOS)
        self.photo = ImageTk.PhotoImage(img)
        if self.img_id:
            self.canvas.delete(self.img_id)
        self.img_id = self.canvas.create_image(0, 0, anchor='nw', image=self.photo)

    def on_resize(self, event):
        self.draw_wallpaper()

def get_latest_bing_wallpaper():
    bg_dir = os.path.join("files", "background")
    if not os.path.exists(bg_dir):
        return None
    files = [f for f in os.listdir(bg_dir) if f.startswith("bing_") and f.endswith(".jpg")]
    if not files:
        return None
    files.sort(reverse=True)
    return os.path.join(bg_dir, files[0])

# 加载壁纸并显示控件
try:
    # 优先使用最新必应壁纸
    bg_path = get_latest_bing_wallpaper()
    image_title = "每日必应壁纸" if bg_path else "默认壁纸"
    if bg_path and os.path.exists(bg_path):
        wallpaper = CanvasWallpaper(MayOSDesktop, bg_path)
        canvas = wallpaper.canvas
    else:
        default_path = os.path.join("files", "background", "default.jpg")
        if os.path.exists(default_path):
            wallpaper = CanvasWallpaper(MayOSDesktop, default_path)
            canvas = wallpaper.canvas
        MayOSDesktop.configure(bg='black')
        Label(
            MayOSDesktop,
            text="背景加载失败",
            font=("Arial", 24),
            foreground="white",
            background="black"
        ).pack(expand=True)
except Exception as e:
    default_path = os.path.join("files", "background", "default.jpg")
    try:
        if os.path.exists(default_path):
            wallpaper = CanvasWallpaper(MayOSDesktop, default_path)
            canvas = wallpaper.canvas
    except Exception as img_e:
        print(f"默认壁纸加载错误: {img_e}")
        MayOSDesktop.configure(bg='black')
        Label(
            MayOSDesktop,
            text="背景加载失败",
            font=("Arial", 24),
            foreground="white",
            background="black"
        ).pack(expand=True)
    print(f"背景加载错误: {e}")
    MayOSDesktop.configure(bg='black')
    Label(
        MayOSDesktop,
        text="背景加载失败",
        font=("Arial", 24),
        foreground="white",
        background="black"
    ).pack(expand=True)

# 桌面控件放在Canvas上
if 'canvas' in locals():
    welcome_label = Label(
        canvas,
        text="欢迎使用 MayOS_GUI",
        font=("Arial", 24, "bold"),
        foreground="white",
        background="black"
    )
    canvas.create_window(canvas.winfo_reqwidth()//2, 80, window=welcome_label, anchor='n')

    ai_button = Button(
        canvas,
        text="MayOS GUI\nAI Chat",
        command=launch_ai_web,
        style="TButton"
    )
    canvas.create_window(120, 180, window=ai_button)

    calc_btn = Button(
        canvas,
        text="启动计算器",
        command=launch_calc,
        style="TButton"
    )
    canvas.create_window(120, 240, window=calc_btn)

    music_btn = Button(
        canvas,
        text="启动音乐播放器",
        command=launch_music,
        style="TButton"
    )
    canvas.create_window(120, 300, window=music_btn)

# 状态栏
status_bar = tk.Label(
    MayOSDesktop,
    text="就绪",
    bd=1,
    relief=tk.SUNKEN,
    anchor=tk.W
)
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

# 右下角时钟
clock_label = tk.Label(
    MayOSDesktop,
    font=('Arial', 12),
    fg='white',
    bg='black',
    bd=0
)
clock_label.place(relx=0.95, rely=0.95, anchor='se')  # 右下角定位
update_clock()  # 启动时钟更新

# 尝试自动更新壁纸
try:
    bg_photo, image_title = WallpaperManager.update_bing_wallpaper()
    if bg_photo and test_label:
        test_label.config(image=bg_photo)
        test_label.image = bg_photo  # 保持引用防止垃圾回收
        status_bar.config(text=f"壁纸已更新: {image_title}")
    else:
        print("壁纸更新失败")
except Exception as e:
    print(f"自动更新壁纸失败: {e}")

download_info()

# 启动时检查更新
startup_check_for_updates()

# 主循环
MayOSDesktop.mainloop()