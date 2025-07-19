from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import sys

class MiniMaxBrowser(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MayOS GUI AI Chat(Service By DeepSeek)")
        self.setGeometry(100, 100, 1200, 800)
        main_layout = QVBoxLayout()
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://chat.deepseek.com"))
        main_layout.addWidget(self.browser)
        self.setLayout(main_layout)

    def load_url(self):
        url_text = getattr(self, 'url_bar', None)
        if url_text:
            url_text = url_text.text()
            if not url_text.startswith(("http://", "https://")):
                url_text = "https://" + url_text
            url = QUrl(url_text)
            self.browser.setUrl(url if url.isValid() else QUrl("https://chat.deepseek.com/"))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MiniMaxBrowser()
    window.show()
    sys.exit(app.exec_())