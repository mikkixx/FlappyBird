import sys
from PySide6.QtWidgets import QApplication, QWidget

class Game(QWidget):
    def ___init__(self):
        super().__init__()
        self.setWindowTitle("Flappy Bird")
        self.setFixedSize(400, 600)

app = QApplication(sys.argv)
window = Game()
window.show()
sys.exit(app.exec())