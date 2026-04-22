# main.py
import sys
from PySide6.QtWidgets import QApplication
from ui_main import MainWindow

def main():
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    ) if hasattr(Qt, 'HighDpiScaleFactorRoundingPolicy') else None

    app = QApplication(sys.argv)
    
    font = app.font()
    font.setPointSize(10)
    app.setFont(font)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    from PySide6.QtCore import Qt
    main()