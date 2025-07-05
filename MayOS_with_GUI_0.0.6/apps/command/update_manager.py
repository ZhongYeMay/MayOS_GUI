# apps/command/update_manager.py

import requests
import webbrowser
from .version_manager import VersionManager  # 导入 VersionManager 类

class UpdateManager:
    @staticmethod
    def check_for_updates(current_version):
        """检查是否有新版本"""
        try:
            latest_version = UpdateManager.get_latest_version()
            if latest_version and VersionManager.compare_versions(current_version, latest_version):
                return latest_version
            else:
                return None
        except Exception as e:
            print(f"检查更新失败: {e}")
            return None

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