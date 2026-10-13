import sys
import os
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QPainter, QPixmap
from PySide6.QtCore import Qt, QTimer

class Game(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Flappy Bird")
        self.setFixedSize(500, 750)

        path = os.path.join(os.path.dirname(__file__), "background.png")
        self.bg_img = QPixmap(path).scaled(500, 750)

        bird_path = os.path.join(os.path.dirname(__file__), "bird.png")
        self.bird_img = QPixmap(bird_path).scaled(140, 110, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.bird_x = 100
        self.bird_y = 350

        self.speed = 0
        self.gravity = 0.5

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_game)
        self.timer.start(16)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.bg_img)
        painter.drawPixmap(self.bird_x, int(self.bird_y), self.bird_img)

    def update_game(self):
        self.speed += self.gravity
        self.bird_y += self.speed
        self.update()

app = QApplication(sys.argv)
window = Game()
window.show()
sys.exit(app.exec())