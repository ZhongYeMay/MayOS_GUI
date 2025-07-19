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
            url = "https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=zh-CN"
            response = requests.get(url, timeout=10)
            data = response.json()
            image_url = "https://www.bing.com" + data['images'][0]['url']
            image_title = data['images'][0].get('title', '')
            image_data = requests.get(image_url, timeout=10).content
            bg_dir = os.path.join("files", "background")
            os.makedirs(bg_dir, exist_ok=True)
            today = datetime.datetime.now().strftime("%Y%m%d")
            save_path = os.path.join(bg_dir, f"bing_{today}.jpg")
            with open(save_path, 'wb') as f:
                f.write(image_data)
            img = Image.open(save_path).resize((1280, 720), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            return photo, image_title
        except Exception as e:
            print(f"更新壁纸失败: {e}")
            return None, None