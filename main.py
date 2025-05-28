# main.py
import sys
from PyQt5.QtWidgets import QApplication

from ui.main_window import MainWindow
from models.database import initialize_db

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # Database connection to app
    initialize_db()

    # Create and display main app window
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()