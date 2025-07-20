import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import os
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
from mutagen.flac import FLAC
from mutagen.wave import WAVE
import json
import io
import time
import subprocess
# ffmpeg自动下载到system/func，显示进度条，已下载则跳过
FFMPEG_EXE = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../system/func/ffmpeg.exe'))
FFPLAY_EXE = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../system/func/ffplay.exe'))

class DownloadProgressBar:
    def __init__(self, total_size):
        self.total_size = total_size
        self.downloaded = 0
        self.last_percent = -1
    def __call__(self, block_num, block_size, total_size):
        self.downloaded = block_num * block_size
        percent = int(self.downloaded * 100 / (total_size or self.total_size or 1))
        if percent != self.last_percent:
            print(f"ffmpeg下载进度: {percent}%", end='\r')
            self.last_percent = percent
        if self.downloaded >= (total_size or self.total_size):
            print("ffmpeg下载完成!           ")

if not os.path.exists(FFMPEG_EXE):
    import urllib.request
    try:
        url = 'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip'
        zip_path = os.path.join(os.path.dirname(FFMPEG_EXE), 'ffmpeg_tmp.zip')
        with urllib.request.urlopen(url) as u:
            total_size = int(u.info().get('Content-Length', 0))
        print("正在下载 ffmpeg...")
        urllib.request.urlretrieve(url, zip_path, DownloadProgressBar(total_size))
        import zipfile
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            for name in zip_ref.namelist():
                if name.endswith('ffmpeg.exe'):
                    zip_ref.extract(name, os.path.dirname(FFMPEG_EXE))
                    os.rename(os.path.join(os.path.dirname(FFMPEG_EXE), name), FFMPEG_EXE)
                    break
        os.remove(zip_path)
    except Exception as e:
        print(f"ffmpeg下载失败: {e}")
        FFMPEG_EXE = None

if not os.path.exists(FFPLAY_EXE):
    import urllib.request
    try:
        url = 'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip'
        zip_path = os.path.join(os.path.dirname(FFPLAY_EXE), 'ffplay_tmp.zip')
        with urllib.request.urlopen(url) as u:
            total_size = int(u.info().get('Content-Length', 0))
        print("正在下载 ffmpeg/ffplay...")
        urllib.request.urlretrieve(url, zip_path, DownloadProgressBar(total_size))
        import zipfile
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            for name in zip_ref.namelist():
                if name.endswith('ffplay.exe'):
                    zip_ref.extract(name, os.path.dirname(FFPLAY_EXE))
                    os.rename(os.path.join(os.path.dirname(FFPLAY_EXE), name), FFPLAY_EXE)
                    break
        os.remove(zip_path)
    except Exception as e:
        print(f"ffplay下载失败: {e}")
        FFPLAY_EXE = None


class EnhancedMusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("增强版Python音乐播放器")
        self.root.geometry("1050x650")
        self.root.resizable(1, 1)

        # 当前播放状态
        self.playing = False
        self.paused = False
        self.stopped = True
        self.current_song = ""
        self.playlist = []
        self.current_index = 0

        # 支持的音频格式
        self.supported_formats = ('.mp3', '.wav', '.flac')  # ffmpeg支持绝大多数格式

        # 专辑封面缓存
        self.album_art = None
        self.default_art = self.create_default_art()

        # 创建UI
        self.create_ui()

        # 更新进度条
        self.update_progress()

        self.status_bar.config(text="支持绝大多数音频格式，播放由ffmpeg实现。")

        self.vlc_player = None  # VLC播放器实例
        self.vlc_instance = None
        self.vlc_module = None  # 动态导入vlc模块
        self._check_vlc_install()

    def _check_vlc_install(self):
        import sys, glob, platform, tkinter.simpledialog, urllib.request, zipfile, importlib, os
        vlc_bin_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../system/func/vlc-3.0.20/vlc-3.0.20'))
        vlc_dll = os.path.join(vlc_bin_dir, 'libvlc.dll')
        vlc_core = os.path.join(vlc_bin_dir, 'libvlccore.dll')
        plugins_dir = os.path.join(vlc_bin_dir, 'plugins')
        # 自动下载并解压完整 VLC bin 目录
        if not (os.path.exists(vlc_dll) and os.path.exists(vlc_core) and os.path.exists(plugins_dir)):
            try:
                url = 'https://get.videolan.org/vlc/3.0.20/win64/vlc-3.0.20-win64.zip'
                zip_path = os.path.join(os.path.dirname(vlc_bin_dir), 'vlc_tmp.zip')
                os.makedirs(vlc_bin_dir, exist_ok=True)
                print("正在下载并解压 VLC 主程序...")
                with urllib.request.urlopen(url) as u:
                    total_size = int(u.info().get('Content-Length', 0))
                urllib.request.urlretrieve(url, zip_path, DownloadProgressBar(total_size))
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    for name in zip_ref.namelist():
                        if name.startswith('vlc-3.0.20/'):
                            zip_ref.extract(name, os.path.dirname(vlc_bin_dir))
                os.remove(zip_path)
                print("VLC主程序下载并解压完成!")
            except Exception as e:
                print(f"VLC主程序下载失败: {e}")
        # 只检测完整 bin 目录
        plugin_path = None
        if os.path.exists(vlc_dll) and os.path.exists(vlc_core) and os.path.exists(plugins_dir):
            plugin_path = vlc_bin_dir
            # 将 VLC bin 目录加入 PATH，确保 DLL 能被找到
            os.environ['PATH'] = plugin_path + os.pathsep + os.environ.get('PATH', '')
        # 允许用户手动选择
        if not plugin_path:
            answer = messagebox.askyesno("VLC依赖缺失", "未检测到完整 VLC bin 目录，是否手动指定？\n目录需包含 libvlc.dll、libvlccore.dll 和 plugins 文件夹。")
            if answer:
                plugin_path = tkinter.filedialog.askdirectory(title="请选择包含 libvlc.dll、libvlccore.dll 和 plugins 的 VLC bin 目录")
                if not plugin_path or not (os.path.exists(os.path.join(plugin_path, 'libvlc.dll')) and os.path.exists(os.path.join(plugin_path, 'libvlccore.dll')) and os.path.exists(os.path.join(plugin_path, 'plugins'))):
                    messagebox.showerror("VLC错误", "未找到有效的 VLC bin 目录，音乐播放功能不可用！")
                    return
                os.environ['PATH'] = plugin_path + os.pathsep + os.environ.get('PATH', '')
            else:
                messagebox.showerror("VLC错误", "未检测到完整 VLC 主程序，请先安装 VLC 或等待自动下载！")
                return
        # 动态导入vlc模块
        try:
            self.vlc_module = importlib.import_module('vlc')
            self.vlc_instance = self.vlc_module.Instance(f'--plugin-path={plugin_path}')
        except Exception as e:
            messagebox.showerror("VLC错误", f"VLC初始化失败: {e}\n请检查 VLC bin 目录和依赖文件。")
            self.vlc_instance = None

    def create_default_art(self):
        """创建默认专辑封面"""
        from PIL import ImageDraw
        img = Image.new('RGB', (300, 300), color='#333333')
        d = ImageDraw.Draw(img)
        d.text((100, 140), "无专辑封面", fill=(255, 255, 255))
        return ImageTk.PhotoImage(img)

    def create_ui(self):
        # 主框架
        main_frame = tk.Frame(self.root, bg="#F5F5F5")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=16, pady=16)

        # 左侧面板 (专辑封面和歌曲信息)
        left_panel = tk.Frame(main_frame, width=320, bg="#F5F5F5", bd=0, highlightthickness=0)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=8, pady=8)
        left_panel.pack_propagate(False)

        # 专辑封面
        self.album_art_label = tk.Label(left_panel, image=self.default_art, bg="#F5F5F5", bd=0)
        self.album_art_label.pack(pady=16)

        # 歌曲信息
        song_info_frame = tk.Frame(left_panel, bg="#F5F5F5")
        song_info_frame.pack(fill=tk.X, padx=8, pady=8)

        info_font = ("Google Sans", 13)
        self.song_title = tk.Label(song_info_frame, text="标题: ", bg="#F5F5F5", fg="#1A1A1A", anchor='w', font=info_font)
        self.song_title.pack(fill=tk.X)
        self.song_artist = tk.Label(song_info_frame, text="艺术家: ", bg="#F5F5F5", fg="#1A1A1A", anchor='w', font=info_font)
        self.song_artist.pack(fill=tk.X)
        self.song_album = tk.Label(song_info_frame, text="专辑: ", bg="#F5F5F5", fg="#1A1A1A", anchor='w', font=info_font)
        self.song_album.pack(fill=tk.X)
        self.song_year = tk.Label(song_info_frame, text="年份: ", bg="#F5F5F5", fg="#1A1A1A", anchor='w', font=info_font)
        self.song_year.pack(fill=tk.X)
        self.song_genre = tk.Label(song_info_frame, text="流派: ", bg="#F5F5F5", fg="#1A1A1A", anchor='w', font=info_font)
        self.song_genre.pack(fill=tk.X)

        # 右侧面板 (播放列表和控制按钮)
        right_panel = tk.Frame(main_frame, bg="#FFFFFF", bd=0, highlightthickness=0)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # 播放列表
        playlist_frame = tk.Frame(right_panel, bg="#FFFFFF")
        playlist_frame.pack(fill=tk.BOTH, expand=True, pady=8)

        self.playlist_box = tk.Listbox(playlist_frame, bg="#FFFFFF", fg="#1A1A1A",
                                       font=("Google Sans", 13),
                                       width=60, height=15, selectbackground="#4285F4",
                                       selectforeground="#FFFFFF", bd=0, highlightthickness=0)
        self.playlist_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 滚动条
        scrollbar = tk.Scrollbar(playlist_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.playlist_box.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.playlist_box.yview)
        self.playlist_box.bind("<Double-1>", self.play_selected_song)

        # 控制按钮框架
        control_frame = tk.Frame(right_panel, bg="#FFFFFF")
        control_frame.pack(fill=tk.X, pady=12)

        btn_font = ("Google Sans", 14, "bold")
        btn_style = dict(bd=0, relief=tk.FLAT, padx=0, pady=0, height=1, width=10, cursor="hand2")
        accent = {"bg": "#4285F4", "fg": "#FFFFFF", "activebackground": "#3367D6", "activeforeground": "#FFFFFF"}
        default = {"bg": "#E8EAED", "fg": "#1A1A1A", "activebackground": "#DADCE0", "activeforeground": "#1A1A1A"}

        self.play_btn = tk.Button(control_frame, text="播放", font=btn_font, **accent, **btn_style, command=self.play_music)
        self.play_btn.grid(row=0, column=0, padx=8)
        self.pause_btn = tk.Button(control_frame, text="暂停", font=btn_font, **default, **btn_style, command=self.pause_music)
        self.pause_btn.grid(row=0, column=1, padx=8)
        self.stop_btn = tk.Button(control_frame, text="停止", font=btn_font, **default, **btn_style, command=self.stop_music)
        self.stop_btn.grid(row=0, column=2, padx=8)
        self.next_btn = tk.Button(control_frame, text="下一首", font=btn_font, **accent, **btn_style, command=self.next_song)
        self.next_btn.grid(row=0, column=3, padx=8)
        self.prev_btn = tk.Button(control_frame, text="上一首", font=btn_font, **accent, **btn_style, command=self.prev_song)
        self.prev_btn.grid(row=0, column=4, padx=8)

        # 音量控制
        volume_frame = tk.Frame(right_panel, bg="#FFFFFF")
        volume_frame.pack(fill=tk.X, pady=8)
        self.volume_label = tk.Label(volume_frame, text="音量:", font=("Google Sans", 12), bg="#FFFFFF", fg="#1A1A1A")
        self.volume_label.pack(side=tk.LEFT)
        self.volume_slider = tk.Scale(volume_frame, from_=0, to=100, orient=tk.HORIZONTAL,
                                      command=self.set_volume, bg="#FFFFFF", fg="#1A1A1A",
                                      highlightthickness=0, troughcolor="#E8EAED", sliderrelief=tk.FLAT,
                                      font=("Google Sans", 11))
        self.volume_slider.set(70)
        self.volume_slider.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # 进度条
        style = ttk.Style()
        style.theme_use('default')
        style.configure("MD3.Horizontal.TProgressbar", background="#4285F4", troughcolor="#E8EAED", thickness=8, borderwidth=0)
        self.progress = ttk.Progressbar(right_panel, orient=tk.HORIZONTAL,
                                        length=400, mode='determinate', style="MD3.Horizontal.TProgressbar")
        self.progress.pack(fill=tk.X, pady=12)

        # 时间显示
        self.time_label = tk.Label(right_panel, text="00:00 / 00:00", font=("Google Sans", 12), bg="#FFFFFF", fg="#1A1A1A")
        self.time_label.pack()

        # 状态栏
        self.status_bar = tk.Label(right_panel, text="就绪", bd=0, relief=tk.FLAT, anchor=tk.W,
                                   font=("Google Sans", 11), bg="#F5F5F5", fg="#4285F4")
        self.status_bar.pack(fill=tk.X, pady=(8,0))

        # 菜单栏
        self.create_menu()

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # 文件菜单
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="添加歌曲", command=self.add_song)
        file_menu.add_command(label="添加文件夹", command=self.add_folder)
        file_menu.add_separator()
        file_menu.add_command(label="打开播放列表", command=self.load_playlist)
        file_menu.add_command(label="保存播放列表", command=self.save_playlist)
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.root.quit)
        menubar.add_cascade(label="文件", menu=file_menu)

        # 编辑菜单
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="清空播放列表", command=self.clear_playlist)
        edit_menu.add_command(label="移除选中歌曲", command=self.remove_selected)
        menubar.add_cascade(label="编辑", menu=edit_menu)

        # 帮助菜单
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="关于", command=self.show_about)
        menubar.add_cascade(label="帮助", menu=help_menu)

    def add_song(self):
        songs = filedialog.askopenfilenames(
            title="选择歌曲",
            filetypes=(("音频文件", "*.mp3 *.wav *.flac"), ("所有文件", "*.*"))
        )
        for song in songs:
            if song.lower().endswith(self.supported_formats):
                self.playlist.append(song)
                self.playlist_box.insert(tk.END, os.path.basename(song))
        if songs:
            self.status_bar.config(text=f"已添加 {len(songs)} 首歌曲")

    def add_folder(self):
        folder = filedialog.askdirectory(title="选择文件夹")
        if folder:
            count = 0
            for root, _, files in os.walk(folder):
                for file in files:
                    if file.lower().endswith(self.supported_formats):
                        path = os.path.join(root, file)
                        self.playlist.append(path)
                        self.playlist_box.insert(tk.END, file)
                        count += 1
            self.status_bar.config(text=f"已添加 {count} 首歌曲")

    def load_playlist(self):
        playlist_file = filedialog.askopenfilename(
            title="打开播放列表",
            filetypes=(("播放列表文件", "*.json"), ("所有文件", "*.*"))
        )
        if playlist_file:
            try:
                with open(playlist_file, 'r') as f:
                    self.playlist = json.load(f)
                self.playlist_box.delete(0, tk.END)
                for song in self.playlist:
                    self.playlist_box.insert(tk.END, os.path.basename(song))
                self.status_bar.config(text=f"已加载播放列表，共 {len(self.playlist)} 首歌曲")
            except Exception as e:
                messagebox.showerror("错误", f"无法加载播放列表: {e}")

    def save_playlist(self):
        if not self.playlist:
            messagebox.showwarning("警告", "播放列表为空!")
            return
        playlist_file = filedialog.asksaveasfilename(
            title="保存播放列表",
            defaultextension=".json",
            filetypes=(("播放列表文件", "*.json"), ("所有文件", "*.*"))
        )
        if playlist_file:
            try:
                with open(playlist_file, 'w') as f:
                    json.dump(self.playlist, f)
                self.status_bar.config(text=f"播放列表已保存到 {playlist_file}")
            except Exception as e:
                messagebox.showerror("错误", f"无法保存播放列表: {e}")

    def clear_playlist(self):
        self.playlist_box.delete(0, tk.END)
        self.playlist = []
        self.stop_music()
        self.status_bar.config(text="播放列表已清空")

    def remove_selected(self):
        sel = self.playlist_box.curselection()
        if not sel:
            return
        selected = sel[0]
        if selected == self.current_index:
            self.stop_music()
        self.playlist_box.delete(selected)
        self.playlist.pop(selected)
        if selected < self.current_index:
            self.current_index -= 1
        elif selected == self.current_index:
            self.current_index = 0 if self.playlist else -1
        self.status_bar.config(text="已移除选中的歌曲")

    def play_music(self):
        if not self.playlist:
            messagebox.showwarning("警告", "播放列表为空!")
            return
        self.stop_music()  # 停止当前播放
        self.current_song = self.playlist[self.current_index]
        song_path = os.path.abspath(self.current_song)
        song_path = os.path.normpath(song_path)
        print(f"尝试播放: {song_path}")
        if not os.path.exists(song_path):
            self.status_bar.config(text=f"文件不存在: {song_path}")
            print(f"文件不存在: {song_path}")
            return
        # VLC实际播放
        try:
            if self.vlc_player:
                self.vlc_player.stop()
            if self.vlc_instance and self.vlc_module:
                self.vlc_player = self.vlc_module.MediaPlayer(song_path)
                self.vlc_player.play()
                self.set_volume(self.volume_slider.get())
                self.status_bar.config(text=f"正在播放: {os.path.basename(self.current_song)}")
                self.playing = True
                self.paused = False
                self.stopped = False
                self.update_song_info()
                self.update_album_art()
                self.update_progress_vlc()
            else:
                self.status_bar.config(text="VLC未初始化，无法播放！")
        except Exception as e:
            self.status_bar.config(text=f"播放失败: {e}")
            print(f"VLC播放失败: {e}")

    def stop_music(self):
        if self.vlc_player:
            self.vlc_player.stop()
        self.playing = False
        self.paused = False
        self.stopped = True
        self.progress["value"] = 0
        self.time_label.config(text="00:00 / 00:00")
        self.status_bar.config(text="已停止")

    def pause_music(self):
        if self.vlc_player:
            if self.playing and not self.paused:
                self.vlc_player.pause()
                self.paused = True
                self.status_bar.config(text="已暂停")
            elif self.paused:
                self.vlc_player.play()
                self.paused = False
                self.status_bar.config(text="恢复播放")
        else:
            messagebox.showinfo("提示", "当前未实际播放音频。")

    def set_volume(self, val):
        if self.vlc_player:
            try:
                self.vlc_player.audio_set_volume(int(val))
            except Exception as e:
                print(f"设置音量失败: {e}")

    def update_progress_vlc(self):
        # VLC进度条与时间显示
        if self.vlc_player and self.playing and not self.stopped:
            try:
                length = self.vlc_player.get_length() / 1000  # ms->s
                pos = self.vlc_player.get_time() / 1000
                if length > 0:
                    self.progress["maximum"] = length
                    self.progress["value"] = pos
                    mins, secs = divmod(pos, 60)
                    total_mins, total_secs = divmod(length, 60)
                    self.time_label.config(text=f"{int(mins):02d}:{int(secs):02d} / {int(total_mins):02d}:{int(total_secs):02d}")
            except Exception as e:
                print(f"进度同步失败: {e}")
        self.root.after(500, self.update_progress_vlc)

    def update_song_info(self):
        """更新歌曲标签信息"""
        try:
            if self.current_song.lower().endswith('.mp3'):
                audio = ID3(self.current_song)
                title = audio.get('TIT2', ['未知'])[0]
                artist = audio.get('TPE1', ['未知艺术家'])[0]
                album = audio.get('TALB', ['未知专辑'])[0]
                year = audio.get('TYER', ['未知年份'])[0]
                genre = audio.get('TCON', ['未知流派'])[0]
            elif self.current_song.lower().endswith('.flac'):
                audio = FLAC(self.current_song)
                title = audio.get('title', ['未知'])[0]
                artist = audio.get('artist', ['未知艺术家'])[0]
                album = audio.get('album', ['未知专辑'])[0]
                year = audio.get('date', ['未知年份'])[0]
                genre = audio.get('genre', ['未知流派'])[0]
            else:  # WAV等其他格式
                title = os.path.basename(self.current_song)
                artist = "未知艺术家"
                album = "未知专辑"
                year = "未知年份"
                genre = "未知流派"

            self.song_title.config(text=f"标题: {title}")
            self.song_artist.config(text=f"艺术家: {artist}")
            self.song_album.config(text=f"专辑: {album}")
            self.song_year.config(text=f"年份: {year}")
            self.song_genre.config(text=f"流派: {genre}")

            # 获取歌曲长度
            if self.current_song.lower().endswith('.mp3'):
                audio = MP3(self.current_song)
                length = audio.info.length
            elif self.current_song.lower().endswith('.flac'):
                audio = FLAC(self.current_song)
                length = audio.info.length
            elif self.current_song.lower().endswith('.wav'):
                audio = WAVE(self.current_song)
                length = audio.info.length
            else:
                length = 0

            mins, secs = divmod(length, 60)
            self.total_length = f"{int(mins):02d}:{int(secs):02d}"
        except Exception as e:
            print(f"获取歌曲信息错误: {e}")
            self.song_title.config(text="标题: 未知")
            self.song_artist.config(text="艺术家: 未知")
            self.song_album.config(text="专辑: 未知")
            self.song_year.config(text="年份: 未知")
            self.song_genre.config(text="流派: 未知")
            self.total_length = "00:00"

    def update_album_art(self):
        """更新专辑封面，支持MP3/FLAC，其他格式显示默认封面"""
        try:
            if self.current_song.lower().endswith('.mp3'):
                audio = ID3(self.current_song)
                for tag in audio.values():
                    if getattr(tag, 'FrameID', None) == 'APIC':
                        img = Image.open(io.BytesIO(tag.data)).resize((300, 300), Image.LANCZOS)
                        self.album_art = ImageTk.PhotoImage(img)
                        self.album_art_label.config(image=self.album_art)
                        return
            elif self.current_song.lower().endswith('.flac'):
                audio = FLAC(self.current_song)
                if audio.pictures:
                    pic = audio.pictures[0]
                    img = Image.open(io.BytesIO(pic.data)).resize((300, 300), Image.LANCZOS)
                    self.album_art = ImageTk.PhotoImage(img)
                    self.album_art_label.config(image=self.album_art)
                    return
        except Exception as e:
            print(f"获取专辑封面错误: {e}")
        # 没有专辑封面或出错，显示默认封面
        self.album_art_label.config(image=self.default_art)

    def update_progress(self):
        # 进度条与时间显示未实现（ffmpeg播放无法获取进度），此处仅做UI刷新
        self.root.after(1000, self.update_progress)

    def show_about(self):
        messagebox.showinfo("关于", "增强版Python音乐播放器\n版本 2.0\n支持绝大多数音频格式\n显示专辑封面和歌曲标签\n播放由ffmpeg实现")

    def play_selected_song(self, event=None):
        sel = self.playlist_box.curselection()
        if not sel:
            return
        self.current_index = sel[0]
        self.stop_music()
        self.play_music()

    def next_song(self):
        if not self.playlist:
            return
        self.current_index = (self.current_index + 1) % len(self.playlist)
        self.stop_music()
        self.play_music()

    def prev_song(self):
        if not self.playlist:
            return
        self.current_index = (self.current_index - 1) % len(self.playlist)
        self.stop_music()
        self.play_music()


if __name__ == "__main__":
    root = tk.Tk()
    EnhancedMusicPlayer(root)
    root.mainloop()