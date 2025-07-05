# apps/command/version_manager.py

import os
import requests
import markdown

class VersionManager:
    @staticmethod
    def get_current_version():
        """获取当前版本信息"""
        try:
            with open(os.path.join("system", "info", "ver.txt"), "r", encoding="utf-8") as f:
                return f.read().strip()
        except Exception:
            return "MayOS_with_GUI_0.0."  # 默认版本

    @staticmethod
    def get_version_content(version):
        """获取指定版本的内容"""
        try:
            filename = os.path.join("system", "info", f"{version}.txt")
            with open(filename, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            return f"{version} 版本信息不可用"

    @staticmethod
    def get_changelog():
        """获取更新日志内容"""
        try:
            filename = os.path.join("system", "info", "changelog.md")
            with open(filename, "r", encoding="utf-8") as f:
                md_text = f.read()
            html = markdown.markdown(md_text, extensions=['fenced_code', 'codehilite'])
            return html
        except Exception:
            return "<p>更新日志不可用</p>"

    @staticmethod
    def get_latest_version():
        """获取最新版本信息"""
        try:
            url = "https://maydos-team.github.io/about/ver.txt"
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # 检查请求是否成功
            return response.text.strip()
        except Exception as e:
            print(f"获取最新版本失败: {e}")
            return None

    @staticmethod
    def compare_versions(current, latest):
        """比较版本号"""
        def version_tuple(v):
            return tuple(map(int, (v.split("_")[-1].split("."))))
        return version_tuple(latest) > version_tuple(current)

    @staticmethod
    def initialize_version_files():
        """确保版本文件存在"""
        os.makedirs(os.path.join("system", "info"), exist_ok=True)
        
        # 如果ver.txt不存在则创建
        ver_file_path = os.path.join("system", "info", "ver.txt")
        if not os.path.exists(ver_file_path):
            with open(ver_file_path, "w", encoding="utf-8") as f:
                f.write("MayOS_with_GUI_0.0.6")
        
        # 如果changelog.md不存在则创建
        changelog_path = os.path.join("system", "info", "changelog.md")
        if not os.path.exists(changelog_path):
            with open(changelog_path, "w", encoding="utf-8") as f:
                f.write("# 更新日志 - MayOS_with_GUI_0.0.6\n\n## 新增功能\n\n- 初始版本发布")