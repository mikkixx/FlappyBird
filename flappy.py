import sys
import os
import random
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QPainter, QPixmap, QTransform, QFont, QColor, QPen
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

        pipe_path = os.path.join(os.path.dirname(__file__), "pipe.png")
        self.pipe_w = 350
        self.pipe_margin = 135
        self.pipe_img = QPixmap(pipe_path).scaledToWidth(self.pipe_w, Qt.SmoothTransformation)
        self.pipe_h = self.pipe_img.height()
        self.pipe_top_img = self.pipe_img.transformed(QTransform().scale(1, -1))
        self.pipe_x = 350
        self.gap_y = 250
        self.gap = 150
        self.pipe_speed = 3

        self.speed = 0
        self.gravity = 0.5
        self.jump_power = -6
        self.started = False
        self.game_over = False
        self.score = 0
        self.record_path = os.path.join(os.path.dirname(__file__), "record.txt")
        self.best = self.load_best()
        self.passed = False
        self.hit_x = 40
        self.hit_y = 24

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_game)
        self.timer.start(16)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.bg_img)
        painter.drawPixmap(self.pipe_x, self.gap_y - self.pipe_h, self.pipe_top_img)
        painter.drawPixmap(self.pipe_x, self.gap_y + self.gap, self.pipe_img)
        painter.drawPixmap(self.bird_x, int(self.bird_y), self.bird_img)
        
        painter.setPen(QColor("white"))
        painter.setFont(QFont("Arial", 40, QFont.Bold))
        painter.drawText(0, 20, 500, 80, Qt.AlignCenter, str(self.score))

        if self.game_over:
            painter.setPen(QPen(QColor(0, 80, 0), 4))
            painter.setBrush(QColor(60, 160, 40))
            painter.drawRoundedRect(50, 230, 400, 180, 20, 20)

            painter.setPen(QColor("white"))
            painter.setFont(QFont("Arial", 20, QFont.Bold))
            painter.drawText(50, 230, 400, 180, Qt.AlignCenter,
                             f"Ты проиграл!\nСчёт: {self.score}   Рекорд: {self.best}\nНажми пробел, чтобы\nперезапустить игру")

    def jump(self):
            self.started = True
            self.speed = self.jump_power

    def check_collision(self):
        bird_left = self.bird_x + self.hit_x
        bird_right = self.bird_x + self.bird_img.width() - self.hit_x
        bird_top = self.bird_y + self.hit_y
        bird_bottom = self.bird_y + self.bird_img.height() - self.hit_y

        if bird_top < 0 or bird_bottom > self.height():
            self.end_game()

        pipe_left = self.pipe_x + self.pipe_margin
        pipe_right = self.pipe_x + self.pipe_w - self.pipe_margin
        if bird_right > pipe_left and bird_left < pipe_right:
            if bird_top < self.gap_y or bird_bottom > self.gap_y + self.gap:
                self.end_game()

    def load_best(self):
        try:
            with open(self.record_path, "r") as f:
                return int(f.read())
        except (FileNotFoundError, ValueError):
            return 0

    def save_best(self):
        with open(self.record_path, "w") as f:
            f.write(str(self.best))
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            if self.game_over:
                self.reset_game()
            else:
                self.jump()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and not self.game_over:
            self.jump()

    def update_game(self):
        if self.started and not self.game_over:
            self.speed += self.gravity
            self.bird_y += self.speed

            self.pipe_x -= self.pipe_speed
            if self.pipe_x < -self.pipe_w + self.pipe_margin:
                self.pipe_x = 375
                self.gap_y = random.randint(120, 450)
                self.passed = False
            self.check_collision()
            pipe_right = self.pipe_x + self.pipe_w - self.pipe_margin
            if not self.passed and pipe_right < self.bird_x:
                self.score += 1
                self.passed = True
                if self.score > self.best:
                    self.best = self.score
        self.update()

    def reset_game(self):
        self.bird_y = 350
        self.speed = 0
        self.started = False
        self.game_over = False
        self.pipe_x = 375
        self.gap_y = 250
        self.score = 0
        self.passed = False

    def end_game(self):
        self.game_over = True
        self.save_best()

app = QApplication(sys.argv)
window = Game()
window.show()
sys.exit(app.exec())