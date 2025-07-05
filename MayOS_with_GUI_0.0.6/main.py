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
from tkhtmlview import HTMLLabel

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
operation_menu.add_command(label="更新Bing壁纸", command=lambda: WallpaperManager.update_bing_wallpaper())
operation_menu.add_command(label="退出", command=MayOSDesktop.quit)
menubar.add_cascade(label="操作", menu=operation_menu)

# 帮助菜单
help_menu = Menu(menubar, tearoff=0)
help_menu.add_command(label="官方网址", command=lambda: AIManager.open_official_website())
help_menu.add_command(
    label="更新日志",
    command=show_changelog
)
help_menu.add_command(label="检查更新", command=check_for_updates)
menubar.add_cascade(label="帮助", menu=help_menu)

# 关于菜单
about_menu = Menu(menubar, tearoff=0)
about_menu.add_command(
    label="版本信息",
    command=lambda: messagebox.showinfo("关于", f"当前版本: {current_version}")
)
menubar.add_cascade(label="关于", menu=about_menu)

MayOSDesktop.config(menu=menubar)

# 加载背景图片
try:
    bg_photo, image_title = WallpaperManager.update_bing_wallpaper()
    if bg_photo:
        test_label = Label(MayOSDesktop, image=bg_photo)
        test_label.image = bg_photo  # 保持引用防止垃圾回收
        test_label.pack(fill=tk.BOTH, expand=True)
        
        # 欢迎文本
        welcome_label = Label(
            test_label,
            text="欢迎使用 MayOS_GUI",
            font=("Arial", 24, "bold"),
            foreground="white",
            background="black"
        )
        welcome_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        # 添加AI网页应用按钮
        ai_button = Button(
            test_label,
            text="MayOS GUI\nAI Chat",
            command=launch_ai_web,
            style="TButton"
        )
        ai_button.place(relx=0.1, rely=0.2, anchor=tk.CENTER)
    else:
        MayOSDesktop.configure(bg='black')
        Label(
            MayOSDesktop,
            text="背景加载失败",
            font=("Arial", 24),
            foreground="white",
            background="black"
        ).pack(expand=True)
except Exception as e:
    print(f"背景加载错误: {e}")
    MayOSDesktop.configure(bg='black')
    Label(
        MayOSDesktop,
        text="背景加载失败",
        font=("Arial", 24),
        foreground="white",
        background="black"
    ).pack(expand=True)

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
    if bg_photo:
        test_label.config(image=bg_photo)
        test_label.image = bg_photo
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