# apps/command/wallpaper_manager.py

import os
import requests
from PIL import Image, ImageTk
import datetime

class WallpaperManager:
    @staticmethod
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
            os.makedirs(os.path.join("files", "background"), exist_ok=True)

            # 保存图片
            today = datetime.datetime.now().strftime("%Y%m%d")
            save_path = os.path.join("files", "background", f"bing_{today}.jpg")
            with open(save_path, 'wb') as f:
                f.write(image_data)

            # 加载并设置新壁纸
            img = Image.open(save_path).resize((1280, 720), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)

            return photo, image_title
        except Exception as e:
            print(f"更新壁纸失败: {e}")
            return None, None