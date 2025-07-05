---
Chinese Ver.
# MayOS_GUI 操作系统图形界面介绍

## 系统概述

MayOS_GUI 是一款基于 Python 开发的轻量级图形界面操作系统环境，旨在为用户提供简洁美观的桌面体验和基本功能。系统采用模块化设计，具有良好的可扩展性。

### 更新日志

---

#### **版本：MayOS_with_GUI_0.0.6**

**发布日期：2025年7月5日**

**主要更新内容：**

1. **版本管理功能**：
   - **版本检测**：程序现在可以自动检测当前版本与最新版本，并在发现新版本时提示用户更新。
   - **版本信息获取**：从指定的GitHub地址获取最新版本信息，确保用户始终使用最新版本。
   - **版本文件初始化**：确保 `ver.txt` 和 `changelog.md` 文件存在，并在必要时创建默认版本文件。

2. **Markdown格式更新日志支持**：
   - **更新日志显示**：更新日志现在支持Markdown格式，用户可以更清晰地查看更新内容。
   - **显示优化**：使用 `tkhtmlview` 库在Tkinter界面中正确渲染Markdown格式的更新日志。

3. **壁纸更新功能**：
   - **Bing壁纸自动更新**：程序现在可以自动从Bing获取每日壁纸并设置为桌面背景。
   - **错误处理**：增加了对网络请求和文件操作的错误处理，确保在更新壁纸失败时给予用户提示。

4. **AI应用启动功能**：
   - **AI网页应用启动**：用户可以通过按钮或菜单启动AI网页应用。
   - **错误处理**：增加了对文件存在性和启动过程的错误处理，确保在启动失败时给予用户提示。

5. **代码结构优化**：
   - **模块化设计**：将各个功能模块拆分到不同的文件中，并放在 `apps/command` 目录下，方便维护和扩展。
   - **项目结构**：优化了项目结构，确保代码的可维护性和可扩展性。

---

#### **版本：MayOS_with_GUI_0.0.5**

**发布日期：2025年6月28日**

**主要更新内容：**

1. **新增AI聊天功能**：
   - **AI聊天功能**：集成了由DeepSeek提供的AI聊天功能，用户可以通过点击桌面上的“MayOS GUI AI Chat”按钮启动AI聊天界面。
   - **实现方式**：当前版本通过浏览器调用DeepSeek的网页版，未来收费版将使用API进行调用。

2. **桌面按钮**：
   - **AI聊天按钮**：在桌面上新增“MayOS GUI AI Chat”按钮，用户可以方便地启动AI聊天功能。

**注意事项**：
- AI聊天功能依赖于网络连接。
- 当前版本为测试版，功能和界面可能会有所调整。

---

#### **版本：MayOS_with_GUI_0.0.4 Test Release**

**发布日期：2025年6月2日**

**主要更新内容**：

1. **漏洞修复**：
   - **版本信息读取问题**：修复了系统版本信息无法正常读取的问题。
   - **更新日志读取问题**：修复了更新日志无法正常读取的问题。

2. **功能改进**：
   - **窗口分辨率调整**：将窗口分辨率调整为1280x740，确保壁纸信息显示完整。
   - **窗口标题更改**：将窗口标题更改为系统版本，方便用户识别当前版本。

3. **新功能**：
   - **实时时钟功能**：
     - 在右下角添加了数字时钟，使用 `update_clock()` 函数每秒更新一次时间。
     - 时钟使用白色文字黑色背景，确保可见性。
   - **界面优化**：
     - 时钟使用 `place` 布局精确定位在右下角。
     - 时钟文字使用Arial 12号字体。
     - 时钟会自动适应窗口大小变化。
   - **代码结构改进**：
     - 将时钟功能封装为独立函数。
     - 使用 `after` 方法实现定时刷新。
   - **使用说明**：
     - 时钟会自动启动并每秒刷新。
     - 时钟位置固定在窗口右下角，不会随其他内容移动。
     - 可以通过修改 `update_clock()` 函数中的 `strftime` 格式来改变时间显示样式。

4. **新增“版本管理器”类**：
   - **版本管理器**：专门负责系统版本及更新日志的读取，确保版本信息的准确性和更新日志的可用性。

---

#### **版本：MayOS_with_GUI_0.0.3 Stable Release**

**发布日期：2025年6月2日**

**主要更新内容**：

1. **新功能**：
   - **Bing每日壁纸自动更新功能**：
     - 系统启动时自动获取并设置Bing当日精选壁纸。
     - 新增“更新Bing壁纸”菜单选项，支持手动更新。
     - 壁纸本地缓存保存至 `files/background/` 目录，文件名包含日期信息（如 `bing_20230602.jpg`）。
   - **壁纸更新状态显示**：
     - 底部状态栏显示当前壁纸标题信息。
     - 壁纸更新失败时显示友好错误提示。

2. **菜单结构调整**：
   - “操作”菜单新增“更新Bing壁纸”选项。
   - 保持原有菜单结构不变。

3. **技术变更**：
   - **新增依赖库**：
     - `requests`：用于HTTP请求。
     - `Pillow`：用于图像处理。
   - **代码优化**：
     - 增强错误处理机制。
     - 改进文件保存逻辑。
     - 保持原有功能兼容性。

4. **已知问题**：
   - 在无网络连接情况下无法获取Bing壁纸。
   - 首次运行时需要联网获取壁纸。
   - 需要手动创建 `files/background/` 目录。

5. **升级说明**：
   - **安装新依赖**：
     ```bash
     pip install pillow requests
     ```
   - **建议创建目录**：
     ```bash
     mkdir -p files/background
     ```
   - **配置文件兼容**：原配置文件无需迁移。

6. **注意事项**：
   - Bing壁纸版权归微软所有。
   - 每日仅自动更新一次壁纸。
   - 手动更新不受限制。

---

#### **版本：MayOS_with_GUI_0.0.2 DevRelease**

**发布日期：2025年6月2日**

**主要更新内容**：

1. **新功能**：
   - **新增应用[GUI]**：
     - 音乐播放器 2.0。
   - **菜单栏**：
     - **操作菜单**：包含退出选项。
     - **帮助菜单**：包含官方网址（点击会打开浏览器）和更新日志。
     - **关于菜单**：显示版本信息。
   - **背景图片**：
     - **加载并显示背景图片**。
     - **错误处理**：如果图片不存在，会显示黑色背景和错误消息。
   - **欢迎消息**：
     - **控制台和GUI都会显示欢迎消息**。
     - **帮助命令**：现在同时在控制台和GUI中显示结果。
   - **状态栏**：
     - **底部添加了状态栏**，显示当前状态。

2. **错误处理**：
   - **文件不存在的情况进行了处理**。

3. **使用说明**：
   - **确保有 `files/background/default.jpg` 背景图片文件**。
   - **确保有 `system/info/MayOS_GUI_0.0.1.txt` 帮助文件**。
   - **运行程序后可以通过菜单栏访问各种功能**。

---

#### **版本：MayOS_with_GUI_0.0.1_test_release**

**发布日期：2025年5月18日**

**主要更新内容**：

1. **当前状态**：
   - **漏洞**：存在许多未经测试的漏洞，稳定性未知。
   - **启动脚本**：还未完成，只完成了注册部分。
   - **多语言支持**：不完善，当前仅支持英语（美国）、中文（简体）、中文（台湾、香港、澳门）。
   - **系统目录**：正在完善，后期会根据需求继续完善。
   - **壁纸**：使用Windows自带壁纸，如侵权会在未来发布的版本中删除。
   - **传播限制**：此系统为内部测试，未经许可禁止擅自以任何形式传播该系统的任意部分。

2. **最后修改时间**：
   - **2025年5月18日02点21分**。

---



## MayOS_GUI项目目录结构解释

以下是MayOS_GUI项目目录结构的详细解释：

```
project/
│
├── apps/
│   ├─ command/
│   │   ├─ __init__.py
│   │   ├─ version_manager.py
│   │   ├─ wallpaper_manager.py
│   │   ├─ update_manager.py
│   │   └─ ai_manager.py
│   └─ gui_test/
│       └─ AI_web.py
│
├── files/
│   ├─ background/
│   │   └─ default.jpg
│   ├─ image/
│   ├─ mayos_ng/
│   └─ users/
│
├── system/
│   ├─ display/
│   ├─ info/
│   │   ├─ ver.txt
│   │   ├─ MayOS_with_GUI_0.0.6.txt
│   │   └─ changelog.md
│   └─ lang/
│
└── main.py

```

### 1. apps/ - 应用程序代码目录

#### apps/command/ - 功能模块目录
存放了各个功能模块的实现代码：

- **version_manager.py**: 
  - 负责版本管理
  - 功能：获取当前版本、获取版本内容、获取最新版本、比较版本、初始化版本文件
  - 关键方法：`get_current_version()`, `get_version_content()`, `get_latest_version()`, `compare_versions()`, `initialize_version_files()`

- **wallpaper_manager.py**: 
  - 负责壁纸管理
  - 功能：从Bing获取壁纸并设置壁纸
  - 关键方法：`update_bing_wallpaper()`

- **update_manager.py**: 
  - 负责更新检测
  - 功能：检查是否有新版本、获取最新版本信息
  - 关键方法：`check_for_updates()`, `get_latest_version()`

- **ai_manager.py**: 
  - 负责AI应用启动
  - 功能：启动AI网页应用、打开官方网站
  - 关键方法：`launch_ai_web()`, `open_official_website()`

- **__init__.py**: 
  - Python包初始化文件
  - 可能为空，也可能包含包的初始化代码

#### apps/gui_test/ - GUI测试代码目录
存放图形用户界面测试相关的代码：

- **AI_web.py**: 
  - AI网页应用的实现代码
  - 功能：提供AI聊天功能接口

### 2. files/ - 资源文件目录

存放应用程序所需的各种文件资源：

- **background/**: 
  - 存放背景图片文件
  - 包含`default.jpg`作为默认背景图片

- **image/**: 
  - 可能存放其他图片文件
  - 具体用途取决于应用程序需求

- **mayos_ng/**: 
  - 可能存放与MayOS相关的文件
  - 具体内容取决于项目需求

- **users/**: 
  - 可能存放用户相关的数据
  - 例如用户配置文件、用户数据等

### 3. system/ - 系统文件目录

存放系统相关的文件：

- **display/**: 
  - 可能存放与显示相关的文件
  - 具体用途取决于应用程序需求

- **info/**: 
  - 存放信息文件
  - **ver.txt**: 存储当前版本信息
  - **MayOS_with_GUI_0.0.6.txt**: 存储版本内容
  - **changelog.md**: 存储更新日志，支持Markdown格式

- **lang/**: 
  - 可能存放多语言支持相关的文件
  - 例如不同语言的翻译文件

### 4. main.py - 主程序文件

- 应用程序的入口点
- 功能：初始化窗口、创建菜单栏、加载背景图片、更新时钟、启动AI应用等
- 负责调用各个功能模块的功能，实现完整的应用程序

### 项目特点

- **模块化设计**：各个功能模块相对独立，便于维护和扩展
- **清晰的目录结构**：按照功能划分目录，便于查找和理解代码
- **版本管理**：支持版本检测和更新提示
- **壁纸功能**：支持Bing每日壁纸自动更新
- **AI集成**：可以启动AI网页应用
- **用户界面**：提供友好的图形用户界面，包括菜单栏、状态栏、时钟等

这个项目结构设计合理，功能模块划分清晰，便于团队协作开发和后续功能扩展。

---

>*Copyright © 2025 **MayOS Team***
>*All Rights Reserved.*
---
English Ver.
## Introduction to MayOS_GUI Operating System Graphical Interface

---

## System Overview

MayOS_GUI is a lightweight graphical interface operating system environment developed using Python. It aims to provide users with a clean and aesthetically pleasing desktop experience along with essential functionalities. The system employs a modular design, ensuring excellent scalability.

### **Changelog**

---

#### **Version: MayOS_with_GUI_0.0.6**

**Release Date: July 5, 2025**

**Major Updates:**

1. **Version Management Features:**
   - **Version Detection:** The program can now automatically detect the current version and notify the user when a newer version is available.
   - **Version Information Retrieval:** Fetches the latest version information from a specified GitHub address to ensure users are always on the latest version.
   - **Version File Initialization:** Ensures that `ver.txt` and `changelog.md` files exist and creates default version files when necessary.

2. **Markdown Format Support for Changelog:**
   - **Changelog Display:** The changelog now supports Markdown formatting, allowing users to view update content more clearly.
   - **Display Optimization:** Utilizes the `tkhtmlview` library to properly render Markdown-formatted changelogs within the Tkinter interface.

3. **Wallpaper Update Feature:**
   - **Bing Wallpaper Auto-Update:** The program can now automatically fetch the daily wallpaper from Bing and set it as the desktop background.
   - **Error Handling:** Enhanced error handling for network requests and file operations to provide user-friendly error messages when wallpaper updates fail.

4. **AI Application Launch Feature:**
   - **AI Web Application Launch:** Users can now launch the AI web application via a button or menu.
   - **Error Handling:** Improved error handling for file existence and the launch process to notify users of any issues during startup.

5. **Code Structure Optimization:**
   - **Modular Design:** Split various functional modules into separate files within the `apps/command` directory for easier maintenance and scalability.
   - **Project Structure:** Optimized the project structure to ensure code maintainability and extensibility.

---

#### **Version: MayOS_with_GUI_0.0.5**

**Release Date: June 28, 2025**

**Major Updates:**

1. **New AI Chat Feature:**
   - **AI Chat Functionality:** Integrated AI chat functionality powered by DeepSeek. Users can initiate the AI chat interface by clicking the "MayOS GUI AI Chat" button on the desktop.
   - **Implementation:** Currently, the feature uses the DeepSeek web version via a browser. Future paid versions will utilize an API for enhanced performance.

2. **Desktop Button:**
   - **AI Chat Button:** Added a "MayOS GUI AI Chat" button to the desktop for easy access to the AI chat feature.

**Notes:**
- The AI chat feature relies on an internet connection.
- This version is a test release, and the functionality and interface may be subject to change.

---

#### **Version: MayOS_with_GUI_0.0.4 Test Release**

**Release Date: June 2, 2025**

**Major Updates:**

1. **Bug Fixes:**
   - **Version Information Reading Issue:** Fixed the problem where system version information could not be read correctly.
   - **Changelog Reading Issue:** Resolved the issue where the changelog could not be read properly.

2. **Feature Improvements:**
   - **Window Resolution Adjustment:** Adjusted the window resolution to 1280x740 to ensure complete display of wallpaper information.
   - **Window Title Change:** Changed the window title to reflect the system version for easier identification.

3. **New Features:**
   - **Real-Time Clock Feature:**
     - Added a digital clock to the bottom-right corner.
     - The `update_clock()` function updates the time every second.
     - The clock uses white text on a black background for visibility.
   - **Interface Optimization:**
     - The clock is precisely positioned using the `place` layout in the bottom-right corner.
     - The clock text uses the Arial 12-point font.
     - The clock automatically adjusts to changes in window size.
   - **Code Structure Improvements:**
     - Encapsulated the clock functionality into a separate function.
     - Uses the `after` method for timed refresh.
   - **Usage Instructions:**
     - The clock automatically starts and refreshes every second.
     - The clock position is fixed in the bottom-right corner and does not move with other content.
     - The `strftime` format in the `update_clock()` function can be modified to change the time display style.

4. **New "Version Manager" Class:**
   - **Version Manager:** Specifically handles the retrieval of system version and changelog information to ensure accuracy and availability.

---

#### **Version: MayOS_with_GUI_0.0.3 Stable Release**

**Release Date: June 2, 2025**

**Major Updates:**

1. **New Features:**
   - **Bing Daily Wallpaper Auto-Update:**
     - The system automatically fetches and sets the Bing daily wallpaper upon startup.
     - Added a "Update Bing Wallpaper" menu option for manual updates.
     - Wallpaper is cached locally in the `files/background/` directory.
     - Filenames include date information (e.g., `bing_20230602.jpg`).
   - **Wallpaper Update Status Feedback:**
     - The bottom status bar displays the current wallpaper title information.
     - Displays friendly error messages when wallpaper updates fail.

2. **Menu Structure Adjustment:**
   - Added the "Update Bing Wallpaper" option to the "Operation" menu.
   - Maintained the original menu structure.

3. **Technical Changes:**
   - **New Dependencies:**
     - `requests` for HTTP requests.
     - `Pillow` for image processing.

4. **Code Optimization:**
   - Enhanced error handling mechanisms.
   - Improved file-saving logic.
   - Maintained compatibility with existing features.

5. **Known Issues:**
   - Cannot fetch Bing wallpaper without an internet connection.
   - Internet connection is required for the first run to fetch the wallpaper.
   - The `files/background/` directory must be created manually.

6. **Upgrade Instructions:**
   - **Install New Dependencies:**
     ```bash
     pip install pillow requests
     ```
   - **Create Directory:**
     ```bash
     mkdir -p files/background
     ```
   - **Configuration File Compatibility:** No migration of configuration files is required.

7. **Notes:**
   - Bing wallpaper copyright belongs to Microsoft.
   - Wallpaper updates automatically once a day.
   - Manual updates are unlimited.

---

#### **Version: MayOS_with_GUI_0.0.2 DevRelease**

**Release Date: June 2, 2025**

**Major Updates:**

1. **New Features:**
   - **New Application [GUI]:**
     - Music Player 2.0.
   - **Menu Bar:**
     - **Operation Menu:** Includes an exit option.
     - **Help Menu:** Includes the official website (opens in the browser) and the changelog.
     - **About Menu:** Displays version information.
   - **Background Image:**
     - **Load and Display:** Loads and displays the background image.
     - **Error Handling:** If the image does not exist, displays a black background with an error message.
   - **Welcome Message:**
     - **Console and GUI:** Both display the welcome message.
     - **Help Command:** Now displays results in both the console and GUI.

2. **Error Handling:**
   - **File Not Found:** Handled cases where files are missing.

3. **Usage Instructions:**
   - **Ensure `files/background/default.jpg` exists.**
   - **Ensure `system/info/MayOS_GUI_0.0.1.txt` exists.**
   - **Access various features via the menu bar after running the program.**

---

#### **Version: MayOS_with_GUI_0.0.1_test_release**

**Release Date: May 18, 2025**

**Major Updates:**

1. **Current Status:**
   - **Bugs:** Numerous untested bugs exist; stability is unknown.
   - **Startup Script:** Not yet completed; only the registration section is finished.
   - **Multilingual Support:** Incomplete; currently supports only English (US), Chinese (Simplified), and Chinese (Taiwan, Hong Kong, Macau).
   - **System Directory:** Under development; will be refined based on future needs.
   - **Wallpaper:** Uses Windows default wallpapers; will be removed in future releases if found to be infringing.
   - **Distribution Restrictions:** This system is for internal testing; unauthorized distribution of any part of the system is prohibited.

2. **Last Modified Time:**
   - **2025年5月18日02点21分**.

---

This comprehensive update log ensures that users are informed about the latest features, bug fixes, and system improvements in each version of MayOS_GUI.
