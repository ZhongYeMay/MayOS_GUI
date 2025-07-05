# apps/command/ai_manager.py

import os
import subprocess
import webbrowser

class AIManager:
    @staticmethod
    def launch_ai_web():
        """启动AI网页应用"""
        try:
            script_path = os.path.join("apps", "gui_test", "AI_web.py")
            if os.path.exists(script_path):
                # 使用subprocess运行Python脚本
                subprocess.Popen(["python", script_path])
                return True
            else:
                print(f"找不到文件: {script_path}")
                return False
        except Exception as e:
            print(f"启动AI网页应用失败: {e}")
            return False

    @staticmethod
    def open_official_website():
        """打开官方网站"""
        try:
            webbrowser.open("https://maydos-team.github.io")
            return True
        except Exception as e:
            print(f"打开官方网站失败: {e}")
            return False