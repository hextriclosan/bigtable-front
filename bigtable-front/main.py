import sys
from PyQt6.QtWidgets import QApplication
from widget import Widget

if __name__ == "__main__":
    app = QApplication([])

    widget = Widget()
    widget.resize(1200, 800)
    widget.show()

    sys.exit(app.exec())
