# apps/command/version_manager.py

import os
import requests
import markdown

class VersionManager:
    @staticmethod
    def get_current_version():
        """获取当前版本信息"""
        path = os.path.join("system", "info", "ver.txt")
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read().strip()
        except Exception:
            return "MayOS_with_GUI_0.0.6"  # 默认版本

    @staticmethod
    def get_version_content(version):
        """获取指定版本的内容"""
        path = os.path.join("system", "info", f"{version}.txt")
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            return f"{version} 版本信息不可用"

    @staticmethod
    def get_changelog():
        """优先使用本地HTML文件展示更新日志，若无则渲染markdown"""
        html_path = os.path.join("system", "info", "changelog.html")
        if os.path.exists(html_path):
            try:
                with open(html_path, "r", encoding="utf-8") as f:
                    return f.read()
            except Exception:
                return "<p>更新日志HTML文件读取失败</p>"
        md_path = os.path.join("system", "info", "changelog.md")
        try:
            with open(md_path, "r", encoding="utf-8") as f:
                md_text = f.read()
            css = '''<style>
                body { font-family: Arial, 'Microsoft YaHei', sans-serif; background: #fafafa; color: #222; }
                h1, h2, h3 { color: #4285F4; margin-top: 1em; }
                ul, ol { margin-left: 2em; }
                li { margin-bottom: 0.5em; }
                pre, code { background: #f5f5f5; border-radius: 4px; padding: 2px 6px; }
            </style>'''
            html = markdown.markdown(md_text, output_format='html5')
            return css + html
        except Exception:
            return "<p>更新日志不可用</p>"

    @staticmethod
    def get_latest_version():
        """获取最新版本信息"""
        url = "https://maydos-team.github.io/about/ver.txt"
        try:
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
            return tuple(map(int, v.split("_")[-1].split(".")))
        return version_tuple(latest) > version_tuple(current)

    @staticmethod
    def initialize_version_files():
        """确保版本文件存在"""
        info_dir = os.path.join("system", "info")
        os.makedirs(info_dir, exist_ok=True)
        ver_file = os.path.join(info_dir, "ver.txt")
        if not os.path.exists(ver_file):
            with open(ver_file, "w", encoding="utf-8") as f:
                f.write("MayOS_with_GUI_0.0.6")
        changelog_md = os.path.join(info_dir, "changelog.md")
        if not os.path.exists(changelog_md):
            with open(changelog_md, "w", encoding="utf-8") as f:
                f.write("# 更新日志 - MayOS_with_GUI_0.0.6\n\n## 新增功能\n\n- 初始版本发布")