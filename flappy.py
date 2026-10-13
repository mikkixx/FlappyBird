import sys
import os
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QPainter, QPixmap

class Game(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Flappy Bird")
        self.setFixedSize(500, 750)

        path = os.path.join(os.path.dirname(__file__), "background.png")
        self.bg_img = QPixmap(path).scaled(500, 750)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.bg_img)

app = QApplication(sys.argv)
window = Game()
window.show()
sys.exit(app.exec())