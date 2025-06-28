import os
import tkinter as tk
from tkinter import messagebox, Menu
from tkinter.ttk import Label, Button
from PIL import Image, ImageTk, ImageOps
import requests
import webbrowser
from datetime import datetime
import subprocess  # 新增导入

class VersionManager:
    @staticmethod
    def get_current_version():
        """获取当前版本信息"""
        try:
            with open(f"system/info/ver.txt", "r", encoding="utf-8") as f:
                return f.read().strip()
        except Exception:
            return "MayOS_GUI_0.0.5"  # 默认版本

    @staticmethod
    def get_version_content(version):
        """获取指定版本的内容"""
        try:
            with open(f"system/info/MayOS_with_GUI_0.0.5.txt", "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            return f"{version} 版本信息不可用"

    @staticmethod
    def initialize_version_files():
        """确保版本文件存在"""
        os.makedirs("system/info", exist_ok=True)
        
        # 如果ver.txt不存在则创建
        if not os.path.exists("system/info/ver.txt"):
            with open("system/info/ver.txt", "w", encoding="utf-8") as f:
                f.write("MayOS_GUI_0.0.5")

def update_bing_wallpaper():
    """从Bing获取最新壁纸并设置为背景"""
    try:
        # 获取Bing每日图片
        response = requests.get(
            "https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=zh-CN",
            timeout=10
        )
        data = response.json()

        # 提取图片信息
        image_url = "https://www.bing.com" + data['images'][0]['url']
        image_title = data['images'][0]['title']

        # 下载图片
        image_data = requests.get(image_url, timeout=10).content

        # 确保背景目录存在
        os.makedirs("files/background", exist_ok=True)

        # 保存图片
        today = datetime.now().strftime("%Y%m%d")
        save_path = f"files/background/bing_{today}.jpg"
        with open(save_path, 'wb') as f:
            f.write(image_data)

        # 加载并设置新壁纸
        img = Image.open(save_path).resize((1280, 720), Image.LANCZOS)
        photo = ImageTk.PhotoImage(img)

        # 更新界面
        test_label.config(image=photo)
        test_label.image = photo
        status_bar.config(text=f"壁纸已更新: {image_title}")

        return True
    except Exception as e:
        messagebox.showerror("错误", f"更新壁纸失败: {e}")
        return False

def update_clock():
    """更新右下角时钟"""
    current_time = datetime.now().strftime("%H:%M:%S\n"f"%Y/%m/%d")
    clock_label.config(text=current_time)
    clock_label.after(1000, update_clock)  # 每秒更新一次

def launch_ai_web():
    """启动AI网页应用"""
    try:
        script_path = os.path.join("apps", "gui_test", "AI_web.py")
        if os.path.exists(script_path):
            # 使用subprocess运行Python脚本
            subprocess.Popen(["python", script_path])
            status_bar.config(text="已启动AI网页应用")
        else:
            messagebox.showerror("错误", f"找不到文件: {script_path}")
    except Exception as e:
        messagebox.showerror("错误", f"启动AI网页应用失败: {e}")

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
operation_menu.add_command(label="更新Bing壁纸", command=update_bing_wallpaper)
operation_menu.add_command(label="退出", command=MayOSDesktop.quit)
menubar.add_cascade(label="操作", menu=operation_menu)

# 帮助菜单
help_menu = Menu(menubar, tearoff=0)
help_menu.add_command(label="官方网址", command=lambda: webbrowser.open("http://mayos.liveblog365.com/"))
help_menu.add_command(
    label="更新日志",
    command=lambda: messagebox.showinfo(
        f"更新日志 - {current_version}",
        version_content
    )
)
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
    bg_path = "files/background/default.jpg"
    if os.path.exists(bg_path):
        img = Image.open(bg_path)
    else:
        img = Image.new('RGB', (1280, 720), 'black')
    
    photo = ImageTk.PhotoImage(img.resize((1280, 720), Image.LANCZOS))
    test_label = Label(MayOSDesktop, image=photo)
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
    update_bing_wallpaper()
except Exception as e:
    print(f"自动更新壁纸失败: {e}")

# 主循环
MayOSDesktop.mainloop()