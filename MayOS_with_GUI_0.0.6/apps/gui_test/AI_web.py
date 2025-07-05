from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QHBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import sys

class MiniMaxBrowser(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MayOS GUI AI Chat(Service By DeepSeek)")
        self.setGeometry(100, 100, 1200, 800)  # 设置窗口大小

        # 创建主布局
        main_layout = QVBoxLayout()

        # 创建导航栏
        # nav_layout = QHBoxLayout()

        # self.url_bar = QLineEdit()
        # self.url_bar.setPlaceholderText(">>>Type the URL to load the website")
        # self.url_bar.returnPressed.connect(self.load_url)

        # self.go_button = QPushButton("前往")
        # self.go_button.clicked.connect(self.load_url)

        # nav_layout.addWidget(self.url_bar)
        # nav_layout.addWidget(self.go_button)

        # 创建浏览器视图
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://chat.deepseek.com"))  # 设置默认加载的网页

        # 将导航栏和浏览器视图添加到主布局
        # main_layout.addLayout(nav_layout)
        main_layout.addWidget(self.browser)

        self.setLayout(main_layout)

    def load_url(self):
        url_text = self.url_bar.text()
        if not url_text.startswith("http://") and not url_text.startswith("https://"):
            url_text = "https://" + url_text
        url = QUrl(url_text)
        if url.isValid():
            self.browser.setUrl(url)
        else:
            self.browser.setUrl(QUrl("https://chat.deepseek.com/"))  # 如果 URL 无效，加载默认网页

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MiniMaxBrowser()
    window.show()
    sys.exit(app.exec_())