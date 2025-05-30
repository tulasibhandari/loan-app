# main.py
import sys
from PyQt5.QtWidgets import QApplication

from ui.login_window import LoginWindow
from ui.main_window import MainWindow
from models.database import initialize_db
from models.user_model import create_user_table

def main():
    app = QApplication(sys.argv)
    create_user_table()  # ensures users table is created

    # Hold reference globally
    app_window = {}

    def launch_main_app(username):
        app_window['main'] = MainWindow(username)
        app_window['main'].show()

    login = LoginWindow(on_login_success=launch_main_app)
    login.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

